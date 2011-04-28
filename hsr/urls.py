#   Copyright Alexandre Zani (alexandre.zani@gmail.com) 
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import hsr.views

view_paths = [
    ("/main/", hsr.views.static, ()),
    ("/logout/", hsr.views.logout, ()),
    ("/change_password/", hsr.views.change_password, ()),
    ("/account_management/", hsr.views.static, ()),
    ("/museum_objects/", hsr.views.museum_objects, ()),
    ("/museum_object/(\d+)/", hsr.views.museum_object, ("id",)),
    ("/bio_individuals/", hsr.views.bio_individuals, ()),
    ("/bio_individual/(\d+)/", hsr.views.bio_individual, ("id",)),
]
