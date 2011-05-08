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

from cgi import parse_qs, escape
from hsr.controller.secure_auth import InsufficientPermissions

def change_password(environ, start_response):
  data_len = int(environ.get('CONTENT_LENGTH', '0'))

  data = environ['wsgi.input'].read(data_len)
  data_dict = parse_qs(data)

  status = "200 OK"

  try:
    environ['hsr']['auth_controller'].change_own_password(data_dict['old_password'][0],
        data_dict['new_password'][0])
  except InsufficientPermissions:
    status = "401 Incorrect Old Password"

  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', "0"),
      ]
  start_response(status, response_headers)
  return iter([""])
