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
import MySQLdb
from MySQLdb import IntegrityError

def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass')

class User:
  def __init__(self, user_id = None, username = None, password_hash =
      None, salt = None):
    self.user_id = user_id
    self.username = str(username)
    self.salt = str(salt)
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

  def __eq__(self, right):
    try:
      return (self.username == right.username
        and self.user_id == right.user_id)
    except Exception:
      return False

class Session:
  def __init__(self, user_id = None, session_id = None, created =
      None, last_used = None):
    self.session_id = str(session_id)
    if user_id != None:
      self.user_id = int(user_id)
    else:
      self.user_id = None
    self.created = created
    self.last_used = last_used
    if(self.session_id == None):
      sha1func = sha1()
      sha1func.update(urandom(128))
      self.session_id = sha1func.hexdigest()

    if(created == None and last_used == None):
      self.created = time.time()
      self.last_used = time.time()

  def Touch(self):
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

  def writeUser(self, user): abstract()

  def createUser(self, username, password): abstract()

  def deleteUser(self, used): abstract()

  def deleteSession(self, session): abstract()

  def writeSession(self, session): abstract()

  def getSessionsByID(self, session_id): abstract()

  def getSessionsByUser(self, user): abstract()


class HSRAuthDBMySQLImpl(HSRAuthDB):
  def __init__(self, host, user, password, database, clear=False):
    self.db_host = host
    self.db_user = user
    self.db_pass = password
    self.db_name = database
    self.OpenDatabase()
    if clear:
      self.ClearDatabase()

  def OpenDatabase(self):
    self.db = MySQLdb.connect(self.db_host, self.db_user,
        self.db_pass, self.db_name)

  def ClearDatabase(self):
    cursor = self.db.cursor();
    cursor.execute("DELETE FROM Users;")
    cursor.execute("DELETE FROM Sessions;")

  def writeUser(self, user):
    params = [user.username, user.password_hash, user.salt,
        user.user_id]
    sql = """UPDATE Users
    SET Username=%s, PasswordHash=%s, Salt=%s
    WHERE UserID=%s
    """
    cursor = self.db.cursor()
    try:
      cursor.execute(sql, params)
    except IntegrityError:
      raise HSRAuthDBExcept("Could not write User!")

    if cursor.rowcount < 1:
      raise HSRAuthDBExcept("Could not write User!")

  def createUser(self, username, password):
    user = User(0, username, password)
    params = [user.username, user.salt, user.password_hash]
    sql = """INSERT INTO Users(Username, Salt, PasswordHash)
      VALUES (%s, %s, %s);"""
    
    cursor = self.db.cursor()
    try:
      cursor.execute(sql, params)
    except IntegrityError:
      raise HSRAuthDBExcept("Could not create User!")
    user.user_id = int(cursor.lastrowid)

    return user

  def getUserByName(self, username):
    params = [username]
    sql = """SELECT UserID, Username, PasswordHash, Salt FROM Users
    WHERE Username=%s"""
    cursor = self.db.cursor()
    cursor.execute(sql, params)
    try:
      result = cursor.fetchall()[0]
    except IndexError:
      return None
    return User(result[0], result[1], result[2], result[3])

  def deleteUser(self, user):
    params = [user.user_id]
    sql = "DELETE FROM Users WHERE UserID=%s;"
    cursor = self.db.cursor()
    cursor.execute(sql, params)

  def getSessionsByID(self, session_id):
    params = [session_id]
    sql = """SELECT UserID, SessionID, CreationTime, LastTouched FROM
    Sessions WHERE SessionID=%s;"""
    cursor = self.db.cursor()
    cursor.execute(sql, params)
    results = cursor.fetchall()
    sessions = []
    for session in results:
      sessions.append(Session(session[0], session[1], session[2],
        session[3]))
    return sessions

  def writeSession(self, session):
    params = [session.user_id, session.session_id,
        session.created, session.last_used]
    sql = """INSERT INTO Sessions(UserID, SessionID, CreationTime,
    LastTouched) VALUES(%s, %s, %s, %s);"""
    cursor = self.db.cursor()
    cursor.execute(sql, params)

  def deleteSession(self, session):
    params = [session.session_id, session.user_id]
    sql = """DELETE FROM Sessions WHERE SessionID=%s AND UserID=%s"""
    cursor = self.db.cursor()
    cursor.execute(sql, params)

  def getSessionsByUser(self, user):
    params = [user.user_id]
    sql = """SELECT UserID, SessionID, CreationTime, LastTouched FROM
    Sessions WHERE UserID=%s;"""
    cursor = self.db.cursor()
    cursor.execute(sql, params)
    results = cursor.fetchall()
    sessions = []
    for session in results:
      sessions.append(Session(session[0], session[1], session[2],
        session[3]))
    return sessions












