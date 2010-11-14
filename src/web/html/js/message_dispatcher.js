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

function Message(msg, callback) {
  this.msg = msg;
  this.callback = callback;
}

function MessageDispatcher(xhr) {
  this.masterCallback = function() {
    if(this.readyState != 4) {
      return;
    }

    this.dispatcher.current_msg.callback(xhr, this.dispatcher.current_msg);
    this.dispatcher.current_msg = null;
    this.dispatcher.nextInQueue();
  }

  this.nextInQueue = function() {
    if(this.current_msg != null) {
      throw "XhrNotReady";
    }

    if(this.msg_queue.length <= 0) {
      return;
    }

    this.current_msg = this.msg_queue.shift();

    this.xhr.send(this.current_msg.msg);
  }

  this.sendMessage = function(msg) {
    this.msg_queue.push(msg);
    if(this.current_msg == null) {
      this.nextInQueue();
    }
  }

  this.xhr = xhr;
  this.xhr.onreadystatechange = this.masterCallback;
  this.xhr.dispatcher=this;

  this.msg_queue = new Array();

  this.current_msg = null;
}

