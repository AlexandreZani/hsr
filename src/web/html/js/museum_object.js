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

function onPageLoad(id) {
  api = getHsrApi();
  api.getMuseumObject(id, getMuseumObjectCallback);
}

function getMuseumObjectCallback(response, credentials, error, msg) {
  var table_innerHTML = "";
  node = response.getElementsByTagName("museum_object")[0];

  table_innerHTML += "<tr><td>Catalogue Number</td>"
  table_innerHTML += "<td>" + node.getElementsByTagName("catalogue_number")[0].firstChild.nodeValue + "</td></tr>";
  table_innerHTML += "<tr><td>Object Number</td>"
  table_innerHTML += "<td>" + node.getElementsByTagName("object_number")[0].firstChild.nodeValue + "</td></tr>";
  table_innerHTML += "<tr><td>Site</td>"
  table_innerHTML += "<td>" + node.getElementsByTagName("site")[0].firstChild.nodeValue + "</td></tr>";

  document.getElementById("museum_object").innerHTML = table_innerHTML;
}
