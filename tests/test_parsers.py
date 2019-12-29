# THIS FILE IS PROVIDED AS IS UNDER THE CONDITIONS DETAILED IN LICENSE
"""Test the parser utilities"""

import io
import re
import os
import types

import pytest
from drewtils import KeywordParser, PatternReader


@pytest.fixture
def kwargParserSetup():

    class KwargTestHelper:
        content = (
            "// This a comment line\nset goodrun True\n"
            "multiline line0\nline1\nline2\n//Comment inside\n"
            "multiline\nother1\nother2\nset done True\n")
        keys = ["set", "multiline"]
        separators = ["\n", "//"]

    return KwargTestHelper()


@pytest.fixture
def expectedChunks():
    return [
        ['set goodrun True\n', ],
        ['multiline line0\n', 'line1\n', 'line2\n'],
        ['multiline\n', 'other1\n', 'other2\n'],
        ['set done True\n']]


@pytest.fixture
def keywordParser(kwargParserSetup):
    return KeywordParser(
        io.StringIO(kwargParserSetup.content),
        kwargParserSetup.keys,
        kwargParserSetup.separators)


def test_kwargParserParse(keywordParser, expectedChunks):
    """Verify that the keyword parser is functional."""
    actual = keywordParser.parse()
    assert expectedChunks == actual


def test_yieldChunks(keywordParser, expectedChunks):
    """Verify that the chunk generator is functional."""
    for index, actual in enumerate(keywordParser):
        assert expectedChunks[index] == actual


def test_fileIteration(kwargParserSetup, expectedChunks):
    """Verify the file based iteration can be obtained"""
    filepath = "fileIteration.txt"
    with open(filepath, "w") as stream:
        stream.write(kwargParserSetup.content)

    chunks = KeywordParser.iterateOverFile(filepath, kwargParserSetup.keys, separators=kwargParserSetup.separators)
    assert isinstance(chunks, types.GeneratorType)

    for ix, chunk in enumerate(chunks):
        assert chunk == expectedChunks[ix]

    os.remove(filepath)


@pytest.fixture
def patternParser():
        stream = io.StringIO("""22:20:02:INFO    :root : Initializing ---------
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
22:26:42:DEBUG   :root : Error code: 1""")
        return PatternReader(stream)

@pytest.fixture
def pattern():
        return re.compile(
            r'(\d{2}:\d{2}:\d{2}):(WARN|CRITICAL)\s*:([a-z]{5}):\s*(.*)')


def test_searchAndSeek(patternParser, pattern):
    """Verify the sequential processor can search and seek to the top."""
    assert patternParser.searchFor('compr')
    assert not patternParser.searchFor('nothing matches this')
    patternParser.seekToTop()
    assert patternParser.searchFor('compr')
    assert patternParser.searchFor(pattern)

def test_yieldMatches(patternParser, pattern):
    expectedMatches = (
        ('22:20:14', 'WARN', 'prepr',
         'FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING'),
        ('22:24:40', 'CRITICAL', 'upldr',
         'LOST CONNECTION. ATTEMPTING CLEAN FAIL')
    )
    for indx, match in enumerate(patternParser.yieldMatches(pattern)):
        assert match.groups() == expectedMatches[indx]
