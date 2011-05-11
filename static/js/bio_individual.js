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
  var enabled = ['suffix_designation_field_td'];
  var disabled = ['suffix_designation_static', 'delete_btn', 'cancel_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
}

function startEdit() {
  var enabled = ['sex_field_td', 'age_field_td', 'catalogue_number_field_td',
      'save_btn', 'cancel_btn', 'age_min_field_tr', 'age_max_field_tr',
      'suffix_field_tr'];
  var disabled = ['sex_static', 'age_static', 'catalogue_number_static',
      'edit_btn'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
  document.getElementById('suffix_field').value = window.cur_bio_individual.suffix;
  document.getElementById('suffix_designation_field').value =
    window.cur_bio_individual.suffix_designation;
  document.getElementById('age_field').value = window.cur_bio_individual.age;
  document.getElementById('age_max_field').value = window.cur_bio_individual.age_max;
  document.getElementById('age_min_field').value = window.cur_bio_individual.age_min;
  document.getElementById('sex_field').value = window.cur_bio_individual.sex;
  document.getElementById('catalogue_number_field').value = window.cur_bio_individual.catalogue_num;
  document.getElementById('catalogue_number_field').onClick = "";
}

function cancelEdit() {
  var disabled = ['sex_field_td', 'age_field_td', 'catalogue_number_field_td',
      'save_btn', 'cancel_btn', 'age_min_field_tr', 'age_max_field_tr',
      'suffix_field_tr', 'suffix_designation_field_td'];
  var enabled = ['sex_static', 'age_static', 'catalogue_number_static',
      'edit_btn', 'suffix_designation_static'];
  setAttributeOfMany(enabled, 'style', '');
  setAttributeOfMany(disabled, 'style', 'display:none');
  document.getElementById('catalogue_number_field').onClick = "window.location=" + window.cur_bio_individual.catalogue_num;
}

function saveBioIndividual() {
  request = getXMLHttpRequest();
  request.onreadystatechange = saveBioIndividualCallback;

  var request_str = "suffix_designation=" +
    escape(document.getElementById('suffix_designation_field').value); 
  request_str += "&suffix=" + escape(document.getElementById('suffix_field').value); 
  request_str += "&age=" + escape(document.getElementById('age_field').value);
  request_str += "&age_max=" + escape(document.getElementById('age_max_field').value);
  request_str += "&age_min=" + escape(document.getElementById('age_min_field').value);
  request_str += "&sex=" + escape(document.getElementById('sex_field').value);
  request_str += "&catalogue_number=" + escape(document.getElementById('catalogue_number_field').value);
  request.open("POST", "/edit_bio", true);
  request.send(request_str);
}

function saveBioIndividualCallback() {
  if (this.readyState == 4) {
    var response_element = document.getElementById("response");

    if (this.status == 200) {
      response_element.innerHTML = "Success";
      response_element.setAttribute("class", "");
      window.cur_bio_individual = JSON.parse(this.responseText);
      cancelEdit();
      document.getElementById('suffix_designation_static').innerHTML =
        window.cur_bio_individual.suffix_designation;
      document.getElementById('age_static').innerHTML = window.cur_bio_individual.age;
      document.getElementById('sex_static').innerHTML = window.cur_bio_individual.sex_str;
      document.getElementById('catalogue_number_static').innerHTML = window.cur_bio_individual.catalogue_num;
      document.getElementById('catalogue_number_static').setAttribute("onclick",
        "window.location='/museum_object/" +
        window.cur_bio_individual.museum_object_id + "';");
    } else {
      response_element.innerHTML = this.statusText;
      response_element.setAttribute("class", "error");
    }
  }
}

function deleteBio() {
  var sure = confirm("You are about to permanently delete this biological individual from the database. This operation may not be undone. Are you sure you want to continue?");
  if (! sure) {
    return;
  }

  request = getXMLHttpRequest();
  request.onreadystatechange = deleteBioCallback;

  request.open("POST", "/delete_bio", true);
  request.send("suffix_designation=" + escape(window.cur_bio_individual.suffix_designation));
}

function deleteBioCallback() {
  if (this.readyState == 4) {
    if (this.status == 200) {
      alert("Success");
      history.back();
    } else {
      var response_element = document.getElementById("response");
      response_element.innerHTML = this.statusText;
      response_element.setAttribute("class", "error");
    }
  }
}
