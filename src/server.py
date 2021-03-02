# Imports
import os, asyncio, logging, time, datetime
from asyncua import Server, ua, uamethod
from asyncua.common.instantiate_util import instantiate

from examples import DemoBeschichtungsanlage

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAME = "VDMA-OPC-Surface-Technology-Initiative-CS"
XML_FILENAME = os.path.join(NAME + ".xml")

NAMESPACE = "http://vdma-opc-st-initiative-cs/ua/Prototyp1"

async def main():
    # Serversetup
    server = Server()
    server.name = "VDMA-OPC-ST-Prototype"
    await server.init()
    await server.set_build_info(
        product_uri="https://github.com/orgs/VDMA-OPC-Surface-Technology-Initiative",
        product_name="VDMA-OPC-ST-Prototype",
        manufacturer_name="VDMA-OPC-Surface-Technology-Initiative",
        software_version="beta",
        build_number="---",
        build_date=datetime.datetime.utcnow(),
    )

    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    idx = await server.register_namespace(NAMESPACE)

    # Import nodes.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Di.NodeSet2.xml"))
    except Exception as e:
        print(e)

    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")

    # Import nodes.xml
    try:
        # await server.import_xml(os.path.join(BASE_DIR, "nodeset","Opc.Ua.Machinery.NodeSet2.xml"))
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Machinery.NodeSet2.xml"))
    except Exception as e:
        print(e)

    ma_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Machinery/")

    # Import nodes.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", XML_FILENAME))
    except Exception as e:
        print(e)

    st_idx = await server.get_namespace_index("http://vdma-opc-st-initiative-cs/ua")

    # importiere basis beschichtungsanlage
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "BaseDemo.xml"))
    except Exception as e:
        print(e)
        
    # importiere teilanlage

    await server.load_data_type_definitions()

    objects = server.get_objects_node()
    deviceset = await objects.get_child([f"{di_idx}:DeviceSet"])
    base_object_type = server.get_node("ns=0;i=58")
    vessel_object_type = await base_object_type.get_child([f"{st_idx}:VesselObjectType"])
    valve_object_type = await base_object_type.get_child([f"{st_idx}:ValveObjectType"])
    machines_folder = await objects.get_child([f"{ma_idx}:Machines"])



    # read csv and generate data


    async with server:
        while 1:
            # itterate over data nd update nodes
            await asyncio.sleep(1)


# Start Server
if __name__ == "__main__":
    asyncio.run(main())
