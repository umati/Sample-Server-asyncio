# Imports
from asyncua import ua, uamethod, Server
from asyncua.common.instantiate_util import instantiate
import os, asyncio, datetime

from models.VesselObjectType import VesselObjectTypeClass
from models.ValveObjectType import ValveObjectTypeClass
from models.SurfaceTechnologieParameterType import SurfaceTechnologieParameterTypeClass
from models.PumpObjectType import PumpObjectTypeClass
from models.PipeObjectType import PipeObjectTypeClass
from models.MaterialObjectType import MaterialObjectTypeClass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "VDMA-OPC-Surface-Technology-Initiative-CS"
XML_FILENAME = os.path.join(NAME + ".xml")
NAMESPACE = "http://vdma-opc-st-initiative-cs/ua"

async def main():
    # Setup Namespace
    server = Server()
    await server.init()
    print("Server init done!")

    # Import nodes.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Di.NodeSet2.xml"))
    except Exception as e:
        print(e)

    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")

    # Import nodes.xml
    try:
        # await server.import_xml(os.path.join(BASE_DIR, "nodeset","Opc.Ua.Machinery.NodeSet2.xml"))
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "unofficial","machinery.xml"))
    except Exception as e:
        print(e)

    ma_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Machinery/")

    ns_idx = await server.register_namespace(NAMESPACE)

    base_object_type = server.get_node(ua.ObjectIds.BaseObjectType)
    folder_object_type = server.get_node(ua.ObjectIds.FolderType)
    
    # Build DataTypes
    await SurfaceTechnologieParameterTypeClass(server, ns_idx).build()

    # Build ObjectTypes
    await VesselObjectTypeClass(server, ns_idx).build()
    await ValveObjectTypeClass(server, ns_idx).build()
    await PumpObjectTypeClass(server, ns_idx).build()
    await MaterialObjectTypeClass(server, ns_idx).build()
    await PipeObjectTypeClass(server, ns_idx).build()

    # Export Namespace as xml
    try:
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

    await server.export_xml_by_ns(os.path.join(BASE_DIR, "nodeset", XML_FILENAME), namespaces=NAMESPACE)


if __name__ == "__main__":
    asyncio.run(main())
