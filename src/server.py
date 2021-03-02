# Imports
import os, asyncio, logging, time, datetime
from asyncua import Server, ua, uamethod
from asyncua.common.instantiate_util import instantiate

# from examples import DemoBeschichtungsanlage
from importer import CSV_IMPORTER

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAME = "VDMA-OPC-Surface-Technology-Initiative-CS"
XML_FILENAME = os.path.join(NAME + ".xml")

NAMESPACE = "http://vdma-opc-st-initiative-cs/ua/Prototyp1"

async def parse_to_datavalue(item):
    if str(item[0][1]) == "i=10":
        val = ua.Variant(float(item[1]), ua.VariantType.Float)
    elif str(item[0][1]) == "i=9":
        val = ua.Variant(int(item[1]), ua.VariantType.Int64)
    else:
        val = ua.Variant(item[1])
        # type will be guessed by Variant-Class under the hood
    return ua.DataValue(val, ua.StatusCode(ua.StatusCodes.Good),sourceTimestamp=datetime.datetime.utcnow(), serverTimestamp=datetime.datetime.utcnow())

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

    # Import VDMA-OPC-Surface-Technology-Initiative-CS.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", XML_FILENAME))
    except Exception as e:
        print(e)

    st_idx = await server.get_namespace_index("http://vdma-opc-st-initiative-cs/ua")

    # Import UmatiDemo.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "UmatiDemo.xml"))
    except Exception as e:
        print(e)
    
    demo_idx = await server.get_namespace_index("http://vdma-opc-st-initiative-cs/ua/demo")

    # Load TypeDefinitions    
    await server.load_data_type_definitions()

    # objects = server.get_objects_node()
    # deviceset = await objects.get_child([f"{di_idx}:DeviceSet"])
    # base_object_type = server.get_node("ns=0;i=58")
    # vessel_object_type = await base_object_type.get_child([f"{st_idx}:VesselObjectType"])
    # valve_object_type = await base_object_type.get_child([f"{st_idx}:ValveObjectType"])
    # machines_folder = await objects.get_child([f"{ma_idx}:Machines"])

    # read csv and generate data
    imp = CSV_IMPORTER(server=server, nsidx=demo_idx)
    # imp.read_csv("data.csv")
    data = []
    # data = imp.get_rows()

    async with server:
        while 1:
            await asyncio.sleep(1)
            # for each in data:
            #     for item in each:
            #         # item = ((node, dtype), val)
            #         await item[0][0].write_value(await parse_to_datavalue(item))
            #     await asyncio.sleep(1)


# Start Server
if __name__ == "__main__":
    asyncio.run(main())
