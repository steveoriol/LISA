# -*- coding: UTF-8 -*-
import os
import json
from twisted.internet import reactor, ssl
from twisted.application import internet, service
from twisted.web import server, wsgi, static
from twisted.python import threadpool, log
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.resource import WebSocketResource
from OpenSSL import SSL
import lisa
import pkg_resources
from lisa.server.plugins import PluginManager

if not os.path.exists('/etc/lisa/server/lisa.json'):
    configuration = json.load(open(pkg_resources.resource_filename(__name__, 'configuration/lisa.json.sample')))
else:
    configuration = json.load(open('/etc/lisa/server/lisa.json'))
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
pluginmanager = PluginManager()

class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()


# Twisted Application Framework setup:
application = service.Application('LISA')

def makeService(config):
    from django.core.handlers.wsgi import WSGIHandler
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lisa.server.web.weblisa.settings'

    global configuration

    if config['configuration']:
        configuration = json.load(open(config['configuration']))

    # Check if plugin directory exists. If not, create it
    try:
        if not os.path.exists(os.path.dirname(lisa.__file__)):
            os.makedirs(os.path.normpath(os.path.dirname(lisa.__file__) + '/plugins'))
        if not os.path.exists(os.path.dirname(lisa.__file__) + '/plugins/__init__.py'):
            file = open(os.path.normpath(os.path.dirname(lisa.__file__) + '/plugins/__init__.py'), 'w')
            file.write("__import__('pkg_resources').declare_namespace(__name__)")
            file.close()
    except:
        log.err("Directory %s doesn't exist, and it seems impossible to create it" % os.path.normpath(
            os.path.dirname(lisa.__file__) + '/plugins'))
        pass

    from lisa.server import libs

    # Creating MultiService
    multi = service.MultiService()
    pool = threadpool.ThreadPool()
    tps = ThreadPoolService(pool)
    tps.setServiceParent(multi)

    # Creating the web stuff
    resource_wsgi = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
    root = libs.Root(resource_wsgi)
    staticrsrc = static.File('/'.join([dir_path,'web/interface/static']))
    root.putChild("static", staticrsrc)

    # Create the websocket
    if configuration['enable_secure_mode']:
        socketfactory = WebSocketServerFactory("wss://" + configuration['lisa_url'] + ":" +
                                               str(configuration['lisa_web_port_ssl']),debug=False)
    else:
        socketfactory = WebSocketServerFactory("ws://" + configuration['lisa_url'] + ":" +
                                               str(configuration['lisa_web_port']),debug=False)
    socketfactory.protocol = libs.WebSocketProtocol
    socketfactory.protocol.configuration, socketfactory.protocol.dir_path = configuration, dir_path
    socketresource = WebSocketResource(socketfactory)
    root.putChild("websocket", socketresource)

    # Configuring servers to launch
    if configuration['enable_secure_mode'] or configuration['enable_unsecure_mode']:
        if configuration['enable_secure_mode']:
            SSLContextFactoryEngine = ssl.DefaultOpenSSLContextFactory(
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.key'),
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.crt')
            )
            SSLContextFactoryWeb = ssl.DefaultOpenSSLContextFactory(
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.key'),
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.crt')
            )
            ctx = SSLContextFactoryEngine.getContext()
            ctx.set_verify(
                SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
                libs.verifyCallback
            )
            # Since we have self-signed certs we have to explicitly
            # tell the server to trust them.
            with open(os.path.normpath(dir_path + '/' + 'configuration/ssl/server.pem'), 'w') as outfile:
                for file in os.listdir(os.path.normpath(dir_path + '/' + 'configuration/ssl/public/')):
                    with open(os.path.normpath(dir_path + '/' + 'configuration/ssl/public/'+file)) as infile:
                        for line in infile:
                            outfile.write(line)


            ctx.load_verify_locations(os.path.normpath(dir_path + '/' + 'configuration/ssl/server.pem'))
            internet.SSLServer(configuration['lisa_web_port_ssl'],
                               server.Site(root), SSLContextFactoryWeb).setServiceParent(multi)
            internet.SSLServer(configuration['lisa_engine_port_ssl'],
                               libs.LisaInstance, SSLContextFactoryEngine).setServiceParent(multi)
        if configuration['enable_unsecure_mode']:
            # Serve it up:
            internet.TCPServer(configuration['lisa_web_port'], server.Site(root)).setServiceParent(multi)
            internet.TCPServer(configuration['lisa_engine_port'], libs.LisaInstance).setServiceParent(multi)

    else:
        exit(1)
    libs.scheduler.setServiceParent(multi)
    multi.setServiceParent(application)
    libs.Initialize()
    return multi