#   Copyright Alexandre Zani (alexandre.zani@gmail.com) 
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

from pythia.app import Application
from hsr.controller.checkpoint import Checkpoint
from hsr.model.meta import Base
from hsr import settings
from hsr.controller.auth import AuthController, DuplicateUsername
from sqlalchemy import create_engine
from hsr.views import login

class HSRInit(object):
  def __init__(self, engine):
    self.engine = engine
  
  def __call__(self, environ, start_response):
    environ['hsr'] = {
        'db_engine' : self.engine,
        }
    return environ['pythia']['chain'](environ, start_response)

engine = create_engine(settings.db_url)
Base.metadata.create_all(engine)

auth_controller = AuthController(engine)
try:
  auth_controller.create_user("admin", "admin")
except DuplicateUsername:
  pass

hsr_init = HSRInit(engine)
settings.pre_views.append(hsr_init)

checkpoint = Checkpoint(engine, login, settings.session_expiration)
settings.pre_views.append(checkpoint)

app = Application(settings)
