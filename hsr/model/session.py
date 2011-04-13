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
from sqlalchemy import Integer, Column, ForeignKey, LargeBinary, String
from os import urandom
from binascii import hexlify, unhexlify
from time import time

class Session(Base):
  __tablename__ = 'sessions'

  username = Column(String, ForeignKey('users.username'))
  session_id = Column(LargeBinary, primary_key=True)
  last_touched = Column(Integer)

  def __init__(self, username):
    self.username = username
    self.session_id = hexlify(urandom(256/8))
    self.touch()

  def touch(self):
    self.last_touched = int(time())

  def is_valid(self, max_length):
    return (int(time()) - self.last_touched) < max_length

  def __repr__(self):
    return "<Session (%s, %s)>" % (self.username, self.session_id,)
