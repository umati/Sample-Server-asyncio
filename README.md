# Sample-Server-asyncio

OPC UA Sample Server based on [FreeOpcUa/opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio)

## Prototype implementations of OPC UA Companion Specifications

Based on the Hannover Messe 2021 demonstration of the VDMA Group OPC UA for Surface Technology.

This Sample Server implementation should help companion specification working groups to easily implement a first running server.

This repository provides a container image to be run by Docker as well as a running instance of the `main` branch at `opc.tcp://opcua2.umati.app:4840`

[![Build Docker image](https://github.com/umati/Sample-Server-asyncio/actions/workflows/Dockerbuild.yml/badge.svg)](https://github.com/umati/Sample-Server-asyncio/actions/workflows/Dockerbuild.yml)

## Folder Structure

```text
├──.github              GitHub Workflows
├──doc/images           Documentation and images
├──deps/UA-Nodeset      Normative NodeSet files as external deps of OPC-Foundation/UA-Nodeset repo
├──nodeset              Normative NodeSet files
├──src
    |-data
        |-datasets      Datasets for update variable of the virtual coating line instance
    |-models            XML NodeSets containing the instances of machines in the server
```

## Local development

Please clone with `git clone --recurse-submodules` to resolve the external [deps/UA-Nodeset](https://github.com/OPCFoundation/UA-Nodeset).

## Modell View Surface Technology

![Modell-View ](doc/images/Model-View-ST.png)

## Modell View Industrial Joining Technology

![Modell-View ](doc/images/Model-View-IJT.png)
