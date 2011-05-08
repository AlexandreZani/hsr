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
from hsr.model.user import Permissions, User
from hsr.controller.secure import secure, InsufficientPermissions

class C(object):
  def __init__(self, user):
    self._user = user

  @secure(Permissions.ADMIN)
  def admin_op(self):
    return "admin"

  @secure(Permissions.WRITE)
  def write_op(self):
    return "write"

class TestSecure(object):
  def test_sufficient(self):
    c = C(User("a", "b", Permissions.WRITE))

    assert "write" == c.write_op()

  def test_insufficient(self):
    c = C(User("a", "b", Permissions.WRITE))

    with pytest.raises(InsufficientPermissions):
      c.admin_op()



