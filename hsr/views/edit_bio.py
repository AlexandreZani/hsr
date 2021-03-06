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

from hsr.model import BioIndividual
from urlparse import parse_qs
import json

def edit_bio(pipe, environ, start_response):
  try:
    data_len = int(environ.get('CONTENT_LENGTH', '0'))
  except ValueError:
    data_len = 0

  params = parse_qs(environ['wsgi.input'].read(data_len))

  suffix_design = params["suffix_designation"][0]
  suffix = params["suffix"][0]
  age = params["age"][0]
  age_min = params["age_min"][0]
  age_max = params["age_max"][0]
  sex = int(params["sex"][0])
  catalogue_num = params["catalogue_number"][0]

  engine = environ['hsr']['db_engine']
  session = engine.get_db_session()

  bio_indiv = session.query(BioIndividual).filter(BioIndividual.suffix_designation==suffix_design).first()
  if bio_indiv:
    bio_indiv.age = age
    bio_indiv.age_max = age_max
    bio_indiv.age_min = age_min
    bio_indiv.suffix = suffix
    bio_indiv.sex = sex
    bio_indiv.catalogue_num = catalogue_num
  else:
    bio_indiv = BioIndividual(suffix_design, suffix, sex, age, age_max,
        age_min, catalogue_num)
    session.add(bio_indiv)

  session.commit()

  json_str = json.dumps(bio_indiv.to_dict())

  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(json_str))),
      ]

  status = "200 OK"
  start_response(status, response_headers)

  return iter([json_str])
