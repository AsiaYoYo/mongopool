from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.application import internet
from twisted.application.service import IServiceMaker
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.python import log,usage

from MongoPool import MongoPool


class Options(usage.Options):
    optParameters = [
        ['port', 'p', 33400, 'the port number to listen on', int],
        ]


class MongoPoolMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname     = "mongopool"
    description = "XT mongopool"
    options     = Options

    def makeService(self, options):
        port    = options['port']
        root    = Resource()
        mongoPool = MongoPool()
        log.discardLogs()
        #reactor.addSystemEventTrigger('before', 'shutdown', mongoPool.shutdown)

        root.putChild(mongoPool.version, mongoPool)
        factory = Site(root)
        httpService = internet.TCPServer(port, factory)
        return httpService

service_maker = MongoPoolMaker()
