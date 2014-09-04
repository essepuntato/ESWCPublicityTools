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


class Reporter:
    """This class is used as a metaphoric agent being a reporter"""

    def __init__(self):
        self.articles = []
        self.lastArticle = None
        self.lastSentence = None
        self.lastType = None

    def newArticle(self):
        self.lastArticle = []
        self.lastSentence = None
        self.lastType = None
        self.articles.append(self.lastArticle)

    def addSentence(self, sentence, type="DEFAULT"):
        self.lastSentence = sentence
        self.lastType = type
        self.lastArticle.append([sentence, type])

    def getLastSentence(self):
        return self.lastSentence

    def getLastType(self):
        return self.lastType

    def getArticlesAsString(self, filterType=None):
        result = ""
        for article in self.articles:
            for sentence, type in article:
                if filterType == None:
                    result += str(sentence) + "\n"
                elif filterType == type:
                    result += str(sentence) + "\n"
            result += "\n"
        return result

    def writeFile(self, filePath, filterType=None):
        with open(filePath, 'w') as file:
            file.write(self.getArticlesAsString(filterType))
		