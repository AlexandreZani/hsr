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

from paste.request import get_cookie_dict
from hsr.controller.auth import *
from hsr.controller.secure_auth import SecureAuthController
from hsr.controller.secure_engine import SecureEngine
import hsr.views.login
from cgi import parse_qs, escape
import logging

class Checkpoint(object):
  def __init__(self, engine, login_view=hsr.views.login,
      session_expiration=60*60):
    self.engine = engine
    self.auth_controller = AuthController(engine)
    self.login_view = login_view
    self.session_expiration = session_expiration

  def __call__(self, pipe, environ, start_response):
    remote_ip = environ.get('REMOTE_ADDR', "Unknown")
    cookies = get_cookie_dict(environ)

    try:
      environ['hsr']['user'] = None 
    except KeyError:
      environ['hsr'] = {'user' : None}

    environ['hsr']['auth_except'] = None
    environ['hsr']['session'] = None

    try:
      sid = cookies['sid']
      if sid == None:
        raise KeyError
      session = self.auth_controller.get_session(sid,
          session_expiration=self.session_expiration)
      user = session.user
    except (NoSuchSession, SessionExpired), e:
      logging.info("%s failed to authenticate using (%s): %s" %
          (remote_ip, sid, type(e).__name__))
      environ['hsr']['auth_except'] = e
      start_response.delete_cookie('sid')
      return self.login_view(None, environ, start_response)
    except KeyError, e:
      environ['hsr']['auth_except'] = e
      try:
        data_len = int(environ.get('CONTENT_LENGTH', '0'))
      except ValueError:
        logging.info("%s sent a malformed or no login request." % remote_ip)
        return self.login_view(None, environ, start_response)

      try:
        username = None
        data = environ['wsgi.input'].read(data_len)
        data_dict = parse_qs(data)
        username = data_dict['username'][0]
        password = data_dict['password'][0]
        session = self.auth_controller.create_session(
            username, password)
        user = session.user
        environ['hsr']['auth_except'] = None
        start_response.add_headers([('Set-Cookie', 'sid=' + session.session_id)])
        logging.info("%s logged in as %s" % (remote_ip, username))
      except (KeyError, WrongPassword, NoSuchUser), e:
        logging.info("%s Failed login attempt for %s: %s" %
            (remote_ip, username, type(e).__name__))
        environ['hsr']['auth_except'] = e
        return self.login_view(None, environ, start_response)

    environ['hsr']['user'] = user
    environ['hsr']['session'] = session
    environ['hsr']['auth_controller'] = SecureAuthController(
        self.auth_controller, user)
    environ['hsr']['db_engine'] = SecureEngine(self.engine, user)
    environ['pythia']['jinja_env'].add_context_variables(user=user,
        Permissions=Permissions)

    return pipe(environ, start_response)
