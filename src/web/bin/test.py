#!/usr/bin/python

from wsgiref import simple_server
from hsr_server.hsr_main import Application
import sys, os

if __name__ == "__main__":
  root_path = os.path.dirname(sys.argv[0])
  html_path = "../html/"

  if root_path != "":
    config_file = root_path + "/../conf/hsr.conf"
    html_path = root_path + "/../html/"
  else:
    config_file = "../conf/hsr.conf"

  app = Application(config_file, html_path)
  httpd = simple_server.WSGIServer(('localhost', 8000), simple_server.WSGIRequestHandler,)
  httpd.set_app(app)
  httpd.serve_forever()
