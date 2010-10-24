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

def getHSRCredentials(method, args, ip):
  if method in credential_types:
    return globals()[credential_types[method]](args, ip)
  return NoneCredentials(args, ip)

class HSRCredentials:
  def getUserId(self, auth_db): abstract()
  def getResponse(self): abstract()
  def getCredentialsType(self): abstract()

class NoneCredentials(HSRCredentials):
  def __init__(self, args, ip):
    pass

  def getCredentialsType(self):
    return "None"

  def getUserId(self, auth_db=None):
    raise HSRCredentialsException("InvalidCredentials")

  def getResponse(self):
    return ""

class UsernamePasswordCredentials(HSRCredentials):
  def __init__(self, args, ip):
    try:
      self.username = args["username"]
      self.password = args["password"]
    except KeyError:
      self.username = None
      self.password = None
    self.ip = ip

  def getCredentialsType(self):
    return "UsernamePassword"

  def getUserId(self, auth_db):
    self.user = auth_db.getUserByName(self.username)
    if self.user == None:
      raise HSRCredentialsException("InvalidCredentials")
    if not self.user.CheckPassword(self.password):
      raise HSRCredentialsException("InvalidCredentials")

    self.session = auth_db.newSession(self.user.user_id)

    return self.user.user_id

  def getResponse(self):
    return "<credentials><session_id>" + self.session.session_id + "</session_id></credentials>"

class SessionIdCredentials(HSRCredentials):
  def __init__(self, args, ip):
    try:
      self.session_id = args["session_id"]
      self.timeout = 60*60
    except KeyError, (ex):
      self.session_id = None

  def getCredentialsType(self):
    return "SessionId"

  def getUserId(self, auth_db):
    self.session = auth_db.getSessionById(self.session_id)
    if self.session == None:
      raise HSRCredentialsException("InvalidCredentials")
    if (self.session.last_used - time.time()) > self.timeout:
      raise HSRCredentialsException("InvalidCredentials")
    self.session.touch()

    return self.session.user_id

  def getResponse(self):
    return ""