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
from sqlalchemy import *

def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass')

class Permissions(object):
  NONE = 128
  READ = 64
  WRITE = 32
  ADMIN = 0

class User(object):
  def __init__(self, user_id = None, username = None, password_hash = None, salt = None, permissions = Permissions.READ):
    self.user_id = user_id
    self.username = str(username)
    self.salt = str(salt)
    self.permissions = permissions
    if salt == None and password_hash != None:
      self.UpdatePassword(password_hash)
    else:
      self.password_hash = str(password_hash)

  def PrivateHashPassword(self, salt, password):
    sha1func = sha1()
    sha1func.update(salt)
    sha1func.update(password)

    return sha1func.hexdigest()

  def UpdatePassword(self, new_password):
    sha1func = sha1()
    sha1func.update(urandom(128))
    self.salt = sha1func.hexdigest()
    self.password_hash = self.PrivateHashPassword(self.salt,
        new_password)

  def CheckPassword(self, password):
    sha1func = sha1()
    password_hash = self.PrivateHashPassword(self.salt, password)
    if password_hash == self.password_hash:
      return True
    else:
      return False

  def CheckPermissions(self, needed_permissions):
    return (self.permissions <= needed_permissions)

  def __eq__(self, right):
    try:
      return (self.username == right.username
        and self.user_id == right.user_id)
    except Exception:
      return False

class Session(object):
  def __init__(self, user_id = None, session_id = None, created =
      None, last_used = None):
    self.session_id = str(session_id)
    if user_id != None:
      self.user_id = int(user_id)
    else:
      self.user_id = None
    self.created = created
    self.last_used = last_used
    if(session_id == None):
      sha1func = sha1()
      sha1func.update(urandom(128))
      self.session_id = sha1func.hexdigest()

    if(created == None and last_used == None):
      self.created = time.time()
      self.last_used = time.time()

  def touch(self):
    self.last_used = time.time()

  def __eq__(self, right):
    try:
      return (self.user_id == right.user_id
        and self.session_id == right.session_id)
    except Exception:
      return False

class HSRAuthDBExcept(Exception): pass

class HSRAuthDB:
  def getUserByName(self, username): abstract()

  def getUserById(self, uid): abstract()

  def writeUser(self, user): abstract()

  def createUser(self, username, password, permissions=Permissions.READ): abstract()

  def deleteUser(self, used): abstract()

  def deleteSession(self, session): abstract()

  def writeSession(self, session): abstract()

  def getSessionById(self, session_id): abstract()

  def getSessionsByUser(self, user): abstract()

  def newSession(self, user_id):
    need_new_session = True
    while need_new_session:
      need_new_session = False
      session = Session(user_id)
      try:
        self.writeSession(session)
      except HSRAuthDB:
        need_new_session = True

    return session

class HSRAuthDBSqlAlchemyImpl(HSRAuthDB):
  def __init__(self, db):
    self.db_engine = db

  def getConn(self):
    return self.db_engine.connect()

  def createUser(self, username, password, permissions=Permissions.READ):
    conn = self.getConn()
    metadata = MetaData(conn)
    users = Table('Users', metadata, autoload=True)

    user = User(0, username, password, permissions=permissions)
    stmt = users.insert().values(Username=user.username,
        Salt=user.salt, PasswordHash=user.password_hash,
        Permissions=user.permissions)
    try:
      result = conn.execute(stmt)
    except Exception:
      conn.close()
      raise HSRAuthDBExcept("Could not create User!")

    user.user_id = result.lastrowid
    conn.close()
    return user

  def writeUser(self, user):
    conn = self.getConn()
    metadata = MetaData(conn)
    users = Table('Users', metadata, autoload=True)

    stmt = users.update().values(
        Username=user.username,
        Salt=user.salt,
        PasswordHash=user.password_hash,
        Permissions=user.permissions
        ).where(users.c.UserID==user.user_id)
    try:
      result = conn.execute(stmt)
    except Exception:
      conn.close()
      raise HSRAuthDBExcept("Could not write User!")

    conn.close()

    if result.rowcount < 1:
      raise HSRAuthDBExcept("Could not write User!")

  def getUserByName(self, username):
    conn = self.getConn()
    metadata = MetaData(conn)
    users = Table('Users', metadata, autoload=True)

    stmt = users.select().where(users.c.Username==username)
    result = conn.execute(stmt)
    row = result.fetchone()
    conn.close()

    if not row:
      return None

    return User(row.UserID, row.Username, row.PasswordHash, row.Salt,
        row.Permissions)

  def getUserById(self, uid):
    conn = self.getConn()
    metadata = MetaData(conn)
    users = Table('Users', metadata, autoload=True)

    stmt = users.select().where(users.c.UserID==uid)
    result = conn.execute(stmt)
    row = result.fetchone()
    conn.close()

    if not row:
      return None

    return User(row.UserID, row.Username, row.PasswordHash, row.Salt)

  def deleteUser(self, user):
    conn = self.getConn()
    metadata = MetaData(conn)
    users = Table('Users', metadata, autoload=True)

    stmt = users.delete().where(users.c.UserID==user.user_id)
    result = conn.execute(stmt)
    conn.close()

  def getSessionById(self, session_id):
    conn = self.getConn()
    metadata = MetaData(conn)
    sessions = Table('Sessions', metadata, autoload=True)

    stmt = sessions.select().where(sessions.c.SessionID==session_id)
    result = conn.execute(stmt)
    row = result.fetchone()
    conn.close()

    if not row:
      return None

    return Session(row.UserID, row.SessionID, row.CreationTime,
        row.LastTouched)

  def writeSession(self, session):
    conn = self.getConn()
    metadata = MetaData(conn)
    sessions = Table('Sessions', metadata, autoload=True)

    stmt = sessions.insert().values(
        UserID=session.user_id,
        SessionID=session.session_id,
        CreationTime=session.created,
        LastTouched=session.last_used)
    try:
      result = conn.execute(stmt)
    except Exception:
      raise HSRAuthDBExcept("Could not write Session!")
    conn.close()

  def deleteSession(self, session):
    conn = self.getConn()
    metadata = MetaData(conn)
    sessions = Table('Sessions', metadata, autoload=True)

    stmt = sessions.delete().where(sessions.c.SessionID==session.session_id)
    result = conn.execute(stmt)
    conn.close()

  def getSessionsByUser(self, user):
    conn = self.getConn()
    metadata = MetaData(conn)
    sessions = Table('Sessions', metadata, autoload=True)

    stmt = sessions.select().where(sessions.c.UserID==user.user_id)
    results = conn.execute(stmt)
    conn.close()

    matching_sessions = []
    for row in results:
      matching_sessions.append(Session(row.UserID, row.SessionID, row.CreationTime,
         row.LastTouched))

    return matching_sessions

  def newSession(self, user_id):
    need_new_session = True
    while need_new_session:
      need_new_session = False
      session = Session(user_id)
      try:
        self.writeSession(session)
      except HSRAuthDBExcept:
        need_new_session = True

    return session













