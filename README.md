VDMA OPC Surface Technology Initiative

Anlagenschema "Materialbereitstellung":  
1. Step Materialversorgungsraum DÜRR  
2. Step Materialaufbereitung & -bereitstellung WIWA  

Use Case 1:  
Qualitätssicherung/Rückverfolgbarkeit  
-Bereitstellung der Rohdaten aller qualitätsrelevanten Parameter mit Zeitstempel an übergeordnetes System 
  
  
  
Endpoint-Url: opc.tcp://127.0.0.1:4840  
src <- python quellcode  
dst <- server.exe (generiert aus dem quellcode)  
  
Generierung der server.exe mit pyinstaller:  
> pyinstaller --onefile src/server.py
