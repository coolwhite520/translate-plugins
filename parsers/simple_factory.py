from parsers.parser_pptx import ParserPPTX
from parsers.parser_eml import ParserEML
import os


class SimpleFactory(object):
    @staticmethod
    def product_parser(row_id, src_file, des_file, src_lang, des_lang):
        ext = os.path.splitext(src_file)[1]
        if ext.lower() == '.pptx':
            return ParserPPTX(row_id, src_file, des_file, src_lang, des_lang)
        elif ext.lower() == '.eml':
            return ParserEML(row_id, src_file, des_file, src_lang, des_lang)