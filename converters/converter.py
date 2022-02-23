from pdf2docx import Converter
import subprocess
import os


def p2dx(src_file):
    portion = os.path.splitext(src_file)
    if len(portion) > 1:
        cv = Converter(src_file)
        output_file_docx = portion[0] + ".docx"
        cv.convert(output_file_docx)
        cv.close()
        # 将docx转doc
        dx2d(output_file_docx)
        # 删除中间的docx
        os.unlink(output_file_docx)
        output_file_dox = portion[0] + ".doc"
        # 将doc转docx
        d2dx(output_file_dox)
        # 删除中间的doc
        os.unlink(output_file_dox)
    else:
        raise IndexError("文件名解析错误")


def dx2d(src_file):
    output_dir = os.path.dirname(src_file)
    cmd = 'libreoffice  --invisible --convert-to doc "{0}" --outdir "{1}"'.format(src_file, output_dir)
    subprocess.call(cmd, shell=True)


def d2dx(src_file):
    output_dir = os.path.dirname(src_file)
    cmd = 'libreoffice  --invisible --convert-to docx "{0}" --outdir "{1}"'.format(src_file, output_dir)
    subprocess.call(cmd, shell=True)


def p2px(src_file):
    output_dir = os.path.dirname(src_file)
    cmd = 'libreoffice  --invisible --convert-to pptx "{0}" --outdir "{1}"'.format(src_file, output_dir)
    subprocess.call(cmd, shell=True)


def x2xx(src_file):
    output_dir = os.path.dirname(src_file)
    cmd = 'libreoffice  --invisible --convert-to xlsx "{0}" --outdir "{1}"'.format(src_file, output_dir)
    subprocess.call(cmd, shell=True)


class Converters(object):

    def __init__(self, convert_type, src_file):
        self.convert_type = convert_type
        self.src_file = src_file

    def convert(self):
        if self.convert_type == 'p2dx':
            p2dx(self.src_file)
        elif self.convert_type == 'd2dx':
            d2dx(self.src_file)
        elif self.convert_type == 'p2px':
            p2px(self.src_file)
        elif self.convert_type == 'x2xx':
            x2xx(self.src_file)
