from twisted.web import server
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool
from twisted.internet import reactor
from twisted.application import service, strports
from hsr_server.hsr_main import Application
import ConfigParser

# Create and start a thread pool,
wsgiThreadPool = ThreadPool()
wsgiThreadPool.start()

# ensuring that it will be stopped when the reactor shuts down
reactor.addSystemEventTrigger('after', 'shutdown', wsgiThreadPool.stop)

config_file = "/etc/hsr/hsr.conf"
html_path = "/var/hsr/html/"

config = ConfigParser.RawConfigParser()
config.readfp(open(config_file))

ssl_desc = "ssl:"
ssl_desc += config.get("ssl", "port") + ":"
ssl_desc += "privateKey=" + config.get("ssl", "private_key") + ":"
ssl_desc += "certKey=" + config.get("ssl", "certificate")

application = Application(config, html_path)

# Create the WSGI resource
wsgiAppAsResource = WSGIResource(reactor, wsgiThreadPool, application)

# Hooks for twistd
application = service.Application('Twisted.web.wsgi Human Skeletal Remains Database')
server = strports.service(ssl_desc, server.Site(wsgiAppAsResource))
server.setServiceParent(application)
