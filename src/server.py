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

    await server.load_type_definitions()

    objects = server.get_objects_node()
    idx_cs = await server.get_namespace_index(NAMESPACE_CS)

    '''
    Beispiel 1:
    '''
    await objects.add_object(idx, "Behälter_1", f"ns={idx_cs};i=1")

    async with server:
        while 1:
            await asyncio.sleep(1)

# Start Server
if __name__ == "__main__":
    asyncio.run(main())
