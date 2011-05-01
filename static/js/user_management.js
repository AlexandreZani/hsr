/*
 * Copyright 2011 Alexandre Zani (Alexandre.Zani@gmail.com)
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

function editUser(username, permissions) {
  var username_el = document.getElementById("username");
  var permissions_el = document.getElementById("permissions");

  username_el.value = username;
  username_el.setAttribute("disabled", "true");
  permissions_el.value = permissions;
  document.getElementById("edit_user_legend").innerHTML = "Edit User " + username;
  document.getElementById("delete_user_btn").setAttribute('style', '');
}

function cancelEditUser() {
  document.getElementById("username").value = "";
  document.getElementById("username").removeAttribute("disabled");
  document.getElementById("new_password").value = "";
  document.getElementById("repeat_password").value = "";
  document.getElementById("permissions").value = 128;
  document.getElementById("response").innerHTML = "";
  document.getElementById("edit_user_legend").innerHTML = "New User";
  document.getElementById("delete_user_btn").setAttribute('style', 'display:none;');
}

function passwordsMatch() {
  var new_password = document.getElementById("new_password").value;
  var repeat_password = document.getElementById("repeat_password").value;
  var no_match = document.getElementById("no_match");
  var button = document.getElementById("save_user_btn");

  if (new_password == repeat_password) {
    no_match.setAttribute("style", "visibility:hidden;");
    button.removeAttribute("disabled");
  } else {
    no_match.setAttribute("style", "");
    button.setAttribute("disabled", true);
  }
}

function saveUser() {
  var new_password = escape(document.getElementById("new_password").value);
  var username = document.getElementById("username").value;
  var permissions = document.getElementById("permissions").value;

  if (username == "") {
    document.getElementById("response").innerHTML = "No username specified!";
    return;
  }

  var current_user = getCurrentUser();
  if (current_user.username == username && permissions > 0) {
    if (! confirm("You are about to revoke your own admin priviledges.")) {
      return;
    }
  }

  request = getXMLHttpRequest();
  request.onreadystatechange = saveUserCallback;

  var request_str = "username=" + username + "&permissions=" + permissions;

  if (new_password != "") {
    request_str += "&password=" + escape(new_password);
  }

  request.open("POST", "/edit_user", true);
  request.send(request_str);
}

function saveUserCallback() {
  if (this.readyState == 4) {
    var response_element = document.getElementById("response");

    if (this.status == 200) {
      response_element.innerHTML = "Success";
      response_element.setAttribute("class", "");
      var user = JSON.parse(this.responseText);
      updateTableWithUser(user);
    } else {
      response_element.innerHTML = this.statusText;
      response_element.setAttribute("class", "error");
    }
  }
}

function updateTableWithUser(user) {
  var row = document.getElementById("user_" + user.username);

  if (row == null) {
    var user_table_el = document.getElementById("user_table");
    var idx = user_table_el.rows.length;

    row = user_table_el.insertRow(idx);

    row.setAttribute("onMouseOver", "this.setAttribute('style', 'background-color:#CAF3F2');");
    row.setAttribute("onMouseOut", "this.setAttribute('style', '');");
    if (idx % 2 == 0) {
      row.setAttribute("class", "even_row");
    } else {
      row.setAttribute("class", "odd_row");
    }
  }
  
  row.setAttribute("id", "user_" + user.username);
  row.setAttribute("onClick", "editUser('" + user.username + "','" + user.permissions + "')");
  row.innerHTML = "<td>" + user.username + "</td><td>" + user.permissions_str + "</td>";
}

function deleteUser() {
}
