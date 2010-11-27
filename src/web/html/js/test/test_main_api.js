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

var global_obj = new Object();

function MockXhr() {
  this.readyState = 0;
  this.rcvd = "";
  this.responseText = "";
  this.responseXML = null;

  this.onreadystatechange = function() {
  }

  this.changeReadyState = function(new_state) {
    this.readyState = new_state;

    this.onreadystatechange();
  }

  this.respond = function(responseText) {
    this.responseText = responseText;
    this.changeReadyState(4);
  }

  this.send = function(string) {
    this.rcvd = string;
    this.changeReadyState(3);
  }
}

function TestHsrApi() {
  this.test_Login = function() {
    var xhr = new MockXhr();
    var dispatcher = new MessageDispatcher(xhr);
    var api = new HsrApi(dispatcher);

    api.login("armence", "test"); 

    var ping = getRequest("Ping");

    var args = new Array();
    args["username"] = "armence";
    args["password"] = "test";
    
    var credentials = getCredentials("UsernamePassword", args);
    assertEquals("<HSR>" + credentials.toXml() + ping.toXml() + "</HSR>", xhr.rcvd);
  }
}

load_test_file("../message_dispatcher.js");
load_test_file("../credentials.js");
load_test_file("../requests.js");
load_test_file("../main_api.js");

RhinoTestEngine(new TestHsrApi(), "HsrApi");
