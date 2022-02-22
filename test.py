from flanker import mime
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


extracted_data = {}
inline_attachments = {}
base64_attachment = {}
with open("test_files/aa.eml", 'rb') as f:
    raw_email = f.read()
    mimeContents = mime.from_string(raw_email)
    # if mimeContents.content_type.is_multipart():
    for part in mimeContents.walk():
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


    html_doc = extracted_data['html_body']
    soup = BeautifulSoup(html_doc, features="lxml")
    all_paragraphs = soup.find_all("p", recursive=True)
    for p in all_paragraphs:
        for c in p.children:
            print(c)

    # print(soup.prettify())
