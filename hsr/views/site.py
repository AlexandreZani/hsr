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

def site(pipe, environ, start_response):
  engine = environ['hsr']['db_engine']
  session = engine.get_db_session()

  try:
    site_id = environ['pythia']['url_params']['id']
    site = session.query(Site).filter_by(id=site_id).first()
    new = False
  except KeyError:
    site = Site(0, "")
    new = True

  status = "200 OK"
  template = environ['pythia']['jinja_env'].get_template("hsr/site.html")
  data = template.render(site=site, new_site=new)
  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(data))),
      ]

  start_response(status, response_headers)

  return iter([data])
