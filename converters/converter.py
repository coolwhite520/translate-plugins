from pdf2docx import Converter
import subprocess
import os


def p2d(src_file):
    portion = os.path.splitext(src_file)
    if len(portion) > 1:
        cv = Converter(src_file)
        output_file = portion[0] + ".docx"
        cv.convert(output_file)
        cv.close()
    else:
        raise IndexError("文件名解析错误")


def d2d(src_file):
    cmd = 'libreoffice  --invisible --convert-to docx {0}'.format(src_file)
    subprocess.call(cmd, shell=True)


def p2p(src_file):
    cmd = 'libreoffice  --invisible --convert-to pptx {0}'.format(src_file)
    subprocess.call(cmd, shell=True)


def x2x(src_file):
    cmd = 'libreoffice  --invisible --convert-to xlsx {0}'.format(src_file)
    subprocess.call(cmd, shell=True)


class Converters(object):

    def __init__(self, convert_type, src_file):
        self.convert_type = convert_type
        self.src_file = src_file

    def convert(self):
        if self.convert_type == 'p2d':
            p2d(self.src_file)
        elif self.convert_type == 'd2d':
            d2d(self.src_file)
        elif self.convert_type == 'p2p':
            p2p(self.src_file)
        elif self.convert_type == 'x2x':
            x2x(self.src_file)
