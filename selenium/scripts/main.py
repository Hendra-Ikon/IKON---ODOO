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
        
        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': f'Summarization failed | Details: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
