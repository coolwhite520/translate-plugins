from flanker import mime
from parsers.api import TranslateAPI
from parsers.db import DB
from email import generator
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import base64
from flanker.mime import create

from bs4 import BeautifulSoup


def parse_eml_content(eml):
    extracted_data = {}
    inline_attachments = {}
    base64_attachment = {}
    # if mimeContents.content_type.is_multipart():
    for part in eml.walk():
        item_subtype = str(part.detected_subtype)
        if item_subtype.lower() == 'plain':
            if part.body is not None:
                extracted_data['plain_body'] = part.body
        elif item_subtype.lower() == 'html':
            if part.body is not None:
                extracted_data['html_body'] = part.body
        elif part.is_inline():
            if part.body is not None:
                for items in part.headers._v._items:
                    if str(items[0]).lower() == 'content-id':
                        temp_file_name = items[1]
                        content_id = temp_file_name[1: len(temp_file_name) - 1]
                        inline_attachments[content_id] = part.body
        if part.is_attachment():
            if part.body is not None:
                base64_attachment[part.detected_file_name] = part.body
    return extracted_data, inline_attachments, base64_attachment


def calculate_total_progress(all_paragraphs):
    return all_paragraphs, len(all_paragraphs)


class ParserEML(object):

    def __init__(self, row_id, src_file, des_file, src_lang, des_lang):
        self.row_id = row_id
        self.src_file = src_file
        self.des_file = des_file
        self.src_lang = src_lang
        self.des_lang = des_lang
        self.soup = None

    def save_to_file(self, e_from, e_to, e_date, trans_subject, html_text, inline_attachments, base64_attachment):
        with open(self.des_file, 'w') as outfile:
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = trans_subject
            msgRoot['From'] = e_from
            msgRoot['Date'] = e_date
            msgRoot['To'] = e_to

            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)
            h = MIMEText(html_text, 'html')
            msgAlternative.attach(h)

            for k, v in inline_attachments.items():
                msgImage = MIMEImage(v)
                msgImage.add_header('Content-ID', k)
                msgRoot.attach(msgImage)

            for k, v in base64_attachment.items():
                att = MIMEText(v, 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename="{0}"'.format(k)
                msgRoot.attach(att)
            gen = generator.Generator(outfile)
            gen.flatten(msgRoot)

    # def save_to_file_new(self, e_from, e_to, e_date, trans_subject, html_text):
    #     with open(self.des_file, 'w') as outfile:
    #         message = create.multipart("mixed")
    #         message.headers['From'] = e_from
    #         message.headers['To'] = e_to
    #         message.headers['Date'] = e_date
    #         message.headers['Subject'] = trans_subject
    #         message.append(create.text("html", html_text))
    #         outfile.write(message.to_string())

    def parse(self):
        with open(self.src_file, 'rb') as f:
            raw_email = f.read()
            eml = mime.from_string(raw_email)
            e_subject = eml.subject
            e_from = eml.headers.get('From')
            e_to = eml.headers.get('To')
            e_time = eml.headers.get('Date')
            trans = TranslateAPI()
            db = DB()
            trans_subject = trans.translate(self.src_lang, self.des_lang, e_subject)
            extracted_data, inline_attachments, base64_attachment = parse_eml_content(eml)
            eml_body = extracted_data['html_body']
            self.soup = BeautifulSoup(eml_body, features="lxml")
            all_paragraphs = self.soup.find_all("p", recursive=True)
            all_tags, total = calculate_total_progress(all_paragraphs)
            current = 0
            percent = 0
            for tag in all_tags:
                c = tag.text.strip()
                if len(c) > 0:
                    tag.string = trans.translate(self.src_lang, self.des_lang, c)
                current = current + 1
                if percent != int(current * 100 / total):
                    percent = int(current * 100 / total)
                    db.update_record_progress(self.row_id, percent)
            self.save_to_file(e_from, e_to, e_time, trans_subject, self.soup.prettify(), inline_attachments, base64_attachment)
            db.update_record_progress(self.row_id, 100)
            trans.close()
            db.close()
