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
from hsr_auth.tests.HSRAuthDBTest import HSRAuthDBTestImpl, HSRAuthDBExcept
from sqlalchemy import *

class TestUser:
  def test_CheckPasswordTrue(self):
    user = User()

    user.UpdatePassword("Hello!")
    assert user.CheckPassword("Hello!")

  def test_CheckPasswordFalse(self):
    user = User()

    user.UpdatePassword("Hello!")
    assert not user.CheckPassword("Hello!2")

  def test_CheckPermission(self):
    user = User()

    assert user.CheckPermissions(Permissions.NONE)
    assert user.CheckPermissions(Permissions.READ)
    assert not user.CheckPermissions(Permissions.WRITE)
    assert not user.CheckPermissions(Permissions.ADMIN)

def pytest_generate_tests(metafunc):
  if 'db' in metafunc.funcargnames:
    metafunc.addcall(param=1)
    metafunc.addcall(param=2)
    metafunc.addcall(param=3)

def pytest_funcarg__db(request):
  if request.param == 1:
    return HSRAuthDBTestImpl()
  elif request.param == 2:
    return HSRAuthDBMySqlImpl('localhost', 'test', 'password',
        'HSRAuthDB', True)
  elif request.param == 3:
    db = create_engine("mysql://test:password@localhost/HSRAuthDB")
    conn = db.connect()
    metadata = MetaData(conn)
    users = Table('Users', metadata, autoload=True)
    users.delete().execute()
    sessions = Table('Sessions', metadata, autoload=True)
    sessions.delete().execute()
    conn.close()
    return HSRAuthDBSqlAlchemyImpl(db)

class TestDB:
  def test_CreateUser(self, db):
    user = db.createUser('armence', 'Hello!', Permissions.ADMIN)
    user2 = db.getUserByName('armence')

    assert user.username == user2.username
    assert user.user_id == user2.user_id
    assert user.password_hash == user2.password_hash
    assert user.salt == user2.salt
    assert user.permissions == user2.permissions
    assert Permissions.ADMIN == user.permissions
    assert user == user2

  def test_GetUserById(self, db):
    user = db.createUser('armence', 'Hello!')
    user2 = db.getUserById(user.user_id)

    assert user == user2

  def test_CreateSameUsername(self, db):
    user = db.createUser('armence', 'Hello!')
    try:
      user = db.createUser('armence', 'Pass2')
    except HSRAuthDBExcept, (instance):
      assert str(instance) == "Could not create User!"
    else:
      assert False

  def test_ChangeUser(self, db):
    user = db.createUser('armence', 'Hello!')
    user.UpdatePassword('World!')
    user.username = 'loki'
    user.permissions = Permissions.ADMIN
    db.writeUser(user)
    user2 = db.getUserByName('loki')
    assert user2.CheckPassword('World!')
    assert user2.CheckPermissions(Permissions.ADMIN)

  def test_ChangeSameUsername(self, db):
    db.createUser('armence', 'Hello!')
    user = db.createUser('cat', 'Hello!')
    user.username = 'armence'
    try:
      db.writeUser(user)
    except HSRAuthDBExcept, (instance):
      print str(instance)
      assert str(instance) == "Could not write User!"
    else:
      assert False

  def test_ChangeUnknownUser(self, db):
    user = db.createUser('armence', 'Hello!')
    db.deleteUser(user)
    try:
      db.writeUser(user)
    except HSRAuthDBExcept, (instance):
      assert str(instance) == "Could not write User!"
    else:
      assert False

  def test_DeleteUser(self, db):
    user = db.createUser('armence', 'Hello!')
    db.deleteUser(user)
    user2 = db.getUserByName('armence')

    assert user2 == None

  def test_FindUnknownUser(self, db):
    user2 = db.getUserByName('armence')

    assert user2 == None

  def test_FindUnknownSession(self, db):
    session = db.getSessionById(46431)

    assert session == None

  def test_FindCreateSession(self, db):
    session = Session(7657856, 46431)
    db.writeSession(session)
    session2 = db.getSessionById(46431)

    assert session2 == session

  def test_SessionNotNone(self, db):
    session = Session(1231231)
    assert None != session.session_id

  def test_CreateSessionFail(self, db):
    session = Session(7657856, 46431)
    db.writeSession(session)
    session = Session(7657856, 46431)
    try:
      db.writeSession(session)
    except HSRAuthDBExcept, (instance):
      assert str(instance) == "Could not write Session!"
    else:
      assert False

  def test_DeleteSession(self, db):
    session = Session(7657856, 46431)
    db.writeSession(session)
    db.deleteSession(session)
    session = db.getSessionById(46431)

    assert session == None

  def test_FindUserSessions(self, db):
    user = User(1, 'armence', 'Hello!')
    session = Session(user.user_id, 46431)
    db.writeSession(session)
    sessions = db.getSessionsByUser(user)

    assert session == sessions[0]

  def test_newSession(self, db):
    user = User(1, 'armence', 'Hello!')
    session = db.newSession(user.user_id)
    session2 = db.getSessionsByUser(user)[0]

    assert session == session2
