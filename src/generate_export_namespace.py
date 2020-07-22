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
    Behälter:
    '''
    vessel_object_type = await base_object_type.add_object_type(ns_idx, "VesselObjectType")


    # Metadaten
    vessel_meta_object = await vessel_object_type.add_object(ns_idx, "Meta")
    await vessel_meta_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_meta_name = await vessel_meta_object.add_property(ns_idx, "Name", "", ua.VariantType.String)
    await vessel_meta_name.set_modelling_rule(True)

    vessel_meta_location= await vessel_meta_object.add_property(ns_idx, "Location", "", ua.VariantType.String)
    await vessel_meta_location.set_modelling_rule(True)

    vessel_meta_serial = await vessel_meta_object.add_property(ns_idx, "SerialNumber", "", ua.VariantType.String)
    await vessel_meta_serial.set_modelling_rule(True)

    vessel_meta_volume = await vessel_meta_object.add_property(ns_idx, "Volume", "", ua.VariantType.String)
    await vessel_meta_volume.set_modelling_rule(True)


    # Behälter State
    vessel_state_object = await vessel_object_type.add_object(ns_idx, "State")
    await vessel_state_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_state_operationalstate = await vessel_state_object.add_variable(ns_idx, "OperationalState", 0, ua.VariantType.Int64) # Datentyp?
    await vessel_state_operationalstate.set_modelling_rule(True) # Mandatory ?

    vessel_state_operationalhours = await vessel_state_object.add_variable(ns_idx, "OperationalHours", 0, ua.VariantType.Int64) # Datentyp?
    await vessel_state_operationalhours.set_modelling_rule(True) # Mandatory ?

    vessel_state_poweronhours = await vessel_state_object.add_variable(ns_idx, "PowerOnHours", 0, ua.VariantType.Int64) # Datentyp? -> hh:mm:ss ?
    await vessel_state_poweronhours.set_modelling_rule(True) # Mandatory ?

    # Prozessdaten
    vessel_process_daten_object = await vessel_object_type.add_object(ns_idx, "Process")
    await vessel_process_daten_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_process_speed = await vessel_process_daten_object.add_object(ns_idx, "AgitatorSpeed")
    await vessel_process_speed.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    vessel_speed_setpoint = await vessel_process_speed.add_variable(ns_idx, "SetpointValue", 0, ua.VariantType.Float)
    await vessel_speed_setpoint.set_modelling_rule(True) # Mandatory ?
    vessel_speed_act_val = await vessel_process_speed.add_variable(ns_idx, "ActualValue", 0, ua.VariantType.Float)
    await vessel_speed_act_val.set_modelling_rule(True) # Mandatory ? NEIN zum testen JA

    vessel_process_temperature = await vessel_process_daten_object.add_object(ns_idx, "Temperature")
    await vessel_process_temperature.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    vessel_process_temperature_setpoint = await vessel_process_temperature.add_variable(ns_idx, "SetpointValue", 0, ua.VariantType.Float)
    await vessel_process_temperature_setpoint.set_modelling_rule(True) # Mandatory ?
    vessel_process_temperature_act_val = await vessel_process_temperature.add_variable(ns_idx, "ActualValue", 0, ua.VariantType.Float)
    await vessel_process_temperature_act_val.set_modelling_rule(True) # Mandatory ? NEIN zum testen JA

    vessel_process_level = await vessel_process_daten_object.add_object(ns_idx, "Level")
    await vessel_process_level.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_process_level_volume = await vessel_process_level.add_object(ns_idx, "Volume")
    await vessel_process_level_volume.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    vessel_process_level_volume_measured = await vessel_process_level_volume.add_variable(ns_idx, "Measured", 0, ua.VariantType.Float)
    await vessel_process_level_volume_measured.set_modelling_rule(True) # Mandatory ?
    vessel_process_level_volume_calculated = await vessel_process_level_volume.add_variable(ns_idx, "Calculated", 0, ua.VariantType.Float)
    await vessel_process_level_volume_calculated.set_modelling_rule(True) # Mandatory ?

    vessel_process_level_weight = await vessel_process_level.add_object(ns_idx, "Weight")
    await vessel_process_level_weight.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    vessel_process_level_weight_measured = await vessel_process_level_weight.add_variable(ns_idx, "Measured", 0, ua.VariantType.Float)
    await vessel_process_level_weight_measured.set_modelling_rule(True) # Mandatory ?
    vessel_process_level_weight_calculated = await vessel_process_level_weight.add_variable(ns_idx, "Calculated", 0, ua.VariantType.Float)
    await vessel_process_level_weight_calculated.set_modelling_rule(True) # Mandatory ?

    vessel_process_container = await vessel_process_daten_object.add_object(ns_idx, "Container")
    await vessel_process_container.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_process_container_id = await vessel_process_container.add_property(ns_idx, "ContainerId", "", ua.VariantType.String)
    await vessel_process_container_id.set_modelling_rule(True)
    vessel_process_container_batch_id = await vessel_process_container.add_property(ns_idx, "BatchId", "", ua.VariantType.String)
    await vessel_process_container_batch_id.set_modelling_rule(True)
    vessel_process_container_start_of_use = await vessel_process_container.add_property(ns_idx, "StartOfUse", "", ua.VariantType.String)
    await vessel_process_container_start_of_use.set_modelling_rule(True)

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
