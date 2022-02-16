import pdfplumber


class ParserPdf(object):
    def __init__(self, src_file, des_file, src_lang, des_lang):
        self.src_file = src_file
        self.des_file = des_file
        self.src_lang = src_lang
        self.des_lang = des_lang

    def parse(self):
        with pdfplumber.open(self.src_file) as pdf:
            first_page = pdf.pages[0]
            for char in first_page.chars:
                print(char)
