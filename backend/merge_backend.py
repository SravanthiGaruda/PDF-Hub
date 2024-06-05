from PyPDF2 import PdfMerger

def merge_pdf(uploaded_files, output_pdf):
    merger = PdfMerger()

    for file in uploaded_files:
        merger.append(file)

    merger.write(output_pdf)
    merger.close()
