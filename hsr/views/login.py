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

from hsr.controller.auth import NoSuchUser, WrongPassword, SessionExpired

def login(pipe, environ, start_response):
  status = "401 Unauthorized"
  template = environ['pythia']['jinja_env'].get_template("hsr/login.html")

  ex = type(environ['hsr']['auth_except'])

  if ex is SessionExpired:
    reason = "Session Expired"
  elif ex is WrongPassword or ex is NoSuchUser:
    reason = "Wrong Username Password Combination"
  else:
    reason = ""

  data = template.render(reason=reason)
  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(data))),
      ]
  start_response(status, response_headers)
  return iter([data])
