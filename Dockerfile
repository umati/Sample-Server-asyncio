FROM python:3.10
LABEL org.opencontainers.image.source https://github.com/umati/Sample-Server-asyncio

ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]
