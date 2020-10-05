from asyncua import ua
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SurfaceTechnologieParameterTypeClass(object):
    def __init__(self, server, namespace):
        self.server = server
        self.namespace = namespace
        self.base_variable_type = self.server.get_node(ua.ObjectIds.BaseDataVariableType)
        self.folder_object_type = self.server.get_node(ua.ObjectIds.FolderType)
        self.analog_item_type = self.server.get_node(ua.ObjectIds.AnalogItemType)


    async def build(self):
        parameter_type = await self.base_variable_type.add_variable_type(self.namespace, "SurfaceTechnologieParameterType", ua.ObjectIds.Float)

        parameter_type_actual_value = await parameter_type.add_object(self.namespace, "ActualValue", self.analog_item_type)
        parameter_type_setpoint_value = await parameter_type.add_object(self.namespace, "SetpointValue", self.analog_item_type)
