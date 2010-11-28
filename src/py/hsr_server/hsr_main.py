#!/usr/bin/python

from hsr_server.hsr_db import HSRDBSqlAlchemyImpl
from hsr_auth.auth_db import HSRAuthDBSqlAlchemyImpl
from hsr_server.handler import HsrHandler
from hsr_auth.credentials import getHSRCredentials
from sqlalchemy import *
from cgi import parse_qs, escape
from xml.dom.minidom import parseString
import ConfigParser
import os
from urllib2 import unquote
import string
from jinja2 import Environment, FileSystemLoader

class Application(object):
  def __init__(self, config_file=None, html_path=None):
    if config_file == None:
      self.config_file = "/etc/hsr/hsr.conf"
    else:
      self.config_file = config_file

    if html_path == None:
      self.html_path = "../html/"
    else:
      self.html_path = html_path

    config = ConfigParser.RawConfigParser()
    config.readfp(open(self.config_file))
  
    hsr_db_url = config.get("hsr_db", "type") + "://"
    hsr_db_url += config.get("hsr_db", "username")
    hsr_db_url += ":" + config.get("hsr_db", "password")
    hsr_db_url += "@" + config.get("hsr_db", "location")
    hsr_db_url += "/" + config.get("hsr_db", "database")

    hsr_db_engine = create_engine(hsr_db_url)
    self.hsr_db = HSRDBSqlAlchemyImpl(hsr_db_engine)

    auth_db_url = config.get("auth_db", "type") + "://"
    auth_db_url += config.get("auth_db", "username")
    auth_db_url += ":" + config.get("auth_db", "password")
    auth_db_url += "@" + config.get("auth_db", "location")
    auth_db_url += "/" + config.get("auth_db", "database")

    auth_db_engine = create_engine(auth_db_url)
    self.auth_db = HSRAuthDBSqlAlchemyImpl(auth_db_engine)

    self.handler = HsrHandler(self.hsr_db, self.auth_db)

    self.template_env = Environment(loader=FileSystemLoader(self.html_path + "../jinja/"))

    try:
      self.auth_db.createUser('admin', 'admin')
    except Exception:
      pass

  def __call__(self, environ, start_response):
    if environ['PATH_INFO'] == "/" or environ['PATH_INFO'] == "":
      environ['PATH_INFO'] = "/static"

    if environ['PATH_INFO'] == "/api":
      return self.api(environ, start_response)
    elif environ['PATH_INFO'][0:7] == "/static":
      return self.static(environ, start_response)
    elif environ['PATH_INFO'][0:6] == "/jinja":
      return self.jinja(environ, start_response)
    else:
      return self.error(environ, start_response)

  def error(self, environ, start_response):
      start_response('404 Not Found', [('Content-type','text/html')])
      return ['Not found']

  def jinja(self, environ, start_response):
    filename = environ['PATH_INFO'][6:]

    try:
      if environ['HTTP_COOKIE'][:12] != "credentials=":
        raise Exception()
      value = unquote(environ['HTTP_COOKIE'][12:])
      eov = string.find(value, ";")
      if eov > 0:
        value = value[:eov]

      (cred_type, cred_args) = self.handler.parseMethod(parseString(value))
      creds = getHSRCredentials(cred_type, cred_args, None, self.auth_db)
      creds.getUserId()
    except Exception, (instance):
      return self.static(environ, start_response, "login.html")

    if not os.path.exists(self.html_path + "../jinja/" + filename):
      return self.error(environ, start_response)

    template = self.template_env.get_template(filename)
    d = parse_qs(environ['QUERY_STRING'])
    for k in d:
      d[k] = d[k][0]

    start_response('200 OK', [('Content-type','text/html')])
    return [str(template.render(d))]

  def static(self, environ, start_response, filename=None):
    if filename == None:
      filename = environ['PATH_INFO'][8:]

    if filename == "":
      filename = "main.html"

    if filename != "main.html" and filename != "login.html" and filename[-5:] == ".html":
      try:
        if environ['HTTP_COOKIE'][:12] != "credentials=":
          raise Exception()
        value = unquote(environ['HTTP_COOKIE'][12:])
        eov = string.find(value, ";")
        if eov > 0:
          value = value[:eov]

        (cred_type, cred_args) = self.handler.parseMethod(parseString(value))
        creds = getHSRCredentials(cred_type, cred_args, None, self.auth_db)
        creds.getUserId()
      except Exception, (instance):
        filename = "login.html"

    try:
      f = open(self.html_path + filename, "r")
    except IOError:
      return self.error(environ, start_response)

    start_response('200 OK', [('Content-type','text/html')])
    return f

  def api(self, environ, start_response):
    try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
      request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)

    start_response('200 OK', [('Content-type','text/xml')])
    response = self.handler.execute(request_body)
    xml_header = "<?xml version='1.0' encoding='UTF-8'?>"

    return [xml_header, response]
