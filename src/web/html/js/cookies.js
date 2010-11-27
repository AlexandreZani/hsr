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

function setCookie(name, value, expiration_days) {
  var expiration_date = new Date();
  expiration_date.setDate(expiration_date.getDate() + expiration_days);

  document.cookie = name + "=" + escape(value) + ((expiration_days == null) ? "" : ";expires=" + expiration_date.toUTCString()) + "; path=/";
}

function getCookie(name) {
  if(document.cookie.length <= 0)
    return "";

  start = document.cookie.indexOf(name);

  if(start < 0)
    return "";

  start += name.length + 1;

  end = document.cookie.indexOf(";", start);

  if(end < 0)
    end = document.cookie.length;

  return unescape(document.cookie.substring(start, end));
}
