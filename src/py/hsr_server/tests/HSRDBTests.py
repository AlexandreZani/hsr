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

from hsr_server.hsr_db import HSRDB, MuseumObject, BioIndividual

class HSRDBTestImpl(HSRDB):
  def __init__(self):
    self.museum_objects = []
    self.indivs = []
    self.mo_id = 0
    self.indivs_id = 0

  def newMuseumObject(self, catalogue_num, object_num, site):
    mo = MuseumObject(self.mo_id, catalogue_num, object_num, site)
    self.mo_id += 1
    self.museum_objects.append(mo.copy())
    return mo

  def getMuseumObjectById(self, object_id):
    for mo in self.museum_objects:
      if mo.object_id == object_id:
        return mo.copy()
    return None

  def getMuseumObjectByCatalogueNum(self, catalogue_num):
    for mo in self.museum_objects:
      if mo.catalogue_num == catalogue_num:
        return mo.copy()
    return None

  def getAllMuseumObjects(self):
    mos = []
    for mo in self.museum_objects:
      mos.append(mo.copy())
    return mos

  def writeMuseumObject(self, museum_object):
    for mo in self.museum_objects:
      if mo.object_id == museum_object.object_id:
        self.museum_objects.remove(mo)
        self.museum_objects.append(museum_object.copy())
        return True
    return False 

  def deleteMuseumObject(self, object_id):
    for mo in self.museum_objects:
      if mo.object_id == object_id:
        self.museum_objects.remove(mo)
        return True
    return False

  def newIndividual(self, suffix, suffix_design, min_age, max_age,
      sex, museum_object):
    bi = BioIndividual(
        self.indivs_id,
        suffix,
        suffix_design,
        min_age,
        max_age,
        sex,
        museum_object)
    self.indivs_id += 1
    self.indivs.append(bi.copy())
    return bi

  def getIndividualById(self, indiv_id):
    for bi in self.indivs:
      if bi.indiv_id == indiv_id:
        return bi.copy()
    return None

  def getIndividualBySuffixDesign(self, suffix_design):
    for bi in self.indivs:
      if bi.suffix_design== suffix_design:
        return bi.copy()
    return None

  def writeIndividual(self, indiv):
    for bi in self.indivs:
      if bi.indiv_id == indiv.indiv_id:
        self.indivs.remove(bi)
        self.indivs.append(indiv)
        return True
    return False 

  def getAllIndividuals(self):
    bis = []
    for bi in self.indivs:
      bis.append(bi)
    return bis

  def deleteIndividual(self, indiv_id):
    for bi in self.indivs:
      if bi.indiv_id == indiv_id:
        self.indivs.remove(bi)
        return True
    return False
