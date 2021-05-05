FROM python:3.8
LABEL org.opencontainers.image.source https://github.com/VDMA-OPC-Surface-Technology-Initiative/Prototype1

ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]
