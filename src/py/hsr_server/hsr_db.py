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


def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass')

class MuseumObject:
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
    xml += "<object_number>" + self.object_num + "</ObjectNumber>"
    xml += "<catalogue_number>" + self.object_num + "</catalogue_number>"
    xml += "<site>" + self.object_num + "</site>"
    xml += "</museum_object>"
    return xml

class BioIndividual:
  NA = 0
  MALE = 1
  FEMALE = 2

  @property
  def museum_object(self):
    return self._museum_object

  @museum_object.setter
  def museum_object(self, value):
    self._museum_object = str(value)

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
    self._age = float(max_age)

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
    try:
      self.museum_object = str(museum_object.catalogue_num)
    except AttributeError:
      self.museum_object = str(museum_object)

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
    xml += "<suffix>" + str(self.suffix) + "</suffix>"
    xml += "<suffix_design>" + str(self.suffix_design) + "</suffix_design>"
    xml += "<min_age>" + str(self.min_age) + "</min_age>"
    xml += "<max_age>" + str(self.max_age) + "</max_age>"

    xml += "<sex>"
    if self.sex == self.NA:
      xml += "NA"
    elif self.sex == self.MALE:
      xml += "Male"
    elif self.sex == self.FEMALE:
      xml += "Female"
    xml += "</sex>"

    xml += "<museum_object_id>" + str(self.museum_object) + "</museum_object_id>"

    xml += "</bio_individual>"

    return xml

############################################################

class HSRDBException(Exception):
  pass

class HSRDB:
  def getMuseumObjectById(self, object_id): abstract()
  def newMuseumObject(self, catalogue_num, object_num, site): abstract()
  def writeMuseumObject(self, museum_object): abstract()
  def getAllMuseumObjects(self): abstract()
  def writeIndividual(self, invidividual): abstract()
  def getIndividualById(self, indiv_id): abstract()
  def getAllIndividuals(self): abstract()
  def newIndividual(self, suffix, suffix_design, min_age, max_age, sex): abstract()
