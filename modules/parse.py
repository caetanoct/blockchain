import json
from hexbytes import HexBytes
'''
    result = {}
    for key, val in tx.items():
        if isinstance(val, HexBytes):
            result[key] = val.hex()
        else:
            result[key] = val    
    return json.dumps(result)
'''
def attributedict_to_json(tx):    
    txdict = dict(tx)
    return json.dumps(txdict, cls=HexJsonEncoder)
class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)
