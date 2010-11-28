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

function onPageLoad(suffix_design) {
  api = getHsrApi();
  api.getBioIndividual(suffix_design, getBioIndividualCallback);
}

function getBioIndividualCallback(response, credentials, error, msg) {
  var table_innerHTML = "";
  var node = response.getElementsByTagName("bio_individual")[0];

  table_innerHTML += "<tr><td>Suffix Designation</td>";
  table_innerHTML += "<td>" + node.getElementsByTagName("suffix_design")[0].firstChild.nodeValue + "</td></tr>";

  table_innerHTML += "<tr><td>Sex</td>";
  table_innerHTML += "<td>" + node.getElementsByTagName("sex")[0].firstChild.nodeValue + "</td></tr>";

  table_innerHTML += "<tr><td>Age</td>";
  table_innerHTML += "<td>" + node.getElementsByTagName("min_age")[0].firstChild.nodeValue;
  table_innerHTML += " to " + node.getElementsByTagName("max_age")[0].firstChild.nodeValue + "</td></tr>";

  document.getElementById("bio_individual").innerHTML = table_innerHTML;
}
