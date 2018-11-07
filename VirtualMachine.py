#!/usr/bin/env python

from twisted.web.resource import Resource
from twisted.python import log
import json

import requests


class VirtualMachine(object, Resource):

    def __init__(self, pool):
        Resource.__init__(self)
        #self.conn = conn
        #self.close = close
        self.pool = pool

    def render_GET(self, request):
        data = json.load(request.content)
        
        filters = {}
        for key in data:
            filters[key] = {"$in":data[key]}
        #conn = self.get.getConn()
        db = self.pool.getConn()

        #self.pool.busy()
        output = db.get_collection('virtualmachine').count(filters)
        #self.pool.idle()
        log.msg("###virtualmachine###")
        log.msg("OUTPUT is %s" % (str(output)))
        return str(output)

    def render_PUT(self, request):
        pass
