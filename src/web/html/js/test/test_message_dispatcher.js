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

var global_obj = new Object();

function MockXhr() {
  this.readyState = 0;
  this.rcvd = "";
  this.responseText = "";

  this.onreadystatechange = function() {
  }

  this.changeReadyState = function(new_state) {
    this.readyState = new_state;

    this.onreadystatechange();
  }

  this.respond = function(responseText) {
    this.responseText = responseText;
    this.changeReadyState(4);
  }

  this.send = function(string) {
    this.rcvd = string;
    this.changeReadyState(3);
  }
}

function TestMessageDispatcher() {
  this.test_NewDispatcher = function() {
    var dispatcher = new MessageDispatcher(new MockXhr());
    assert(dispatcher != undefined);
  }

  this.test_Message = function() {
    global_obj = new Object();
    var msg = new Message("alpha",
        function(xhr, msg) {
          global_obj.response = xhr.responseText; 
          global_obj.original = msg.msg;
        });

    var xhr = new MockXhr();
    var dispatcher = new MessageDispatcher(xhr);

    dispatcher.sendMessage(msg);
    xhr.respond("beta");
    assert(global_obj.original == "alpha");
    assert(global_obj.response == "beta");
  }

  this.test_MessageQueue = function() {
    global_obj = new Object();

    var xhr = new MockXhr();
    var dispatcher = new MessageDispatcher(xhr);

    var msg1 = new Message("alpha",
        function(xhr, msg) {
          global_obj.response = xhr.responseText; 
          global_obj.original = msg.msg;
        });
    dispatcher.sendMessage(msg1);

    var msg2 = new Message("omicron",
        function(xhr, msg) {
          global_obj.response = xhr.responseText; 
          global_obj.original = msg.msg;
        });
    dispatcher.sendMessage(msg2);

    xhr.respond("beta");
    assert(global_obj.original == "alpha");
    assert(global_obj.response == "beta");

    xhr.respond("gamma");
    assert(global_obj.original == "omicron");
    assert(global_obj.response == "gamma");
  }
}

load_test_file("../message_dispatcher.js");

RhinoTestEngine(new TestMessageDispatcher(), "MessageDispatcher");
