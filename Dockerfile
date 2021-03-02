FROM python:3.8

RUN pip install asyncua==0.9.12
RUN pip install aiofile
RUN pip install aiofiles
WORKDIR /opcua
COPY . /

EXPOSE 4840

ENTRYPOINT ["python", "/src/server.py"]