#基于的基础镜像
FROM python:3.8.7
#代码添加到code文件夹
ADD . /code
# 设置code文件夹是工作目录
WORKDIR /code
# 安装支持
RUN apt update
RUN apt install -y -qq libgl1-mesa-glx
RUN pip install -r requirements.txt
EXPOSE 5001
CMD ["python", "./app.py", "--thread"]
