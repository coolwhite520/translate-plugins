#基于的基础镜像
FROM python:3.8.7
#代码添加到code文件夹
ADD ./app.py  /code/app.py
ADD ./requirements.txt  /code/requirements.txt
ADD ./gunicorn  /code/gunicorn
# 设置code文件夹是工作目录
WORKDIR /code
# 安装libreoffice
RUN apt update && apt install -y -qq libgl1-mesa-glx
RUN pip install pip --upgrade  && pip install gunicorn gevent && pip install -r requirements.txt
RUN rm -rf ./requirements.txt
EXPOSE 5002
#CMD ["python", "./app.py", "--thread"]
CMD ["gunicorn", "app:app", "-c", "./gunicorn/config.py"]