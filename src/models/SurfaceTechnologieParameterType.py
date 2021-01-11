from asyncua import ua

class SurfaceTechnologieParameterTypeClass(object):
    def __init__(self, server, namespace):
        self.server = server
        self.namespace = namespace
        self.base_object_type = self.server.get_node(ua.ObjectIds.BaseObjectType)
        self.folder_object_type = self.server.get_node(ua.ObjectIds.FolderType)
        self.analog_item_type = self.server.get_node(ua.ObjectIds.AnalogItemType)


    async def build(self):
        parameter_type = await self.base_object_type.add_object_type(self.namespace, "SurfaceTechnologieParameterType")

        parameter_type_actual_value = await parameter_type.add_object(self.namespace, "ActualValue", self.analog_item_type, instantiate_optional=True)
        await parameter_type_actual_value.set_modelling_rule(True)
        parameter_type_actual_value_EURange = await parameter_type_actual_value.get_child("EURange")
        await parameter_type_actual_value_EURange.set_modelling_rule(True)
        parameter_type_actual_value_EngineeringUnits = await parameter_type_actual_value.get_child("EngineeringUnits")
        await parameter_type_actual_value_EngineeringUnits.set_modelling_rule(False)
        parameter_type_actual_value_InstrumentRange = await parameter_type_actual_value.get_child("InstrumentRange")
        await parameter_type_actual_value_InstrumentRange.set_modelling_rule(False)
        parameter_type_actual_value_Definition = await parameter_type_actual_value.get_child("Definition")
        await parameter_type_actual_value_Definition.set_modelling_rule(False)
        parameter_type_actual_value_ValuePrecision = await parameter_type_actual_value.get_child("ValuePrecision")
        await parameter_type_actual_value_ValuePrecision.set_modelling_rule(False)

        parameter_type_setpoint_value = await parameter_type.add_object(self.namespace, "SetpointValue", self.analog_item_type, instantiate_optional=True)
        await parameter_type_setpoint_value.set_modelling_rule(False)
        parameter_type_setpoint_value_EURange = await parameter_type_setpoint_value.get_child("EURange")
        await parameter_type_setpoint_value_EURange.set_modelling_rule(True)
        parameter_type_setpoint_value_EngineeringUnits = await parameter_type_setpoint_value.get_child("EngineeringUnits")
        await parameter_type_setpoint_value_EngineeringUnits.set_modelling_rule(False)
        parameter_type_setpoint_value_InstrumentRange = await parameter_type_setpoint_value.get_child("InstrumentRange")
        await parameter_type_setpoint_value_InstrumentRange.set_modelling_rule(False)
        parameter_type_setpoint_value_Definition = await parameter_type_setpoint_value.get_child("Definition")
        await parameter_type_setpoint_value_Definition.set_modelling_rule(False)
        parameter_type_setpoint_value_ValuePrecision = await parameter_type_setpoint_value.get_child("ValuePrecision")
        await parameter_type_setpoint_value_ValuePrecision.set_modelling_rule(False)
