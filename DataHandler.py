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

import os
import json


class DataHandler:
    """This class is the responsible entity to store/read data into/from
    files (using JSON as default format)."""

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def addData(self, category, type, time, object):
        if category not in self.data:
            self.data[category] = {}
        if type not in self.data[category]:
            self.data[category][type] = []

        self.data[category][type] += [{"onTime": time, "object": object}]
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def getObjects(self, category, type):
        result = []
        if category in self.data and type in self.data[category]:
            for object in self.data[category][type]:
                result += [object["object"]]
        return result

    def getDatesAndObjects(self, category, type):
        result = []
        if category in self.data and type in self.data[category]:
            for object in self.data[category][type]:
                result += [(object["onTime"], object["object"])]
        return result

    def getAllObjects(self):
        result = []
        for category in self.data:
            for type in self.data[category]:
                result += self.getObjects(category, type)
        return result

    def getAllCategories(self):
        return [category for category in self.data]

    def getAllTypes(self, category):
        return [type for type in self.data[category]]

    def getData(self):
        return self.data