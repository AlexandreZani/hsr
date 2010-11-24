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

from hsr_server.handler import *
from hsr_server.tests.HSRDBTests import HSRDBTestImpl
from hsr_auth.tests.HSRAuthDBTest import HSRAuthDBTestImpl
from xml.dom.minidom import parseString

class TestMethodParser:
  def test_ParseMethod(self):
    handler = HsrHandler(HSRDBTestImpl(), HSRAuthDBTestImpl())
    method = "TestMethod"
    args = {"key1" : "val1", "key2" : "val2", "key3" : "val3"}

    xml = "<top><type>"+ method +"</type><args>"
    for arg in args:
      xml += "<" + arg + ">" + args[arg] + "</" + arg + ">"
    xml += "</args></top>"

    xml_node = parseString(xml).firstChild

    (m, a) = handler.parseMethod(xml_node)

    assert m == method

    for arg in args:
      assert args[arg] == a[arg]

  def test_NoType(self):
    handler = HsrHandler(HSRDBTestImpl(), HSRAuthDBTestImpl())
    method = "TestMethod"
    args = {"key1" : "val1", "key2" : "val2", "key3" : "val3"}

    xml = "<top><args>"
    for arg in args:
      xml += "<" + arg + ">" + args[arg] + "</" + arg + ">"
    xml += "</args></top>"

    xml_node = parseString(xml).firstChild

    try:
      (m, a) = handler.parseMethod(xml_node)
    except HSRException, (instance):
      assert "MalformedRequest" == str(instance)
    else:
      assert False

  def test_NoArgs(self):
    handler = HsrHandler(HSRDBTestImpl(), HSRAuthDBTestImpl())
    method = "TestMethod"
    args = {"key1" : "val1", "key2" : "val2", "key3" : "val3"}

    xml = "<top><type>"+ method +"</type></top>"

    xml_node = parseString(xml).firstChild

    (m, a) = handler.parseMethod(xml_node)
    assert a == {}

class TestRequestParser:
  def test_ParseRequest(self):
    handler = HsrHandler(HSRDBTestImpl(), HSRAuthDBTestImpl())
    xml = "<HSR><request><type>Ping</type></request></HSR>"
    request = handler.parseRequest(xml)

    assert "Ping" == request.getRequestType()




