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

def static(pipe, environ, start_response):
  status = "200 OK"

  path = environ['PATH_INFO']
  if path[-1] != '/':
    path += '/'

  start_idx = path.rfind('/', 0, -1) + 1

  template_name = "hsr/" + path[start_idx:-1] + ".html"

  template = environ['pythia']['jinja_env'].get_template(template_name)
  data = template.render()
  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(data))),
      ]
  start_response(status, response_headers)
  return iter([data])
