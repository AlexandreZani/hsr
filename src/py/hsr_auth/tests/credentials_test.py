#!/usr/bin/python

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

from hsr_auth.credentials import getHSRCredentials

class TestNoneCredentials:
  def test_CreateNoneCredentials(self):
    credentials = getHSRCredentials("None", {}, "127.0.0.1")
    assert credentials.getCredentialsType() == "None"

  def test_GetUserIdNoneCredentials(self):
    credentials = getHSRCredentials("None", {}, "127.0.0.1")
    try:
      credentials.getUserId()
    except Exception, (ex):
      assert str(ex) == "InvalidCredentials"
    else:
      assert False

