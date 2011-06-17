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
    ("/user_management/", hsr.views.user_management, ()),
    ("/museum_objects/", hsr.views.museum_objects, ()),
    ("/museum_object/(\d+)/", hsr.views.museum_object, ("id",)),
    ("/museum_object/", hsr.views.museum_object, ()),
    ("/bio_individuals/", hsr.views.bio_individuals, ()),
    ("/bio_individual/(\d+)/", hsr.views.bio_individual, ("id",)),
    ("/bio_individual/", hsr.views.bio_individual, ()),
    ("/edit_user/", hsr.views.edit_user, ()),
    ("/delete_user/", hsr.views.delete_user, ()),
    ("/edit_bio/", hsr.views.edit_bio, ()),
    ("/edit_museum_object/", hsr.views.edit_museum_object, ()),
    ("/delete_bio/", hsr.views.delete_bio, ()),
    ("/sites/", hsr.views.sites, ()),
    ("/site/(\d+)/", hsr.views.site, ("id",)),
    ("/site/", hsr.views.site, ()),
    ("/edit_site/", hsr.views.edit_site, ()),
]
