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

function startNew() {
  startEdit();
  var enabled = ['site_id_field_td'];
  var disabled = ['site_id_static_td'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
  document.getElementById('cancel_btn').setAttribute(
      'onClick', 'window.location="/sites/"');
}

function startEdit() {
  var enabled = ['site_name_field_td', 'cancel_btn', 'save_btn'];
  var disabled = ['site_name_static_td', 'delete_btn', 'edit_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
  document.getElementById('site_id_field').value = window.cur_site.id;
  document.getElementById('site_name_field').value = window.cur_site.name;
}

function cancelEdit() {
  var disabled = ['site_id_field_td', 'site_name_field_td', 'cancel_btn', 'save_btn'];
  var enabled = ['site_id_static_td', 'site_name_static_td', 'delete_btn', 'edit_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
}

function saveSite() {
  request = getXMLHttpRequest();
  request.onreadystatechange = saveSiteCallback;

  var request_str = "site_id=" +
    escape(document.getElementById('site_id_field').value);
  request_str += "&site_name=" + 
    escape(document.getElementById('site_name_field').value);
  request.open("POST", "/edit_site", true);
  request.send(request_str);
}

function saveSiteCallback() {
  if (this.readyState == 4) {
    var response_element = document.getElementById("response");

    if (this.status == 200) {
      response_element.innerHTML = "Success";
      response_element.setAttribute("class", "");

      window.cur_site = JSON.parse(this.responseText);
      cancelEdit();

      document.getElementById('site_id_static_td').innerHTML =
        window.cur_site.id;
      document.getElementById('site_name_static_td').innerHTML =
        window.cur_site.name;
    } else {
      response_element.innerHTML = this.statusText;
      response_element.setAttribute("class", "error");
    }
  }
}
