from asyncua import ua

class VesselObjectTypeClass(object):
    def __init__(self, server, namespace):
        self.server = server
        self.namespace = namespace
        self.base_object_type = self.server.get_node(ua.ObjectIds.BaseObjectType)
        self.folder_object_type = self.server.get_node(ua.ObjectIds.FolderType)
        self.analog_item_type = self.server.get_node(ua.ObjectIds.AnalogItemType)

    async def build(self):
        vessel_object_type = await self.base_object_type.add_object_type(self.namespace, "VesselObjectType")
        parameter_type = await self.base_object_type.get_child([f"{self.namespace}:SurfaceTechnologieParameterType"])

        # Metadaten
        vessel_meta_object = await vessel_object_type.add_object(self.namespace, "Meta", self.folder_object_type)
        await vessel_meta_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        vessel_meta_name = await vessel_meta_object.add_property(self.namespace, "Name", "", ua.VariantType.String)
        await vessel_meta_name.set_modelling_rule(True) # Mandatory ?
        await vessel_meta_name.set_writable(False)

        vessel_meta_location= await vessel_meta_object.add_property(self.namespace, "Location", "", ua.VariantType.String)
        await vessel_meta_location.set_modelling_rule(True) # Mandatory ?
        await vessel_meta_location.set_writable(True)

        vessel_meta_serial = await vessel_meta_object.add_property(self.namespace, "SerialNumber", "", ua.VariantType.String)
        await vessel_meta_serial.set_modelling_rule(True) # Mandatory ?
        await vessel_meta_serial.set_writable(False)

        vessel_meta_volume = await vessel_meta_object.add_property(self.namespace, "Volume", 0.0, ua.VariantType.Float)
        await vessel_meta_volume.set_modelling_rule(True) # Mandatory ?
        await vessel_meta_volume.set_writable(False)

        # State
        vessel_state_object = await vessel_object_type.add_object(self.namespace, "State", self.folder_object_type)
        await vessel_state_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        vessel_state_operationalstate = await vessel_state_object.add_variable(self.namespace, "OperationalState", 0, ua.VariantType.Int64) # !!! FIXME !!! FiniteStateMachineType
        await vessel_state_operationalstate.set_modelling_rule(True)
        await vessel_state_operationalstate.set_writable(False)

        vessel_state_operationalhours = await vessel_state_object.add_variable(self.namespace, "OperationalHours", 0, ua.VariantType.Int64) # Datentyp?
        await vessel_state_operationalhours.set_modelling_rule(True) # Mandatory ?
        await vessel_state_operationalhours.set_writable(False)

        vessel_state_poweronhours = await vessel_state_object.add_variable(self.namespace, "PowerOnHours", 0, ua.VariantType.Int64) # Datentyp? A.Heine: hh:mm:ss ?
        await vessel_state_poweronhours.set_modelling_rule(True) # Mandatory ?
        await vessel_state_poweronhours.set_writable(False)

        # Prozessdaten
        vessel_process_daten_object = await vessel_object_type.add_object(self.namespace, "Process", self.folder_object_type)
        await vessel_process_daten_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        # !!! FIXME !!! 
        # Actual values -> AnalogItemType
        # Setpoint values -> AnalogItemType

        vessel_process_speed = await vessel_process_daten_object.add_object(self.namespace, "AgitatorSpeed", objecttype=parameter_type)
        await vessel_process_speed.add_reference(ua.ObjectIds.ModellingRule_Optional, ua.ObjectIds.HasModellingRule, True, False)
        # vessel_speed_setpoint = await vessel_process_speed.add_variable(self.namespace, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste Int!
        vessel_speed_setpoint = await vessel_process_speed.get_child(f"{self.namespace}:SetpointValue")
        await vessel_speed_setpoint.set_modelling_rule(True) # Mandatory ?
        await vessel_speed_setpoint.set_writable(True)
        # vessel_speed_act_val = await vessel_process_speed.add_variable(self.namespace, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste Int!
        vessel_speed_act_val = await vessel_process_speed.get_child(f"{self.namespace}:ActualValue")
        await vessel_speed_act_val.set_modelling_rule(True) # Mandatory ?
        await vessel_speed_act_val.set_writable(False)

        vessel_process_temperature = await vessel_process_daten_object.add_object(self.namespace, "Temperature", objecttype=parameter_type)
        await vessel_process_temperature.add_reference(ua.ObjectIds.ModellingRule_Optional, ua.ObjectIds.HasModellingRule, True, False)
        # vessel_process_temperature_setpoint = await vessel_process_temperature.add_variable(self.namespace, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
        vessel_process_temperature_setpoint = await vessel_process_temperature.get_child(f"{self.namespace}:SetpointValue")
        await vessel_process_temperature_setpoint.set_modelling_rule(True) # Mandatory ?
        await vessel_process_temperature_setpoint.set_writable(True)
        # vessel_process_temperature_act_val = await vessel_process_temperature.add_variable(self.namespace, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
        vessel_process_temperature_act_val = await vessel_process_temperature.get_child(f"{self.namespace}:ActualValue")
        await vessel_process_temperature_act_val.set_modelling_rule(True) # Mandatory ?
        await vessel_process_temperature_act_val.set_writable(False)

        vessel_process_level = await vessel_process_daten_object.add_object(self.namespace, "Level")
        await vessel_process_level.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        vessel_process_level_volume = await vessel_process_level.add_object(self.namespace, "Volume")
        await vessel_process_level_volume.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
        vessel_process_level_volume_measured = await vessel_process_level_volume.add_variable(self.namespace, "Measured", 0.0, ua.VariantType.Float) # Datentyp?
        await vessel_process_level_volume_measured.set_modelling_rule(False)
        await vessel_process_level_volume_measured.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?
        vessel_process_level_volume_calculated = await vessel_process_level_volume.add_variable(self.namespace, "Calculated", 0.0, ua.VariantType.Float) # Datentyp?
        await vessel_process_level_volume_calculated.set_modelling_rule(True)
        await vessel_process_level_volume_calculated.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?

        vessel_process_level_weight = await vessel_process_level.add_object(self.namespace, "Weight")
        await vessel_process_level_weight.add_reference(ua.ObjectIds.ModellingRule_Optional, ua.ObjectIds.HasModellingRule, True, False)
        vessel_process_level_weight_measured = await vessel_process_level_weight.add_variable(self.namespace, "Measured", 0.0, ua.VariantType.Float) # Datentyp?
        await vessel_process_level_weight_measured.set_modelling_rule(False)
        await vessel_process_level_weight_measured.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?
        vessel_process_level_weight_calculated = await vessel_process_level_weight.add_variable(self.namespace, "Calculated", 0.0, ua.VariantType.Float) # Datentyp?
        await vessel_process_level_weight_calculated.set_modelling_rule(False)
        await vessel_process_level_weight_calculated.set_writable(False) # Write ? A.Heine: Laut Parameterliste ...?

        vessel_process_container = await vessel_process_daten_object.add_object(self.namespace, "Container")
        await vessel_process_container.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        vessel_process_container_id = await vessel_process_container.add_property(self.namespace, "ContainerId", "", ua.VariantType.String) # Datentyp?
        await vessel_process_container_id.set_modelling_rule(True) # Mandatory ?
        await vessel_process_container_id.set_writable(False) # Write ?
        vessel_process_container_batch_id = await vessel_process_container.add_property(self.namespace, "BatchId", "", ua.VariantType.String) # Datentyp?
        await vessel_process_container_batch_id.set_modelling_rule(True) # Mandatory ?
        await vessel_process_container_batch_id.set_writable(False) # Write ?
        vessel_process_container_start_of_use = await vessel_process_container.add_property(self.namespace, "StartOfUse", ua.Variant(value=None, varianttype=ua.VariantType.DateTime), ua.VariantType.DateTime) # Datentyp?
        await vessel_process_container_start_of_use.set_modelling_rule(False)
        await vessel_process_container_start_of_use.set_writable(False) # Write ?

        # Alarms & Conditions
        '''
        Die Variable die einen Alarm hat bekommt eine "HasCondition"-Referenz die auf den Alarm namen verweist welcher im Alarms ordner ist!? 
        Überprüfen wie es in anderen AG realisiert wurde evtl. muss man den Alarm direkt bei der Variable einordnen (selber Parentnode)!
        '''
        # vessel_alarms = await vessel_object_type.add_object(self.namespace, "Alarms", self.folder_object_type)
        # await vessel_alarms.set_modelling_rule(False) # Mandatory ?