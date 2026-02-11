FROM python:3.14-trixie
LABEL org.opencontainers.image.source=https://github.com/umati/Sample-Server-asyncio

RUN apt update && \
    apt install -yy --no-install-recommends --no-install-suggests \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    cargo \
    pkg-config \
    cmake

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]
