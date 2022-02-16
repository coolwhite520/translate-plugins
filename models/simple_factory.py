from models.parser_pdf import ParserPdf
from models.parser_pptx import ParserPPTX
import os


class SimpleFactory(object):
    @staticmethod
    def product_parser(src_file, des_file, src_lang, des_lang):
        ext = os.path.splitext(src_file)[1]
        if ext == '.pptx':
            return ParserPPTX(src_file, des_file, src_lang, des_lang)
        elif ext == '.pdf':
            return ParserPdf(src_file, des_file, src_lang, des_lang)
