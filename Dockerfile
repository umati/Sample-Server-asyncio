FROM python:3.13-bookworm
LABEL org.opencontainers.image.source https://github.com/umati/Sample-Server-asyncio

RUN apt update && \
    apt install -yy build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cargo \
    pkg-config \
    cmake

ADD requirements.txt /
RUN \
    if [ `dpkg --print-architecture` = "armhf" ]; then \
    printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf ; \
    fi
#RUN pip install --index-url=https://www.piwheels.org/simple --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]
