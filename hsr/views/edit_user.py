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

from hsr.model import User
from urlparse import parse_qs
import json

def edit_user(environ, start_response):
  auth_controller = environ['hsr']['auth_controller']

  try:
    data_len = int(environ.get('CONTENT_LENGTH', '0'))
  except ValueError:
    data_len = 0

  params_str = environ['wsgi.input'].read(data_len)
  params = parse_qs(params_str)

  username = params['username'][0]
  permissions = int(params['permissions'][0])

  try:
    password = params['password'][0]
  except KeyError:
    password = None

  user = auth_controller.create_user(username, password, permissions)

  user_dict = {
      'username' : user.username,
      'permissions' : user.permissions,
      'permissions_str' : user.permissions_str
      }

  user_json = json.dumps(user_dict)

  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(user_json))),
      ]

  status = "200 OK"
  start_response(status, response_headers)

  return iter([user_json])
