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

function onLogoutClick() {
  setCookie("credentials", "", -1);
  document.getElementById("body_frame").src = "/static/login.html";
}

function onAccountMgmtClick() {
  document.getElementById("body_frame").src = "/static/account_management_menu.html";
}

function onMainMenuClick() {
  document.getElementById("body_frame").src = "/static/main_menu.html";
}

function onBodyFrameLoad() {
  var titles = new Array();
  titles["login.html"] = "Login";
  titles["change_password.html"] = "Change Password";
  titles["account_management_menu.html"] = "Account Management";
  titles["main_menu.html"] = "Main Menu";

  var static = "static/";
  var path = document.getElementById("body_frame").src;
  var start = path.indexOf(static);
  start += static.length;

  path = path.substring(start, path.length);

  document.getElementById("current_title").innerHTML = "Human Skeletal Remains Database: " + titles[path];
}
