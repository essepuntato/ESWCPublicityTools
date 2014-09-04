#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2014, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

import json
from email.MIMEText import MIMEText
from smtplib import SMTP


def sendMail(strTo, strSubject, strMessage, confPath, reporter, success, failure):
    with open(confPath, 'r') as f:
        # Load the configuration file
        conf = json.load(f)

        strFrom = conf["sender"].strip()

        # Create the root message and fill in the from, to, and subject headers
        msg = MIMEText(strMessage)
        msg['From'] = strFrom
        msg['To'] = strTo
        msg['Subject'] = strSubject

        # Send the email (this example assumes SMTP authentication is required)
        try:
            smtp = SMTP()
            smtp.connect(conf["smtp"])
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(conf["user"], conf["password"])
            smtp.sendmail(strFrom, [strTo], msg.as_string())
            reporter.addSentence("Mail sent to " + strTo, success)
        except Exception as e:
            reporter.addSentence("Unable to send email to " + strTo + ": " + str(e), failure)

        try:
            smtp.quit()
        except Exception as e:
            reporter.addSentence("Unable to send email to " + strTo + ": " + str(e), failure)
        print reporter.getLastSentence()