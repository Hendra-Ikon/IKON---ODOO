import os
import shutil
from flask import Flask, request, jsonify
from interview_summarizer import InterviewSummarizer  # Import your class

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    name = data['name']
    interview_link = data['interview_link']
    prompts = data['prompts']
    applied_job = data['applied_job']

    try:
        summarizer = InterviewSummarizer(name, interview_link, prompts, applied_job)
        summary = summarizer.get_interview_summary()
        
        del summarizer
        clean_tmp_folder()
        
        return jsonify({'summary': summary})
    except Exception as e:
        del summarizer
        clean_tmp_folder()
        return jsonify({'error': f'Summarization failed | Details: {str(e)}'})
    
def clean_tmp_folder():
    tmp_dir = '/tmp'
    
    # Iterate over all files and directories in /tmp
    for filename in os.listdir(tmp_dir):
        file_path = os.path.join(tmp_dir, filename)
        
        try:
            # Check if it's a file or directory and remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and all its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
