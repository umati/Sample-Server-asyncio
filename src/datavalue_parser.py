import time
from datetime import datetime
from asyncua import Server, ua
from asyncua.common.ua_utils import value_to_datavalue

async def parse_to_datavalue(item, start_time, build_date):
    '''
    item[1] -> Value from csv -> type string (must be casted to correct type)
    item[0] -> tuple(node, dtype, bname)
    item[0][0] -> Node-Instance
    item[0][1] -> DataType
    item[0][2] -> BrowseName
    '''
    if item[0] is None:
        return None

    if item[0][2].Name == "PowerOnHours":
        v = int((time.time()-start_time)/3600)
        val = ua.Variant(Value=v, VariantType=ua.VariantType.UInt64)
        return value_to_datavalue(val)

    if item[0][2].Name == "OperationalHours":
        duration = datetime.now() - build_date
        v = int(duration.total_seconds()/3600)
        val = ua.Variant(Value=v, VariantType=ua.VariantType.UInt64)
        return value_to_datavalue(val)

    if item[0][1].Identifier == ua.ObjectIds.Null:
        val = ua.Variant(None)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Boolean:
        val = ua.Variant(Value=bool(item[1]), VariantType=ua.VariantType.Boolean)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.SByte:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.SByte)  
        return value_to_datavalue(val)      
    elif item[0][1].Identifier == ua.ObjectIds.Byte:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Byte)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Int16:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Int16)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.UInt16:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.UInt16)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Int32:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Int32)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.UInt32:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.UInt32)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.UInt64:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.UInt64)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Int64:
        val = ua.Variant(Value=int(item[1]), VariantType=ua.VariantType.Int64)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Float:
        val = ua.Variant(Value=float(item[1]), VariantType=ua.VariantType.Float)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Double:
        val = ua.Variant(Value=float(item[1]), VariantType=ua.VariantType.Double)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.String:
        val = ua.Variant(Value=f"{item[1]}", VariantType=ua.VariantType.String)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.DateTime:
        val = ua.Variant(Value=datetime.strptime(f"{item[1]}", '%Y-%m-%d %H:%M:%S.%f'), VariantType=ua.VariantType.DateTime)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Guid:
        val = ua.Variant(Value=f"{item[1]}", VariantType=ua.VariantType.Guid)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.ByteString:
        val = ua.Variant(Value=f"{item[1]}", VariantType=ua.VariantType.ByteString)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.NodeId:
        val = ua.Variant(Value=ua.NodeId.from_string(f"{item[1]}"), VariantType=ua.VariantType.NodeId)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.ExpandedNodeId:
        val = ua.Variant(Value=ua.NodeId.from_string(f"{item[1]}"), VariantType=ua.VariantType.ExpandedNodeId)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.StatusCode:
        val = ua.Variant(Value=ua.StatusCode(int(item[1])), VariantType=ua.VariantType.StatusCode)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.QualifiedName:
        val = ua.Variant(Value=ua.QualifiedName.from_string(f"{item[1]}"), VariantType=ua.VariantType.QualifiedName)
        return value_to_datavalue(val)    
    elif item[0][1].Identifier == ua.ObjectIds.LocalizedText:
        val = ua.Variant(Value=ua.LocalizedText(Text=f"{item[1]}", Locale="en"), VariantType=ua.VariantType.LocalizedText)
        return value_to_datavalue(val)
    elif item[0][1].Identifier == ua.ObjectIds.Range:
        if not "|" in item[1]:
            return None
        splititem = item[1].strip().split("|")
        eurange = ua.uaprotocol_auto.Range()
        eurange.Low = float(splititem[0].strip())
        eurange.High = float(splititem[1].strip())
        val = ua.Variant(Value=eurange, VariantType=ua.VariantType.ExtensionObject)
        return value_to_datavalue(val)
    else:
        # Unknown DataType
        print("Error:", item)
        return None