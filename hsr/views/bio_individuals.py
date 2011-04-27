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

def bio_individuals(environ, start_response):
  params = parse_qs(environ['QUERY_STRING'])
  
  engine = environ['hsr']['db_engine']
  session = engine.get_db_session()

  context = {}

  try:
    sort_column = params['sort_by'][0]
  except KeyError:
    sort_column = 'suffix_designation'

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

  total = session.query(BioIndividual).count()

  if offset + limit + 1 > total:
    context['last'] = True

  bis_q = session.query(BioIndividual).order_by(sort_column).offset(offset).limit(limit)
  bio_individuals = bis_q.all()

  status = "200 OK"
  template = environ['pythia']['jinja_env'].get_template("hsr/bio_individuals.html")
  data = template.render(context, bio_individuals=bio_individuals)
  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(data))),
      ]

  start_response(status, response_headers)

  return iter([data])

