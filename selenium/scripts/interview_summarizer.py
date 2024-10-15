from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import urllib.error
import socket
import tempfile
import random
import glob
import time
import os

class InterviewSummarizer():

    def __init__(self, name, interview_link, prompts, applied_job):
        # Function to suppress exceptions in the `__del__` method of `uc.Chrome`
        # Suppress exceptions for uc.Chrome
        self.suppress_exception_in_del(uc)
        self.name = name
        self.interview_link = interview_link
        self.prompts = prompts 
        self.applied_job = applied_job
        self.interview_summary = ""

        self.temp_dir = tempfile.TemporaryDirectory()
        self.download_dir = self.temp_dir.name

        self.start_time = time.time()

        chrome_options = uc.ChromeOptions()
        chrome_options.add_experimental_option("prefs", {
            r"download.default_directory": self.download_dir,                                # Set the download directory
            "download.prompt_for_download": False,                                      # Disable download prompt
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,                                               # Enable safe browsing
            "profile.default_content_setting_values.popups": 1,                         # Enable popup
            "profile.default_content_setting_values.password_manager_enabled": False,   # Prevent password manager
            "credentials_enable_service": False,                                        # Disable password saving
        })

        # chrome_options.add_argument(f"user-data-dir={self.temp_dir.name}")
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection

        # Set headless mode (if needed)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-software-rasterizer")

        # Add user-agent rotation
        user_agents = [
            # Add your list of user agents here
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        ]

        user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"--user-agent={user_agent}")

        # Initialize the WebDriver with the combined options
        self.driver = self.initialize_driver(chrome_options)

        self.wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds

        self.interview_summary = self.process_interview()
    
    def __del__(self):
        # Cleanup the temporary directory when the object is deleted
        self.temp_dir.cleanup()  # Remove the temporary directory
    
    def initialize_driver(self, chrome_options):
        # Attempt to initialize the Chrome driver with retries
        retries = 3
        for attempt in range(retries):
            try:
                # Here you should put your logic to create the Chrome driver
                self.driver = uc.Chrome(use_subprocess=True, options=chrome_options)
                return self.driver  # Return the driver if successful
            except (urllib.error.URLError, socket.gaierror) as e:
                time.sleep(2)  # Wait for 2 seconds before retrying

        raise Exception(f"Failed to initialize driver after multiple attempts")

    def get_interview_summary(self):
        return self.interview_summary

    def suppress_exception_in_del(self, uc):
        old_del = uc.Chrome.__del__

        def new_del(self) -> None:
            try:
                old_del(self)
            except:
                pass
        
        # Replace the original __del__ with the new one
        setattr(uc.Chrome, '__del__', new_del)

    def wait_for_download(self, extension):
        while True:
            # Check for files in the download directory
            if not self.get_latest_file(self.download_dir, extension):
                time.sleep(5)  # Wait for 5 seconds before checking again
            else:
                break  # Exit the loop if no .crdownload files are found
    
    def wait_for_button_visible(self, button, check_interval=5):
        while True:
            try:
                # Check if the download link is present
                download_link = button

                # Check if the download link is clickable
                if download_link.is_displayed() and download_link.is_enabled():
                    download_link.click()
                    return

            except NoSuchElementException:
                continue

            # Wait before the next check
            time.sleep(check_interval)

    def get_latest_file(self, folder_path, extension):
        # Ensure the extension starts with '*'
        if not extension.startswith("*"):
            extension = f"*.{extension}"
            
        # Create a pattern to match all .txt files in the specified folder
        files_pattern = os.path.join(folder_path, extension)
        
        # Get a list of all .txt files in the folder
        files = glob.glob(files_pattern)
        
        # Check if any files exist
        if not files:
            return False
        else:
            return max(files, key=os.path.getmtime)

    def process_interview(self):
        last_error = ""
        for attempt in range(3):
            try:
                interview_video = self.download_interview()

                if not interview_video:
                    last_error = "Interview video not downloaded. Please make sure the link is valid before summarizing again."

                else:
                    try:
                        transcript = self.transcribe(interview_video)
                    except Exception as e:
                        last_error = f"Error when processing transcript: {e}"
                    
                    try:
                        summary = self.ask_chatgpt(transcript)
                    except Exception as e:
                        last_error = f"Error when processing summary. Please summarize again: {e}"
                    
                    # Uncomment for debugging
                    # elapsed_time = time.time() - self.start_time
                    # print(f"Processing time: {elapsed_time} seconds")
                    
                    return summary
            except Exception as e:
                time.sleep(2)

        raise Exception(f"Video not summarized. Please check again if the link is valid, server is up and no error in Sharepoint, Restream and ChatGPT => {last_error}")

    def download_interview(self):
        last_error = ""
        for attempt in range(3):
            try:
                self.driver.get(self.interview_link)  

                # Wait for the label to be present
                download_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ms-Button-label label-79' and text()='Download']")))
                download_button.click()

                # Wait for the button to be clickable and then click it
                try:
                    # Using WebDriverWait for better stability
                    download_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @aria-label='Download video']"))
                    )
                    download_button.click()

                except Exception as e:
                    last_error = f"Error occurred when clicking download button: {e}"

                self.wait_for_download(extension="*.mp4")

                return self.get_latest_file(self.download_dir, "*.mp4")

            except Exception as e:
                time.sleep(2)
    
        raise Exception(f"Error when processing interview video. Please make sure the link is valid and Sharepoint is alive before summarizing again. => {last_error}")
    
    def transcribe(self, interview_video):
        last_error = ""
        for attempt in range(3):
            try:
                # Upload to transcription service
                self.driver.get("https://restream.io/tools/transcribe-video-to-text")
                # Wait for the button to be clickable and then click it
                # Wait for the input file element to be present
                try:
                    # Locate the input[type='file'] element (it might be hidden)
                    file_input = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )

                    # Send the file path to the input[type='file'] element
                    file_input.send_keys(interview_video)

                except Exception as e:
                    last_error = f"Error occurred when submitting video: {e}"

                try:
                    # Wait for the button to be clickable and then click it
                    transcribe_button = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//button[@type='submit' and contains(@class, 'bg-blue-600') and span[text()='Transcribe']]"))
                    )
                    
                    # Click the button
                    transcribe_button.click()

                except Exception as e:
                    last_error = f"Error occurred when clicking transcribe: {e}"

                try:
                    # Wait for the download link to be clickable
                    download_link = WebDriverWait(self.driver, 250).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'bg-blue-600') and span[text()='Download']]"))
                    )

                    # Get the href attribute of the download link
                    href = download_link.get_attribute("href")

                    # Click the link to download the file
                    self.driver.get(href)  # Navigate to the download URL
                            
                    self.wait_for_download(extension="*.txt")
                    
                    return self.get_latest_file(self.download_dir, "*.txt")

                except Exception as e:
                    last_error = f"Error occurred when downloading transcript: {e}"
            except Exception as e:
                time.sleep(2)
        
        raise Exception(f"Error when transcribing video. Please check if Restream.io is alive => {last_error}")

    def prompt_send(self, input_prompt):
         # Locate the contenteditable div using a suitable selector (XPath here)
        input_field = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )

        # Send keys (text) to the contenteditable div
        input_field.click()  # Focus the element
        input_field.clear()  # Clear any existing text if necessary
        
        self.driver.execute_script("arguments[0].innerText = arguments[1];", input_field, input_prompt)
        # Optional: Trigger an input event to simulate user input
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_field)

        time.sleep(random.uniform(3,5))

        # Wait for the button to be clickable
        send_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='send-button']"))
        )
        
        # Click the button
        send_button.click()

        time.sleep(random.uniform(5,10))

    # ChatGPT Interaction
    def ask_chatgpt(self, transcript_path):
        last_error = ""
        for attempt in range(3):
            try:
                self.driver.get("https://chatgpt.com/")

                # Read the contents of the file into a string
                try:
                    with open(transcript_path, 'r', encoding='utf-8') as file:
                        transcript_content = file.read()  # Read the entire file content
                except Exception as e:
                    last_error = f"The specified file was not found: {e}"

                # Wait for the element to be present
                try: 
                    transcript_prompt = f"""Use the interview transcript on {self.applied_job} application here for context on the subsequent prompts:
        {transcript_content}"""

                    try: 
                        self.prompt_send(transcript_prompt)
                    except Exception as e:
                        last_error = f"Error occurred when sending transcript: {e}"

                    for prompt in self.prompts:
                        try: 
                            self.prompt_send(prompt)
                        except Exception as e:
                            last_error = f"Error occurred when sending summary: {e}"
                    
                    self.prompt_send("Thank you!")

                except Exception as e:
                    last_error = f"Error occurred when processing summary: {e}"

                try:
                    # Locate the <p> element using XPath and extract its text
                    gpt_responses = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'code.hljs.language-html')))

                    summary = """"""

                    for html in gpt_responses:
                        current_summary = html.get_attribute('innerHTML') + "\n"
                        summary += current_summary

                    summary = summary.replace('&lt;', '<').replace('&gt;', '>').replace('<span class=\"hljs-tag\">', '').replace('<span class=\"hljs-name\">', '').replace('</span>', '')
                    time.sleep(5)

                    self.driver.close()
                    
                    return(summary)

                except Exception as e:
                    last_error = f"Error occurred when reading output: {e}"

            except Exception as e:
                time.sleep(2)

        raise Exception(f"Error when processing transcript. Please make sure if ChatGPT is alive and there is no significant update since 11-Oct-2024 => {last_error}")