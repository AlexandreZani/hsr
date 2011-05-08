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

from functools import partial

class InsufficientPermissions(Exception): pass

class secure(object):
  def __init__(self, min_permissions):
    self.min_permissions = min_permissions

  def __call__(self, func):
    self.func = func
    self.__name__ = func.__name__
    return self

  def _check_permissions(self, user):
    if self.min_permissions < user.permissions:
      raise InsufficientPermissions()
    return True

  def __get__(self, instance, owner):
    def secured(*args, **kwargs):
      self._check_permissions(instance._user)
      return self.func(*args, **kwargs)

    return partial(secured, instance)
