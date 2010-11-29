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

from hsr_auth.credentials import getHSRCredentials, HSRCredentialsException
from hsr_auth.auth_db import Permissions
from hsr_auth.tests.HSRAuthDBTest import HSRAuthDBTestImpl, HSRAuthDBExcept

class TestNoneCredentials:
  def test_CreateNoneCredentials(self):
    credentials = getHSRCredentials("None", {}, "127.0.0.1")
    assert credentials.getCredentialsType() == "None"

  def test_GetUserIdNoneCredentials(self):
    credentials = getHSRCredentials("None", {}, "127.0.0.1")
    try:
      credentials.getUserId()
    except HSRCredentialsException, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

  def test_CheckPermissions(self):
    credentials = getHSRCredentials("None", {}, "127.0.0.1")
    try:
      credentials.checkPermissions(Permissions.NONE)
    except HSRCredentialsException, (ex):
      assert str(ex) == "InsufficientPermissions"
    else:
      assert False

class TestUsernamePasswordCredentials:
  def test_Factory(self):
    args = {
        "username" : "loki",
        "password" : "key"
        }
    credentials = getHSRCredentials("UsernamePassword", args, "127.0.0.1")
    assert credentials.getCredentialsType() == "UsernamePassword"

  def test_GetUserId(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    args = {
        "username" : username,
        "password" : password
        }
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    assert credentials.getUserId() == user.user_id

  def test_WrongPassword(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    args = {
        "username" : username,
        "password" : "bad_pass"
        }
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    try:
      credentials.getUserId()
    except HSRCredentialsException, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

  def test_WrongUsername(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    args = {
        "username" : "other",
        "password" : password
        }
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    try:
      credentials.getUserId()
    except HSRCredentialsException, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

  def test_MissingUsername(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    args = {"password" : password}
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    try:
      credentials.getUserId()
    except HSRCredentialsException, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

  def test_MissingPassword(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    args = {"username" : username}
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    try:
      credentials.getUserId()
    except HSRCredentialsException, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

  def test_GetSession(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    args = {
        "username" : username,
        "password" : password
        }
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    credentials.getUserId()
    session = db.getSessionById(credentials.session.session_id)
    assert session == credentials.session

  def test_CheckPermissionsFail(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password, Permissions.WRITE)
    args = {
        "username" : username,
        "password" : password
        }
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    credentials.getUserId()

    try:
      credentials.checkPermissions(Permissions.ADMIN)
    except HSRCredentialsException, (ex):
      assert str(ex) == "InsufficientPermissions"
    else:
      assert False

  def test_CheckPermissionsFail(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password, Permissions.WRITE)
    args = {
        "username" : username,
        "password" : password
        }
    credentials = getHSRCredentials("UsernamePassword", args,
        "127.0.0.1", db)
    credentials.getUserId()

    credentials.checkPermissions(Permissions.WRITE)

class TestSessionIdCredentials:
  def test_Factory(self):
    args = {"session_id" : "abcdef"}
    credentials = getHSRCredentials("SessionId", args, "127.0.0.1")
    assert credentials.getCredentialsType() == "SessionId"

  def test_GetUserId(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    session = db.newSession(user.user_id)
    args = {"session_id" : session.session_id}
    credentials = getHSRCredentials("SessionId", args, "127.0.0.1", db)
    assert credentials.getUserId() == user.user_id

  def test_WrongSessionId(self):
    db = HSRAuthDBTestImpl()
    args = {"session_id" : "blah"}
    credentials = getHSRCredentials("SessionId", args, "127.0.0.1", db)
    try:
      credentials.getUserId()
    except HSRCredentialsException, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

  def test_MissingSessionId(self):
    db = HSRAuthDBTestImpl()
    args = {}
    credentials = getHSRCredentials("SessionId", args, "127.0.0.1", db)
    try:
      credentials.getUserId()
    except HSRCredentialsException, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

  def test_CheckPermissionsFails(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    session = db.newSession(user.user_id)
    args = {"session_id" : session.session_id}
    credentials = getHSRCredentials("SessionId", args, "127.0.0.1", db)

    try:
      credentials.checkPermissions(Permissions.ADMIN)
    except HSRCredentialsException, (ex):
      assert str(ex) == "InsufficientPermissions"
    else:
      assert False
