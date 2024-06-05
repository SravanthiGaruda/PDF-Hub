import PyPDF2
from flask import request, send_file, redirect, url_for
import os

def split_pdf():
    start_page = int(request.form['start_page'])
    end_page = int(request.form['end_page'])
    
    if start_page <= end_page:
        uploaded_pdf = request.files['pdf']
        filename = uploaded_pdf.filename
        uploaded_pdf.save(filename)

        output_pdf = f"split_output_{start_page}_to_{end_page}.pdf"
        split_pdf_file(filename, output_pdf, start_page, end_page)

        os.remove(filename)

        return redirect(url_for('index'))
    else:
        return "Error: Start page must be greater than end page."


def split_pdf_file(input_pdf, output_pdf, start_page, end_page):
    with open(input_pdf, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(start_page - 1, min(end_page, len(pdf_reader.pages))):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        with open(output_pdf, "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)
