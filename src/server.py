# Imports
import os, asyncio
from asyncua import Server, ua, uamethod
from asyncua.common.instantiate_util import instantiate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAME = "VDMA-OPC-Surface-Technology-Initiative-CS"
XML_FILENAME = os.path.join(NAME + ".xml")

NAMESPACE = "http://vdma-opc-st-initiative-cs/ua/Prototyp1"
NAMESPACE_CS = "http://vdma-opc-st-initiative-cs/ua"

async def main():
    # Serversetup
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")
    idx = await server.register_namespace(NAMESPACE)

    # Import nodes.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", XML_FILENAME))
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(e)

    await server.load_type_definitions()

    objects = server.get_objects_node()
    idx_cs = await server.get_namespace_index(NAMESPACE_CS)

    base_object_type = server.get_node("ns=0;i=58")
    vessel_object_type = await base_object_type.get_child([f"{idx_cs}:VesselObjectType"])
    valve_object_type = await base_object_type.get_child([f"{idx_cs}:ValveObjectType"])

    await objects.add_object(idx, "Test_Behälter_1", objecttype=vessel_object_type)
    await objects.add_object(idx, "Test_Ventil_1", objecttype=valve_object_type)

    '''
    Beispiel 1:
    '''
    example1 = await objects.add_object(idx, "Dürr Farbmischraum", objecttype=ua.ObjectIds.BaseObjectType)
    example1_ansatzbehälter = await example1.add_object(idx, "FG01_Ansatzbehälter", objecttype=vessel_object_type)
    auslassventil = await example1.add_object(idx, "FG01_Auslassventil", objecttype=valve_object_type)

    example1_versorgungsbehälter = await example1.add_object(idx, "FG02_Versorgungsbehälter", objecttype=vessel_object_type)
    einlassventil = await example1.add_object(idx, "FG02_Einlassventil", objecttype=valve_object_type)
    auslassventil = await example1.add_object(idx, "FG02_Auslassventil", objecttype=valve_object_type)

    async with server:
        while 1:
            await asyncio.sleep(1)

# Start Server
if __name__ == "__main__":
    asyncio.run(main())
