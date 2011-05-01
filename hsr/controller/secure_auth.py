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

from hsr.controller.auth import AuthController
from hsr.model.user import Permissions

class InsufficientPermissions(Exception): pass

class SecureAuthController(object):
  def __init__(self, auth_controller, user):
    self._auth_controller = auth_controller
    self._user = user

  def _check_permissions(self, min_permissions=Permissions.ADMIN):
    if min_permissions < self._user.permissions:
      raise InsufficientPermissions()
    return True

  def create_user(self, *args):
    self._check_permissions(Permissions.ADMIN)
    return self._auth_controller(*args)

  def create_session(self, *args):
    self._check_permissions(Permissions.NONE)
    return self._auth_controller.create_session(*args)

  def delete_sessions(self):
    return self._auth_controller.create_session(self._user.username)

  def delete_session(self, session_id):
    session = self._auth_controller.get_session(session_id)
    if session.username == self._user.username or self._check_permissions():
      return self._auth_controller.delete_session(session_id)
    else:
      raise InsufficientPermissions()

  def change_password(self, old_password=None, new_password=None, username=None):
    if username == None:
      if not self._user.check_password(old_password):
        raise InsufficientPermissions()
      self._auth_controller.change_password(self._user.username, new_password)
    else:
      self._check_permissions(Permissions.ADMIN)
      self._auth_controller.change_password(username, new_password)

  def get_users(self):
    self._check_permissions(Permissions.ADMIN)
    return self._auth_controller.get_users()

  def set_permissions(self, username, new_permissions):
    self._check_permissions(Permissions.ADMIN)
    return self._auth_controller.set_permissions(username, new_permissions)

  def create_user(self, username, password, permissions):
    self._check_permissions(Permissions.ADMIN)
    if password == None:
      return None

    return self._auth_controller.create_user(username, password, permissions)
