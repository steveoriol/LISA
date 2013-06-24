# -*- coding: UTF-8 -*-
import os,libs,json,sys,uuid
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.application import internet, service
from twisted.web import server, wsgi, static, resource
from twisted.python import threadpool, log
from django.core.handlers.wsgi import WSGIHandler
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.resource import WebSocketResource
from pymongo import MongoClient
from libs.txscheduler.manager import ScheduledTaskManager
from libs.txscheduler.service import ScheduledTaskService

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
configuration = json.load(open(os.path.normpath(dir_path + '/' + 'Configuration/lisa.json')))
if not os.path.exists(os.path.normpath(dir_path + '/' + 'Plugins')):
    os.mkdir(os.path.normpath(dir_path + '/' + 'Plugins'))

class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()

class Lisa(Protocol):
    def __init__(self,factory, bot_library):
        self.factory = factory
        self.bot_library = bot_library

    def connectionMade(self):
        self.client_uuid = str(uuid.uuid1())
        self.factory.clients.append({"object": self, "zone": "", "type": "", "uuid": self.client_uuid})

    def connectionLost(self, reason):
        log.msg('Lost connection.  Reason:', reason)
        for client in self.factory.clients:
            if client['object'] == self:
                self.factory.clients.remove(client)

    def dataReceived(self, data):
        jsonData = json.loads(data)
        for client in self.factory.clients:
            if client['object'] == self and (not client['type'] or not client['zone']):
                client['type'],client['zone'] = jsonData['type'],jsonData['zone']
        libs.RulesEngine(configuration).Rules(jsonData=jsonData, lisaprotocol=self)


class LisaFactory(Factory):
    def __init__(self):
        try:
            self.bot_library = libs.RiveScriptBot()
            log.msg("Successfully loaded bot")
        except:
            log.msg("Couldn't load bot")
        self.clients = []
        self.syspath = sys.path
        mongo = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = mongo.lisa

        # Install the default Chatterbot plugin
        self.build_grammar()

    def build_grammar(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        self.bot_library.learn(os.path.normpath(dir_path + '/' + 'Configuration/'))
        # Load enabled plugins for the main language
        for plugin in self.database.plugins.find( { "enabled": True, "lang": configuration['lang'] } ):
            sys.path.append(str(os.path.normpath(dir_path + '/Plugins/' + plugin['name'] + '/lang/' \
                                             + configuration['lang'] + '/modules/')))
            self.bot_library.learn(os.path.normpath(dir_path + '/' + 'Plugins/' + plugin['name'] + '/lang/' \
                                                    + configuration['lang'] + '/text'))

    def buildProtocol(self, addr):
        self.Lisa = Lisa(self,self.bot_library)
        return self.Lisa

class Root(resource.Resource):
    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

class WebSocketProtocol(WebSocketServerProtocol):
    def connectionMade(self):
        WebSocketServerProtocol.connectionMade(self)
        self.lisaclientfactory = libs.LisaClientFactory(self)
        reactor.connectTCP(configuration['lisa_url'], configuration['lisa_engine_port'], self.lisaclientfactory)

    def onMessage(self, msg, binary):
        self.lisaclientfactory.protocol.sendMessage(json.dumps( \
            {"from": "Lisa-Web","type": "Chat", "body": unicode(msg.decode('utf-8')), "zone": "WebSocket"}))

class LisaReload(resource.Resource):
    def __init__(self, LisaFactory):
        self.LisaFactory = LisaFactory
        sys.path = self.LisaFactory.syspath
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        self.LisaFactory.build_grammar()
        return "OK"

    def render_GET(self, request):
        self.LisaFactory.build_grammar()
        return "OK"

class Scheduler_reload(resource.Resource):
    def __init__(self, taskman):
        self.taskman = taskman
        resource.Resource.__init__(self)
    def getChild(self, path, request):
        return self.taskman.reload()

    def render_GET(self, request):
        return self.taskman.reload()

def verifyCallback(connection, x509, errnum, errdepth, ok):
    if not ok:
        print 'invalid cert from subject:', x509.get_subject()
        return False
    else:
        print "Certs are fine"
    return True

# Twisted Application Framework setup:
application = service.Application('LISA')

# Instance of LisaFactory to pass it to other services.
LisaInstance = LisaFactory()

# Create a task manager to pass it to other services
taskman = ScheduledTaskManager(configuration)
scheduler = ScheduledTaskService(taskman)

# Environment setup for Django project files:
sys.path.append(os.path.normpath(os.path.join(os.path.abspath("."), "web")))
sys.path.append(os.path.normpath(os.path.join(os.path.abspath("."), "web/lisa")))
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.lisa.settings'

# Creating MultiService
multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)
resource_wsgi = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
root = Root(resource_wsgi)

staticrsrc = static.File(os.path.normpath(os.path.join(os.path.abspath("."), "web/lisa/static")))
root.putChild("static", staticrsrc)
root.putChild("lisareload", LisaReload(LisaInstance))
root.putChild("schedulerreload", Scheduler_reload(taskman))

socketfactory = WebSocketServerFactory("ws://" + configuration['lisa_url'] + ":" +\
                                       str(configuration['lisa_web_port']),debug=False)
socketfactory.protocol = WebSocketProtocol
socketresource = WebSocketResource(socketfactory)
root.putChild("websocket", socketresource)

if configuration['enable_secure_mode']:
    from OpenSSL import SSL
    from twisted.internet import ssl

    SSLContextFactory = ssl.DefaultOpenSSLContextFactory(
        os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.key'),
        os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.crt')
    )
    ctx = SSLContextFactory.getContext()
    ctx.set_verify(
        SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
        verifyCallback
    )
    # Since we have self-signed certs we have to explicitly
    # tell the server to trust them.
    with open(os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.pem'), 'w') as outfile:
        for file in os.listdir(os.path.normpath(dir_path + '/' + 'Configuration/ssl/public/')):
            with open(os.path.normpath(dir_path + '/' + 'Configuration/ssl/public/'+file)) as infile:
                for line in infile:
                    outfile.write(line)


    ctx.load_verify_locations(os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.pem'))

    internet.SSLServer(configuration['lisa_web_port_ssl'], server.Site(root), SSLContextFactory).setServiceParent(multi)
    internet.SSLServer(configuration['lisa_engine_port_ssl'], LisaInstance, SSLContextFactory).setServiceParent(multi)

elif configuration['enable_unsecure_mode']:
    # Serve it up:
    internet.TCPServer(configuration['lisa_web_port'], server.Site(root)).setServiceParent(multi)
    internet.TCPServer(configuration['lisa_engine_port'], LisaInstance).setServiceParent(multi)
else:
    exit(1)
scheduler.setServiceParent(multi)
multi.setServiceParent(application)