# Imports
import os 
import asyncio
import logging
import time
from datetime import datetime
from asyncua import Server, ua
from asyncua.common.ua_utils import value_to_datavalue
from importer import CSV_IMPORTER

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

time_value = None

async def parse_to_datavalue(item, start_time):
    '''
    item[1] -> Value from csv -> type string (must be casted to correct type)
    item[0] -> tuple(node, dtype, bname)
    item[0][0] -> Node-Instance
    item[0][1] -> DataType
    item[0][2] -> BrowseName
    '''
    if item[0] is None:
        return None

    if item[0][1].Identifier == ua.ObjectIds.Null:
        val = ua.Variant(None)
    elif item[0][1].Identifier == ua.ObjectIds.Boolean:
        val = ua.Variant(Value=bool(item[1]), VariantType=ua.VariantType.Boolean)
    elif item[0][1].Identifier == ua.ObjectIds.SByte:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.SByte)        
    elif item[0][1].Identifier == ua.ObjectIds.Byte:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Byte)
    elif item[0][1].Identifier == ua.ObjectIds.Int16:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Int16)
    elif item[0][1].Identifier == ua.ObjectIds.UInt16:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.UInt16)
    elif item[0][1].Identifier == ua.ObjectIds.Int32:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Int32)
    elif item[0][1].Identifier == ua.ObjectIds.UInt32:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.UInt32)
    elif item[0][1].Identifier == ua.ObjectIds.UInt64:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.UInt64)
    elif item[0][1].Identifier == ua.ObjectIds.Int64:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Int64)
    elif item[0][1].Identifier == ua.ObjectIds.Float:
        val = ua.Variant(Value=float(item[1]), VariantType=ua.VariantType.Float)
    elif item[0][1].Identifier == ua.ObjectIds.Double:
        val = ua.Variant(Value=float(item[1]), VariantType=ua.VariantType.Double)
    elif item[0][1].Identifier == ua.ObjectIds.String:
        val = ua.Variant(Value=f"{item[1]}", VariantType=ua.VariantType.String)
    elif item[0][1].Identifier == ua.ObjectIds.DateTime:
        val = ua.Variant(Value=datetime.strptime(f"{item[1]}", '%Y-%m-%d %H:%M:%S.%f'), VariantType=ua.VariantType.DateTime)
    elif item[0][1].Identifier == ua.ObjectIds.Guid:
        val = ua.Variant(Value=f"{item[1]}", VariantType=ua.VariantType.Guid)
    elif item[0][1].Identifier == ua.ObjectIds.ByteString:
        val = ua.Variant(Value=f"{item[1]}", VariantType=ua.VariantType.ByteString)
    elif item[0][1].Identifier == ua.ObjectIds.XmlElement:
        # cant be resolved with the current csv structure!
        val = ua.Variant(Value=None, VariantType=ua.VariantType.XmlElement)
        return None
    elif item[0][1].Identifier == ua.ObjectIds.NodeId:
        val = ua.Variant(Value=ua.NodeId.from_string(f"{item[1]}"), VariantType=ua.VariantType.NodeId)
    elif item[0][1].Identifier == ua.ObjectIds.ExpandedNodeId:
        val = ua.Variant(Value=ua.NodeId.from_string(f"{item[1]}"), VariantType=ua.VariantType.ExpandedNodeId)
    elif item[0][1].Identifier == ua.ObjectIds.StatusCode:
        val = ua.Variant(Value=ua.StatusCode(int(item[1])), VariantType=ua.VariantType.StatusCode)
    elif item[0][1].Identifier == ua.ObjectIds.QualifiedName:
        val = ua.Variant(Value=ua.QualifiedName.from_string(f"{item[1]}"), VariantType=ua.VariantType.QualifiedName)        
    elif item[0][1].Identifier == ua.ObjectIds.LocalizedText:
        val = ua.Variant(Value=ua.LocalizedText(Text=f"{item[1]}", Locale="en"), VariantType=ua.VariantType.LocalizedText)
    elif item[0][1].Identifier == ua.ObjectIds.ExtensionObject:
        # cant be resolved with the current csv structure!
        val = ua.Variant(Value=None, VariantType=ua.VariantType.ExtensionObject)
        return None
    elif item[0][1].Identifier == ua.ObjectIds.DataValue:
        # cant be resolved with the current csv structure!
        val = ua.Variant(Value=None, VariantType=ua.VariantType.DataValue)
        return None
    elif item[0][1].Identifier == ua.ObjectIds.Variant:
        # cant be resolved with the current csv structure!
        val = ua.Variant(Value=None, VariantType=ua.VariantType.Variant)
        return None
    elif item[0][1].Identifier == ua.ObjectIds.DiagnosticInfo:
        # cant be resolved with the current csv structure!
        val = ua.Variant(Value=None, VariantType=ua.VariantType.DiagnosticInfo)
        return None
    else:
        # Unknown DataType
        # return an empty Variant to make it typesafe for companion spec. compliance
        print("Error:", item)
        return None

    if item[0][2].Name == "PowerOnHours":
        v = int((time.time()-start_time)/3600)
        val = ua.Variant(Value=v, VariantType=ua.VariantType.UInt64)

    return value_to_datavalue(val)

async def main():
    time_value = time.time()
    print("Start setup...")
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
        build_date=datetime.utcnow(),
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
        time_value = time.time()
        while 1:
            for row in data:
                await asyncio.sleep(1)
                for item in row:
                    # item = ((node, dtype, bname), val)
                    try:
                        dv = await parse_to_datavalue(item, time_value)
                    except Exception as e:
                        print(e)
                        dv = None

                    if dv is not None:
                        dv.ServerTimestamp = datetime.utcnow()
                        await server.write_attribute_value(item[0][0].nodeid, dv, ua.AttributeIds.Value)

# Start Server
if __name__ == "__main__":
    asyncio.run(main())
