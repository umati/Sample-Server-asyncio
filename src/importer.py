import asyncio
import datetime
import logging
from aiofile import AIOFile, LineReader
from asyncua import Server, Node, ua

class CSV_IMPORTER(object):
    def __init__(self, server, nsidx):
        super().__init__()
        self.server = server
        self.nsidx = nsidx
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
                # path starts from root so objects is the first item
                if item == "Objects":
                    # add default ns idx 0
                    item ="0:Objects"
                else:
                    # setup BrowseName ("ns:name")
                    item = f"{self.nsidx}:{item}"
                new_path.append(item)
        return await self.server.nodes.root.get_child(new_path)

    async def read_csv(self, csv):
        async with AIOFile(csv, 'r') as afp:
            linecount = 0
            bpaths = []
            values = []
            async for line in LineReader(afp):
                if linecount == 0:
                    # first line had BrowsePaths
                    line = line.replace("\n","")
                    line = line.replace("\r","")
                    bpaths = line.split(",")
                    for p in bpaths:
                        if p == "":
                            pass
                        else:
                            try:
                                node = await self.get_node_from_path(p)
                                dtype = await node.read_data_type()
                                self.nodes.append((node, dtype))
                            except Exception:
                                pass
                else:
                    # following lines have values
                    line = line.replace("\n","")
                    line = line.replace("\r","")
                    values = line.split(",")
                    row = list(zip(self.nodes, values))
                    self.rows.append(row)
                    await asyncio.sleep(0)
                linecount+=1

    async def get_rows(self):
        return self.rows      
