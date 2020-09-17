FROM python:3.8

RUN pip install asyncua
WORKDIR /opcua
COPY . /

EXPOSE 4840

CMD python /src/server.py