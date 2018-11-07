#!/usr/bin/env python


import json
from bson import ObjectId

class JsonEncoder(json.JSONEncoder):
    def __init__(self):
        super(JsonEncoder, self).__init__(indent=2)

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


if __name__ == "__main__":
    obj = {"a":"1", "b":2, "c":ObjectId(), "d": 1.2}
    print JsonEncoder().encode(obj)

