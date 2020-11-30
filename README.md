![Build Docker image](https://github.com/VDMA-OPC-Surface-Technology-Initiative/Prototype1/workflows/Build%20Docker%20image/badge.svg?branch=master&event=push)  

### VDMA OPC Surface Technology Initiative

Anlagenschema "Materialbereitstellung":  
1. Step Materialversorgungsraum DÜRR  
2. Step Materialaufbereitung & -bereitstellung WIWA  
  
### TO DO:  
https://github.com/VDMA-OPC-Surface-Technology-Initiative/Prototype1/projects/1
   
### Endpoint-Url: 
> opc.tcp://127.0.0.1:4840  

### Ordner:   
> src <- python quellcode  
> dst <- server.exe (generiert aus dem quellcode)  
> nodeset <- generiertes nodeset  
  
### Generierung der server.exe mit pyinstaller:  
> pyinstaller --onefile src/server.py  
  
### Docker: 
> docker build . -t opcuaserver  
> docker run -d -p 4840:4840 opcuaserver  

EndpointURL: "opc.tcp://localhost:4840" or "opc.tcp://{hostip}:4840"
