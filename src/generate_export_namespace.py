# Imports
from asyncua import ua, uamethod, Server
from asyncua.common.instantiate_util import instantiate
import os, asyncio, datetime

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
    Behälter Metadaten
    '''
    vessel_meta_object_type = await base_object_type.add_object_type(ns_idx, "VesselMetaObjectType")

    # Metadaten
    vessel_meta_object = await vessel_object_type.add_object(ns_idx, "Meta")
    await vessel_meta_location.set_modelling_rule(True)

    vessel_meta_serial = await vessel_meta_object_type.add_property(ns_idx, "SerialNumber", "", ua.VariantType.String)
    await vessel_meta_serial.set_modelling_rule(True)

    vessel_meta_volume = await vessel_meta_object_type.add_property(ns_idx, "Volume", "", ua.VariantType.String)
    await vessel_meta_volume.set_modelling_rule(True)

    '''
    Behälter State
    '''
    vessel_state_object_type = await base_object_type.add_object_type(ns_idx, "VesselStateObjectType")

    vessel_state_operationalstate = await vessel_state_object_type.add_variable(ns_idx, "OperationaState", 0, ua.VariantType.Int64) # Datentyp?
    await vessel_state_operationalstate.set_modelling_rule(True) # Mandatory ?

    vessel_state_operationalhours = await vessel_state_object_type.add_variable(ns_idx, "OperationaHours", 0, ua.VariantType.Int64) # Datentyp?
    await vessel_state_operationalhours.set_modelling_rule(True) # Mandatory ?

    vessel_state_poweronhours = await vessel_state_object_type.add_variable(ns_idx, "PowerOnHours", ua.Variant(datetime.datetime.utcnow(),ua.VariantType.DateTime), ua.VariantType.DateTime) # Datentyp? -> hh:mm:ss ?
    await vessel_state_poweronhours.set_modelling_rule(True) # Mandatory ?

    '''
    Parameter (Soll/Ist)
    '''
    vessel_parameter_object_type = await base_object_type.add_object_type(ns_idx, "VesselParameterObjectType")

    vessel_parameter_setpoint = await vessel_parameter_object_type.add_variable(ns_idx, "Sollwert", 0, ua.VariantType.Float)
    await vessel_parameter_setpoint.set_modelling_rule(True) # Mandatory ?

    vessel_parameter_act_val = await vessel_parameter_object_type.add_variable(ns_idx, "Istwert", 0, ua.VariantType.Float)
    await vessel_parameter_act_val.set_modelling_rule(True) # Mandatory ?


    # '''
    # Behälter:
    # '''
    # vessel_object_type = await base_object_type.add_object_type(ns_idx, "VesselObjectType")

    # #meta
    # # await instantiate(vessel_object_type, vessel_meta_object_type, idx=ns_idx ,instantiate_optional=True)
    # vessel_object_meta = await vessel_object_type.add_object(ns_idx, "Metadaten", objecttype=vessel_meta_object_type) # <--------------------- wird nicht richtig instanziert!
    # await vessel_object_meta.set_modelling_rule(True)
    # #state
    # vessel_object_state = await vessel_object_type.add_object(ns_idx, "State", objecttype=vessel_state_object_type) # <--------------------- wird nicht richtig instanziert!
    # await vessel_object_state.set_modelling_rule(True)
    # #prozessdaten
    # vessel_object_processdata = await vessel_object_type.add_object(ns_idx, "Prozessdaten", objecttype=vessel_processdata_object_type) # <--------------------- wird nicht richtig instanziert!
    # await vessel_object_processdata.set_modelling_rule(True)

    # '''
    # Behälter:
    # '''
    # vessel_object_type = await base_object_type.add_object_type(ns_idx, "VesselObjectType")

    # #mandatory:
    # vessel_name = await vessel_object_type.add_variable(ns_idx, "Name", "BehälterName", ua.VariantType.String)
    # await vessel_name.set_writable(False) # True = writable
    # await vessel_name.set_modelling_rule(True) # True = mandatory

    # vessel_location = await vessel_object_type.add_variable(ns_idx, "Location", "BehälterLocation", ua.VariantType.String)
    # await vessel_location.set_writable(False) # True = writable
    # await vessel_location.set_modelling_rule(True) # True = mandatory

    # vessel_state = await vessel_object_type.add_variable(ns_idx, "State", 0, ua.VariantType.Int16)
    # await vessel_state.set_writable(False) # True = writable
    # await vessel_state.set_modelling_rule(True) # True = mandatory

    # vessel_level = await vessel_object_type.add_variable(ns_idx, "Level", 0.0, ua.VariantType.Float)
    # await vessel_level.set_writable(False) # True = writable
    # await vessel_level.set_modelling_rule(True) # True = mandatory

    # #optional:
    # # ... WIP!
    
    
    # '''
    # Rührwerk:
    # '''
    # agitator_object_type = await base_object_type.add_object_type(ns_idx, "AgitatorObjectType")

    # #mandatory:
    # agitator_name = await agitator_object_type.add_variable(ns_idx, "Name", "RührwerkName", ua.VariantType.String)
    # await agitator_name.set_writable(False) # True = writable
    # await agitator_name.set_modelling_rule(True) # True = mandatory

    # agitator_location = await agitator_object_type.add_variable(ns_idx, "Location", "RührwerkLocation", ua.VariantType.String)
    # await agitator_location.set_writable(False) # True = writable
    # await agitator_location.set_modelling_rule(True) # True = mandatory

    # agitator_speed = await agitator_object_type.add_variable(ns_idx, "Speed", 0.0, ua.VariantType.Float)
    # await agitator_speed.set_writable(False) # True = writable
    # await agitator_speed.set_modelling_rule(True) # True = mandatory

    
    # #optional:
    # # ... WIP!
    
    # '''
    # Ventil:
    # '''
    # valve_object_type = await base_object_type.add_object_type(ns_idx, "ValveObjectType")

    # #mandatory:
    # valve_name = await valve_object_type.add_variable(ns_idx, "Name", "VentilName", ua.VariantType.String)
    # await valve_name.set_writable(False) # True = writable
    # await valve_name.set_modelling_rule(True) # True = mandatory

    # valve_type = await valve_object_type.add_variable(ns_idx, "Type", "VentilTyp", ua.VariantType.String)
    # await valve_type.set_writable(False) # True = writable
    # await valve_type.set_modelling_rule(True) # True = mandatory

    # valve_state = await valve_object_type.add_variable(ns_idx, "State", 0, ua.VariantType.Int16)
    # await valve_state.set_writable(False) # True = writable
    # await valve_state.set_modelling_rule(True) # True = mandatory

    # #optional:
    # valve_hub = await valve_object_type.add_variable(ns_idx, "Hub", 0.0, ua.VariantType.Float)

    # Export Namespace as xml
    try:
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

    await server.export_xml_by_ns(os.path.join(BASE_DIR, "nodeset", XML_FILENAME), namespaces=NAMESPACE)


if __name__ == "__main__":
    asyncio.run(main())
