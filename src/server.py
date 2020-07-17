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
    server.set_endpoint("opc.tcp://127.0.0.1:4840")
    idx = await server.register_namespace(NAMESPACE)

    # Import nodes.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", XML_FILENAME))
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(e)

    objects = server.get_objects_node()
    idx_cs = await server.get_namespace_index(NAMESPACE_CS)

    '''
    Beispiel 1:
    '''

    example1 = await objects.add_object(idx, "Beispiel  1", objecttype=ua.ObjectIds.BaseObjectType)

    fg1 = await example1.add_object(idx, "FG01 - Ansatz", objecttype=ua.ObjectIds.BaseObjectType)
    fg2 = await example1.add_object(idx, "FG02 - Versorgung", objecttype=ua.ObjectIds.BaseObjectType)

    # instantiate nodes from nodeset
    # my_vessel = await objects.add_object(idx, "MyVessel", "ns=3;i=1")
    await fg1.add_object(idx, "Behälter", f"ns={idx_cs};i=1")
    await fg2.add_object(idx, "Behälter", f"ns={idx_cs};i=1")

    # my_agitator = await objects.add_object(idx, "MyAgitator", "ns=3;i=6")
    await fg1.add_object(idx, "Rührwerk", f"ns={idx_cs};i=6")
    await fg2.add_object(idx, "Rührwerk", f"ns={idx_cs};i=6")

    # my_valve = await objects.add_object(idx, "MyValve", "ns=3;i=10")
    await fg1.add_object(idx, "Valve", f"ns={idx_cs};i=10")
    await fg2.add_object(idx, "Valve1", f"ns={idx_cs};i=10")
    await fg2.add_object(idx, "Valve2", f"ns={idx_cs};i=10")

    '''
    Beispiel 2:
    '''

    example2 = await objects.add_object(idx, "Beispiel  2", objecttype=ua.ObjectIds.BaseObjectType)

    fg1 = await example2.add_object(idx, "FG01 - Ansatz", objecttype=ua.ObjectIds.BaseObjectType)
    vessel1 = await fg1.add_object(idx, "Behälter", f"ns={idx_cs};i=1")
    await vessel1.add_object(idx, "Rührwerk", f"ns={idx_cs};i=6")
    await vessel1.add_object(idx, "Valve", f"ns={idx_cs};i=10")

    fg2 = await example2.add_object(idx, "FG02 - Versorgung", objecttype=ua.ObjectIds.BaseObjectType)    
    vessel2 = await fg2.add_object(idx, "Behälter", f"ns={idx_cs};i=1")
    await vessel2.add_object(idx, "Rührwerk", f"ns={idx_cs};i=6")
    await vessel2.add_object(idx, "Valve1", f"ns={idx_cs};i=10")
    await vessel2.add_object(idx, "Valve2", f"ns={idx_cs};i=10")


    async with server:
        while 1:
            await asyncio.sleep(1)

# Start Server
if __name__ == "__main__":
    asyncio.run(main())