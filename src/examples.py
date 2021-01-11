from asyncua import ua

class DemoBeschichtungsanlage(object):
    def __init__(self, server, idx):
        self.server = server
        self.idx = idx
        self.base_object_type = self.server.get_node(ua.ObjectIds.BaseObjectType)
        self.folder_object_type = self.server.get_node(ua.ObjectIds.FolderType)
        self.analog_item_type = self.server.get_node(ua.ObjectIds.AnalogItemType)


    async def install(self):
        di_idx = await self.server.get_namespace_index("http://opcfoundation.org/UA/DI/")
        ma_idx = await self.server.get_namespace_index("http://opcfoundation.org/UA/Machinery/")
        st_idx = await self.server.get_namespace_index("http://vdma-opc-st-initiative-cs/ua")

        objects = self.server.get_objects_node()
        deviceset = await objects.get_child([f"{di_idx}:DeviceSet"])

        base_object_type = self.server.get_node("ns=0;i=58")
        vessel_object_type = await base_object_type.get_child([f"{st_idx}:VesselObjectType"])
        valve_object_type = await base_object_type.get_child([f"{st_idx}:ValveObjectType"])

        machines_folder = await objects.get_child([f"{ma_idx}:Machines"])

        self.anlage = await objects.add_object(self.idx, "Beschichtungsanlage", objecttype=ua.ObjectIds.BaseObjectType)
        await self.anlage.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        self.anlage_components = await self.anlage.add_folder(self.idx, "Components")
        await machines_folder.add_reference(self.anlage, ua.ObjectIds.Organizes)
        await deviceset.add_reference(self.anlage, ua.ObjectIds.Organizes)

        materialversorgungsraum = await self.anlage.add_object(self.idx, "MaterialversorgungsRaum", objecttype=ua.ObjectIds.BaseObjectType)
        await materialversorgungsraum.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        materialversorgungsraum_components = await materialversorgungsraum.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(materialversorgungsraum, ua.ObjectIds.Organizes)

        '''
        Materialversorgung
        '''
        materialversorgung = await materialversorgungsraum.add_object(self.idx, "Materialversorgung", objecttype=ua.ObjectIds.BaseObjectType)
        await materialversorgung.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        farbmischraum_components = await materialversorgung.add_folder(self.idx, "Components")
        await materialversorgungsraum_components.add_reference(materialversorgung, ua.ObjectIds.Organizes)

        # anlage_fg01  = await self.anlage.add_folder(self.idx, "FG01")
        fg01 = await materialversorgung.add_object(self.idx, "FG01", self.server.get_node(f"ns={di_idx};i=1005"), instantiate_optional=False)

        fg01_ansatzbehälter = await fg01.add_object(self.idx, "FG01_Ansatzbehälter", objecttype=vessel_object_type)
        await fg01_ansatzbehälter.add_folder(self.idx, "ComponentsIdentification")
        await farbmischraum_components.add_reference(fg01_ansatzbehälter, ua.ObjectIds.Organizes)

        fg01_auslassventil = await fg01.add_object(self.idx, "FG01_Auslassventil", objecttype=valve_object_type)
        await fg01_auslassventil.add_folder(self.idx, "ComponentsIdentification")
        await farbmischraum_components.add_reference(fg01_auslassventil, ua.ObjectIds.Organizes)

        # anlage_fg02  = await self.anlage.add_folder(self.idx, "FG02")
        fg02 = await materialversorgung.add_object(self.idx, "FG02", self.server.get_node(f"ns={di_idx};i=1005"), instantiate_optional=False)

        fg02_versorgungsbehälter = await fg02.add_object(self.idx, "FG02_Versorgungsbehälter", objecttype=vessel_object_type)
        await fg02_versorgungsbehälter.add_folder(self.idx, "ComponentsIdentification")
        await farbmischraum_components.add_reference(fg02_versorgungsbehälter, ua.ObjectIds.Organizes)

        fg02_einlassventil = await fg02.add_object(self.idx, "FG02_Einlassventil", objecttype=valve_object_type)
        await fg02_einlassventil.add_folder(self.idx, "ComponentsIdentification")
        await farbmischraum_components.add_reference(fg02_einlassventil, ua.ObjectIds.Organizes)

        fg02_auslassventil = await fg02.add_object(self.idx, "FG02_Auslassventil", objecttype=valve_object_type)
        await fg02_auslassventil.add_folder(self.idx, "ComponentsIdentification")
        await farbmischraum_components.add_reference(fg02_auslassventil, ua.ObjectIds.Organizes)

        '''
        ############################################################################################################################
        '''
        applikationsgeraet = await self.anlage.add_object(self.idx, "Applikationsgerät", objecttype=ua.ObjectIds.BaseObjectType)
        await applikationsgeraet.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        applikationsgeraet_components = await applikationsgeraet.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(applikationsgeraet, ua.ObjectIds.Organizes)

        vbh = await self.anlage.add_object(self.idx, "Vorbehandlung", objecttype=ua.ObjectIds.BaseObjectType)
        await vbh.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        vbh_components = await vbh.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(vbh, ua.ObjectIds.Organizes)

        beschichtunngskabine = await self.anlage.add_object(self.idx, "Beschichtunngskabine", objecttype=ua.ObjectIds.BaseObjectType)
        await beschichtunngskabine.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        beschichtunngskabine_components = await beschichtunngskabine.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(beschichtunngskabine, ua.ObjectIds.Organizes)

        tauchlackieranalge = await self.anlage.add_object(self.idx, "Tauchlackieranalge", objecttype=ua.ObjectIds.BaseObjectType)
        await tauchlackieranalge.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        tauchlackieranalge_components = await tauchlackieranalge.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(tauchlackieranalge, ua.ObjectIds.Organizes)

        trockner = await self.anlage.add_object(self.idx, "Trockner", objecttype=ua.ObjectIds.BaseObjectType)
        await trockner.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        trockner_components = await trockner.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(trockner, ua.ObjectIds.Organizes)

        foerdertechnik = await self.anlage.add_object(self.idx, "Fördertechnik", objecttype=ua.ObjectIds.BaseObjectType)
        await foerdertechnik.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        foerdertechnik_components = await foerdertechnik.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(foerdertechnik, ua.ObjectIds.Organizes)

        prozesslufttechnischeanlage = await self.anlage.add_object(self.idx, "ProzesslufttechnischeAnlage", objecttype=ua.ObjectIds.BaseObjectType)
        await prozesslufttechnischeanlage.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        prozesslufttechnischeanlage_components = await prozesslufttechnischeanlage.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(prozesslufttechnischeanlage, ua.ObjectIds.Organizes)

        filteranlage = await self.anlage.add_object(self.idx, "Filteranlage", objecttype=ua.ObjectIds.BaseObjectType)
        await filteranlage.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        filteranlage_components = await filteranlage.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(filteranlage, ua.ObjectIds.Organizes)

        abluftreinigungssystem = await self.anlage.add_object(self.idx, "Abluftreinigungssystem", objecttype=ua.ObjectIds.BaseObjectType)
        await abluftreinigungssystem.add_object(self.idx, "Identification", self.server.get_node(f"ns={ma_idx};i=1012"), instantiate_optional=False)
        abluftreinigungssystem_components = await abluftreinigungssystem.add_folder(self.idx, "Components")
        await self.anlage_components.add_reference(abluftreinigungssystem, ua.ObjectIds.Organizes)