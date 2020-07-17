# Imports
from asyncua import ua, uamethod, Server
import os, asyncio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "VDMA-OPC-Surface-Technology-Initiative-CS"
XML_FILENAME = os.path.join(NAME + ".xml")
NAMESPACE = "http://vdma-opc-st-initiative-cs/ua"

async def main():
    # Setup Namespace
    server = Server()
    await server.init()
    ns_idx = await server.register_namespace(NAMESPACE)

    base_object_type = server.get_node(ua.ObjectIds.BaseObjectType)

    '''
    Behälter:
    '''
    vessel_object_type = await base_object_type.add_object_type(ns_idx, "VesselObjectType")

    #mandatory:
    vessel_name = await vessel_object_type.add_variable(ns_idx, "Name", "BehälterName", ua.VariantType.String)
    await vessel_name.set_writable(False) # True = writable
    await vessel_name.set_modelling_rule(True) # True = mandatory

    vessel_location = await vessel_object_type.add_variable(ns_idx, "Location", "BehälterLocation", ua.VariantType.String)
    await vessel_location.set_writable(False) # True = writable
    await vessel_location.set_modelling_rule(True) # True = mandatory

    vessel_state = await vessel_object_type.add_variable(ns_idx, "State", 0, ua.VariantType.Int16)
    await vessel_state.set_writable(False) # True = writable
    await vessel_state.set_modelling_rule(True) # True = mandatory

    vessel_level = await vessel_object_type.add_variable(ns_idx, "Level", 0.0, ua.VariantType.Float)
    await vessel_level.set_writable(False) # True = writable
    await vessel_level.set_modelling_rule(True) # True = mandatory

    #optional:
    # ... WIP!
    
    
    '''
    Rührwerk:
    '''
    agitator_object_type = await base_object_type.add_object_type(ns_idx, "AgitatorObjectType")

    #mandatory:
    agitator_name = await agitator_object_type.add_variable(ns_idx, "Name", "RührwerkName", ua.VariantType.String)
    await agitator_name.set_writable(False) # True = writable
    await agitator_name.set_modelling_rule(True) # True = mandatory

    agitator_location = await agitator_object_type.add_variable(ns_idx, "Location", "RührwerkLocation", ua.VariantType.String)
    await agitator_location.set_writable(False) # True = writable
    await agitator_location.set_modelling_rule(True) # True = mandatory

    agitator_speed = await agitator_object_type.add_variable(ns_idx, "Speed", 0.0, ua.VariantType.Float)
    await agitator_speed.set_writable(False) # True = writable
    await agitator_speed.set_modelling_rule(True) # True = mandatory

    
    #optional:
    # ... WIP!
    
    '''
    Ventil:
    '''
    valve_object_type = await base_object_type.add_object_type(ns_idx, "ValveObjectType")

    #mandatory:
    valve_name = await valve_object_type.add_variable(ns_idx, "Name", "VentilName", ua.VariantType.String)
    await valve_name.set_writable(False) # True = writable
    await valve_name.set_modelling_rule(True) # True = mandatory

    valve_type = await valve_object_type.add_variable(ns_idx, "Type", "VentilTyp", ua.VariantType.String)
    await valve_type.set_writable(False) # True = writable
    await valve_type.set_modelling_rule(True) # True = mandatory

    valve_state = await valve_object_type.add_variable(ns_idx, "State", 0, ua.VariantType.Int16)
    await valve_state.set_writable(False) # True = writable
    await valve_state.set_modelling_rule(True) # True = mandatory

    #optional:
    valve_hub = await valve_object_type.add_variable(ns_idx, "Hub", 0.0, ua.VariantType.Float)

    # Export Namespace as xml
    try:
        os.remove(os.path.join(BASE_DIR, "nodeset", XML_FILENAME))
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

    await server.export_xml_by_ns(os.path.join(BASE_DIR, "nodeset", XML_FILENAME), namespaces=NAMESPACE)


if __name__ == "__main__":
    asyncio.run(main())
