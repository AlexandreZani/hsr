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

from cgi import parse_qs

def delete_user(pipe, environ, start_response):
  auth_controller = environ['hsr']['auth_controller']

  try:
    data_len = int(environ.get('CONTENT_LENGTH', '0'))
  except ValueError:
    data_len = 0

  params_str = environ['wsgi.input'].read(data_len)
  params = parse_qs(params_str)

  username = params['username'][0]

  auth_controller.delete_user(username)

  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(username))),
      ]

  status = "200 OK"
  start_response(status, response_headers)

  return iter([username])
