FROM python:3.8

WORKDIR /opcua
COPY . /

ADD requirements.txt /opcua
RUN pip install -r /opcua/requirements.txt

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]
