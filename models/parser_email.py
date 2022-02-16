import email


class ParserEmail(object):
    def __init__(self, src_file, des_file, src_lang, des_lang):
        self.src_file = src_file
        self.des_file = des_file
        self.src_lang = src_lang
        self.des_lang = des_lang

    def parse(self):
        with open(self.src_file) as fp:
            msg = email.message_from_file(fp)
            for par in msg.walk():
                if not par.is_multipart():
                    pass
