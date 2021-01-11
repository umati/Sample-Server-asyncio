# Imports
import os, asyncio, logging, time
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
        build_date="---",
    )

    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    idx = await server.register_namespace(NAMESPACE)

    # Import nodes.xml
    try:
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "Opc.Ua.Di.NodeSet2.xml"))
    except Exception as e:
        print(e)

    di_idx = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")
    print(await server.get_namespace_array())

    # Import nodes.xml
    try:
        # await server.import_xml(os.path.join(BASE_DIR, "nodeset","Opc.Ua.Machinery.NodeSet2.xml"))
        await server.import_xml(os.path.join(BASE_DIR, "nodeset", "unofficial","machinery.xml"))
    except Exception as e:
        print(e)

    ma_idx = await server.get_namespace_index("http://opcfoundation.org/UA/Machinery/")
    
    print(await server.get_namespace_array())

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

    '''
    Beispiel 1:
    '''
    await DemoBeschichtungsanlage(server, idx).install()

    # '''
    # Workbench
    # '''
    # workbench = await objects.add_folder(idx, "Workbench")

    # # Instance of AnalogItemType
    # speed = await workbench.add_object(idx, "AnalogItemType", objecttype=ua.NodeId(2368, 0))

    # # writing the AnalogItemType:
    # await speed.set_value(ua.Variant(50.0, varianttype=ua.VariantType.Float))
    # speed_Definition = await speed.get_child("Definition")
    # await speed_Definition.set_value(ua.Variant("AnalogMesswertXY", ua.VariantType.String))

    # speed_EURange = await speed.get_child("EURange")
    # speed_range = ua.uaprotocol_auto.Range()
    # speed_range.High = 100.0
    # speed_range.Low = 0.0
    # await speed_EURange.set_value(ua.Variant(speed_range , ua.VariantType.ExtensionObject))

    # speed_EngineeringUnits = await speed.get_child("EngineeringUnits")
    # speed_units = ua.uaprotocol_auto.EUInformation()
    # await speed_EngineeringUnits.set_value(ua.Variant(speed_units , ua.VariantType.ExtensionObject))

    # speed_InstrumentRange = await speed.get_child("InstrumentRange")
    # speed_irange = ua.uaprotocol_auto.Range()
    # speed_irange.High = 100.0
    # speed_irange.Low = 0.0
    # await speed_InstrumentRange.set_value(ua.Variant(speed_irange , ua.VariantType.ExtensionObject))

    # speed_ValuePrecision = await speed.get_child("ValuePrecision")
    # await speed_ValuePrecision.set_value(2.0)

    # # Instance of SurfaceTechnologieParameterType
    # surface_technologie_parameter_type = await base_object_type.get_child([f"{st_idx}:SurfaceTechnologieParameterType"])
    # st_p_type = await workbench.add_object(idx, "SurfaceTechnologieParameterType", objecttype=surface_technologie_parameter_type, instantiate_optional=True)
    # # st_p_type_alarm = await instantiate(st_p_type, server.get_node("ns=0;i=9764"), instantiate_optional=False)


    # alarm_folder = await workbench.add_folder(idx, "Alarms")
    # await instantiate(alarm_folder, server.get_node("ns=0;i=2955"), instantiate_optional=False)

    # await instantiate(alarm_folder, server.get_node("ns=0;i=9341"), instantiate_optional=False)
    # await instantiate(alarm_folder, server.get_node("ns=0;i=9482"), instantiate_optional=False)
    # await instantiate(alarm_folder, server.get_node("ns=0;i=9764"), instantiate_optional=False)

    # await instantiate(alarm_folder, server.get_node("ns=0;i=9906"), instantiate_optional=False)
    # await instantiate(alarm_folder, server.get_node("ns=0;i=10368"), instantiate_optional=False)
    # await instantiate(alarm_folder, server.get_node("ns=0;i=10060"), instantiate_optional=False)

    async with server:
        while 1:
            await asyncio.sleep(1)


# Start Server
if __name__ == "__main__":
    asyncio.run(main())
