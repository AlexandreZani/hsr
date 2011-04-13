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

from hsr.model.meta import Base
from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship
from os import urandom
from hashlib import sha256

hash_algo = sha256

class Permissions(object):
  NONE = 128
  READ = 64
  WRITE = 32
  ADMIN = 0

class User(Base):
  __tablename__ = 'users'

  username = Column(String, primary_key=True)
  salted_password = Column(LargeBinary)
  password_salt = Column(LargeBinary)
  permissions = Column(Integer)

  def __init__(self, username, password, permissions=Permissions.NONE):
    self.username = username
    self.set_password(password)
    self.permissions = Permissions.NONE

  def set_password(self, password):
    self.password_salt = urandom(256/8)
    self.salted_password = self._salt_password(self.password_salt, password)

  def check_password(self, password):
    return self.salted_password == self._salt_password(self.password_salt, password)

  def _salt_password(self, salt, password):
    hash_obj = hash_algo()
    hash_obj.update(password)
    hash_obj.update(salt)
    return hash_obj.digest()

  def __repr__(self):
    return "<User (%s)>" % (self.username,)
