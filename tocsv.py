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


# EXEMPLAR DATA FOR ESWC
# {
#	"conference" : {
#		"first-call" : [
#			{ 
#				"onTime": "2013-05-13T14:45:15" ,
#				"object" : { 
#					"success" : [ "john@mail.com" , "doe@mail.com" ] ,
#					"failure" : [ "jane@mail.com" ] 
#				} 
#			} ,
#			{ 
#				"onTime": "2013-05-17T16:15:17" ,
#				"object" : { 
#					"success" : [ "jane@mail.com" ] ,
#					"failure" : [ ] 
#				} 
#			}
#		] ,
#		"second-call" : [
#			{ 
#				"onDate": "2013-06-19T14:45:15" ,
#				"object" : { 
#					"success" : [ "john@mail.com" , "doe@mail.com" , "jane@mail.com" ] ,
#					"failure" : [ ] 
#				} 
#			}
#		]
#	} ,
#	"workshop" : { ... } ,
#	"tutorial" : { ... } ,
#	"challenge" : { ... } ,
#	"demo" : { ... }
#}

from DataHandler import *
import csv
import sys

# HOW TO CALL THE SERVICE
# python tocsv.py <jsonPath> <csvPath>

# FOR TESTING
# python tocsv.py data.json data.csv

jsonPath = sys.argv[1]
csvPath = sys.argv[2]

successString = "success"
failureString = "failure"
dh = DataHandler(jsonPath)

# Collect all emails
filter = set([item for object in dh.getAllObjects() for item in object[successString] + object[failureString]])

header = ["mail"]
for category in sorted(dh.getAllCategories()):
    for type in reversed(dh.getAllTypes(category)):
        header += [category + "#" + type]

rows = []
for email in sorted(filter):
    row = [email]
    for category in sorted(dh.getAllCategories()):
        for type in reversed(dh.getAllTypes(category)):
            currentDate = ""
            datesAndObjects = dh.getDatesAndObjects(category, type)
            for date, object in datesAndObjects:
                if email in object[successString]:
                    if currentDate == "" or currentDate < date:
                        currentDate = date
            row += [currentDate]
    rows += [tuple(row)]

with open(csvPath, 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(header)
    f_csv.writerows(rows)