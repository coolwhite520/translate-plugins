from pptx import Presentation
from parsers.api import translate


class ParserPPTX(object):
    def __init__(self, src_file, des_file, src_lang, des_lang):
        self.src_file = src_file
        self.des_file = des_file
        self.src_lang = src_lang
        self.des_lang = des_lang

    def parse(self):
        prs = Presentation(self.src_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.text = translate(self.src_lang, self.des_lang, run.text)
        prs.save(self.des_file)
