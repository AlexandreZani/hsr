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

from hsr_server.requests import *
from hsr_auth.credentials import HSRCredentialsException, HSRCredentials, getHSRCredentials
from hsr_server.tests.HSRDBTests import HSRDBTestImpl
from hsr_auth.tests.HSRAuthDBTest import HSRAuthDBTestImpl, HSRAuthDBExcept

class MockCredentials(HSRCredentials):
  def __init__(self, valid=True, user_id=None, response=""):
    self.valid = valid
    self.user_id = user_id
    self.response = response

  def getUserId(self):
    if not self.valid:
      raise HSRCredentialsException("InvalidCredentials")
    return self.user_id

  def getResponse(self):
    return self.response

class TestUnknownRequestType:
  def test_UnknownFactory(self):
    method = "asdasda"
    try:
      request = getHSRRequest(method, {}, None, None)
    except HSRRequestException, (instance):
      assert "Unknown request type " + method == str(instance)
    else:
      assert False

class TestPingRequest:
  def test_PingFactory(self):
    request = getHSRRequest("Ping", {}, None, None)
    assert request.getRequestType() == "Ping"

  def test_PingExec(self):
    request = getHSRRequest("Ping", {}, MockCredentials(True), None)
    assert "<response>Ping</response>" == request.execute()[0]

class TestListMuseumObjects:
  def test_ListMuseumObjectsFactory(self):
    request = getHSRRequest("ListMuseumObjects", {}, None, None)
    assert request.getRequestType() == "ListMuseumObjects"

  def test_ListMuseumObjects(self):
    db = HSRDBTestImpl()
    mo1 = db.newMuseumObject("hello", "hi", "berkeley")
    mo2 = db.newMuseumObject("helslo", "hsfi", "berdkeley")

    request = getHSRRequest("ListMuseumObjects", {}, MockCredentials(True), db)

    response = request.execute()[0]

    assert mo1.toXml() in response
    assert mo2.toXml() in response

  def test_ListMuseumObjectsInvalidCreds(self):
    db = HSRDBTestImpl()
    request = getHSRRequest("ListMuseumObjects", {}, MockCredentials(False), db)

    try:
      request.execute()
    except HSRCredentialsException, (instance):
      assert str(instance) == "InvalidCredentials"
    else:
      assert False

class TestGetMuseumObjectRequest(HSRRequest):
  def test_GetMuseumObjectRequestFactory(self):
    request = getHSRRequest("GetMuseumObject", {}, None, None)
    assert request.getRequestType() == "GetMuseumObject"

  def test_GetMuseumObjectRequest(self):
    db = HSRDBTestImpl()
    mo = db.newMuseumObject("hello", "hi", "berkeley")
    args = {"object_id" : mo.object_id}
    credentials = MockCredentials(True)

    request = getHSRRequest("GetMuseumObject", args, credentials, db)

    response = request.execute()

    assert mo.toXml() in response[0]
    
  def test_GetMuseumObjectRequestBadCreds(self):
    db = HSRDBTestImpl()
    mo = db.newMuseumObject("hello", "hi", "berkeley")
    args = {"object_id" : mo.object_id}
    credentials = MockCredentials(False)

    request = getHSRRequest("GetMuseumObject", args, credentials, db)

    try:
      request.execute()
    except HSRCredentialsException, (instance):
      assert str(instance) == "InvalidCredentials"
    else:
      assert False

  def test_GetMuseumObjectRequestMissingObjectId(self):
    db = HSRDBTestImpl()
    mo = db.newMuseumObject("hello", "hi", "berkeley")
    args = {}
    credentials = MockCredentials(True)

    request = getHSRRequest("GetMuseumObject", args, credentials, db)

    response = request.execute()

    assert response[0] == "<response></response>"

class TestListIndividualsRequest:
  def test_ListIndividualsRequestFactory(self):
    request = getHSRRequest("ListIndividuals", {}, None, None)
    assert request.getRequestType() == "ListIndividuals"

  def test_ListIndividuals(self):
    db = HSRDBTestImpl()
    bi1 = db.newIndividual("a", "a1", 10, 30, "NA", 1)
    bi2 = db.newIndividual("b", "b1", 130, 310, "NA", 1)

    args = {}
    credentials = MockCredentials(True)

    request = getHSRRequest("ListIndividuals", args, credentials, db)

    response = request.execute()

    assert bi1.toXml() in response[0]
    assert bi2.toXml() in response[0]

  def test_ListIndividualsBadCreds(self):
    db = HSRDBTestImpl()
    bi1 = db.newIndividual("a", "a1", 10, 30, "NA", 1)
    bi2 = db.newIndividual("b", "b1", 130, 310, "NA", 1)

    args = {}
    credentials = MockCredentials(False)

    request = getHSRRequest("ListIndividuals", args, credentials, db)

    try:
      response = request.execute()
    except HSRCredentialsException, (instance):
      str(instance) == "InvalidCredentials"
    else:
      assert False

class TestGetIndividualRequest:
  def test_GetIndividualRequestFactory(self):
    request = getHSRRequest("GetBiologicalIndividual", {}, None, None)
    assert request.getRequestType() == "GetBiologicalIndividual"

  def test_GetIndividualRequest(self):
    db = HSRDBTestImpl()
    bi = db.newIndividual("a", "a1", 10, 30, "NA", 1)

    args = {"indiv_id" : bi.indiv_id}
    credentials = MockCredentials(True)

    request = getHSRRequest("GetBiologicalIndividual", args, credentials, db)

    assert request.execute()[0] == "<response>" + bi.toXml() + "</response>"

  def test_GetIndividualRequestNone(self):
    db = HSRDBTestImpl()
    bi = db.newIndividual("a", "a1", 10, 30, "NA", 1)

    args = {"indiv_id" : bi.indiv_id+2}
    credentials = MockCredentials(True)

    request = getHSRRequest("GetBiologicalIndividual", args, credentials, db)

    assert request.execute()[0] == "<response></response>"

  def test_GetIndividualRequestBadCred(self):
    db = HSRDBTestImpl()
    bi = db.newIndividual("a", "a1", 10, 30, "NA", 1)

    args = {"indiv_id" : bi.indiv_id}
    credentials = MockCredentials(False)

    request = getHSRRequest("GetBiologicalIndividual", args, credentials, db)

    try:
      request.execute()[0] == "<response>" + bi.toXml() + "</response>"
    except HSRCredentialsException, (instance):
      assert str(instance) == "InvalidCredentials"
    else:
      assert False

class TestChangePasswordRequest:
  def test_ChangePasswordRequestFactory(self):
    request = getHSRRequest("ChangePassword", {"new_password" : "s"}, None, None)
    assert request.getRequestType() == "ChangePassword"

  def test_ChangePasswordRequest(self):
    db = HSRAuthDBTestImpl()
    username = "loki"
    password = "key"
    user = db.createUser(username, password)
    session = db.newSession(user.user_id)

    args = {"session_id" : session.session_id}
    credentials = getHSRCredentials("SessionId", args, "127.0.0.1", db)

    new_password = "card"
    args = {"new_password" : new_password}
    request = getHSRRequest("ChangePassword", args, credentials, None)

    request.execute()

    user = db.getUserByName(username)
    assert user.CheckPassword(new_password)






