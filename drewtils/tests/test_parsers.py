# THIS FILE IS PROVIDED AS IS UNDER THE CONDITIONS DETAILED IN LICENSE
"""Test the parser utilities"""

import os
import re
import unittest

from drewtils.parsers import KeywordParser, PatternReader


class KwargParseTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = 'kwargtest.txt'
        dummyInput = ("// This a comment line\nset goodrun True\n"
                      "multiline line0\nline1\nline2\n//Comment inside\n"
                      "multiline\nother1\nother2\nset done True\n")
        cls.expectedChunks = [['set goodrun True\n', ],
                              ['multiline line0\n', 'line1\n', 'line2\n'],
                              ['multiline\n', 'other1\n', 'other2\n'],
                              ['set done True\n']]
        with open(cls.path, 'w') as dummyFile:
            dummyFile.write(dummyInput)
        cls.parser = KeywordParser(cls.path, keys=['set', 'multiline'],
                                   separators=['\n', '//'])

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.path)

    def test_parse(self):
        """Verify that the keyword parser is functional."""
        with self.parser as parser:
            actual = parser.parse()
        self.assertListEqual(actual, self.expectedChunks)

    def test_yieldChunks(self):
        """Verify that the chunk generator is functional."""
        with self.parser as parser:
            for index, actual in enumerate(parser.yieldChunks()):
                self.assertListEqual(actual, self.expectedChunks[index])


class PatternReaderTester(unittest.TestCase):
    """Class to test the pattern reader."""

    @classmethod
    def setUpClass(cls):
        lines = """22:20:02:INFO    :root : Initializing ---------
22:20:10:DEBUG   :prepr: Prepping files to be uploaded
22:20:14:WARN    :prepr: FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING
22:20:20:DEBUG   :compr: compressing 4 files
22:21:31:DEBUG   :compr: compression complete - 60 % compression ratio
22:22:05:DEBUG   :cnctr: Opening connection
22:22:09:INFO    :root : Beginning upload -------
22:22:11:DEBUG   :upldr: Launching upload of 1.21 Gb to destination
22:24:35:DEBUG   :closr: Experienced keyboard interupt
22:24:40:CRITICAL:upldr: LOST CONNECTION. ATTEMPTING CLEAN FAIL
22:24:42:DEBUG   :upldr: Launching clean fail routines
22:25:06:DEBUG   :upldr: Clean fail routines sucessful
22:25:56:INFO    :inspt: Likely source of error - keyboard interupt
22:26:23:INFO    :closr: Exiting processes ---------
22:26:41:INFO    :root : Process complete
22:26:42:DEBUG   :root : Error code: 1"""
        cls.parser = PatternReader('patterns.txt')
        with open(cls.parser.path, 'w') as output:
            output.write(lines)
        cls.regexp = re.compile(
            r'(\d{2}:\d{2}:\d{2}):(WARN|CRITICAL)\s*:([a-z]{5}):\s*(.*)')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.parser.path)

    def test_searchAndSeek(self):
        """Verify the sequential processor can search and seek to the top."""
        with self.parser as parser:
            self.assertTrue(parser.searchForString('compr'))
            self.assertFalse(parser.searchForString('nothing matches this'))
            self.parser.seekToTop()
            self.assertTrue(parser.searchForString('compr'))
            self.assertTrue(parser.searchForPattern(self.regexp))

    def test_yieldMatches(self):
        expectedMatches = (
            ('22:20:14', 'WARN', 'prepr',
             'FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING'),
            ('22:24:40', 'CRITICAL', 'upldr',
             'LOST CONNECTION. ATTEMPTING CLEAN FAIL')
        )
        with self.parser as parser:
            for indx, match in enumerate(parser.yieldMatches(self.regexp)):
                self.assertTupleEqual(expectedMatches[indx], match.groups())


if __name__ == '__main__':
    unittest.main()
