from flask import Flask, render_template, request, send_file, send_from_directory
import os
import pikepdf

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    password = request.form['password']
    
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        original_filename, file_extension = os.path.splitext(file.filename)
        output_filename = f"{original_filename}_encrypted{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        encrypt_pdf(file_path, output_pdf, password)
        return send_file(output_pdf, as_attachment=True)
    return 'Invalid file format'

def encrypt_pdf(input_pdf, output_pdf, password):
    pdf = pikepdf.open(input_pdf)
    pdf.save(output_pdf, encryption=pikepdf.Encryption(owner=password, user=password, R=4))

if __name__ == '__main__':
    app.run(debug=True)
