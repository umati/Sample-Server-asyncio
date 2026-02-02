# Copyright (c) 2020-2021 Andreas Heine, AFOTEK Anlagen für Oberflächentechnik GmbH
# Copyright (c) 2021 Fabian Beitler, konzeptpark GmbH
# Copyright (c) 2021 Moritz Walker, ISW University of Stuttagart (for umati and VDW e.V.)
# Copyright (c) 2021-2022 Goetz Goerisch, VDW - Verein Deutscher Werkzeugmaschinenfabriken e.V.
# Copyright (c) 2021-2022 Harald Weber, VDMA e.V.
# Copyright (c) 2024 Sebastian Friedl, interop4X - FVA GmbH 

# Imports
import os 
import asyncio
import logging
import time
import random
from datetime import datetime, timezone
from asyncua import Server, ua
from asyncua.common.ua_utils import value_to_datavalue
from asyncua.common.instantiate_util import instantiate
from importer import CSV_IMPORTER
from datavalue_parser import parse_to_datavalue

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

build_date = datetime(2022, 6, 15, 17, 00)
time_value = None

async def import_xml_file(server, file_path, strict_mode=True):
    """
    Imports an XML file into the server.

    Args:
        server: The OPC UA server instance.
        file_path: The path to the XML file to import.
        strict_mode: Specifies whether to use strict mode during import.
    """
    try:
        await server.import_xml(file_path, strict_mode=strict_mode)
        print(f"Successfully imported {file_path}")
    except Exception as e:
        print(f"Failed to import {file_path}: {e}")
        
async def setup_server():
    print("Start setup...")
    server = Server()
    server.name = "umati-Sample-Server-asyncio"
    await server.init()
    await server.set_build_info(
        product_uri="https://github.com/umati/Sample-Server-asyncio",
        product_name="umati Sample-Server-asyncio",
        manufacturer_name="umati community",
        software_version="alpha",
        build_number="202206151700",
        build_date=build_date,
    )

    server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
        ])
    server.set_security_IDs([
        "Anonymous",
        ])
    server.set_endpoint("opc.tcp://0.0.0.0:4840")
    return server

async def import_models(server):
    print("Importing companion spec. XML...")
    xml_files = [
        ("deps/UA-Nodeset/DI/Opc.Ua.Di.NodeSet2.xml", True),
        ("deps/UA-Nodeset/IA/Opc.Ua.IA.NodeSet2.xml", True),
        ("deps/UA-Nodeset/AMB/Opc.Ua.AMB.NodeSet2.xml", True),
        ("deps/UA-Nodeset/Machinery/Opc.Ua.Machinery.NodeSet2.xml", True),
        #("deps/UA-Nodeset/Machinery/Result/Opc.Ua.Machinery_Result.NodeSet2.xml", True),
        ("deps/UA-Nodeset/PackML/Opc.Ua.PackML.NodeSet2.xml", True), 
        ("deps/UA-Nodeset/Robotics/Opc.Ua.Robotics.NodeSet2.xml", True),
        #("deps/UA-Nodeset/ISA95-JOBCONTROL/opc.ua.isa95-jobcontrol.nodeset2.xml", True),
        #("deps/UA-Nodeset/Machinery/Jobs/Opc.Ua.Machinery.Jobs.Nodeset2.xml", True),
        ("deps/UA-Nodeset/Woodworking/Opc.Ua.Woodworking.NodeSet2.xml", True),
        ("deps/UA-Nodeset/Mining/General/1.0.0/Opc.Ua.Mining.General.NodeSet2.xml", False),
        ("deps/UA-Nodeset/Mining/TransportDumping/General/1.0.0/Opc.Ua.Mining.TransportDumping.General.NodeSet2.xml", False),
        ("deps/UA-Nodeset/PlasticsRubber/GeneralTypes/1.03/Opc.Ua.PlasticsRubber.GeneralTypes.NodeSet2.xml", True),
        ("deps/UA-Nodeset/PlasticsRubber/IMM2MES/1.01/Opc.Ua.PlasticsRubber.IMM2MES.NodeSet2.xml", True),
        ("nodeset/Opc.Ua.SurfaceTechnology.NodeSet2.xml", True),
        ("deps/UA-Nodeset/IA/Opc.Ua.IA.NodeSet2.xml", True),
        ("nodeset/Opc.Ua.Ijt.Tightening.NodeSet2.xml", True),
        ("src/models/CoatingLine-example.xml", True),
        ("src/models/ConveyorGunsAxes.xml", True),
        ("src/models/Materialsupplyroom.xml", True),
        ("src/models/dosingsystem.xml", True),
        ("src/models/ovenbooth.xml", True),
        ("src/models/Pretreatment.xml", True),
        ("src/models/ijt_tightening_server.xml", True),
        ("src/models/opcroboticstestserver.xml", True),
        ("src/models/Opc.Ua.Eumabois.Nodeset2.xml", True),
        ("src/models/WWM_Basic.xml", True),
        ("src/models/WWM_Full.xml", True),
        ("src/models/umati_opc40077_sample_instance.xml", True),
       
        ("deps/UA-Nodeset/Scales/Opc.Ua.Scales.NodeSet2.xml", True),
        ("deps/UA-Nodeset/Pumps/Opc.Ua.Pumps.NodeSet2.xml", True),
        ("deps/UA-Nodeset/Pumps/instanceexample.xml", True)
    ]
    
    # missing namespaces
    #     await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.PlasticsRubber.GeneralTypes.NodeSet2.xml"), strict_mode=False)
    #     await server.import_xml(os.path.join(BASE_DIR,  "deps", "UA-Nodeset", "Pumps", "instanceexample.xml"))
    # TODO disables until upstream is fixed
    # await server.import_xml(os.path.join(BASE_DIR, "deps", "UA-Nodeset", "Woodworking", "Opc.Ua.Eumabois.Nodeset2.xml"))


    for rel_path, strict_mode in xml_files:
        # Construct the full file path, ensuring OS compatibility
        file_path = os.path.join(BASE_DIR, *rel_path.split('/'))
        await import_xml_file(server, file_path, strict_mode)

async def main():
    time_value = time.time()

    server = await setup_server()
    print(f"Setup done! {time.time()-time_value}s")

    await import_models(server)
    print(f"All imports completed in {time.time() - time_value} seconds.")

    ##################################################################################################################

    time_value = time.time()
    print("Create TypeDefinitions from XML...")
    # Load TypeDefinitions
    await server.load_data_type_definitions()
    print(f"TypeDefinitions created!  {time.time()-time_value}s")

    scale_node = await create_scale_instance(server)
    await init_scale_identification_values(server,scale_node)

    truck_node = await create_mining_instance(server)
    await init_truck_identification_values(server, truck_node)


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
        i = 0
        while 1:
            for row in data:
                await updateSimpleScale(server,scale_node)
                await update_truck_values(server, truck_node,i)
                i = (1 + i) % 62
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
                            StatusCode=dv.StatusCode,
                            SourceTimestamp=dv.SourceTimestamp,
                            ServerTimestamp=datetime.now(timezone.utc)
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

async def create_scale_instance(server):
    print("Create Scale example")
    idx = await server.register_namespace("http://interop4x.de/example/scale")
    machinery_idx = await server.get_namespace_index('http://opcfoundation.org/UA/Machinery/')
    scale_idx = await server.get_namespace_index('http://opcfoundation.org/UA/Scales/V2/')

    simpleScale_type_nodeid = f"ns={scale_idx};i=3"
    simpleScale_type_node = server.get_node(simpleScale_type_nodeid)
    displayname = ua.LocalizedText("mySimpleScale")
    machines_node = await server.nodes.objects.get_child(f"{machinery_idx}:Machines")

    await instantiate(machines_node, simpleScale_type_node, bname=f"{idx}:mySimpleScale", dname=displayname)
    scale_node = await server.nodes.objects.get_child([f"{machinery_idx}:Machines",f"{idx}:mySimpleScale"])
    print(scale_node)
    return scale_node

async def init_scale_identification_values(server,scale_node):
    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")
    manufacturer = await scale_node.get_child([f"{di_idx}:Identification", f"{di_idx}:Manufacturer"])
    await manufacturer.write_value(ua.LocalizedText("interop4X - FVA GmbH"))
    serialNumber = await scale_node.get_child([f"{di_idx}:Identification", f"{di_idx}:SerialNumber"])
    await serialNumber.write_value(("12-34-56"))
    productInstanceUri = await scale_node.get_child([f"{di_idx}:Identification", f"{di_idx}:ProductInstanceUri"])
    await productInstanceUri.write_value(
    ("http://interop4x.de/12-34-56"))


async def updateSimpleScale(server, scale_node):
    scale_idx = await server.get_namespace_index('http://opcfoundation.org/UA/Scales/V2/')
    currentWeight = await scale_node.get_child(f"{scale_idx}:CurrentWeight")
    value = await currentWeight.read_value()
    value.Gross = (value.Gross + 0.2) % 10
    value.Net = value.Gross - value.Tare
    await currentWeight.write_value(value)


async def create_mining_instance(server):
    print("Create Minng example")
    idx = await server.register_namespace("http://interop4x.de/example/mining")
    machinery_idx = await server.get_namespace_index('http://opcfoundation.org/UA/Machinery/')
    mining_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Mining/TransportDumping/General/")

    HaulageMachineType_nid = f"ns={mining_idx};i=1003"
    HaulageMachineType_node = server.get_node(HaulageMachineType_nid)
    displayname = ua.LocalizedText("myTruck")
    machines_node = await server.nodes.objects.get_child(f"{machinery_idx}:Machines")

    await instantiate(machines_node, HaulageMachineType_node, bname=f"{idx}:myTruck", dname=displayname)
    truck_node = await server.nodes.objects.get_child([f"{machinery_idx}:Machines", f"{idx}:myTruck"])
    return truck_node

async def init_truck_identification_values(server, truck_node):
    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")
    mining_general_idx = await server.get_namespace_index('http://opcfoundation.org/UA/Mining/General/')
    manufacturer = await truck_node.get_child([f"{mining_general_idx}:MiningEquipmentIdentification", f"{di_idx}:Manufacturer"])
    await manufacturer.write_value(ua.LocalizedText("interop4X - FVA GmbH"))
    serialNumber = await truck_node.get_child([f"{mining_general_idx}:MiningEquipmentIdentification", f"{di_idx}:SerialNumber"])
    await serialNumber.write_value(("t-12-34-56"))
    productInstanceUri = await truck_node.get_child([f"{mining_general_idx}:MiningEquipmentIdentification", f"{di_idx}:ProductInstanceUri"])
    await productInstanceUri.write_value(
        ("http://interop4x.de/t-12-34-56"))

async def update_truck_values(server, truck_node,i):
    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")
    mining_general_idx = await server.get_namespace_index('http://opcfoundation.org/UA/Mining/General/')
    mining_idx = await server.get_namespace_index('http://opcfoundation.org/UA/Mining/TransportDumping/General/')
    payload = await truck_node.get_child([f"{di_idx}:ParameterSet",f"{mining_idx}:CurrentPayload"])
    speed = await truck_node.get_child([f"{di_idx}:ParameterSet",f"{mining_idx}:MachineVelocity",f"{mining_general_idx}:Speed"])

    if i < 10:
        await payload.write_value((await payload.read_value() + 0.5))
        await speed.write_value(0.0)
    elif i < 15:
        await payload.write_value(await payload.read_value())
        await speed.write_value(await speed.read_value()+ 0.1)
    elif i < 20:
        await payload.write_value(await payload.read_value())
        await speed.write_value(await speed.read_value())
    elif i < 25:
        await payload.write_value(await payload.read_value())
        await speed.write_value(await speed.read_value() - 0.1)
    elif i < 30:
        await payload.write_value(await payload.read_value() - 0.5)
        await speed.write_value(0.0)
    elif i < 40:
        await payload.write_value(0.0)
        await speed.write_value(await speed.read_value()+ 0.2)
    elif i < 50:
        await payload.write_value(0.0)
        await speed.write_value(await speed.read_value()- 0.2)
    elif i < 60:
        await payload.write_value(0.0)
        await speed.write_value(0.0) 

# Start Server
if __name__ == "__main__":
    asyncio.run(main())
    
