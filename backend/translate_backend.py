from transformers import MarianMTModel, MarianTokenizer
from pdfminer.high_level import extract_text
from fpdf import FPDF
import os
import io
import logging

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def pdf_translator(file_path, target_lang):
    model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    file_text = extract_text(file_path)

    logger.debug("Extracted Text: %s", file_text)

    translated_text = translate_text(model, tokenizer, file_text)

    return translated_text

def translate_text(model, tokenizer, text):
    paragraphs = text.split('\n\n')

    translated_paragraphs = []
    for paragraph in paragraphs:
        if paragraph.strip():
            inputs = tokenizer(paragraph, return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**inputs)
            translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
            translated_paragraphs.append(translated_text)

    translated_text = '\n\n'.join(translated_paragraphs)

    return translated_text

def create_pdf_from_text(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    font_path = '/Users/sravanthi/Desktop/Projects/PDF/PDFWebSite/backend/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf'
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', size=10)

    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            try:
                if len(line) > 100:
                    pdf.set_font_size(8)
                else:
                    pdf.set_font_size(10)
                pdf.multi_cell(0, 5, line)
            except Exception as e:
                logger.error("Error processing line: %s", e)
        pdf.ln()

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output
