#   Copyright 2011 Alexandre Zani (alexandre.zani@gmail.com) 
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

import pytest
from hsr.model.meta import Base
from hsr.model.user import User, Permissions
from hsr.model.session import Session
from hsr.controller.auth import *
from sqlalchemy import create_engine
from time import sleep

def pytest_generate_tests(metafunc):
  if 'auth_controller' in metafunc.funcargnames:
    metafunc.addcall(param=1)

def pytest_funcarg__auth_controller(request):
  if request.param == 1:
    engine = create_engine("sqlite:///")
    Base.metadata.create_all(engine)
    return AuthController(engine)

class TestAuth(object):
  def test_create_user(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    user = auth_controller.get_user(username)

    assert user.username == username
    assert user.check_password(password)

  def test_delete_user(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    auth_controller.delete_user(username)

    with pytest.raises(NoSuchUser):
      auth_controller.get_user(username)

  def test_create_duplicate_user(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    with pytest.raises(DuplicateUsername):
      auth_controller.create_user(username, password, Permissions.ADMIN)

  def test_get_users(self, auth_controller):
    u1 = auth_controller.create_user("user1", "pass", Permissions.NONE)
    u2 = auth_controller.create_user("user2", "pass", Permissions.ADMIN)

    users = map(lambda user: user.username, auth_controller.get_users())
    assert u1.username in users
    assert u2.username in users

  def test_change_password(self, auth_controller):
    username = "name"
    password = "pass"
    new_pass = "new_pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    auth_controller.change_password(username, new_pass)

    user = auth_controller.get_user(username)

    assert user.username == username
    assert user.check_password(new_pass)

  def test_change_user_permission(self, auth_controller):
    username = "name"
    password = "pass"
    new_permissions = Permissions.NONE

    auth_controller.create_user(username, password, Permissions.ADMIN)

    auth_controller.set_permissions(username, new_permissions)

    user = auth_controller.get_user(username)

    assert user.username == username
    assert user.permissions == new_permissions

  def test_create_session(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    s = auth_controller.create_session(username, password)

    assert s.username == username
    assert s.user.username == username
    assert s == s.user.sessions[0]

  def test_create_session_wrong_user(self, auth_controller):
    username = "name"
    password = "pass"

    with pytest.raises(NoSuchUser):
      auth_controller.create_session(username, password)

  def test_create_session_wrong_password(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    with pytest.raises(WrongPassword):
      auth_controller.create_session(username, password + "hello")

  def test_get_session_user(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    s = auth_controller.create_session(username, password)

    user = auth_controller.get_session_user(s.session_id)

    assert user.username == username
    assert user.check_password(password)

  def test_get_session_user_touch(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    session = auth_controller.create_session(username, password)
    first_touch = session.last_touched
    print "First touch:", first_touch

    sleep(1)
    user = auth_controller.get_session_user(session.session_id)

    s = auth_controller.get_session(session.session_id)

    assert s.last_touched > first_touch

  def test_get_session_user_does_not_exist(self, auth_controller):
    with pytest.raises(NoSuchSession):
      auth_controller.get_session_user("asdasda")

  def test_get_session_session_expired(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    session = auth_controller.create_session(username, password)

    with pytest.raises(SessionExpired):
      auth_controller.get_session_user(session.session_id, -1)

  def test_delete_sessions(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    session = auth_controller.create_session(username, password)
    session_id = session.session_id

    auth_controller.delete_sessions(username)

    with pytest.raises(NoSuchSession):
      auth_controller.get_session_user(session_id)

  def test_delete_session_by_id(self, auth_controller):
    username = "name"
    password = "pass"

    auth_controller.create_user(username, password, Permissions.ADMIN)

    session = auth_controller.create_session(username, password)
    session_id = session.session_id

    auth_controller.delete_session(session_id)

    with pytest.raises(NoSuchSession):
      auth_controller.get_session_user(session_id)
