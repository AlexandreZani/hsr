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
from sqlalchemy import create_engine
from hsr.controller.auth import *
from hsr.controller.checkpoint import Checkpoint
from StringIO import StringIO
from pythia.custom_start_response import CustomStartResponse

def pytest_generate_tests(metafunc):
  if 'engine' in metafunc.funcargnames:
    metafunc.addcall(param=1)

def pytest_funcarg__engine(request):
  if request.param == 1:
    engine = create_engine("sqlite:///")
    Base.metadata.create_all(engine)
    return engine

class TestCheckpointSessions(object):
  def test_valid_session(self, engine):
    def check_user(environ, start_response):
      assert 'name' == environ['hsr']['user'].username
      assert None == environ['hsr']['auth_except']
      return 'check_user'

    checkpoint = Checkpoint(engine)

    username = "name"
    password = "pass"

    auth_controller = AuthController(engine)

    auth_controller.create_user(username, password, Permissions.ADMIN)
    s = auth_controller.create_session(username, password)

    environ = {
        'HTTP_COOKIE' : 'sid=' + s.session_id,
        'pythia' : {
          'chain' : check_user
          }
        }

    assert "check_user" == checkpoint(environ, [])

  def test_no_session(self, engine):
    def login(environ, start_response):
      assert None == environ['hsr']['user']
      assert None == environ['hsr']['auth_except']
      return "login"
    checkpoint = Checkpoint(engine, login)

    environ = {
        'HTTP_COOKIE' : '',
        'pythia' : {
          'chain' : None
          }
        }

    assert "login" == checkpoint(environ, [])

  def test_invalid_session(self, engine):
    def login(environ, start_response):
      assert None == environ['hsr']['user']
      assert NoSuchSession == type(environ['hsr']['auth_except'])
      return "login"
    checkpoint = Checkpoint(engine, login)

    environ = {
        'HTTP_COOKIE' : 'sid=jhgaskasgd',
        'pythia' : {
          'chain' : None
          }
        }

    assert "login" == checkpoint(environ, [])

  def test_expired_session(self, engine):
    def login(environ, start_response):
      assert None == environ['hsr']['user']
      assert SessionExpired == type(environ['hsr']['auth_except'])
      return "login"

    checkpoint = Checkpoint(engine, login, -1)

    username = "name"
    password = "pass"

    auth_controller = AuthController(engine)

    auth_controller.create_user(username, password, Permissions.ADMIN)
    s = auth_controller.create_session(username, password)

    environ = {
        'HTTP_COOKIE' : 'sid=' + s.session_id,
        'pythia' : {
          'chain' : None
          }
        }

    assert "login" == checkpoint(environ, [])

class TestCheckpointLogin(object):
  def test_valid_user(self, engine):
    def check_user(environ, start_response):
      assert 'name' == environ['hsr']['user'].username
      assert None == environ['hsr']['auth_except']
      assert 'cookie_checked' == start_response('', [])
      return 'check_user'

    def check_cookie(status, response_headers):
      assert 'Set-Cookie' == response_headers[0][0]
      return 'cookie_checked'

    checkpoint = Checkpoint(engine)

    username = "name"
    password = "pass"

    auth_controller = AuthController(engine)

    auth_controller.create_user(username, password, Permissions.ADMIN)
    post_str = "username=" + username + "&password=" + password

    environ = {
        'wsgi.input' : StringIO(post_str),
        'CONTENT_LENGTH' : len(post_str),
        'pythia' : {
          'chain' : check_user
          }
        }

    assert "check_user" == checkpoint(environ, CustomStartResponse(check_cookie))
