FROM python:3.8

RUN mkdir /app && mkdir /log && apt update && apt-get install default-jdk -y && apt-get clean
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt && pip3 install uwsgi
COPY mysite /app
RUN mkdir -p /home/tsai-jen/Customize-2DString-/ && ln -s /app /home/tsai-jen/Customize-2DString-/mysite 
CMD ["uwsgi", "--ini", "run.ini"]
