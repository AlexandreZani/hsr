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
from hsr.model.site import Site
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

class MuseumObject(Base):
  __tablename__ = 'museum_objects'

  id = Column(Integer, primary_key=True)
  catalogue_num = Column(String, unique=True)
  object_num = Column(Integer)
  site_id = Column(Integer, ForeignKey('sites.id'))
  site = relationship(Site, backref=backref('museum_objects', order_by=catalogue_num))

  def __init__(self, catalogue_num, object_num, site_id):
    self.catalogue_num = catalogue_num
    self.object_num = object_num
    self.site_id = site_id

  def __repr__(self):
    return "<MuseumObject (%s)>" % (self.catalogue_num,)

  def to_dict(self):
    try:
      site_name = self.site.name
    except AttributeError:
      site_name = ''

    return {
        'id': self.id,
        'catalogue_num' : self.catalogue_num,
        'object_num' : self.object_num,
        'site_id' : self.site_id,
        'site_name' : site_name,
        }
