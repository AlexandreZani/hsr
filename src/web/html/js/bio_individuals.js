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

function getNextPage(jump) {
  var limit = 15;
  if(getNextPage.page == undefined) {
    getNextPage.page = -1;
  }
  if(jump == undefined) {
    getNextPage.page += 1;
  } else {
    getNextPage.page += jump;
  }

  if(getNextPage.page < 0) {
    getNextPage.page = 0;
  }

  document.getElementById("page_num").innerHTML = "Page Number: " + getNextPage.page;

  var api = getHsrApi();
  api.getBioIndividuals(limit, getNextPage.page*limit, getIndividualsCallback)
}

function getIndividualsCallback(response, credentials, error, msg) {
  var table = document.getElementById("bio_individuals_table");

  var class = "odd_row";
  table_innerHTML = "<tr><th>Suffix Designation</th><th>Sex</th><th>Minimum Age</th><th>Maximum Age</th></tr>";
  for(var i = 0; i < response.childNodes.length; i++) {
    var node = response.childNodes.item(i);
    if(class == "odd_row")
      class = "";
    else
      class = "odd_row";
    var oid = node.getElementsByTagName("individual_id")[0].firstChild.nodeValue;

    var row = "<tr id='row" + oid + "' class='" + class + "' onclick='onRowClick(\"" + oid  + "\")' onmouseover='onRowMouseOver(\"" + oid + "\")' onmouseout='onRowMouseOut(\""+ oid +"\")'>";
    row += "<td>" + node.getElementsByTagName("suffix_design")[0].firstChild.nodeValue + "</td>";
    row += "<td>" + node.getElementsByTagName("sex")[0].firstChild.nodeValue + "</td>";
    row += "<td>" + node.getElementsByTagName("min_age")[0].firstChild.nodeValue + "</td>";
    row += "<td>" + node.getElementsByTagName("max_age")[0].firstChild.nodeValue + "</td>";
    row += "</tr>";
    table_innerHTML += row;
  }
  table.innerHTML = table_innerHTML;
}

function onRowMouseOver(oid) {
  document.getElementById("row"+oid).setAttribute("style", "background-color:#CAF3F2");
}

function onRowMouseOut(oid) {
  document.getElementById("row"+oid).setAttribute("style", "");
}

function onRowClick(id) {
  window.location = "/jinja/bio_individual.html?suffix_design=" + id;
}
