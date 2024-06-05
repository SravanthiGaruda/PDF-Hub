Pdf-hub   # PDF-HUB Project
The PDF-HUB project is designed to provide an all-in-one solution for various PDF-related tasks. This application offers functionalities such as PDF splitting, merging, viewing, summarizing, encrypting, and translating. It ensures the security of sensitive data while providing a comprehensive set of tools.

## Features
1. **PDF Split**: Split a PDF into multiple parts.
2. **PDF Merge**: Merge multiple PDFs into one.
3. **PDF Viewer**: View uploaded PDFs.
4. **PDF Summarize**: Generate a summary of a PDF.
5. **PDF Encryption**: Encrypt a PDF with a password.
6. **PDF Translation**: Translate the text in a PDF to another language.

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Web framework for building the application.
- **pikepdf**: For handling PDF encryption.
- **PyPDF2**: For splitting and merging PDFs.
- **Langchain**: For summarizing PDF content.
- **Transformers (Hugging Face)**: For translation.
- **pdfminer.six**: For extracting text from PDFs.
- **FPDF**: For generating PDFs.
- **HTML/CSS**: For front-end development.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Required Python Packages
You can install the required packages using the following command:
```bash
pip install flask pikepdf PyPDF2 python-dotenv langchain-openai transformers pdfminer.six fpdf
```

## Folder Structure
```
PDF-HUB/
├── app.py
├── templates/
│   ├── index.html
│   ├── split.html
│   ├── merge.html
│   ├── upload.html
│   ├── viewer.html
│   ├── summarize.html
│   ├── encryption.html
│   ├── translate.html
├── backend/
│   ├── split_backend.py
│   ├── merge_backend.py
│   ├── translate_backend.py
│   ├── summarize_backend.py
│   ├── encryption_backend.py
├── static/
│   ├── index.css
│   ├── split.css
│   ├── merge.css
│   ├── upload.css
│   ├── viewer.css
│   ├── summarize.css
│   ├── encryption.css
│   ├── translate.css
├── uploads/
│   ├── (uploaded PDF files)
```

## How to Run the Project

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/PDF-HUB.git
cd PDF-HUB
```

### Step 2: Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

## Notes
- Make sure to set up the necessary API keys and environment variables as required by Langchain and OpenAI.
- Uploaded files are stored temporarily in the `uploads` folder and should be managed appropriately for production environments.
