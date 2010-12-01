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

from hsr_auth.auth_db import Permissions

def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass') 

request_types = {
    "Ping" : "PingRequest",
    "ListMuseumObjects" : "AllObjectsRequest",
    "GetMuseumObject" : "GetMuseumObjectRequest",
    "ListIndividuals" : "AllIndividualsRequest",
    "ChangePassword" : "ChangePasswordRequest",
    "GetBiologicalIndividual" : "GetBioIndividualRequest"
    }

class HSRRequestException(Exception): pass

def getHSRRequest(method, args, credentials, hsr_db):
  if method in request_types:
    return globals()[request_types[method]](args, credentials, hsr_db)
  raise HSRRequestException("Unknown request type " + method)

class HSRRequest(object):
  def execute(self): abstract()
  def getRequestType(self): abstract()

class PingRequest(HSRRequest):
  def __init__(self, args, credentials, hsr_db):
    self.credentials = credentials
    self.hsr_db = hsr_db
    self.permissions = Permissions.NONE

  def getRequestType(self):
    return "Ping"

  def execute(self):
    self.credentials.getUserId()
    self.credentials.checkPermissions(self.permissions)
    cred_response = self.credentials.getResponse()
    requ_response = "<response>Ping</response>"
    return (requ_response, cred_response)

class AllObjectsRequest(HSRRequest):
  def __init__(self, args, credentials, hsr_db):
    self.credentials = credentials
    self.hsr_db = hsr_db
    self.permissions = Permissions.READ
    try:
      self.limit = int(args["limit"])
    except KeyError:
      self.limit = None

    try:
      self.offset = int(args["offset"])
    except KeyError:
      self.offset = 0

  def getRequestType(self):
    return "ListMuseumObjects"

  def execute(self):
    self.credentials.getUserId()
    self.credentials.checkPermissions(self.permissions)
    mos = self.hsr_db.getAllMuseumObjects(limit=self.limit, offset=self.offset)
    mos_xml = "<response>"
    for mo in mos:
      mos_xml += mo.toXml()
    mos_xml += "</response>"

    return (mos_xml, self.credentials.getResponse())

class GetMuseumObjectRequest(HSRRequest):
  def __init__(self, args, credentials, hsr_db):
    self.credentials = credentials
    self.permissions = Permissions.READ
    self.hsr_db = hsr_db
    try:
      self.object_id = args["object_id"]
    except KeyError:
      self.object_id = None

    try:
      self.catalogue_num = args["catalogue_num"]
    except KeyError:
      self.catalogue_num = None

  def getRequestType(self):
    return "GetMuseumObject"

  def execute(self):
    self.credentials.getUserId()
    self.credentials.checkPermissions(self.permissions)
    cred_response = self.credentials.getResponse()
    if self.object_id != None:
      mo = self.hsr_db.getMuseumObjectById(self.object_id)
    else:
      mo = self.hsr_db.getMuseumObjectByCatalogueNum(self.catalogue_num)
    try:
      mo_xml = "<response>" + mo.toXml() + "</response>"
    except AttributeError:
      mo_xml = "<response></response>"
    return (mo_xml, cred_response)

class AllIndividualsRequest(HSRRequest):
  def __init__(self, args, credentials, hsr_db):
    self.db = hsr_db
    self.credentials = credentials
    self.permissions = Permissions.READ
    try:
      self.limit = int(args["limit"])
    except KeyError:
      self.limit = None

    try:
      self.offset = int(args["offset"])
    except KeyError:
      self.offset = 0

  def getRequestType(self):
    return "ListIndividuals"

  def execute(self):
    self.credentials.getUserId()
    self.credentials.checkPermissions(self.permissions)
    bis = self.db.getAllIndividuals(limit=self.limit,
        offset=self.offset)
    bis_xml = "<response>"
    for bi in bis:
      bis_xml += bi.toXml()
    bis_xml += "</response>"
    return (bis_xml, self.credentials.getResponse())

class GetBioIndividualRequest(HSRRequest):
  def __init__(self, args, credentials, hsr_db):
    self.permissions = Permissions.READ
    self.credentials = credentials
    self.hsr_db = hsr_db
    try:
      self.indiv_id = args["individual_id"]
    except KeyError:
      self.indiv_id = None

    try:
      self.suffix_design = args["suffix_design"]
    except KeyError:
      self.suffix_design = None

  def getRequestType(self):
    return "GetBiologicalIndividual"

  def execute(self):
    self.credentials.getUserId()
    self.credentials.checkPermissions(self.permissions)
    if self.indiv_id != None:
      bi = self.hsr_db.getIndividualById(self.indiv_id)
    else:
      bi = self.hsr_db.getIndividualBySuffixDesign(self.suffix_design)
    try:
      response = "<response>" + bi.toXml() + "</response>"
    except AttributeError:
      response = "<response></response>"
    return (response, self.credentials.getResponse())

class ChangePasswordRequest(HSRRequest):
  def __init__(self, args, credentials, hsr_db):
    self.credentials = credentials
    self.new_password = args["new_password"]
    self.permissions = Permissions.NONE

  def getRequestType(self):
    return "ChangePassword"

  def execute(self):
    uid = self.credentials.getUserId()
    self.credentials.checkPermissions(self.permissions)
    user = self.credentials.auth_db.getUserById(uid)

    user.UpdatePassword(self.new_password)
    self.credentials.auth_db.writeUser(user)

    return ("", self.credentials.getResponse())





