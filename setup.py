#!/usr/bin/python

#   Copyright 2011 Alexandre Zani (alexandre.zani@gmail.com) 
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

from setuptools import setup
setup(name = 'hsr',
    version = '0.2',
    author = 'Alexandre Zani',
    author_email = 'Alexandre.Zani@gmail.com',
    description = ('Human Skeletal Remains'),
    license = 'Apache License Version 2.0',
    packages = ['hsr', 'tests'],
    install_requires = ['sqlalchemy', 'pythia']
    )
