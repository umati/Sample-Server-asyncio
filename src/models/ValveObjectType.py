from asyncua import ua

class ValveObjectTypeClass(object):
    def __init__(self, server, namespace):
        self.server = server
        self.namespace = namespace
        self.base_object_type = self.server.get_node(ua.ObjectIds.BaseObjectType)
        self.folder_object_type = self.server.get_node(ua.ObjectIds.FolderType)
        self.analog_item_type = self.server.get_node(ua.ObjectIds.AnalogItemType)

    async def build(self):
        parameter_type = await self.base_object_type.get_child([f"{self.namespace}:SurfaceTechnologieParameterType"])

        myrange = ua.uaprotocol_auto.Range()
        myrange.High = 0
        myrange.Low = 0

        valve_object_type = await self.base_object_type.add_object_type(self.namespace, "ValveObjectType")

        # Metadaten
        valve_meta_object = await valve_object_type.add_object(self.namespace, "Meta", self.folder_object_type)
        await valve_meta_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        valve_meta_name = await valve_meta_object.add_property(self.namespace, "Name", "", ua.VariantType.String)
        await valve_meta_name.set_modelling_rule(True)
        await valve_meta_name.set_writable(False)

        valve_meta_location= await valve_meta_object.add_property(self.namespace, "Location", "", ua.VariantType.String)
        await valve_meta_location.set_modelling_rule(True)
        await valve_meta_location.set_writable(True)

        valve_meta_serial = await valve_meta_object.add_property(self.namespace, "SerialNumber", "", ua.VariantType.String)
        await valve_meta_serial.set_modelling_rule(True)
        await valve_meta_serial.set_writable(False)

        valve_meta_type = await valve_meta_object.add_property(self.namespace, "Type", "", ua.VariantType.String)
        await valve_meta_type.set_modelling_rule(True)
        await valve_meta_type.set_writable(False)

        valve_meta_sectional_size = await valve_meta_object.add_property(self.namespace, "CrossSectionalSize", 0.0, ua.VariantType.Float)
        await valve_meta_sectional_size.set_modelling_rule(False)
        await valve_meta_sectional_size.set_writable(True)

        valve_meta_range = await valve_meta_object.add_object(self.namespace, "PhysicalRange")
        await valve_meta_range.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
        valve_meta_range_trans = await valve_meta_range.add_property(self.namespace, "Translatonal", 0.0, ua.VariantType.Float)
        await valve_meta_range_trans.set_modelling_rule(False)
        await valve_meta_range_trans.set_writable(False)
        valve_meta_range_rotat = await valve_meta_range.add_property(self.namespace, "Rotational", 0.0, ua.VariantType.Float)
        await valve_meta_range_rotat.set_modelling_rule(False)
        await valve_meta_range_rotat.set_writable(False)

        valve_meta_cycles = await valve_meta_object.add_property(self.namespace, "Cycles", 0, ua.VariantType.UInt64)
        await valve_meta_cycles.set_modelling_rule(False)
        await valve_meta_cycles.set_writable(False)

        valve_meta_switch_open_time = await valve_meta_object.add_property(self.namespace, "OpeningTime", myrange, varianttype=ua.VariantType.ExtensionObject)
        # valve_meta_switch_open_time = await valve_meta_object.add_object(self.namespace, "OpeningTime")
        await valve_meta_switch_open_time.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
        # valve_meta_switch_open_time_min = await valve_meta_switch_open_time.add_property(self.namespace, "Min", "", ua.VariantType.String) # Datentyp?
        # await valve_meta_switch_open_time_min.set_modelling_rule(True) # Mandatory ?
        # await valve_meta_switch_open_time_min.set_writable(False)
        # valve_meta_switch_open_time_max = await valve_meta_switch_open_time.add_property(self.namespace, "Max", "", ua.VariantType.String) # Datentyp?
        # await valve_meta_switch_open_time_max.set_modelling_rule(True) # Mandatory ?
        # await valve_meta_switch_open_time_max.set_writable(False)

        valve_meta_max_pressure = await valve_meta_object.add_property(self.namespace, "MaxPressure", 0.0, ua.VariantType.Float)
        await valve_meta_max_pressure.set_modelling_rule(False)
        await valve_meta_max_pressure.set_writable(True)

        valve_meta_switch_close_time = await valve_meta_object.add_property(self.namespace, "ClosingTime", myrange, varianttype=ua.VariantType.ExtensionObject)
        # valve_meta_switch_close_time = await valve_meta_object.add_object(self.namespace, "ClosingTime")
        await valve_meta_switch_close_time.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
        # valve_meta_switch_close_time_min = await valve_meta_switch_close_time.add_property(self.namespace, "Min", "", ua.VariantType.String) # Datentyp?
        # await valve_meta_switch_close_time_min.set_modelling_rule(True) # Mandatory ?
        # await valve_meta_switch_close_time_min.set_writable(False)
        # valve_meta_switch_close_time_max = await valve_meta_switch_close_time.add_property(self.namespace, "Max", "", ua.VariantType.String) # Datentyp?
        # await valve_meta_switch_close_time_max.set_modelling_rule(True) # Mandatory ?
        # await valve_meta_switch_close_time_max.set_writable(False)

        valve_meta_control_type = await valve_meta_object.add_property(self.namespace, "ControlTpye", "", ua.VariantType.String)
        await valve_meta_control_type.set_modelling_rule(False)
        await valve_meta_control_type.set_writable(True)

        valve_meta_flwo_rate = await valve_meta_object.add_property(self.namespace, "MaxFlowRate", 0.0, ua.VariantType.Float)
        await valve_meta_flwo_rate.set_modelling_rule(False)
        await valve_meta_flwo_rate.set_writable(True)

        valve_meta_ourput_type = await valve_meta_object.add_property(self.namespace, "OutputTpye", "", ua.VariantType.String)
        await valve_meta_ourput_type.set_modelling_rule(False)
        await valve_meta_ourput_type.set_writable(True)

        # State
        valve_state_object = await valve_object_type.add_object(self.namespace, "State", self.folder_object_type)
        await valve_state_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        valve_state_operationalstate = await valve_state_object.add_object(self.namespace, "OperationalState", self.server.get_node(ua.ObjectIds.StateMachineType), instantiate_optional=False)
        await valve_state_operationalstate.set_modelling_rule(True)
        valve_state_operationalstate_currentstate = await valve_state_operationalstate.get_child("CurrentState")
        await valve_state_operationalstate_currentstate.set_modelling_rule(True)
        valve_state_operationalstate_currentstate_id = await valve_state_operationalstate_currentstate.get_child("Id")
        await valve_state_operationalstate_currentstate_id.set_modelling_rule(True)
        # valve_state_operationalstate_lasttransition = await valve_state_operationalstate.get_child("LastTransition")
        # await valve_state_operationalstate_lasttransition.set_modelling_rule(False)
        # valve_state_operationalstate_lasttransition_id = await valve_state_operationalstate_lasttransition.get_child("Id")
        # await valve_state_operationalstate_lasttransition_id.set_modelling_rule(True)

        valve_state_operationalhours = await valve_state_object.add_variable(self.namespace, "OperationalHours", 0, ua.VariantType.Int64) # Datentyp?
        await valve_state_operationalhours.set_modelling_rule(True) # Mandatory ?
        await valve_state_operationalhours.set_writable(False)

        valve_state_poweronhours = await valve_state_object.add_variable(self.namespace, "PowerOnHours", 0, ua.VariantType.Int64) # Datentyp?
        await valve_state_poweronhours.set_modelling_rule(True) # Mandatory ?
        await valve_state_poweronhours.set_writable(False)

        # Prozessdaten
        valve_process_object = await valve_object_type.add_object(self.namespace, "Process", self.folder_object_type)
        await valve_process_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)

        valve_process_opening_degree = await valve_process_object.add_object(self.namespace, "OpeningDegree")
        await valve_process_opening_degree.set_modelling_rule(True) # Mandatory ?

        valve_process_opening_degree_max = await valve_process_opening_degree.add_object(self.namespace, "OpeningDegreeMax", objecttype=parameter_type, instantiate_optional=True)
        await valve_process_opening_degree_max.set_modelling_rule(True) # Mandatory ?
        # valve_process_opening_degree_max_setpoint = await valve_process_opening_degree_max.add_variable(self.namespace, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
        valve_process_opening_degree_max_setpoint = await valve_process_opening_degree_max.get_child(f"{self.namespace}:SetpointValue")
        await valve_process_opening_degree_max_setpoint.set_modelling_rule(True) # Mandatory ?
        await valve_process_opening_degree_max_setpoint.set_writable(True)
        # valve_process_opening_degree_max_act_val = await valve_process_opening_degree_max.add_variable(self.namespace, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
        valve_process_opening_degree_max_act_val = await valve_process_opening_degree_max.get_child(f"{self.namespace}:ActualValue")
        await valve_process_opening_degree_max_act_val.set_modelling_rule(True) # Mandatory ?
        await valve_process_opening_degree_max_act_val.set_writable(False)

        valve_process_opening_degree_min = await valve_process_opening_degree.add_object(self.namespace, "OpeningDegreeMin", objecttype=parameter_type, instantiate_optional=True)
        await valve_process_opening_degree_min.set_modelling_rule(True) # Mandatory ?
        # valve_process_opening_degree_min_setpoint = await valve_process_opening_degree_min.add_variable(self.namespace, "SetpointValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
        valve_process_opening_degree_min_setpoint = await valve_process_opening_degree_min.get_child(f"{self.namespace}:SetpointValue")
        await valve_process_opening_degree_min_setpoint.set_modelling_rule(True) # Mandatory ?
        await valve_process_opening_degree_min_setpoint.set_writable(True)
        # valve_process_opening_degree_min_act_val = await valve_process_opening_degree_min.add_variable(self.namespace, "ActualValue", 0, ua.VariantType.Float) # Datentyp? A.Heine: Laut Parameterliste ...?
        valve_process_opening_degree_min_act_val = await valve_process_opening_degree_min.get_child(f"{self.namespace}:ActualValue")
        await valve_process_opening_degree_min_act_val.set_modelling_rule(True) # Mandatory ?
        await valve_process_opening_degree_min_act_val.set_writable(False)

        valve_process_cylcles = await valve_process_object.add_variable(self.namespace, "Cycles", 0, ua.VariantType.UInt64) # A.Heine was für ein Int ? 16, 32, 64 und warum nicht UInt ?
        await valve_process_cylcles.set_modelling_rule(False)
        await valve_process_cylcles.set_writable(False)

        valve_process_open_time = await valve_process_object.add_variable(self.namespace, "OpenTime", 0, ua.VariantType.Float)
        await valve_process_open_time.set_modelling_rule(False)
        await valve_process_open_time.set_writable(False)

