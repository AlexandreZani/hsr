#!/usr/bin/python

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

from hsr_server.hsr_db import *
from hsr_server.tests.HSRDBTests import HSRDBTestImpl
from sqlalchemy import *

def pytest_generate_tests(metafunc):
  if 'db' in metafunc.funcargnames:
    metafunc.addcall(param=1)
    metafunc.addcall(param=2)

def pytest_funcarg__db(request):
  if request.param == 1:
    return HSRDBTestImpl()
  elif request.param == 2:
    db = create_engine("mysql://test:password@localhost/HSRDB")
    metadata = MetaData(db)
    mos = Table('Objects', metadata, autoload=True)
    mos.delete().execute()
    indivs = Table('Individuals', metadata, autoload=True)
    indivs.delete().execute()
    return HSRDBSqlAlchemyImpl(db)

class TestDB:
  def test_NewMuseumObject(self, db):
    catalogue_num = 2
    object_num = 3
    site = "berkeley"
    nmo = db.newMuseumObject(catalogue_num, object_num, site)
    mo = MuseumObject(nmo.object_id, catalogue_num, object_num, site)
    assert nmo == mo

  def test_ChangeMuseumObject(self, db):
    catalogue_num = 2
    object_num = 3
    site = "berkeley"
    nmo = db.newMuseumObject(catalogue_num, object_num, site)

    nmo.site = "albany"
    assert db.writeMuseumObject(nmo)

    mo = db.getMuseumObjectById(nmo.object_id)
    assert nmo == mo

  def test_ChangeMuseumObjectNone(self, db):
    catalogue_num = 2
    object_num = 3
    site = "berkeley"
    nmo = db.newMuseumObject(catalogue_num, object_num, site)

    nmo.site = "albany"
    nmo.object_id += 1
    assert not db.writeMuseumObject(nmo)

    mo = db.getMuseumObjectById(nmo.object_id)
    assert mo == None

  def test_getMuseumObjectById(self, db):
    catalogue_num = 2
    object_num = 3
    site = "berkeley"
    nmo = db.newMuseumObject(catalogue_num, object_num, site)
    mo = db.getMuseumObjectById(nmo.object_id)
    assert nmo == mo

  def test_getMuseumObjectByIdNone(self, db):
    catalogue_num = 2
    object_num = 3
    site = "berkeley"
    nmo = db.newMuseumObject(catalogue_num, object_num, site)
    mo = db.getMuseumObjectById(nmo.object_id+1)
    assert None == mo

  def test_getAllMuseumObjects(self, db):
    mo1 = db.newMuseumObject("hello", "hi", "berkeley")
    mo2 = db.newMuseumObject("helslo", "hsfi", "berdkeley")
    mo3 = MuseumObject(32, "hels2lo", "h2sfi", "2berdkeley")

    mos = db.getAllMuseumObjects()

    assert mo1 in mos
    assert mo2 in mos
    assert mo3 not in mos

  def test_deleteMuseumObject(self, db):
    mo1 = db.newMuseumObject("hello", "hi", "berkeley")
    mo2 = db.newMuseumObject("helslo", "hsfi", "berdkeley")
    mo3 = db.newMuseumObject("hels2lo", "h2sfi", "2berdkeley")

    assert db.deleteMuseumObject(mo3.object_id)

    mos = db.getAllMuseumObjects()

    assert mo1 in mos
    assert mo2 in mos
    assert mo3 not in mos

  def test_newIndividual(self, db):
    suffix = "a"
    suffix_design = "b"
    min_age = 10
    max_age = 20
    mo = 1
    sex = BioIndividual.NA
    nbi = db.newIndividual(suffix, suffix_design, min_age, max_age,
        sex, mo)
    bi = BioIndividual(nbi.indiv_id, suffix, suffix_design, min_age,
        max_age, sex, mo)
    assert nbi == bi

  def test_getIndividualById(self, db):
    suffix = "a"
    suffix_design = "b"
    min_age = 10
    max_age = 20
    mo = 1
    sex = BioIndividual.NA
    nbi = db.newIndividual(suffix, suffix_design, min_age, max_age,
        sex, mo)
    bi = db.getIndividualById(nbi.indiv_id)
    assert nbi == bi

  def test_getIndividualByIdNone(self, db):
    suffix = "a"
    suffix_design = "b"
    min_age = 10
    max_age = 20
    sex = BioIndividual.NA
    nbi = db.newIndividual(suffix, suffix_design, min_age, max_age,
        sex, 1)
    bi = db.getIndividualById(nbi.indiv_id+1)
    assert bi == None

  def test_writeIndividual(self, db):
    suffix = "a"
    suffix_design = "b"
    min_age = 10
    max_age = 20
    sex = BioIndividual.NA
    nbi = db.newIndividual(suffix, suffix_design, min_age, max_age,
        sex, 1)
    nbi.indiv_id += 1
    nbi.min_age += 5
    nbi.suffix_design = "d"
    assert not db.writeIndividual(nbi)
    bi = db.getIndividualById(nbi.indiv_id)
    assert nbi != bi

  def test_writeIndividualNone(self, db):
    suffix = "a"
    suffix_design = "b"
    min_age = 10
    max_age = 20
    sex = BioIndividual.NA
    nbi = db.newIndividual(suffix, suffix_design, min_age, max_age,
        sex, 1)
    nbi.indiv_id += 1
    nbi.min_age += 5
    nbi.suffix_design = "d"
    assert not db.writeIndividual(nbi)
    bi = db.getIndividualById(nbi.indiv_id)
    assert bi == None

  def test_getAllIndividuals(self, db):
    bi1 = db.newIndividual("a", "a1", 10, 30, "NA", 1)
    bi2 = db.newIndividual("b", "b1", 130, 310, "NA", 1)
    bi3 = BioIndividual(121, "fa", "d1", 140, 320, "NA", 1)
    bis = db.getAllIndividuals()
    assert bi1 in bis
    assert bi2 in bis
    assert bi3 not in bis

  def test_deleteIndividual(self, db):
    bi1 = db.newIndividual("a", "a1", 10, 30, "NA", 1)
    bi2 = db.newIndividual("b", "b1", 130, 310, "NA", 1)
    bi3 = db.newIndividual("sb", "fb1", 1330, 1310, "NA", 1)
    db.deleteIndividual(bi3.indiv_id)
    bis = db.getAllIndividuals()
    assert bi1 in bis
    assert bi2 in bis
    assert bi3 not in bis
