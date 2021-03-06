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

from hsr.model.user import User, Permissions

class TestUser(object):
  def test_password(self):
    user = User("username", "password")
    assert user.check_password("password")

  def test_wrong_password(self):
    user = User("username", "password")
    assert not user.check_password("passord")

  def test_set_password(self):
    user = User("username", "passrd")
    user.set_password("password")
    assert user.check_password("password")

  def test_permissions(self):
    user = User("username", "passrd")
    assert Permissions.NONE == user.permissions
    assert "None" == user.permissions_str
    user = User("username", "passrd", Permissions.NONE)
    assert Permissions.NONE == user.permissions
    assert "None" == user.permissions_str
    user = User("username", "passrd", Permissions.READ)
    assert Permissions.READ == user.permissions
    assert "Read" == user.permissions_str
    user = User("username", "passrd", Permissions.WRITE)
    assert Permissions.WRITE == user.permissions
    assert "Write" == user.permissions_str
    user = User("username", "passrd", Permissions.ADMIN)
    assert Permissions.ADMIN== user.permissions
    assert "Admin" == user.permissions_str
