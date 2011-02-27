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
from sqlalchemy import *
import ConfigParser
import os, sys
import getopt
import csv

def usage(name):
  print name, "[-h] [-c config_file] <suffixed_portion.csv> <catalogue_object.csv>"
  print "\t --[h]elp - Prints this message"
  print "\t --[c]onfig-file - HSR configuration file (default) /etc/hsr/hsr.conf"

def main(config_file, bi_file, mo_file):
  config = ConfigParser.RawConfigParser()
  try:
    config_fp = open(config_file)
  except IOError:
    print "Could not open", config_file
    sys.exit(1)

  config.readfp(config_fp)

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
  
  hsr_db_url = config.get("hsr_db", "type") + "://"
  hsr_db_url += config.get("hsr_db", "username")
  hsr_db_url += ":" + config.get("hsr_db", "password")
  hsr_db_url += "@" + config.get("hsr_db", "location")
  hsr_db_url += "/" + config.get("hsr_db", "database")

  hsr_db_engine = create_engine(hsr_db_url)
  metadata = MetaData(hsr_db_engine)
  mos = Table('Objects', metadata, autoload=True)
  mos.delete().execute()
  indivs = Table('Individuals', metadata, autoload=True)
  indivs.delete().execute()


  hsr_db = HSRDBSqlAlchemyImpl(hsr_db_engine)

  for mo in mo_csv:
    hsr_db.newMuseumObject(mo["CatalogID"], mo["ObjectNumber"], "")

  for bi in bi_csv:
    hsr_db.newIndividual(bi["Suffix"], bi["SuffixDesignation"],
        bi["AgeMin"], bi["AgeMax"], bi["Sex"], bi["CatalogID"])

if __name__ == "__main__":
  config_file = "/etc/hsr/hsr.conf"
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config-file="])
  except getopt.GetoptError, err:
    print str(err)
    usage(sys.argv[0])
    sys.exit(2)

  for o, a in opts:
    if o in ("--help", "-h"):
      usage(sys.argv[0])
      sys.exit(0)
    elif o in ("--config-file", "-c"):
      config_file = a
    else:
      print "Unknown option", o
      usage(sys.argv[0])
      sys.exit(2)

  if len(args) != 2:
    print "Missing arguments"
    usage(sys.argv[0])
    sys.exit(2)

  main(config_file, args[0], args[1])






