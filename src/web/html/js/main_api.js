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

function getHsrApi() {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/api", true);
  var dispatcher = new MessageDispatcher(xhr);
  return new HsrApi(dispatcher);
}

function HsrApi(dispatcher) {
  this.dispatcher = dispatcher;

  this.masterCallback = function(xhr, msg) {
    // Split reply into response, credentials and error if any
    var xml_doc = xhr.responseXML;

    try {
      var response = xml_doc.getElementsByTagName("response")[0];
    } catch(ex) {
      response = null;
    }

    try {
      var credentials = xml_doc.getElementsByTagName("credentials")[0];
      setCookie("credentials", (new XMLSerializer()).serializeToString(credentials), 1);
    } catch(ex) {
      credentials = null;
    }

    try {
      var error = xml_doc.getElementsByTagName("error")[0];
    } catch(ex) {
      error = null;
    }

    if(typeof(msg.outer_callback) == "function")
      msg.outer_callback(response, credentials, error, msg);
  }

  this.login = function(username, password, callback) {
    var args = new Array();
    args["username"] = username;
    args["password"] = password;

    var credentials = getCredentials("UsernamePassword", args);

    var ping = getRequest("Ping");

    var msg_xml = "<HSR>" + credentials.toXml() + ping.toXml() + "</HSR>";

    var msg = new Message(msg_xml, this.masterCallback);
    msg.type = "Login";
    msg.outer_callback = callback;
    this.dispatcher.sendMessage(msg);
  }

  this.changePassword = function(new_password, callback) {
    var args = new Array();
    args["new_password"] = new_password;

    var request = getRequest("ChangePassword", args);

    var msg_xml = "<HSR>" + unescape(getCookie("credentials")) + request.toXml() + "</HSR>";

    var msg = new Message(msg_xml, this.masterCallback);
    msg.type = "ChangePassword";
    msg.outer_callback = callback;
    this.dispatcher.sendMessage(msg);
  }
}
