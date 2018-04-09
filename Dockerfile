FROM python:3.6-slim

ADD src/requirements.txt /usr/src/requirements.txt

RUN pip install -r /usr/src/requirements.txt
