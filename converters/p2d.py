from pdf2docx import Converter


def convert(pdf_file, word_file):
    cv = Converter(pdf_file)
    cv.convert(word_file)
    cv.close()
