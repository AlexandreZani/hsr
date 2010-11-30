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
    var xml_doc = xhr.responseXML;
    if(xml_doc == null || xml_doc == undefined) {
      var parser = new DOMParser();
      xml_doc = parser.parseFromString(xhr.responseText, "text/xml");
    }

    var response = null;
    try {
      response = xml_doc.getElementsByTagName("response")[0];
    } catch(ex) {}

    var credentials = null;
    try {
      credentials = xml_doc.getElementsByTagName("credentials")[0];
      xml_creds = (new XMLSerializer()).serializeToString(credentials);

      if(xml_creds != "")
        setCookie("credentials", xml_creds, 1);
    } catch(ex) {}

    var error = null;
    try {
      error = xml_doc.getElementsByTagName("error")[0];
    } catch(ex) {}

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

  this.getMuseumObjects = function(callback) {
    var request = getRequest("ListMuseumObjects", new Array());
    var msg_xml = "<HSR>" + unescape(getCookie("credentials")) + request.toXml() + "</HSR>";
    var msg = new Message(msg_xml, this.masterCallback);
    msg.type = "ListMuseumObjects";
    msg.outer_callback = callback;
    this.dispatcher.sendMessage(msg);
  }

  this.getBioIndividuals = function(callback) {
    var request = getRequest("ListIndividuals", new Array());
    var msg_xml = "<HSR>" + unescape(getCookie("credentials")) + request.toXml() + "</HSR>";
    var msg = new Message(msg_xml, this.masterCallback);
    msg.type = "ListIndividuals";
    msg.outer_callback = callback;
    this.dispatcher.sendMessage(msg);
  }

  this.getMuseumObject = function(id, callback) {
    var args = new Array();
    args["catalogue_num"] = id;
    var request = getRequest("GetMuseumObject", args);
    var msg_xml = "<HSR>" + unescape(getCookie("credentials")) + request.toXml() + "</HSR>";
    var msg = new Message(msg_xml, this.masterCallback);
    msg.type = "GetMuseumObject";
    msg.outer_callback = callback;
    this.dispatcher.sendMessage(msg);
  }

  this.getBioIndividual = function(indiv_id, callback) {
    var args = new Array();
    args["individual_id"] = indiv_id;
    var request = getRequest("GetBiologicalIndividual", args);
    var msg_xml = "<HSR>" + unescape(getCookie("credentials")) + request.toXml() + "</HSR>";
    var msg = new Message(msg_xml, this.masterCallback);
    msg.type = "GetBiologicalIndividual";
    msg.outer_callback = callback;
    this.dispatcher.sendMessage(msg);
  }
}
