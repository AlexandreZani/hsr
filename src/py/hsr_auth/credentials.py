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

def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass') 

def getHSRCredentials(method, args, ip):
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
    raise Exception("InvalidCredentials")

  def getResponse(self):
    return ""


