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

from hsr_auth.auth_db import *

class HSRAuthDBTestImpl(HSRAuthDB):
  def __init__(self):
    self.users = []
    self.sessions = []
    self.user_id = 0

  def getUserByName(self, username):
    for i in range(len(self.users)):
      if(username == self.users[i].username):
        return self.users[i]
      return None

  def getUserById(self, uid):
    for i in range(len(self.users)):
      if(uid == self.users[i].user_id):
        return self.users[i]
      return None

  def writeUser(self, user):
    for i in range(len(self.users)):
      if(user.user_id == self.users[i].user_id):
        self.users[i] = user
        return
      elif(user.username == self.users[i].username):
        raise HSRAuthDBExcept("Could not write User!")

    raise HSRAuthDBExcept("Could not write User!")

  def createUser(self, username, password, permissions=Permissions.READ):
    for user in self.users:
      if user.username == username:
        raise HSRAuthDBExcept("Could not create User!")
    user = User(self.user_id, username, password, permissions=permissions)
    self.user_id += 1
    self.users.append(user)
    return user

  def deleteUser(self, user):
    for i in range(len(self.users)):
      if(user.user_id == self.users[i].user_id):
        del self.users[i]
        return True
    return False

  def deleteSession(self, session):
    for i in range(len(self.sessions)):
      if(session.user_id == self.sessions[i].user_id
          and session.session_id == self.sessions[i].session_id):
        del self.sessions[i]
        return True
    return False

  def writeSession(self, session):
    for i in range(len(self.sessions)):
      if(session.session_id == self.sessions[i].session_id):
        raise HSRAuthDBExcept("Could not write Session!")
    self.sessions.append(session)

  def newSession(self, user_id):
    session = Session(user_id)
    gen_new_session = True
    while gen_new_session:
      gen_new_session = False
      session = Session(user_id)
      try:
        self.writeSession(session)
      except HSRAuthDBExcept:
        gen_new_session = True

    return session

  def getSessionById(self, session_id):
    session_id = str(session_id)
    for i in range(len(self.sessions)):
      if(session_id == self.sessions[i].session_id):
        return self.sessions[i]
    return None

  def getSessionsByUser(self, user):
    sessions = []
    for i in range(len(self.sessions)):
      if(user.user_id == self.sessions[i].user_id):
        sessions.append(self.sessions[i])
    return sessions
