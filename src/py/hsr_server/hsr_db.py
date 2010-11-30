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

from sqlalchemy import *
from xml.sax.saxutils import escape

def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass')

class MuseumObject(object):
  @property
  def object_id(self):
    return self._object_id

  @object_id.setter
  def object_id(self, value):
    self._object_id = int(value)

  @property
  def object_num(self):
    return self._object_num

  @object_num.setter
  def object_num(self, value):
    self._object_num = str(value)

  @property
  def catalogue_num(self):
    return self._catalogue_num

  @catalogue_num.setter
  def catalogue_num(self, value):
    self._catalogue_num = str(value)

  @property
  def site(self):
    return self._site

  @site.setter
  def site(self, value):
    self._site = str(value)

  def __init__(self, object_id = None, catalogue_num = None,
      object_num = None, site = None):
    self.object_id = object_id
    self.object_num = object_num
    self.catalogue_num = catalogue_num
    self.site = site

  def copy(self):
    return MuseumObject(self.object_id, self.catalogue_num,
        self.object_num, self.site)

  def __eq__(self, other):
    try:
      r = (self.object_id == other.object_id)
      r = r and self.object_num == other.object_num
      r = r and self.catalogue_num == other.catalogue_num
      r = r and self.site == other.site
      return r
    except AttributeError:
      return False

  def __ne__(self, other):
    return not (self == other)

  def toXml(self):
    xml = "<museum_object>"
    xml += "<object_id>" + escape(str(self.object_id)) + "</object_id>"
    xml += "<object_number>" + escape(str(self.object_num)) + "</object_number>"
    xml += "<catalogue_number>" + escape(str(self.catalogue_num)) + "</catalogue_number>"
    xml += "<site>" + escape(str(self.site)) + "</site>"
    xml += "</museum_object>"
    return xml

class BioIndividual(object):
  NA = 0
  MALE = 1
  FEMALE = 2

  @property
  def museum_object(self):
    return self._museum_object

  @museum_object.setter
  def museum_object(self, value):
    try:
      self._museum_object=str(value.catalogue_num)
    except AttributeError:
      self._museum_object=str(value)

  @property
  def min_age(self):
    return self._min_age

  @min_age.setter
  def min_age(self, value):
    self._min_age = float(value)

  @property
  def max_age(self):
    return self._max_age

  @max_age.setter
  def max_age(self, val):
    self._max_age = float(val)

  @property
  def sex(self):
    return self._sex

  @sex.setter
  def sex(self, val):
    unknown = set(["Unknown", "unknown", "NA", "N/A", "na", "n/a",
      self.NA])
    male = set(["Male", "M", "m", "male", self.MALE])
    female = set(["Female", "F", "f", "female", self.FEMALE])
    if val in unknown:
      self._sex = self.NA
    elif val in male:
      self._sex = self.MALE
    elif val in female:
      self._sez = self.FEMALE

  def __init__(self, indiv_id = None, suffix = None, suffix_design =
      None, min_age = None, max_age = None, sex = None, museum_object = None):
    self.indiv_id = indiv_id
    self.suffix_design = suffix_design
    self.suffix = suffix
    self.min_age = min_age
    self.max_age = max_age
    self.sex = sex
    self.museum_object = museum_object

  def copy(self):
    return BioIndividual(self.indiv_id, self.suffix,
        self.suffix_design, self.min_age,
        self.max_age, self.sex, self.museum_object)

  def __eq__(self, other):
    try:
      r = (self.indiv_id == other.indiv_id)
      r = r and (self.suffix_design == other.suffix_design)
      r = r and (self.suffix == other.suffix)
      r = r and (self.min_age == other.min_age)
      r = r and (self.max_age == other.max_age)
      r = r and (self.sex == other.sex)
      r = r and (str(self.museum_object) == str(other.museum_object))
      return r
    except AttributeError:
      return False

  def __ne__(self, other):
    return not (self == other)

  def toXml(self):
    xml = "<bio_individual>"
    xml += "<individual_id>" + escape(str(self.indiv_id)) + "</individual_id>"
    xml += "<suffix>" + escape(str(self.suffix)) + "</suffix>"
    xml += "<suffix_design>" + escape(str(self.suffix_design)) + "</suffix_design>"
    xml += "<min_age>" + escape(str(self.min_age)) + "</min_age>"
    xml += "<max_age>" + escape(str(self.max_age)) + "</max_age>"

    xml += "<sex>"
    if self.sex == self.NA:
      xml += "NA"
    elif self.sex == self.MALE:
      xml += "Male"
    elif self.sex == self.FEMALE:
      xml += "Female"
    xml += "</sex>"

    xml += "<museum_object_id>" + escape(str(self.museum_object)) + "</museum_object_id>"

    xml += "</bio_individual>"

    return xml

############################################################

class HSRDBException(Exception):
  pass

class HSRDB:
  def getMuseumObjectById(self, object_id): abstract()
  def getMuseumObjectByCatalogueNum(self, catalogue_num): abstract()
  def newMuseumObject(self, catalogue_num, object_num, site): abstract()
  def writeMuseumObject(self, museum_object): abstract()
  def getAllMuseumObjects(self): abstract()
  def writeIndividual(self, invidividual): abstract()
  def getIndividualById(self, indiv_id): abstract()
  def getIndividualBySuffixDesign(self, indiv_id): abstract()
  def getAllIndividuals(self): abstract()
  def newIndividual(self, suffix, suffix_design, min_age, max_age, sex, museum_object): abstract()
  def deleteIndividual(self, indiv_id): abstract()
  def deleteMuseumObject(self, object_id): abstract()

class HSRDBSqlAlchemyImpl(HSRDB):
  def __init__(self, db):
    self.db_engine = db

  def getConn(self):
    return self.db_engine.connect()

  def newMuseumObject(self, catalogue_num, object_num, site):
    conn = self.getConn()
    metadata = MetaData(conn)
    mos = Table('Objects', metadata, autoload=True)
    stmt = mos.insert().values(CatalogueID=catalogue_num,
        ObjectNumber=object_num, Site=site)
    result = conn.execute(stmt)
    mo_id = result.lastrowid
    conn.close()
    return MuseumObject(mo_id, catalogue_num, object_num, site)

  def writeMuseumObject(self, museum_object):
    conn = self.getConn()
    metadata = MetaData(conn)
    mos = Table('Objects', metadata, autoload=True)
    stmt = mos.update().where(
        mos.c.ObjectID==museum_object.object_id).values(
            CatalogueNumber=museum_object.catalogue_num,
          ObjectNumber=museum_object.object_num,
          Site=museum_object.site
          )
    result = conn.execute(stmt)
    conn.close()
    if result.rowcount >= 1:
      return True
    return False

  def getMuseumObjectById(self, object_id):
    conn = self.getConn()
    metadata = MetaData(conn)
    mos = Table('Objects', metadata, autoload=True)
    stmt = mos.select().where(mos.c.ObjectID==object_id)
    result = conn.execute(stmt)
    row = result.fetchone()
    conn.close()

    if not row:
      return None

    return MuseumObject(row.ObjectID, row.CatalogueID,
        row.ObjectNumber, row.Site)

  def getMuseumObjectByCatalogueNum(self, catalogue_num):
    conn = self.getConn()
    metadata = MetaData(conn)
    mos = Table('Objects', metadata, autoload=True)
    stmt = mos.select().where(mos.c.CatalogueID==catalogue_num)
    result = conn.execute(stmt)
    row = result.fetchone()
    conn.close()

    if not row:
      return None

    return MuseumObject(row.ObjectID, row.CatalogueID,
        row.ObjectNumber, row.Site)

  def getAllMuseumObjects(self):
    conn = self.getConn()
    metadata = MetaData(conn)
    mos = Table('Objects', metadata, autoload=True)
    stmt = mos.select()
    result = conn.execute(stmt)
    
    mos = []
    for row in result:
      mos.append(MuseumObject(row.ObjectID, row.CatalogueID,
        row.ObjectNumber, row.Site))
    return mos

  def deleteMuseumObject(self, object_id):
    conn = self.getConn()
    metadata = MetaData(conn)
    mos = Table('Objects', metadata, autoload=True)
    stmt = mos.delete().where(mos.c.ObjectID==object_id)
    result = conn.execute(stmt)
    conn.close()

    if result.rowcount >= 1:
      return True
    return False

  def newIndividual(self, suffix, suffix_design, min_age, max_age,
      sex, museum_object):
    conn = self.getConn()
    metadata = MetaData(conn)
    indivs = Table('Individuals', metadata, autoload=True)
    bi = BioIndividual(
        0,
        suffix,
        suffix_design,
        min_age,
        max_age,
        sex,
        museum_object)

    stmt = indivs.insert().values(
        SuffixDesignation=bi.suffix_design,
        Suffix=bi.suffix,
        AgeMax=bi.max_age,
        AgeMin=bi.min_age,
        Sex=bi.sex,
        CatalogueID=bi.museum_object
        )
    result = conn.execute(stmt)
    bi.indiv_id = result.lastrowid
    conn.close()
    return bi

  def getIndividualById(self, indiv_id):
    conn = self.getConn()
    metadata = MetaData(conn)
    indivs = Table('Individuals', metadata, autoload=True)
    stmt = indivs.select().where(indivs.c.IndividualID==indiv_id)
    row = conn.execute(stmt).fetchone()
    conn.close()

    if not row:
      return None
    return BioIndividual(
        row.IndividualID,
        row.Suffix,
        row.SuffixDesignation,
        row.AgeMin,
        row.AgeMax,
        row.Sex,
        row.CatalogueID)

  def getIndividualBySuffixDesign(self, suffix_design):
    conn = self.getConn()
    metadata = MetaData(conn)
    indivs = Table('Individuals', metadata, autoload=True)
    stmt = indivs.select().where(indivs.c.SuffixDesignation==suffix_design)
    row = conn.execute(stmt).fetchone()
    conn.close()

    if not row:
      return None
    return BioIndividual(
        row.IndividualID,
        row.Suffix,
        row.SuffixDesignation,
        row.AgeMin,
        row.AgeMax,
        row.Sex,
        row.CatalogueID)

  def writeIndividual(self, bi):
    conn = self.getConn()
    metadata = MetaData(conn)
    indivs = Table('Individuals', metadata, autoload=True)

    stmt = indivs.update().values(
        SuffixDesignation=bi.suffix_design,
        Suffix=bi.suffix,
        AgeMax=bi.max_age,
        AgeMin=bi.min_age,
        Sex=bi.sex,
        CatalogueID=bi.museum_object
        ).where(indivs.c.IndividualID==bi.indiv_id)
    result = conn.execute(stmt)
    conn.close()

    if result.rowcount >= 1:
      return True
    return False

  def getAllIndividuals(self):
    conn = self.getConn()
    metadata = MetaData(conn)
    indivs = Table('Individuals', metadata, autoload=True)

    stmt = indivs.select()
    result = conn.execute(stmt)
    conn.close()

    indivs = []
    for row in result:
      indivs.append(BioIndividual(
        row.IndividualID,
        row.Suffix,
        row.SuffixDesignation,
        row.AgeMin,
        row.AgeMax,
        row.Sex,
        row.CatalogueID))

    return indivs

  def deleteIndividual(self, indiv_id):
    conn = self.getConn()
    metadata = MetaData(conn)
    indivs = Table('Individuals', metadata, autoload=True)

    stmt = indivs.delete().where(indivs.c.IndividualID==indiv_id)
    result = conn.execute(stmt)
    conn.close()

    if result.rowcount >= 1:
      return True
    return False







