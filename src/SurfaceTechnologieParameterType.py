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

        parameter_type_actual_value = await parameter_type.add_object(self.namespace, "ActualValue", self.analog_item_type)
        await parameter_type_actual_value.set_modelling_rule(True)
        parameter_type_setpoint_value = await parameter_type.add_object(self.namespace, "SetpointValue", self.analog_item_type)
        await parameter_type_setpoint_value.set_modelling_rule(True)


        '''
        To Do:
        Rename SurfaceTechnologieMonitoredParameterType -> HasComp. SurfaceTechnologieParameterType -> Is/HasSubtype AnalogItemType
        '''