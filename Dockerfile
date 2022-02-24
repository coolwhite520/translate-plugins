#基于的基础镜像
FROM python:3.8.7
#代码添加到code文件夹
ADD . /code
# 设置code文件夹是工作目录
WORKDIR /code
RUN rm -rf ./venv
RUN rm -rf ./Dockerfile
# 安装libreoffice
# 安装支持
RUN apt update
RUN tar -zxvf LibreOffice_7.3.0.3_Linux_x86-64_deb.tar.gz
RUN dpkg -i ./LibreOffice_7.3.0.3_Linux_x86-64_deb/DEBS/*.deb
RUN rm -rf LibreOffice_7.3.0.3_Linux_x86-64_deb.tar.gz
RUN rm -rf LibreOffice_7.3.0.3_Linux_x86-64_deb

#RUN apt install -y -qq libreoffice
RUN \
    pip install pip --upgrade \
    && pip install -r requirements.txt \
    && pip uninstall -y fitz \
    && pip uninstall -y pymupdf \
    && pip install PyMuPDF
EXPOSE 5001
CMD ["python", "./app.py", "--thread"]
