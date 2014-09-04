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

import csv
import sys
import time
from sendemail import *
from Reporter import *
from DataHandler import *
from datetime import datetime

# HOW TO CALL THE SERVICE
# python run.py <audience> <communication> <mailsPath> <textPath> <confFile> <nIteration> <sleepFor>
# es:
# python run.py conference first-call all-email.csv CallForPaper.txt my-conf.json 10 60

# FOR TESTING
# python run.py conference first-call test-mails.txt test-message.txt conf-google.json 10 60

# Intended audience: conference, workshop, tutorial, etc.
audience = sys.argv[1].lower()
# Communication type: first-call, second-call, last-call, etc.
call_type = sys.argv[2].lower()
# Path of the file containing the list of mails
mailsPath = sys.argv[3]
# Path of the file containing the text to send
textPath = sys.argv[4]
# Path of the configuration file
confPath = sys.argv[5]
# Number of mails to send before sleeping (0 means all)
nIterations = int(sys.argv[6])
# Number of seconds to sleep
sleepFor = int(sys.argv[7])

# Success and failure strings and sets
successString = "success"
failureString = "failure"
success = []
failure = []

currentTime = time.time()
fileTime = str(datetime.fromtimestamp(currentTime).strftime('%Y%m%d-%H%M%S'))
storeTime = str(datetime.fromtimestamp(currentTime).strftime('%Y-%m-%dT%H:%M:%S'))

with open(mailsPath, 'rt') as mailsFile, open(textPath, 'rt') as textFile:
    mailsCSV = csv.reader(mailsFile)
    content = ""
    firstLine = True
    for line in textFile:
        if firstLine:
            firstLine = False
            subject = line
        else:
            content += line

    reporter = Reporter()
    reporter.newArticle()
    dh = DataHandler("data.json")

    # Find the set of all the emails I've already sent successfully in past sessions involving the same audience and kind of communication, in order to be filter in this session
    filter = set([item for object in dh.getObjects(audience, call_type) for item in object[successString]])

    currentIteration = 1
    headers = next(mailsCSV)
    for row in mailsCSV:
        useIt = row[1].strip().lower() == "true"
        email = row[0].strip()
        if useIt and email not in filter:
            if currentIteration == nIterations + 1:
                currentIteration = 1
                time.sleep(sleepFor)

            sendMail(email, subject, content, confPath, reporter, successString, failureString)
            currentIteration += 1

            if reporter.getLastType() == successString:
                success += [email]
            else:
                failure += [email]

    # Store data into the repository and write the report
    dh.addData(audience, call_type, storeTime, {successString: success, failureString: failure})
    reporter.writeFile(audience + "-" + call_type + "-" + fileTime + ".report")