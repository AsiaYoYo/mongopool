#!/usr/bin/env python

from twisted.web.resource import Resource
from twisted.python import log
import json

import requests


class AdAccount(object, Resource):

    def __init__(self, pool):
        Resource.__init__(self)
        self.pool = pool

    def render_GET(self, request):
        data = json.load(request.content)
        
        #filters = {}
        #for key in data:
        #    filters[key] = {"$in":data[key]}
        db = self.pool.getConn()

        output = db.get_collection('adaccount').count(data)
        log.msg("###adaccount###")
        log.msg("OUTPUT is %s" % (str(output)))
        return str(output)

    def render_PUT(self, request):
        pass
