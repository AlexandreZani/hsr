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

from sqlalchemy.orm import sessionmaker
from hsr.model.user import Permissions
from hsr.controller.secure import InsufficientPermissions, secure

class SecureEngine(object):
  def __init__(self, engine, user):
    self._db_session_class = sessionmaker(bind=engine, expire_on_commit=False)
    self._user = user

  @secure(Permissions.READ)
  def get_db_session(self):
    return SecureDBSession(self._db_session_class(), self._user)

class SecureDBSession(object):
  def __init__(self, db_session, user):
    self._db_session = db_session
    self._user = user

  @secure(Permissions.WRITE)
  def add_all(self, *args, **kwargs):
    return self._db_session.add_all(*args, **kwargs)

  @secure(Permissions.WRITE)
  def add(self, *args, **kwargs):
    return self._db_session.add(*args, **kwargs)

  @secure(Permissions.WRITE)
  def commit(self, *args, **kwargs):
    return self._db_session.commit(*args, **kwargs)

  @secure(Permissions.READ)
  def query(self, *args, **kwargs):
    return self._db_session.query(*args, **kwargs)
