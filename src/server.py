# Copyright 2020-2021 (c) Andreas Heine, AFOTEK Anlagen für Oberflächentechnik GmbH
# Copyright 2021 (c) Fabian Beitler, konzeptpark GmbH
# Copyright 2021 (c) Moritz Walker, ISW University of Stuttagart (for umati and VDW e.V.)
# Copyright 2021 (c) Goetz Goerisch, VDW - Verein Deutscher Werkzeugmaschinenfabriken e.V.



# Imports
import os 
import asyncio
import logging
import time
import random
from datetime import datetime
from asyncua import Server, ua
from asyncua.common.ua_utils import value_to_datavalue
from importer import CSV_IMPORTER
from datavalue_parser import parse_to_datavalue

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

build_date = datetime(2021, 4, 9, 18, 00)
time_value = None

async def main():
    time_value = time.time()
    print("Start setup...")
    # Serversetup
    server = Server()
    server.name = "umati-Sample-Server-asyncio"
    await server.init()
    await server.set_build_info(
        product_uri="https://github.com/umati/Sample-Server-asyncio",
        product_name="umati Sample-Server-asyncio",
        manufacturer_name="umati community",
        software_version="alpha",
        build_number="202106231800",
        build_date=build_date,
    )

    server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
        ])
    server.set_security_IDs([
        "Anonymous",
        ])
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    print(f"Setup done! {time.time()-time_value}s")

    ##################################################################################################################

    time_value = time.time()
    print("Importing companion spec. XML...")

    # Import Opc.Ua.Di.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Di.NodeSet2.xml"))
    except Exception as e:
        print(e)

    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")

    # Import Opc.Ua.Machinery.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Machinery.NodeSet2.xml"))
    except Exception as e:
        print(e)

    ma_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Machinery/")

    # Import Opc.Ua.SurfaceTechnology.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.SurfaceTechnology.NodeSet2.xml"))
    except Exception as e:
        print(e)

    st_idx = await server.get_namespace_index("http://opcfoundation.org/UA/SurfaceTechnology/")

    # Import Opc.Ua.Ijt.Tightening.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Ijt.Tightening.NodeSet2.xml"))
    except Exception as e:
        print(e)

    ijt_idx = await server.get_namespace_index("http://opcfoundation.org/UA/IJT/")

        # Import Opc.Ua.Robotics.NodeSet2.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Robotics.NodeSet2.xml"))
    except Exception as e:
        print(e)

    rob_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Robotics/")

#            # Import Opc.Ua.Ia.NodeSet2.xml
#    try:
#        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.IA.NodeSet2.xml"))
#    except Exception as e:
#        print(e)
#
#    ia_idx = await server.get_namespace_index("http://opcfoundation.org/UA/IA/")
#
#    # Import Opc.Ua.MachineTool.NodeSet2.xml
#    try:
#        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.MachineTool.Nodeset2.xml"))
#    except Exception as e:
#        print(e)
#
#    mt_idx = await server.get_namespace_index("http://opcfoundation.org/UA/MachineTool/")

    ##################################################################################################################
    print(f"Import done! {time.time()-time_value}s")

    time_value = time.time()
    print("Importing models...")

    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "CoatingLine-example.xml"))
    except Exception as e:
        print(e)
    
    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "ConveyorGunsAxes.xml"))
    except Exception as e:
        print(e)
    
    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "Materialsupplyroom.xml"))
    except Exception as e:
        print(e)

    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "dosingsystem.xml"))
    except Exception as e:
        print(e)
    
    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "ovenbooth.xml"))
    except Exception as e:
        print(e)

    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "Pretreatment.xml"))
    except Exception as e:
        print(e)
    
    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "ijt_tightening_server.xml"))
    except Exception as e:
        print(e)    

    try:
        await server.import_xml(os.path.join(BASE_DIR, "src", "models", "opcroboticstestserver.xml"))
    except Exception as e:
        print(e)  


    print(f"Import done! {time.time()-time_value}s")

    ##################################################################################################################

    time_value = time.time()
    print("Create TypeDefinitions from XML...")
    # Load TypeDefinitions    
    await server.load_data_type_definitions()
    print(f"TypeDefinitions created!  {time.time()-time_value}s")

    time_value = time.time()
    print("Start importing CSV-Data...")
    # read csv and generate data
    imp = CSV_IMPORTER(server=server)
    await imp.read_csv(os.path.join(BASE_DIR, "src", "data", "data.csv"))
    data = []
    data = await imp.get_rows()
    print(f"Import done! {time.time()-time_value}s")

    print("Starting Server...")
    async with server:
        print(f"Server is now running!")
        
        # calling fucntion that updates robotics nodes in a parallel task
        await robotvariableupdater(server)

        time_value = time.time()
        while 1:
            for row in data:
                await asyncio.sleep(1)
                for item in row:
                    # item = ((node, dtype, bname), val)
                    try:
                        dv = await parse_to_datavalue(item, time_value, build_date)
                    except Exception as e:
                        print(item, e)
                        dv = None

                    if dv is not None:
                        new_dv = ua.DataValue(
                            Value=dv.Value,
                            StatusCode_=dv.StatusCode_,
                            SourceTimestamp=dv.SourceTimestamp,
                            ServerTimestamp=datetime.utcnow()
                        )
                        await server.write_attribute_value(item[0][0].nodeid, new_dv, ua.AttributeIds.Value)

async def robotvariableupdater(server):
    # prepare a list of variables to be updated 
    nsindex= await server.get_namespace_index("http://vdma.org/OPCRoboticsTestServer/")
    nodesToUpdate=[]
    nodesToUpdate.append(server.get_node(f"ns={nsindex};i=6022"))
    nodesToUpdate.append(server.get_node(f"ns={nsindex};i=6020"))
    nodesToUpdate.append(server.get_node(f"ns={nsindex};i=6024"))
    nodesToUpdate.append(server.get_node(f"ns={nsindex};i=6031"))
    nodesToUpdate.append(server.get_node(f"ns={nsindex};i=6027"))
    nodesToUpdate.append(server.get_node(f"ns={nsindex};i=6033"))
    nodesToUpdate.append(server.get_node(f"ns={nsindex};i=6054"))
    loop = asyncio.get_event_loop()
    loop.create_task(randomvaluesimulator(nodesToUpdate))

async def randomvaluesimulator(nodes):
    while True:
        await asyncio.sleep(2)
        #print("Simulating...")
        for node in nodes:
            value = round(random.uniform(10,20),2)
            await node.write_value(value)
 
# Start Server
if __name__ == "__main__":
    asyncio.run(main())
