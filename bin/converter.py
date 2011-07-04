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

import sys
import getopt
import csv
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from hsr.model.meta import Base
from hsr import settings
from hsr import model

def usage(name):
  print name, "[-h] <suffixed_portion.csv> <catalogue_object.csv> <sites.csv>"
  print "\t --[h]elp - Prints this message"

MALE_STR = set(["m", "male"])
FEMALE_STR = set(["f", "female"])
lower_letters_pattern = re.compile('[^a-z]+')

def main(bi_file, mo_file, sites_file):
  try:
    bi_fp = open(bi_file, "rb")
    bi_csv = csv.DictReader(bi_fp)
  except IOError:
    print "Could not open", bi_file
    sys.exit(1)

  try:
    mo_fp = open(mo_file, "rb")
    mo_csv = csv.DictReader(mo_fp)
  except IOError:
    print "Could not open", mo_file
    sys.exit(1)

  try:
    sites_fp = open(sites_file)
    sites_csv = csv.DictReader(sites_fp)
  except IOError:
    print "Could not open", sites_file
    sys.exit(1)
  
  engine = create_engine(settings.db_url)
  Base.metadata.create_all(engine)
  Session = sessionmaker(bind=engine)
  session = Session()

  duplicates = 0
  for row in sites_csv:
    site = model.Site(
        int(row['SiteID']),
        unicode(row['SiteName'])
        )
    session.add(site)
    try:
      session.commit()
    except IntegrityError:
      session.rollback()
      duplicates += 1
  print "Found %s duplicate sites" % duplicates

  duplicates = 0
  for row in mo_csv:
    try:
      site_id = int(row['Site'])
    except ValueError:
      site_id = -1
    mo = model.MuseumObject(
        unicode(row['CatalogueID']),
        int(row['ObjectNumber']),
        site_id
        )
    session.add(mo)
    try:
      session.commit()
    except IntegrityError:
      session.rollback()
      duplicates += 1
  print "Found %s duplicate museum objects" % duplicates

  duplicates = 0
  for row in bi_csv:
    try:
      age_max = float(row['AgeMax'])
    except ValueError:
      age_max = -1

    try:
      age_min = float(row['AgeMin'])
    except ValueError:
      age_min = -1

    sex = model.Sex.NA
    try:
      sex_str = lower_letters_pattern.sub('', str(row['Sex']).lower())
      if sex_str in MALE_STR:
        sex = model.Sex.MALE
      elif sex_str in FEMALE_STR:
        sex = model.Sex.FEMALE
    except ValueError:
      pass
    print sex_str

    bi = model.BioIndividual(
        unicode(row['SuffixDesignation']),
        unicode(row['Suffix']),
        sex,
        unicode(row['Age']),
        age_max,
        age_min,
        unicode(row['CatalogueID'])
        )
    session.add(bi)
    try:
      session.commit()
    except IntegrityError:
      duplicates += 1
      session.rollback()
  print "Found %s duplicate biological individuals" % duplicates

if __name__ == "__main__":
  try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
  except getopt.GetoptError, err:
    print str(err)
    usage(sys.argv[0])
    sys.exit(2)

  for o, a in opts:
    if o in ("--help", "-h"):
      usage(sys.argv[0])
      sys.exit(0)
    else:
      print "Unknown option", o
      usage(sys.argv[0])
      sys.exit(2)

  if len(args) != 3:
    print "Missing arguments"
    usage(sys.argv[0])
    sys.exit(2)

  main(args[0], args[1], args[2])






