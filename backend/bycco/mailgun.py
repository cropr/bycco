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

import logging
log = logging.getLogger(__name__)

import requests

from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class MailgunEmailBackend(BaseEmailBackend):
    """
    creates a email backend that uses the mailgun API
    so we can defeat the GCE limitations on SMTP traffic
    """

    def send_messages(self, messages):
        """
        sends a list of  email messages
        :param messages:
        :return: number of successfully sent messages
        """
        url = settings.EMAIL_URL
        apikey = settings.EMAIL_APIKEY
        cnt = 0
        for msg in messages:
            log.info('Sending From: %s To: %s cc: %s', msg.from_email, msg.to,
                     msg.cc)
            rc = requests.post(url, auth=("api", apikey),
                data={'to': ','.join(msg.to + msg.cc + msg.bcc)},
                files={'message': msg.message().as_string()}
            )
            if rc.status_code == 200:
                cnt += 1
            else:
                log.error('sending email from %s to %s failed: %d',
                          msg.from_email, msg.to,rc.status_code)
        return cnt

