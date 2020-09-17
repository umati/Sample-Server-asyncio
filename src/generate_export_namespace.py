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
    ##############################################################################################################################################
    Behälter:
    ##############################################################################################################################################
    '''
    vessel_object_type = await base_object_type.add_object_type(ns_idx, "VesselObjectType")

    # Metadaten
    vessel_meta_object = await vessel_object_type.add_object(ns_idx, "Meta")
    await vessel_meta_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_meta_name = await vessel_meta_object.add_property(ns_idx, "Name", "", ua.VariantType.String)
    await vessel_meta_name.set_modelling_rule(True)
    await vessel_meta_name.set_writable(False)

    vessel_meta_location= await vessel_meta_object.add_property(ns_idx, "Location", "", ua.VariantType.String)
    await vessel_meta_location.set_modelling_rule(True)
    await vessel_meta_location.set_writable(True) # Writable !? A.Heine: Why should clients be able to write? Or Where is the location stored File? After Restart Value will be back to default!

    vessel_meta_serial = await vessel_meta_object.add_property(ns_idx, "SerialNumber", "", ua.VariantType.String)
    await vessel_meta_serial.set_modelling_rule(True)
    await vessel_meta_serial.set_writable(False)

    vessel_meta_volume = await vessel_meta_object.add_property(ns_idx, "Volume", 0.0, ua.VariantType.Float)
    await vessel_meta_volume.set_modelling_rule(True)
    await vessel_meta_volume.set_writable(False)

    # State
    vessel_state_object = await vessel_object_type.add_object(ns_idx, "State")
    await vessel_state_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_state_operationalstate = await vessel_state_object.add_variable(ns_idx, "OperationalState", 0, ua.VariantType.Int64) # Datentyp?
    await vessel_state_operationalstate.set_modelling_rule(True) # Mandatory ?
    await vessel_state_operationalstate.set_writable(False) # Write ?

    vessel_state_operationalhours = await vessel_state_object.add_variable(ns_idx, "OperationalHours", 0, ua.VariantType.Int64) # Datentyp?
    await vessel_state_operationalhours.set_modelling_rule(True) # Mandatory ?
    await vessel_state_operationalhours.set_writable(False) # Write ?

    vessel_state_poweronhours = await vessel_state_object.add_variable(ns_idx, "PowerOnHours", 0, ua.VariantType.Int64) # Datentyp? A.Heine: hh:mm:ss ?
    await vessel_state_poweronhours.set_modelling_rule(True) # Mandatory ?
    await vessel_state_poweronhours.set_writable(False) # Write ?

    # Prozessdaten
    vessel_process_daten_object = await vessel_object_type.add_object(ns_idx, "Process")
    await vessel_process_daten_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_process_speed = await vessel_process_daten_object.add_object(ns_idx, "AgitatorSpeed")
    await vessel_process_speed.add_reference(ua.ObjectIds.ModellingRule_Optional, ua.ObjectIds.HasModellingRule, True, False)
    vessel_speed_setpoint = await vessel_process_speed.add_variable(ns_idx, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste Int!
    await vessel_speed_setpoint.set_modelling_rule(True) # Mandatory ?
    await vessel_speed_setpoint.set_writable(True)
    vessel_speed_act_val = await vessel_process_speed.add_variable(ns_idx, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste Int!
    await vessel_speed_act_val.set_modelling_rule(True) # Mandatory ?
    await vessel_speed_act_val.set_writable(False)

    vessel_process_temperature = await vessel_process_daten_object.add_object(ns_idx, "Temperature")
    await vessel_process_temperature.add_reference(ua.ObjectIds.ModellingRule_Optional, ua.ObjectIds.HasModellingRule, True, False)
    vessel_process_temperature_setpoint = await vessel_process_temperature.add_variable(ns_idx, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
    await vessel_process_temperature_setpoint.set_modelling_rule(True) # Mandatory ?
    await vessel_process_temperature_setpoint.set_writable(True)
    vessel_process_temperature_act_val = await vessel_process_temperature.add_variable(ns_idx, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
    await vessel_process_temperature_act_val.set_modelling_rule(True) # Mandatory ?
    await vessel_process_temperature_act_val.set_writable(False)

    vessel_process_level = await vessel_process_daten_object.add_object(ns_idx, "Level")
    await vessel_process_level.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_process_level_volume = await vessel_process_level.add_object(ns_idx, "Volume")
    await vessel_process_level_volume.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    vessel_process_level_volume_measured = await vessel_process_level_volume.add_variable(ns_idx, "Measured", 0, ua.VariantType.Float) # Datentyp?
    await vessel_process_level_volume_measured.set_modelling_rule(False)
    await vessel_process_level_volume_measured.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?
    vessel_process_level_volume_calculated = await vessel_process_level_volume.add_variable(ns_idx, "Calculated", 0, ua.VariantType.Float) # Datentyp?
    await vessel_process_level_volume_calculated.set_modelling_rule(True)
    await vessel_process_level_volume_calculated.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?

    vessel_process_level_weight = await vessel_process_level.add_object(ns_idx, "Weight")
    await vessel_process_level_weight.add_reference(ua.ObjectIds.ModellingRule_Optional, ua.ObjectIds.HasModellingRule, True, False)
    vessel_process_level_weight_measured = await vessel_process_level_weight.add_variable(ns_idx, "Measured", 0, ua.VariantType.Float) # Datentyp?
    await vessel_process_level_weight_measured.set_modelling_rule(False)
    await vessel_process_level_weight_measured.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?
    vessel_process_level_weight_calculated = await vessel_process_level_weight.add_variable(ns_idx, "Calculated", 0, ua.VariantType.Float) # Datentyp?
    await vessel_process_level_weight_calculated.set_modelling_rule(False)
    await vessel_process_level_weight_calculated.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?

    vessel_process_container = await vessel_process_daten_object.add_object(ns_idx, "Container")
    await vessel_process_container.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    vessel_process_container_id = await vessel_process_container.add_property(ns_idx, "ContainerId", "", ua.VariantType.String) # Datentyp?
    await vessel_process_container_id.set_modelling_rule(True) # Mandatory ?
    await vessel_process_container_id.set_writable(False) # Write ?
    vessel_process_container_batch_id = await vessel_process_container.add_property(ns_idx, "BatchId", "", ua.VariantType.String) # Datentyp?
    await vessel_process_container_batch_id.set_modelling_rule(True) # Mandatory ?
    await vessel_process_container_batch_id.set_writable(False) # Write ?
    vessel_process_container_start_of_use = await vessel_process_container.add_property(ns_idx, "StartOfUse", ua.Variant(value=None, varianttype=ua.VariantType.DateTime), ua.VariantType.DateTime) # Datentyp?
    await vessel_process_container_start_of_use.set_modelling_rule(False)
    await vessel_process_container_start_of_use.set_writable(False) # Write ?

    '''
    ##############################################################################################################################################
    Ventil:
    ##############################################################################################################################################
    '''
    valve_object_type = await base_object_type.add_object_type(ns_idx, "ValveObjectType")

    # Metadaten
    valve_meta_object = await valve_object_type.add_object(ns_idx, "Meta")
    await valve_meta_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    valve_meta_name = await valve_meta_object.add_property(ns_idx, "Name", "", ua.VariantType.String) # Datentyp?
    await valve_meta_name.set_modelling_rule(True) # Mandatory ?
    await valve_meta_name.set_writable(False) # Write ?

    valve_meta_location= await valve_meta_object.add_property(ns_idx, "Location", "", ua.VariantType.String) # Datentyp?
    await valve_meta_location.set_modelling_rule(True) # Mandatory ?
    await valve_meta_location.set_writable(False) # Write ?

    valve_meta_serial = await valve_meta_object.add_property(ns_idx, "SerialNumber", "", ua.VariantType.String) # Datentyp?
    await valve_meta_serial.set_modelling_rule(True) # Mandatory ?
    await valve_meta_serial.set_writable(False) # Write ?

    valve_meta_type = await valve_meta_object.add_property(ns_idx, "Type", "", ua.VariantType.String) # Datentyp?
    await valve_meta_type.set_modelling_rule(True) # Mandatory ?
    await valve_meta_type.set_writable(False) # Write ?

    valve_meta_sectional_size = await valve_meta_object.add_property(ns_idx, "CrossSectionalSize", "", ua.VariantType.String) # Datentyp?
    await valve_meta_sectional_size.set_modelling_rule(True) # Mandatory ?
    await valve_meta_sectional_size.set_writable(False) # Write ?

    valve_meta_range = await valve_meta_object.add_object(ns_idx, "PhysicalRange")
    await valve_meta_range.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    valve_meta_range_trans = await valve_meta_range.add_property(ns_idx, "Translatonal", "", ua.VariantType.String) # Datentyp?
    await valve_meta_range_trans.set_modelling_rule(True) # Mandatory ?
    await valve_meta_range_trans.set_writable(False) # Write ?
    valve_meta_range_rotat = await valve_meta_range.add_property(ns_idx, "Rotational", "", ua.VariantType.String) # Datentyp?
    await valve_meta_range_rotat.set_modelling_rule(True) # Mandatory ?
    await valve_meta_range_rotat.set_writable(False) # Write ?

    valve_meta_cycles = await valve_meta_object.add_property(ns_idx, "Cycles", "", ua.VariantType.String) # Datentyp?
    await valve_meta_cycles.set_modelling_rule(True) # Mandatory ?
    await valve_meta_cycles.set_writable(False) # Write ?

    valve_meta_switch_open_time = await valve_meta_object.add_object(ns_idx, "OpeningTime")
    await valve_meta_switch_open_time.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    valve_meta_switch_open_time_min = await valve_meta_switch_open_time.add_property(ns_idx, "Min", "", ua.VariantType.String) # Datentyp?
    await valve_meta_switch_open_time_min.set_modelling_rule(True) # Mandatory ?
    await valve_meta_switch_open_time_min.set_writable(False) # Write ?
    valve_meta_switch_open_time_max = await valve_meta_switch_open_time.add_property(ns_idx, "Max", "", ua.VariantType.String) # Datentyp?
    await valve_meta_switch_open_time_max.set_modelling_rule(True) # Mandatory ?
    await valve_meta_switch_open_time_max.set_writable(False) # Write ?

    valve_meta_max_pressure = await valve_meta_object.add_property(ns_idx, "MaxPressure", "", ua.VariantType.String) # Datentyp?
    await valve_meta_max_pressure.set_modelling_rule(True) # Mandatory ?
    await valve_meta_max_pressure.set_writable(False) # Write ?

    valve_meta_switch_close_time = await valve_meta_object.add_object(ns_idx, "ClosingTime")
    await valve_meta_switch_close_time.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
    valve_meta_switch_close_time_min = await valve_meta_switch_close_time.add_property(ns_idx, "Min", "", ua.VariantType.String) # Datentyp?
    await valve_meta_switch_close_time_min.set_modelling_rule(True) # Mandatory ?
    await valve_meta_switch_close_time_min.set_writable(False) # Write ?
    valve_meta_switch_close_time_max = await valve_meta_switch_close_time.add_property(ns_idx, "Max", "", ua.VariantType.String) # Datentyp?
    await valve_meta_switch_close_time_max.set_modelling_rule(True) # Mandatory ?
    await valve_meta_switch_close_time_max.set_writable(False) # Write ?

    valve_meta_control_type = await valve_meta_object.add_property(ns_idx, "ControlTpye", "", ua.VariantType.String) # Datentyp?
    await valve_meta_control_type.set_modelling_rule(True) # Mandatory ?
    await valve_meta_control_type.set_writable(False) # Write ?

    valve_meta_flwo_rate = await valve_meta_object.add_property(ns_idx, "MaxFlowRate", "", ua.VariantType.String) # Datentyp?
    await valve_meta_flwo_rate.set_modelling_rule(True) # Mandatory ?
    await valve_meta_flwo_rate.set_writable(False) # Write ?

    valve_meta_ourput_type = await valve_meta_object.add_property(ns_idx, "OutputTpye", "", ua.VariantType.String) # Datentyp?
    await valve_meta_ourput_type.set_modelling_rule(True) # Mandatory ?
    await valve_meta_ourput_type.set_writable(False) # Write ?

    # State
    valve_state_object = await valve_object_type.add_object(ns_idx, "State")
    await valve_state_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    valve_state_operationalstate = await valve_state_object.add_variable(ns_idx, "OperationalState", 0, ua.VariantType.Int64) # Datentyp?
    await valve_state_operationalstate.set_modelling_rule(True) # Mandatory ?
    await valve_state_operationalstate.set_writable(False) # Write ?

    valve_state_operationalhours = await valve_state_object.add_variable(ns_idx, "OperationalHours", 0, ua.VariantType.Int64) # Datentyp?
    await valve_state_operationalhours.set_modelling_rule(True) # Mandatory ?
    await valve_state_operationalhours.set_writable(False) # Write ?

    valve_state_poweronhours = await valve_state_object.add_variable(ns_idx, "PowerOnHours", 0, ua.VariantType.Int64) # Datentyp? -> hh:mm:ss ?
    await valve_state_poweronhours.set_modelling_rule(True) # Mandatory ?
    await valve_state_poweronhours.set_writable(False) # Write ?

    # Prozessdaten
    valve_process_object = await valve_object_type.add_object(ns_idx, "ProcessData")
    await valve_process_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

    valve_process_opening_degree = await valve_process_object.add_object(ns_idx, "OpeningDegree")
    await valve_process_opening_degree.set_modelling_rule(True) # Mandatory ?

    valve_process_opening_degree_max = await valve_process_opening_degree.add_object(ns_idx, "OpeningDegreeMax") # wenn in machinery -> monitored parameter type!
    await valve_process_opening_degree_max.set_modelling_rule(True) # Mandatory ?
    valve_process_opening_degree_max_setpoint = await valve_process_opening_degree_max.add_variable(ns_idx, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
    await valve_process_opening_degree_max_setpoint.set_modelling_rule(True) # Mandatory ?
    await valve_process_opening_degree_max_setpoint.set_writable(True)
    valve_process_opening_degree_max_act_val = await valve_process_opening_degree_max.add_variable(ns_idx, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
    await valve_process_opening_degree_max_act_val.set_modelling_rule(True) # Mandatory ?
    await valve_process_opening_degree_max_act_val.set_writable(False)

    valve_process_opening_degree_min = await valve_process_opening_degree.add_object(ns_idx, "OpeningDegreeMin") # wenn in machinery -> monitored parameter type!
    await valve_process_opening_degree_min.set_modelling_rule(True) # Mandatory ?
    valve_process_opening_degree_min_setpoint = await valve_process_opening_degree_min.add_variable(ns_idx, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
    await valve_process_opening_degree_min_setpoint.set_modelling_rule(True) # Mandatory ?
    await valve_process_opening_degree_min_setpoint.set_writable(True)
    valve_process_opening_degree_min_act_val = await valve_process_opening_degree_min.add_variable(ns_idx, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
    await valve_process_opening_degree_min_act_val.set_modelling_rule(True) # Mandatory ?
    await valve_process_opening_degree_min_act_val.set_writable(False)

    valve_process_cylcles = await valve_process_object.add_variable(ns_idx, "Cycles", 0, ua.VariantType.Int64) # A.Heine was für ein Int ? 16, 32, 64 und warum nicht UInt ?
    await valve_process_cylcles.set_modelling_rule(True) # Mandatory 

    valve_process_open_time = await valve_process_object.add_variable(ns_idx, "OpenTime", 0, ua.VariantType.Float)
    await valve_process_open_time.set_modelling_rule(True) # Mandatory 



    # Export Namespace as xml
    try:
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

    await server.export_xml_by_ns(os.path.join(BASE_DIR, "nodeset", XML_FILENAME), namespaces=NAMESPACE)


if __name__ == "__main__":
    asyncio.run(main())
