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
-Definition der States: Id+Text (z.B. 0 NotDefined, 1 Run, 2 Error ...)  
-Anlegen der "State's" als Enumeration (DataTypes -> BaseDataType -> Enumeration)  
  
  
  
  
Endpoint-Url: opc.tcp://127.0.0.1:4840  
src <- python quellcode  
dst <- server.exe (generiert aus dem quellcode)  
  
Generierung der server.exe mit pyinstaller:  
> pyinstaller --onefile src/server.py  
  


Run in a Docker-Container  
1. "docker build . -t opcuaserver"  
2. "docker run -p 4840:4840 opcuaserver"  
3. EndpointURL: "opc.tcp://localhost:4840"  
