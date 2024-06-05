from flask import Flask, render_template, request, send_file, send_from_directory
from backend.split_backend import split_pdf_file
from backend.merge_backend import merge_pdf
from backend.translate_backend import pdf_translator, create_pdf_from_text
from backend.summarize_backend import pdf_summarizer
from backend.encryption_backend import encrypt
import os
from langchain import PromptTemplate

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/split', methods=['GET', 'POST'])
def split():
    if request.method == 'POST':
        start_page = int(request.form['start_page'])
        end_page = int(request.form['end_page'])
        uploaded_pdf = request.files['pdf']
        filename = uploaded_pdf.filename
        uploaded_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        output_pdf = f"split_output_{start_page}_to_{end_page}.pdf"
        split_pdf_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), output_pdf, start_page, end_page)

        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return send_file(output_pdf, as_attachment=True)
    else:
        return render_template('split.html')

@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files[]")
        merged_pdf = "merged.pdf"
        merge_pdf(uploaded_files, merged_pdf)
        return send_file(merged_pdf, as_attachment=True)
    else:
        return render_template('merge.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        file = request.files['file']
        target_lang = request.form['target_lang']
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.pdf')
        file.save(file_path)

        translated_text = pdf_translator(file_path, target_lang)
        pdf_stream = create_pdf_from_text(translated_text)

        os.remove(file_path)

        return send_file(pdf_stream, as_attachment=True, attachment_filename='translated_pdf.pdf')
    return render_template('translate.html')

# Route to render the upload form
@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return 'No file part'
    
    pdf = request.files['pdf']
    if pdf.filename == '':
        return 'No selected file'

    if pdf and pdf.filename.endswith('.pdf'):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
        pdf.save(filename)
        return render_template('viewer.html', pdf=pdf.filename)
    else:
        return 'Invalid file format'

@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':
        pdf_url = request.form['pdf_url']
        user_prompt = request.form['prompt'] + """{text}"""
        api_key = request.form['api_key']

        
        prompt_text = PromptTemplate(input_variables=["text"],
                           template = user_prompt,)
        
        # Pass pdf_url, prompt_text, and api_key to the summarization function
        summary = pdf_summarizer(pdf_url, 1000, 20, prompt_text, api_key)
        
        return render_template('summary.html', summary=summary)
    else:
        return render_template('summarize.html') 

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_route():
    if request.method == 'POST':
        return encrypt()
    else:
        return render_template('encryption.html')


if __name__ == '__main__':
    app.run(debug=True)
