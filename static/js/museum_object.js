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

function startEdit() {
  var enabled = ['object_number_field_tr', 'site_field_td', 'cancel_btn', 'save_btn'];
  var disabled = ['site_static_td', 'delete_btn', 'edit_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
  document.getElementById('site_id_field').value = window.cur_museum_object.site_id;
  document.getElementById('object_number_field').value = window.cur_museum_object.object_num;
  document.getElementById('catalogue_num_field').value = window.cur_museum_object.catalogue_num;
}

function cancelEdit() {
  var disabled = ['object_number_field_tr', 'site_field_td', 'cancel_btn', 'save_btn'];
  var enabled = ['site_static_td', 'delete_btn', 'edit_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
}

function saveMuseumObject() {
  request = getXMLHttpRequest();
  request.onreadystatechange = saveMuseumObjectCallback;

  var request_str = "catalogue_num=" +
    escape(document.getElementById('catalogue_num_field').value);
  request_str += "&object_num=" + 
    escape(document.getElementById('object_number_field').value);
  request_str += "&site_id=" + 
    escape(document.getElementById('site_id_field').value);
  request.open("POST", "/edit_museum_object", true);
  request.send(request_str);
}

function saveMuseumObjectCallback() {
  if (this.readyState == 4) {
    var response_element = document.getElementById("response");

    if (this.status == 200) {
      response_element.innerHTML = "Success";
      response_element.setAttribute("class", "");

      window.cur_museum_object = JSON.parse(this.responseText);
      cancelEdit();

      document.getElementById('site_static_td').innerHTML =
        window.cur_museum_object.site_name;
      document.getElementById('museum_num_static').innerHTML =
        window.cur_museum_object.catalogue_num;
    } else {
      response_element.innerHTML = this.statusText;
      response_element.setAttribute("class", "error");
    }
  }
}
