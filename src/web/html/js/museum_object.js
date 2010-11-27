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
