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

function TestUsernamePasswordCredentials() {
  this.test_Factory = function() {
    var credentials = getCredentials("UsernamePassword", new Array());
    assert(credentials.getCredentialsType() == "UsernamePassword");
  }

  this.test_Values = function() {
    var args = new Array();
    args["username"] = "armence";
    args["password"] = "test";
    var credentials = getCredentials("UsernamePassword", args);

    assert(credentials.username == "armence");
    assert(credentials.password == "test");
  }

  this.test_Xml = function() {
    var args = new Array();
    args["username"] = "armence";
    args["password"] = "test";
    var credentials = getCredentials("UsernamePassword", args);

    assert(credentials.toXml() == "<credentials><type>UsernamePassword</type><args><username>armence</username><password>test</password></args></credentials>")
  }
}

load_test_file("../credentials.js");

RhinoTestEngine(new TestUsernamePasswordCredentials(), "UsernamePasswordCredentials");
