#!/usr/bin/env python

"""
MongoDB Pool Module
"""
from pymongo import MongoClient
from twisted.web.resource import Resource
from twisted.python import log

from VirtualMachine import VirtualMachine
from Host import Host
from AdAccount import AdAccount
from JsonEncoder import JsonEncoder
from Config import Config
import json

DB_CFG = "dbinfo.conf"


class ConnectPool(object):

    def __init__(self, idle, busy):
        self.idle = idle
        self.busy = busy
        self.conn = []

    def appendConn(self, conn):
        self.conn.append(conn)

    def idle(self):
        self.busy -= 1
        self.idle += 1

    def busy(self):
        self.busy += 1
        self.idle -= 1

    def getConn(self):
        for index in range(0, len(self.conn)):
            conn = self.conn[index]
#            if conn.get('busy') == False:
#                conn['busy'] = True
        return conn.get('conn')

class MongoPool(object, Resource):

    def __init__(self, uri='mongodb://192.168.11.7:27017', max_conn=1):

        # if max_connid null or is not 1-200 exception
        if not max_conn or not isinstance(max_conn, int) or max_conn > 200 or max_conn < 1:
            raise MongoPoolInitException(errorMsg='max_conn not is {}'.format(max_conn))
        Resource.__init__(self)
        self.__max_conn = max_conn
        self.__uri = uri
        self.idle = max_conn
        self.busy = 0
        
        config = Config(DB_CFG).config
        dbname = 'vmmgr'
        dbinfo = {
            "name": config.get(dbname, 'name'),
            "user": config.get(dbname, 'user'),
            "pwd": config.get(dbname, 'pwd')
        }
        self.name = dbinfo['name']
        self.user = dbinfo['user']
        self.pwd  = dbinfo['pwd']

        self.pool = ConnectPool(self.idle,self.busy)
        self.__prepare_conn()

        self.version = config.get('global', 'version')

        self.putChild("", self)
        self.putChild("virtualmachine", VirtualMachine(self.pool))
        self.putChild("host", Host(self.pool))
        self.putChild("adaccount", AdAccount(self.pool))

    def __prepare_conn(self):
        """
        Initialize the connection according to the parameter max_conn
        :return: None
        """

        try:
            for x in range(0, self.__max_conn):
                conn = MongoClient(self.__uri)
                
                db = conn.get_database(self.name)
                db.authenticate(self.user,self.pwd)
                conn_dict = {'conn': db, 'busy': False}

                #print conn_dict
                self.pool.appendConn(conn_dict)
        except Exception as e:
            raise MongoPoolException('Bad uri: {}'.format(self.__uri))

    def render_GET(self, request):
        supported = ["virtualmachine", "host", "adaccount"]
        uris = ['/' + self.version + '/' + item for item in supported]

        return JsonEncoder().encode(uris)

    def render_PUT(self, request):
        pass


class MongoPoolInitException(Exception):
    """
    Initialization exception
    """

    def __init__(self, errorMsg):
        super(MongoPoolInitException, self).__init__(errorMsg)


class MongoPoolOutOfConnections(Exception):
    """
    Not enough connections
    """

    def __init__(self, errorMsg):
        super(MongoPoolOutOfConnections, self).__init__(errorMsg)


class MongoPoolException(Exception):
    """
    MongoPool Other exception
    """

    def __init__(self, errorMsg):
        super(MongoPoolException, self).__init__(errorMsg)

