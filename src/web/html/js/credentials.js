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
 * Credentials
*/

function getCredentials(method, args) {
  var credential_types = new Array();
  credential_types["UsernamePassword"] = UsernamePasswordCredentials;

  return new credential_types[method](args);
}

function UsernamePasswordCredentials(args) {
  this.username = args.username;
  this.password = args.password;

  this.getCredentialsType = function() {
    return "UsernamePassword";
  }

  this.toXml = function() {
    var xml = "<credentials>";
    xml += "<type>UsernamePassword</type>";
    xml += "<args>";
    xml += "<username>" + this.username + "</username>";
    xml += "<password>" + this.password + "</password>";
    xml += "</args>";
    xml += "</credentials>";

    return xml;
  }
}

