#    Copyright 2018 Ruben Decrop
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os, os.path
import tempfile
import shutil

vfile = open(os.path.join('data', 'BYCCO_VERSION'))
version = vfile.read().strip()
print('building version', version)
major, minor, patch = version.split('.')

# updating python setup.py

setuppath = os.path.join('backend', 'setup.py')
fh, temppath = tempfile.mkstemp()
with open(temppath, 'w') as tmp:
    with open(setuppath, 'r') as source:
        for line in source:
            if line.strip().startswith('version='):
                tmp.write("    version='{0}',\n".format(version))
            else:
                tmp.write(line)
os.remove(setuppath)
shutil.move(temppath, setuppath)

# update package.json

packagepath = os.path.join('frontend', 'package.json')
fh, temppath = tempfile.mkstemp()
with open(temppath, 'w') as tmp:
    with open(packagepath, 'r') as source:
        for line in source:
            if line.strip().startswith('"version":'):
                tmp.write('  "version": "{0}",\n'.format(version))
            else:
                tmp.write(line)
os.remove(packagepath)
shutil.move(temppath, packagepath)


