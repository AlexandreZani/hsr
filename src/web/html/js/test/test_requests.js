/*
 * Copyright 2010 Alexandre Zani (Alexandre.Zani@gmail.com)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

function TestPingRequest() {
  this.test_Factory = function() {
    request = getRequest("Ping", null);
    assert(request.getRequestType() == "Ping");
  }

  this.test_Xml = function() {
    request = getRequest("Ping", null);
    assert(request.toXml() == "<request><type>Ping</type></request>");
  }
}

load_test_file("../requests.js");

RhinoTestEngine(new TestPingRequest(), "PingRequest");
