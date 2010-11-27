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

function getAllMuseumObjects() {
  var api = getHsrApi();
  api.getMuseumObjects(getMuseumObjectsCallback);
}

function getMuseumObjectsCallback(response, credentials, error, msg) {
  var table = document.getElementById("museum_objects_table");
  table_innerHTML = "<tr><th>Object Number</th><th>Catalogue Number</th><th>Site</th></tr>";
  for(var i = 0; i < response.childNodes.length; i++) {
    var node = response.childNodes.item(i);

    var row = "<tr>";
    row += "<td>" + node.getElementsByTagName("object_number")[0].firstChild.nodeValue + "</td>";
    row += "<td>" + node.getElementsByTagName("catalogue_number")[0].firstChild.nodeValue + "</td>";
    row += "<td>" + node.getElementsByTagName("site")[0].firstChild.nodeValue + "</td>";
    row += "</tr>";
    table_innerHTML += row;
  }
  table.innerHTML = table_innerHTML;
}
