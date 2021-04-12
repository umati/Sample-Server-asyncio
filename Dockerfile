FROM python:3.8

ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]
