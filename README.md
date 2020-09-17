### VDMA OPC Surface Technology Initiative

Anlagenschema "Materialbereitstellung":  
1. Step Materialversorgungsraum DÜRR  
2. Step Materialaufbereitung & -bereitstellung WIWA  

Use Case 1:  
Qualitätssicherung/Rückverfolgbarkeit  
-Bereitstellung der Rohdaten aller qualitätsrelevanten Parameter mit Zeitstempel an übergeordnetes System 
  
### TO DO:  
-Ergänzung fehlender Elemente der Objekthierarchie  
-Abgleich DatenTypen mit Parameterliste  
-Abgleich Modeling-Rule Mandatory/Optional  
-Abgleich UserAccsess Read/Write  
-Definition der States  
-Anlegen der "State's" als Statemaschine-Type  
   
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
