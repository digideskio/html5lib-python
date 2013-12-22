# Copyright (c) 2006-2013 James Graham and other contributors
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import, division, unicode_literals

import unittest

from html5lib.filters.whitespace import Filter
from html5lib.constants import spaceCharacters
spaceCharacters = "".join(spaceCharacters)

try:
    unittest.TestCase.assertEqual
except AttributeError:
    unittest.TestCase.assertEqual = unittest.TestCase.assertEquals


class TestCase(unittest.TestCase):
    def runTest(self, input, expected):
        output = list(Filter(input))
        errorMsg = "\n".join(["\n\nInput:", str(input),
                              "\nExpected:", str(expected),
                              "\nReceived:", str(output)])
        self.assertEqual(output, expected, errorMsg)

    def runTestUnmodifiedOutput(self, input):
        self.runTest(input, input)

    def testPhrasingElements(self):
        self.runTestUnmodifiedOutput(
            [{"type": "Characters", "data": "This is a "},
             {"type": "StartTag", "name": "span", "data": []},
             {"type": "Characters", "data": "phrase"},
             {"type": "EndTag", "name": "span", "data": []},
             {"type": "SpaceCharacters", "data": " "},
             {"type": "Characters", "data": "with"},
             {"type": "SpaceCharacters", "data": " "},
             {"type": "StartTag", "name": "em", "data": []},
             {"type": "Characters", "data": "emphasised text"},
             {"type": "EndTag", "name": "em", "data": []},
             {"type": "Characters", "data": " and an "},
             {"type": "StartTag", "name": "img", "data": [["alt", "image"]]},
             {"type": "Characters", "data": "."}])

    def testLeadingWhitespace(self):
        self.runTest(
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "SpaceCharacters", "data": spaceCharacters},
             {"type": "Characters", "data": "foo"},
             {"type": "EndTag", "name": "p", "data": []}],
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "SpaceCharacters", "data": " "},
             {"type": "Characters", "data": "foo"},
             {"type": "EndTag", "name": "p", "data": []}])

    def testLeadingWhitespaceAsCharacters(self):
        self.runTest(
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": spaceCharacters + "foo"},
             {"type": "EndTag", "name": "p", "data": []}],
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": " foo"},
             {"type": "EndTag", "name": "p", "data": []}])

    def testTrailingWhitespace(self):
        self.runTest(
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": "foo"},
             {"type": "SpaceCharacters", "data": spaceCharacters},
             {"type": "EndTag", "name": "p", "data": []}],
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": "foo"},
             {"type": "SpaceCharacters", "data": " "},
             {"type": "EndTag", "name": "p", "data": []}])

    def testTrailingWhitespaceAsCharacters(self):
        self.runTest(
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": "foo" + spaceCharacters},
             {"type": "EndTag", "name": "p", "data": []}],
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": "foo "},
             {"type": "EndTag", "name": "p", "data": []}])

    def testWhitespace(self):
        self.runTest(
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": "foo" + spaceCharacters + "bar"},
             {"type": "EndTag", "name": "p", "data": []}],
            [{"type": "StartTag", "name": "p", "data": []},
             {"type": "Characters", "data": "foo bar"},
             {"type": "EndTag", "name": "p", "data": []}])

    def testLeadingWhitespaceInPre(self):
        self.runTestUnmodifiedOutput(
            [{"type": "StartTag", "name": "pre", "data": []},
             {"type": "SpaceCharacters", "data": spaceCharacters},
             {"type": "Characters", "data": "foo"},
             {"type": "EndTag", "name": "pre", "data": []}])

    def testLeadingWhitespaceAsCharactersInPre(self):
        self.runTestUnmodifiedOutput(
            [{"type": "StartTag", "name": "pre", "data": []},
             {"type": "Characters", "data": spaceCharacters + "foo"},
             {"type": "EndTag", "name": "pre", "data": []}])

    def testTrailingWhitespaceInPre(self):
        self.runTestUnmodifiedOutput(
            [{"type": "StartTag", "name": "pre", "data": []},
             {"type": "Characters", "data": "foo"},
             {"type": "SpaceCharacters", "data": spaceCharacters},
             {"type": "EndTag", "name": "pre", "data": []}])

    def testTrailingWhitespaceAsCharactersInPre(self):
        self.runTestUnmodifiedOutput(
            [{"type": "StartTag", "name": "pre", "data": []},
             {"type": "Characters", "data": "foo" + spaceCharacters},
             {"type": "EndTag", "name": "pre", "data": []}])

    def testWhitespaceInPre(self):
        self.runTestUnmodifiedOutput(
            [{"type": "StartTag", "name": "pre", "data": []},
             {"type": "Characters", "data": "foo" + spaceCharacters + "bar"},
             {"type": "EndTag", "name": "pre", "data": []}])


def buildTestSuite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


def main():
    buildTestSuite()
    unittest.main()

if __name__ == "__main__":
    main()
