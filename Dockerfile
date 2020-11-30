FROM python:3.8

RUN pip install asyncua
WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]