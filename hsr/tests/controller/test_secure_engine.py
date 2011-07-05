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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hsr.model.meta import Base
from hsr.controller.secure_engine import SecureEngine, SecureDBSession
from hsr.model import User, Permissions, MuseumObject, Site
from hsr.controller.secure_auth import InsufficientPermissions

def pytest_generate_tests(metafunc):
  if 'engine' in metafunc.funcargnames:
    metafunc.addcall(param=1)

def pytest_funcarg__engine(request):
  if request.param == 1:
    engine = create_engine("sqlite:///")
    Base.metadata.create_all(engine)
    return engine

class TestSecureEngine(object):
  def test_create_session(self, engine):
    user = User("u", "p", Permissions.READ)
    secure_engine = SecureEngine(engine, user)

    db_session = secure_engine.get_db_session()

    assert type(db_session) is SecureDBSession

  def test_create_session_no_permissions(self, engine):
    user = User("u", "p", Permissions.NONE)
    secure_engine = SecureEngine(engine, user)

    with pytest.raises(InsufficientPermissions):
      db_session = secure_engine.get_db_session()

class TestSecureDBSession(object):
  def test_write(self, engine):
    user = User("u", "p", Permissions.WRITE)
    secure_engine = SecureEngine(engine, user)
    dbs = secure_engine.get_db_session()

    catalogue_num = "cat_id"
    site = Site(123, "berkeley")
    mo = MuseumObject(catalogue_num, 234, site.id)

    dbs.add_all([mo, site])

    dbs.commit()

    mo2 = dbs.query(MuseumObject).filter_by(catalogue_num=catalogue_num).first()

    assert mo.catalogue_num == mo2.catalogue_num
    assert mo.site_id == mo2.site_id
    assert mo.object_num == mo2.object_num

  def test_write_read_only(self, engine):
    user = User("u", "p", Permissions.READ)
    secure_engine = SecureEngine(engine, user)
    dbs = secure_engine.get_db_session()

    catalogue_num = "cat_id"
    site = Site(123, "berkeley")
    mo = MuseumObject(catalogue_num, 234, site.id)

    with pytest.raises(InsufficientPermissions):
      dbs.add_all([mo, site])

    with pytest.raises(InsufficientPermissions):
      dbs.commit()

  def test_read_only(self, engine):
    SessionClass = sessionmaker(bind=engine, expire_on_commit=False)
    s = SessionClass()

    catalogue_num = "cat_id"

    site = Site(123, "berkeley")
    mo = MuseumObject(catalogue_num, 234, site.id)

    s.add_all([mo, site])

    s.commit()

    user = User("u", "p", Permissions.READ)
    secure_engine = SecureEngine(engine, user)
    dbs = secure_engine.get_db_session()

    mo2 = dbs.query(MuseumObject).filter_by(catalogue_num=catalogue_num).first()

    assert mo.catalogue_num == mo2.catalogue_num
    assert mo.site_id == mo2.site_id
    assert mo.object_num == mo2.object_num

  def test_commit_twice(self, engine):
    user = User("u", "p", Permissions.WRITE)
    secure_engine = SecureEngine(engine, user)
    dbs = secure_engine.get_db_session()

    catalogue_num = "cat_id"
    site = Site(123, "berkeley")
    mo = MuseumObject(catalogue_num, 234, site.id)

    dbs.add_all([mo, site])

    dbs.commit()

    mo2 = dbs.query(MuseumObject).filter_by(catalogue_num=catalogue_num).first()

    assert mo.catalogue_num == mo2.catalogue_num
    assert mo.site_id == mo2.site_id
    assert mo.object_num == mo2.object_num

    cat_num3 = "something here"
    site2 = Site(453, "portland")
    mo3 = MuseumObject(cat_num3, 345, site.id)

    dbs.add_all([mo3, site2])

    dbs.commit()
    mo4 = dbs.query(MuseumObject).filter_by(catalogue_num=cat_num3).first()
    print mo4

    assert mo3.catalogue_num == mo4.catalogue_num
    assert mo3.site_id == mo4.site_id
    assert mo3.object_num == mo4.object_num
