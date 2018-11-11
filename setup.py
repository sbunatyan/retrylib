#!/usr/bin/env python
# Copyright (c) 2014 Sergey Bunatyan <sergey.bunatyan@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path
from setuptools import setup

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='retrylib',
    packages=['retrylib'],
    version='1.2.5',
    description="Smart retry library",
    author="Sergey Bunatyan",
    author_email="sergey.bunatian@gmail.com",
    url="https://github.com/sbunatyan/retrylib",
    download_url="https://github.com/sbunatyan/retrylib/tree/1.2.5",
    keywords=["retry", "retries"],
    license="Apache License 2.0",
    install_requires=["requests", "six"],
    long_description=long_description,
    long_description_content_type='text/markdown'

)
