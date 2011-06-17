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

from hsr.model import Site 
from urlparse import parse_qs
import json

def edit_site(pipe, environ, start_response):
  try:
    data_len = int(environ.get('CONTENT_LENGTH', '0'))
  except ValueError:
    data_len = 0

  params = parse_qs(environ['wsgi.input'].read(data_len))

  site_id = int(params["site_id"][0])
  site_name = params["site_name"][0]

  engine = environ['hsr']['db_engine']
  session = engine.get_db_session()

  site = session.query(Site).filter(Site.id==site_id).first()
  if site:
    site.name = site_name
  else:
    site = Site(site_id, site_name)
    session.add(site)

  session.commit()

  json_str = json.dumps(site.to_dict())

  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(json_str))),
      ]

  status = "200 OK"
  start_response(status, response_headers)

  return iter([json_str])

