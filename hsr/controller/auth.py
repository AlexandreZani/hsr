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

from hsr.model.user import User, Permissions
from hsr.model.session import Session
import hsr.settings
import sqlalchemy
from sqlalchemy.orm import sessionmaker

class DuplicateUsername(Exception): pass
class NoSuchUser(Exception): pass
class WrongPassword(Exception): pass
class NoSuchSession(Exception): pass
class SessionExpired(Exception): pass

class AuthController(object):
  def __init__(self, engine):
    self._db_session_class = sessionmaker(bind=engine)

  def _get_db_session(self):
    return self._db_session_class()

  def create_user(self, username, password, permissions = Permissions.NONE):
    db_session = self._get_db_session()

    user = User(username, password, permissions)

    db_session.add(user)

    try:
      db_session.commit()
    except sqlalchemy.exc.IntegrityError:
      raise DuplicateUsername(username)

    return user

  def get_user(self, username, db_session=None):
    if db_session == None:
      db_session = self._get_db_session()

    try:
      return db_session.query(User).filter_by(username=username).all()[0]
    except IndexError:
      raise NoSuchUser(username)

  def _get_session(self, db_session_id, db_session=None):
    if db_session == None:
      db_session = self._get_db_session()

    try:
      return db_session.query(Session).filter_by(session_id=db_session_id).all()[0]
    except IndexError:
      raise NoSuchSession(db_session_id)

  def create_session(self, username, password):
    db_session = self._get_db_session()

    user = self.get_user(username, db_session)

    if not user.check_password(password):
      raise WrongPassword()

    session = Session(user.username)
    print "At creation:", session.last_touched

    db_session.add(session)

    db_session.commit()

    return session

  def get_session_user(self, session_id,
      session_expiration=60*60):
    db_session = self._get_db_session()

    session = self._get_session(session_id, db_session)

    if not session.is_valid(session_expiration):
      raise SessionExpired()

    session.touch()

    db_session.commit()

    return self.get_user(session.username, db_session)

  def delete_sessions(self, username):
    db_session = self._get_db_session()

    db_session.query(Session).filter(Session.username==username).delete()

    db_session.commit()
