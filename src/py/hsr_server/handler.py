#!/usr/bin/python

#   Copyright Alexandre Zani (alexandre.zani@gmail.com) 
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from xml.dom.minidom import parseString
from hsr_auth.credentials import *
from hsr_server.requests import *

class HSRException(Exception): pass

class HsrHandler(object):
  def __init__(self, hsr_db, hsr_auth_db):
    self.hsr_db = hsr_db
    self.hsr_auth_db = hsr_auth_db

  def execute(self, xml, ip=None, credentials=None):
    ret = "<HSR>"

    try:
     request = self.parseRequest(xml, ip, credentials)
     response = request.execute()
     ret += response[0]
     ret += response[1]
    except HSRException, (instance):
      ret += "<error>" + str(instance) + "</error>"

    ret += "</HSR>"

    return ret

  def parseRequest(self, xml, ip=None, credentials=None):
    try:
      xml_doc = parseString(xml)
    except Exception:
      raise HSRException("MalformedRequest")

    hsr = xml_doc.firstChild

    if hsr.nodeName != "HSR":
      raise HSRException("MalformedRequest")

    cred_type = ""
    cred_args = ""
    request_type = ""
    request_args = ""

    for node in hsr.childNodes:
      if node.nodeName == "credentials":
        (cred_type, cred_args) = self.parseMethod(node)
      elif node.nodeName == "request":
        (request_type, request_args) = self.parseMethod(node)

    if credentials == None:
      credentials = getHSRCredentials(cred_type, cred_args, ip, self.hsr_auth_db)
    request = getHSRRequest(request_type, request_args, credentials, self.hsr_db)

    return request

  def parseMethod(self, node):
    try:
      method = node.getElementsByTagName("type")[0].firstChild.nodeValue
    except Exception:
      raise HSRException("MalformedRequest")

    args = {}

    try:
      for arg in node.getElementsByTagName("args")[0].childNodes:
        arg_name = arg.nodeName
        arg_value = arg.firstChild.nodeValue
        args[arg_name] = arg_value
    except Exception:
      pass

    return (method, args)

