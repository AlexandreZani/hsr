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

  def create_user(self, *args):
    self._check_permissions(Permissions.ADMIN)
    return self._auth_controller(*args)

  def create_session(self, *args):
    self._check_permissions(Permissions.NONE)
    return self._auth_controller.create_session(*args)

  def delete_sessions(self):
    return self._auth_controller.create_session(self._user.username)