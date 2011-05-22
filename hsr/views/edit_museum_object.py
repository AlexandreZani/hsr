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

from hsr.model import MuseumObject
from urlparse import parse_qs
import json

def edit_museum_object(environ, start_response):
  try:
    data_len = int(environ.get('CONTENT_LENGTH', '0'))
  except ValueError:
    data_len = 0

  params = parse_qs(environ['wsgi.input'].read(data_len))

  catalogue_num = params['catalogue_num'][0]
  object_num = params['object_num'][0]
  site_id = params['site_id'][0]

  engine = environ['hsr']['db_engine']
  session = engine.get_db_session()

  mo = session.query(MuseumObject).filter(
      MuseumObject.catalogue_num==catalogue_num).first()
  if mo:
    mo.object_num = object_num
    mo.site_id = site_id
  else:
    mo = MuseumObject(catalogue_num, object_num, site_id)
    session.add(mo)

  session.commit()

  json_str = json.dumps(mo.to_dict())

  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(json_str))),
      ]

  status = "200 OK"
  start_response(status, response_headers)

  return iter([json_str])
