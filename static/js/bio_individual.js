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
  var enabled = ['sex_field_td', 'age_field_td', 'catalogue_number_field_td',
      'save_btn', 'cancel_btn'];
  var disabled = ['sex_static', 'age_static', 'catalogue_number_static', 'edit_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
  document.getElementById('age_field').value = window.cur_bio_individual.age;
  document.getElementById('sex_field').value = window.cur_bio_individual.sex;
  document.getElementById('catalogue_number_field').value = window.cur_bio_individual.catalogue_num;
  document.getElementById('catalogue_number_field').onClick = "";
}

function cancelEdit() {
  var disabled = ['sex_field_td', 'age_field_td', 'catalogue_number_field_td',
      'save_btn', 'cancel_btn'];
  var enabled = ['sex_static', 'age_static', 'catalogue_number_static', 'edit_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
  document.getElementById('catalogue_number_field').onClick = "window.location=" + window.cur_bio_individual.catalogue_num;
}

function saveBioIndividual() {
  request = getXMLHttpRequest();
  request.onreadystatechange = saveBioIndividualCallback;

  var request_str = "suffix_designation=" + escape(cur_bio_individual.suffix_designation);
  request_str += "&age=" + escape(document.getElementById('age_field').value);
  request_str += "&sex=" + escape(document.getElementById('sex_field').value);
  request_str += "&catalogue_number=" + escape(document.getElementById('catalogue_number_field').value);
  request.open("POST", "/edit_bio", true);
  request.send(request_str);
  console.log(request_str);
}

function saveBioIndividualCallback() {
  if (this.readyState == 4) {
    var response_element = document.getElementById("response");

    if (this.status == 200) {
      response_element.innerHTML = "Success";
      response_element.setAttribute("class", "");
      window.cur_bio_individual = JSON.parse(this.responseText);
      cancelEdit();
      console.log(window.cur_bio_individual.age);
      document.getElementById('age_static').innerHTML = window.cur_bio_individual.age;
      document.getElementById('sex_static').innerHTML = window.cur_bio_individual.sex_str;
      document.getElementById('catalogue_number_static').innerHTML = window.cur_bio_individual.catalogue_num;
      console.log(window.cur_bio_individual.museum_object_id);
      document.getElementById('catalogue_number_static').setAttribute("onclick",
        "window.location='/museum_object/" +
        window.cur_bio_individual.museum_object_id + "';");
    } else {
      response_element.innerHTML = this.statusText;
      response_element.setAttribute("class", "error");
    }
  }
}
