# Imports
import os 
import asyncio
import logging
import time
from datetime import datetime
from asyncua import Server, ua
from asyncua.common.ua_utils import value_to_datavalue
from importer import CSV_IMPORTER
from datavalue_parser import parse_to_datavalue

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger('asyncua')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

build_date = datetime(2021, 4, 9, 18, 00)
time_value = None

###############

import pandas as pd
import glob
import os

pattern = os.path.join(BASE_DIR, "src", "data", "datasets", "*.csv")

dframes = [pd.read_csv(csv, encoding="utf-16") for csv in glob.glob(pattern)]
all_df = pd.concat(dframes, axis=1)
all_df.to_csv(os.path.join(BASE_DIR, "src", "data", "data.csv"), index=False)
print("Created: data.csv")

###############

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
        build_number="202104091800",
        build_date=build_date,
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
                        dv = await parse_to_datavalue(item, time_value, build_date)
                    except Exception as e:
                        print(e)
                        dv = None

                    if dv is not None:
                        new_dv = ua.DataValue(
                            Value=dv.Value,
                            StatusCode_=dv.StatusCode_,
                            SourceTimestamp=dv.SourceTimestamp,
                            ServerTimestamp=datetime.utcnow()
                        )
                        await server.write_attribute_value(item[0][0].nodeid, new_dv, ua.AttributeIds.Value)

# Start Server
if __name__ == "__main__":
    asyncio.run(main())
