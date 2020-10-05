FROM python:3.8

RUN pip install asyncua==0.8.4
WORKDIR /opcua
COPY . /

EXPOSE 4840

CMD python /src/server.py