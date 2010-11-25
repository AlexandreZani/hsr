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

/*
 * Requests
*/

function getRequest(method, args) {
  var request_types = new Array();
  request_types["Ping"] = PingRequest;
  request_types["ChangePassword"] = ChangePasswordRequest;

  return new request_types[method](args);
}

function ChangePasswordRequest(args) {
  this.new_password = args["new_password"];

  this.getRequestType = function() {
    return "ChangePassword";
  }

  this.toXml = function() {
    return "<request><type>ChangePassword</type><args><new_password>" + this.new_password + "</new_password></args></request>";
  }
}

function PingRequest(args) {

  this.getRequestType = function() {
    return "Ping";
  }

  this.toXml = function() {
    return "<request><type>Ping</type></request>";
  }
}

/*
 *
*/

