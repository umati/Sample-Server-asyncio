from asyncua import ua

class PumpObjectTypeClass(object):
    def __init__(self, server, namespace):
        self.server = server
        self.namespace = namespace
        self.base_object_type = self.server.get_node(ua.ObjectIds.BaseObjectType)
        self.folder_object_type = self.server.get_node(ua.ObjectIds.FolderType)
        self.analog_item_type = self.server.get_node(ua.ObjectIds.AnalogItemType)


    async def build(self):
        pump_object_type = await self.base_object_type.add_object_type(self.namespace, "PumpObjectType")

        pump_meta_object = await pump_object_type.add_object(self.namespace, "Meta", self.folder_object_type)
        pump_state_object = await pump_object_type.add_object(self.namespace, "State", self.folder_object_type)
        pump_process_object = await pump_object_type.add_object(self.namespace, "ProcessData", self.folder_object_type)