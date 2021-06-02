#!/bin/bash
# Copyright 2021 (c) Moritz Walker, ISW University of Stuttagart (for umati and VDW e.V.)

docker build -t opcuaserver .
docker container rm -f opcuaserver
docker run --name=opcuaserver -p 4840:4840 opcuaserver