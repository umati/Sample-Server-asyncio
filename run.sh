docker build -t opcuaserver .
docker container rm -f opcuaserver
docker run --name=opcuaserver -p 4840:4840 opcuaserver