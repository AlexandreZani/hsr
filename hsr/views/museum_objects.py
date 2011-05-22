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

def museum_objects(pipe, environ, start_response):
  params = parse_qs(environ['QUERY_STRING'])
  
  engine = environ['hsr']['db_engine']
  session = engine.get_db_session()

  context = {}

  try:
    sort_column = params['sort_by'][0]
  except KeyError:
    sort_column = 'catalogue_num'

  context['sort_by'] = sort_column

  try:
    limit = int(params['page_size'][0])
  except KeyError:
    limit = 20

  context['page_size'] = limit

  try:
    offset = int(params['page'][0]) * limit
  except KeyError:
    offset = 0

  context['page'] = offset / limit

  total = session.query(MuseumObject).count()

  if offset + limit + 1 > total:
    context['last'] = True

  mos_q = session.query(MuseumObject).order_by(sort_column).offset(offset).limit(limit)
  museum_objects = mos_q.all()

  status = "200 OK"
  template = environ['pythia']['jinja_env'].get_template("hsr/museum_objects.html")
  data = template.render(context, museum_objects=museum_objects)
  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(data))),
      ]

  start_response(status, response_headers)

  return iter([data])
