
from flask import Flask, request, jsonify
import os
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["OPENAI_API_KEY"] = '<GIVE_API_KEY>'

from flask import Flask, request, jsonify
from langchain import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
import json


app = Flask(__name__)

model_name = ''
# Load the OpenAI model (You can replace this with another model)
llm = OpenAI(model=model_name)  # Replace with the LLM model you intend to use
qa_chain = load_qa_chain(llm, chain_type="stuff")  # Loading a question answering chain

# Helper function to read PDF
def read_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    all_text = "\n".join([page.page_content for page in pages])
    return all_text

@app.route('/answer_questions', methods=['POST'])
def answer_questions():
    if 'questions' not in request.files or 'document' not in request.files:
        return jsonify({'error': 'Please provide both question JSON and document file.'}), 400

    # Load the questions
    questions_file = request.files['questions']
    questions = json.load(questions_file)

    # Load the document (PDF or JSON)
    document_file = request.files['document']
    document_text = ""
    print(document_file.filename)
    if document_file.filename.endswith('.pdf'):
        # Handle PDF document
        pdf_path = os.path.join("../downloaded_documents", document_file.filename)
        document_file.save(pdf_path)
        document_text = read_pdf(pdf_path)
    elif document_file.filename.endswith('.json'):
        # Handle JSON document
        document_text = json.load(document_file)
    else:
        return jsonify({'error': 'Unsupported document type. Use PDF or JSON.'}), 400
    print(document_text)
    # Prepare the document for Langchain
    doc = Document(page_content=document_text)

    # Perform question answering
    answers = {}
    for question in questions['questions']:
        result = qa_chain.run(input_documents=[doc], question=question)
        answers[question] = result

    # Return the structured JSON response
    return jsonify(answers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)