# Question Answering Bot

## Requirements

This is a question answering bot using leveraging the capabilities of a LLM to answer questions based on the content of a document. Langchain framework is used to implement this functionality.
It supports two types of files:
1. A questions.json file containing the list of questions.
2. A document in either PDF or JSON format that contains the information for answering the questions.

### Steps to run and test:
1. Update the value of os.environ["OPENAI_API_KEY"] in app.py with your own Openapi key.
2. Run the flask app by running app.py
3. Now open postman and create following request:
    Method: POST
    URL: http://127.0.0.1:5000/answer_questions
    Body:
    Choose form-data and add the following fields:
    questions (File): The JSON file containing the questions.
    document (File): The PDF or JSON document to process.