import asyncio
import datetime
import logging
from aiofile import AIOFile, LineReader
from asyncua import Server, Node, ua

class CSV_IMPORTER(object):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.nodes = [] # list(tuple(node,dtype))
        self.rows = [] # [list(zip(self.nodes, row_values)), list(zip(self.nodes, row_values)), ...]

    async def get_node_from_path(self, path):
        # check if path starts and/or ends with "/" and remove it before split
        splitpath = path.split("/")
        new_path = []
        for item in splitpath:
            if item == "":
                pass
            else:
                new_path.append(item)
        
        current_node = self.server.nodes.root
        for item in new_path:
            current_node_children = await current_node.get_children()
            for child in current_node_children:
                cname = await child.read_browse_name()
                if cname.Name == item:
                    current_node = child
                    break       
        return current_node

    async def read_csv(self, csv):
        async with AIOFile(csv, 'r') as afp:
            linecount = 0
            bpaths = []
            values = []
            async for line in LineReader(afp):
                if linecount == 0:
                    # first line has BrowsePaths
                    line = line.replace("\n","")
                    line = line.replace("\r","")
                    line = line.strip()
                    bpaths = line.split(",")
                    for p in bpaths:
                        if p == "":
                            pass
                        else:
                            p = p.strip()
                            try:
                                node = await self.get_node_from_path(p)
                                dtype = await node.read_data_type()
                                self.nodes.append((node, dtype))
                            except Exception as e:
                                print(e)
                                pass
                else:
                    # following lines have values
                    line = line.replace("\n","")
                    line = line.replace("\r","")
                    line = line.strip()
                    values = line.split(",")
                    stripped_values = []
                    for v in values:
                        stripped_values.append(v.strip())
                    row = list(zip(self.nodes, stripped_values))
                    self.rows.append(row)
                    await asyncio.sleep(0)
                linecount+=1

    async def get_rows(self):
        return self.rows      