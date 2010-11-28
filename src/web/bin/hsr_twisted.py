from twisted.web import server
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool
from twisted.internet import reactor
from twisted.application import service, strports
from hsr_server.hsr_main import Application

# Create and start a thread pool,
wsgiThreadPool = ThreadPool()
wsgiThreadPool.start()

# ensuring that it will be stopped when the reactor shuts down
reactor.addSystemEventTrigger('after', 'shutdown', wsgiThreadPool.stop)

config_file = "../conf/hsr.conf"
html_path = "../html/"

application = Application(config_file, html_path)

# Create the WSGI resource
wsgiAppAsResource = WSGIResource(reactor, wsgiThreadPool, application)

# Hooks for twistd
application = service.Application('Twisted.web.wsgi Human Skeletal Remains Database')
server = strports.service('tcp:8080', server.Site(wsgiAppAsResource))
server.setServiceParent(application)
