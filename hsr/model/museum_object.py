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
from sqlalchemy import Column, String, Integer, ForeignKey

class MuseumObject(Base):
  __tablename__ = 'museum_objects'

  catalogue_num = Column(String, primary_key=True)
  object_num = Column(Integer)
  site = Column(ForeignKey('sites.id'))

  def __init__(self, catalogue_id, object_num, site):
    self.catalogue_num = catalogue_num
    self.object_num = object_num
    self.site = site

  def __repr__(self):
    return "<MuseumObject (%s)>" % (self.catalogue_num,)
