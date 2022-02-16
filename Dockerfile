#基于的基础镜像
FROM python:3.8.7

#代码添加到code文件夹
ADD . /code
# 设置code文件夹是工作目录
WORKDIR /code
# 安装支持
RUN pip install -r requirements.txt
EXPOSE 5555
CMD ["python", "./app.py", "--thread"]
