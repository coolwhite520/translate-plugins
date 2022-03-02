from docx import Document
from docx.shared import Inches

document = Document('a.docx')
document.add_paragraph('Lorem ipsum dolor sit amet.')
document.save('aa.docx')