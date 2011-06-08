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

import logging

def logout(pipe, environ, start_response):
  session = environ['hsr']['session']
  logging.info("%s logged out from %s : %s" %
      (environ.get('REMOTE_ADDR', "Unknown"),
      session.user.username,
      session.session_id))
  environ['hsr']['auth_controller'].delete_session(session.session_id)
  status = "200 OK"
  template = environ['pythia']['jinja_env'].get_template("hsr/logout.html")
  data = template.render()
  response_headers = [
      ('Content-type','text/html'),
      ('Content-Length', str(len(data))),
      ('Set-Cookie', 'sid='),
      ]
  start_response(status, response_headers)
  return iter([data])
