FROM python:3.12
LABEL org.opencontainers.image.source https://github.com/umati/Sample-Server-asyncio

RUN apt update && apt-get install -yy build-essential libssl-dev libffi-dev \
    python3-dev cargo pkg-config

ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]
