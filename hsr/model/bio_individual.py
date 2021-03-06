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
from hsr.model import MuseumObject
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

class Sex(object):
  MALE = 0
  FEMALE = 1
  NA = 2

  STRINGS = ["Male", "Female", "N/A"]

class BioIndividual(Base):
  __tablename__ = 'bio_individuals'

  id = Column(Integer, primary_key=True)
  suffix_designation = Column(String, unique=True)
  suffix = Column(String)
  sex = Column(Integer)
  age = Column(String)
  age_max = Column(Float)
  age_min = Column(Float)
  catalogue_num = Column(String, ForeignKey('museum_objects.catalogue_num'))
  museum_object = relationship(MuseumObject, backref=backref('bio_individuals',
    order_by=suffix_designation))

  @property
  def sex_str(self):
    try:
      return Sex.STRINGS[self.sex]
    except IndexError:
      return Sex.NA

  def __init__(self, suffix_designation, suffix, sex, age, age_max, age_min,
      catalogue_num):
    self.suffix_designation = suffix_designation
    self.suffix = suffix
    self.sex = sex
    self.age = age
    self.age_min = age_min
    self.age_max = age_max
    self.catalogue_num = catalogue_num

  def __repr__(self):
    return "<BioIndividual (%s)>" % (self.suffix_designation)

  def to_dict(self):
    try:
      museum_object_id = self.museum_object.id
    except AttributeError:
      museum_object_id = ''
    return {
        'suffix_designation' : self.suffix_designation,
        'suffix' : self.suffix,
        'sex' : self.sex,
        'sex_str' : self.sex_str,
        'age' : self.age,
        'age_min' : self.age_min,
        'age_max' : self.age_max,
        'catalogue_num' : self.catalogue_num,
        'museum_object_id' : museum_object_id,
        }
