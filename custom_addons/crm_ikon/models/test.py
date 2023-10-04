from linkedin_scraper import Person, actions
from selenium import webdriver

driver = webdriver.Chrome()
email = "irfansettz@gmail.com"
password = ""
actions.login(driver, email, password) 
person = Person("https://www.linkedin.com/in/irfansettz")