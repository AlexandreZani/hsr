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

function onChangePasswordButtonClick() {
  var new_password = document.getElementById("new_password").value;
  var confirm_password = document.getElementById("confirm_password").value;

  if(new_password != confirm_password) {
    document.getElementById("no_match").setAttribute("style", "");
    return;
  }
  document.getElementById("no_match").setAttribute("style", "visibility:hidden;");

  api = getHsrApi();
  api.changePassword(new_password, changePasswordCallback);
}

function changePasswordCallback(response, credentials, error, msg) {
}
