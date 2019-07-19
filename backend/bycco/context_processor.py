#    Copyright 2017 - 2018 Ruben Decrop
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

import logging
log = logging.getLogger(__name__)

from django.conf import settings # import the settings file
import simplejson as json
import os.path

locale_msg = {}

def local(request):
    l = request.LANGUAGE_CODE
    if l not in locale_msg:
        fname = os.path.join(os.path.dirname(__file__), 'data', 
            'lang', '{}.json'.format(l))
        log.info('loading locale %s fname %s', l, fname)
        with open(fname, 'r') as f:
            locale_msg[l] = json.load(f)
    log.info('locale msgs: %s', locale_msg[l])
    ts = settings.TEMPLATE_SETTINGS
    c = {k:getattr(settings,k,None) for k in ts}
    c['LOCALE_MSG'] = locale_msg[l]
    c['TITLE_WEBSITE'] = locale_msg[l]['Royal Belgian Chess Federation']
    return c
