from asyncua import ua

class PipeObjectTypeClass(object):
    def __init__(self, server, namespace):
        self.server = server
        self.namespace = namespace
        self.base_object_type = self.server.get_node(ua.ObjectIds.BaseObjectType)
        self.folder_object_type = self.server.get_node(ua.ObjectIds.FolderType)
        self.analog_item_type = self.server.get_node(ua.ObjectIds.AnalogItemType)


    async def build(self):
        pipe_object_type = await self.base_object_type.add_object_type(self.namespace, "PipeObjectType")

        pipe_meta_object = await pipe_object_type.add_object(self.namespace, "Meta", self.folder_object_type)
        await pipe_meta_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
        pipe_state_object = await pipe_object_type.add_object(self.namespace, "State", self.folder_object_type)
        await pipe_state_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)
        pipe_process_object = await pipe_object_type.add_object(self.namespace, "Process", self.folder_object_type)
        await pipe_process_object.add_reference(ua.ObjectIds.ModellingRule_Mandatory, ua.ObjectIds.HasModellingRule, True, False)