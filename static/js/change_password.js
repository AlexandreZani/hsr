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

function passwordsMatch() {
  var new_password = document.getElementById("new_password").value;
  var repeat_password = document.getElementById("repeat_password").value;
  var no_match = document.getElementById("no_match");
  var button = document.getElementById("change_password_btn");

  if (new_password == repeat_password) {
    no_match.setAttribute("style", "visibility:hidden;");
    button.removeAttribute("disabled");
  } else {
    no_match.setAttribute("style", "");
    button.setAttribute("disabled", true);
  }
}

function changePassword() {
  var old_password = escape(document.getElementById("old_password").value);
  var new_password = escape(document.getElementById("new_password").value);
  var repeat_password = document.getElementById("repeat_password").value;

  request = getXMLHttpRequest();

  request.onreadystatechange = changePasswordCallback;

  var request_str = "old_password=" + old_password + "&new_password=" + new_password;
  request.open("POST", "/change_password", true);
  request.send(request_str);
}

function changePasswordCallback() {
  if (this.readyState == 4) {
    var response_element = document.getElementById("response");

    switch (this.status) {
      case 200:
        response_element.innerHTML = "Password Changed";
        break;
      default:
        response_element.innerHTML = this.statusText;
    }
  }
}
