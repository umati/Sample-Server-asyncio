# Imports
import os, asyncio, logging
from asyncua import Server, ua, uamethod
from asyncua.common.instantiate_util import instantiate

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAME = "VDMA-OPC-Surface-Technology-Initiative-CS"
XML_FILENAME = os.path.join(NAME + ".xml")

NAMESPACE = "http://vdma-opc-st-initiative-cs/ua/Prototyp1"

async def main():
    # Serversetup
    server = Server()
    await server.init()
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
        await server.import_xml(os.path.join(BASE_DIR, "nodeset","Opc.Ua.Machinery.NodeSet2.xml"))
    except Exception as e:
        print(e)

    ma_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Machinery/")

    # Import nodes.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", XML_FILENAME))
    except Exception as e:
        print(e)

    st_idx = await server.get_namespace_index("http://vdma-opc-st-initiative-cs/ua")

    await server.load_type_definitions()

    objects = server.get_objects_node()
    deviceset = await objects.get_child([f"{di_idx}:DeviceSet"])

    base_object_type = server.get_node("ns=0;i=58")
    vessel_object_type = await base_object_type.get_child([f"{st_idx}:VesselObjectType"])
    valve_object_type = await base_object_type.get_child([f"{st_idx}:ValveObjectType"])

    machines_folder = await objects.get_child([f"{ma_idx}:Machines"])
    base_interface_type = server.get_node("ns=0;i=17602")
    vendor_nameplate_type = await base_interface_type.get_child([f"{di_idx}:IVendorNameplateType"])

    '''
    Beispiel 1:
    '''
    example1 = await deviceset.add_object(idx, "Dürr Farbmischraum", objecttype=ua.ObjectIds.BaseObjectType) # WIP: device_type

    example1_fg01  = await example1.add_folder(idx, "FG01")
    example1_ansatzbehälter = await example1_fg01.add_object(idx, "FG01_Ansatzbehälter", objecttype=vessel_object_type)
    auslassventil = await example1_fg01.add_object(idx, "FG01_Auslassventil", objecttype=valve_object_type)

    await machines_folder.add_reference(example1, ua.ObjectIds.Organizes)

    example1_fg02  = await example1.add_folder(idx, "FG02")
    example1_versorgungsbehälter = await example1_fg02.add_object(idx, "FG02_Versorgungsbehälter", objecttype=vessel_object_type)
    einlassventil = await example1_fg02.add_object(idx, "FG02_Einlassventil", objecttype=valve_object_type)
    auslassventil = await example1_fg02.add_object(idx, "FG02_Auslassventil", objecttype=valve_object_type)


    '''
    Workbench
    '''
    workbench = await objects.add_folder(idx, "Workbench")
    speed = await workbench.add_object(idx, "Speed", objecttype=ua.NodeId(2368, 0)) # AnalogItemType
    await speed.set_value(ua.Variant(50.0, varianttype=ua.VariantType.Float))

    # exclusive_deviation_alarm = await workbench.add_object(idx, "MyExclusiveDeviationAlarm", objecttype=ua.NodeId(9764, 0))
    await instantiate(workbench, server.get_node("ns=0;i=9764"), instantiate_optional=False)

    async with server:
        while 1:
            await asyncio.sleep(1)

# Start Server
if __name__ == "__main__":
    asyncio.run(main())
