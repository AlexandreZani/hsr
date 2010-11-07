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

from hashlib import sha1
from os import urandom
import time

def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass') 

credential_types = {
    "None" : "NoneCredentials",
    "UsernamePassword" : "UsernamePasswordCredentials",
    "SessionId" : "SessionIdCredentials"
    }

class HSRCredentialsException(Exception): pass

def getHSRCredentials(method, args, ip, auth_db=None):
  if method in credential_types:
    return globals()[credential_types[method]](args, ip, auth_db)
  return NoneCredentials(args, ip)

class HSRCredentials(object):
  def getUserId(self): abstract()
  def getResponse(self): abstract()
  def getCredentialsType(self): abstract()

class NoneCredentials(HSRCredentials):
  def __init__(self, args, ip, db):
    pass

  def getCredentialsType(self):
    return "None"

  def getUserId(self):
    raise HSRCredentialsException("InvalidCredentials")

  def getResponse(self):
    return ""

class UsernamePasswordCredentials(HSRCredentials):
  def __init__(self, args, ip, auth_db):
    try:
      self.username = args["username"]
      self.password = args["password"]
    except KeyError:
      self.username = None
      self.password = None
    self.ip = ip
    self.auth_db = auth_db

  def getCredentialsType(self):
    return "UsernamePassword"

  def getUserId(self):
    self.user = self.auth_db.getUserByName(self.username)
    if self.user == None:
      raise HSRCredentialsException("InvalidCredentials")
    if not self.user.CheckPassword(self.password):
      raise HSRCredentialsException("InvalidCredentials")

    self.session = self.auth_db.newSession(self.user.user_id)

    return self.user.user_id

  def getResponse(self):
    return "<credentials><type>SessionId</type><args><session_id>"
    + self.session.session_id + "</session_id></args></credentials>"

class SessionIdCredentials(HSRCredentials):
  def __init__(self, args, ip, auth_db):
    try:
      self.session_id = args["session_id"]
      self.timeout = 60*60
    except KeyError, (ex):
      self.session_id = None
    self.ip = ip
    self.auth_db=auth_db

  def getCredentialsType(self):
    return "SessionId"

  def getUserId(self):
    self.session = self.auth_db.getSessionById(self.session_id)
    if self.session == None:
      raise HSRCredentialsException("InvalidCredentials")
    if (self.session.last_used - time.time()) > self.timeout:
      raise HSRCredentialsException("InvalidCredentials")
    self.session.touch()

    return self.session.user_id

  def getResponse(self):
    return ""
