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

  suffix_designation = Column(String, primary_key=True)
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
    return Sex.STRINGS[self.sex]

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
