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

  def get_session(self, session_id, db_session=None, session_expiration=60*60):
    if db_session == None:
      db_session = self._get_db_session()

    try:
      session = db_session.query(Session).filter_by(session_id=session_id).all()[0]
    except IndexError:
      raise NoSuchSession(session_id)

    if not session.is_valid(session_expiration):
      raise SessionExpired()

    session.touch()

    return session

  def create_session(self, username, password):
    db_session = self._get_db_session()

    user = self.get_user(username, db_session)

    if not user.check_password(password):
      raise WrongPassword()

    session = Session(user.username)

    db_session.add(session)

    db_session.commit()

    return session

  def get_session_user(self, session_id,
      session_expiration=60*60):
    db_session = self._get_db_session()

    session = self.get_session(session_id, db_session, session_expiration)

    db_session.commit()

    return session.user

  def delete_sessions(self, username):
    db_session = self._get_db_session()

    db_session.query(Session).filter(Session.username==username).delete()

    db_session.commit()

  def delete_session(self, session_id):
    db_session = self._get_db_session()

    db_session.query(Session).filter(Session.session_id==session_id).delete()

    db_session.commit()

  def change_password(self, username, new_password):
    db_session = self._get_db_session()

    user = self.get_user(username, db_session)

    user.set_password(new_password)

    db_session.commit()

  def get_users(self):
    db_session = self._get_db_session()

    users = db_session.query(User).all()
    
    return users
