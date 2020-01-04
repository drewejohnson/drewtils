# THIS FILE IS PROVIDED AS IS UNDER THE CONDITIONS DETAILED IN LICENSE
# COPYRIGHT ANDREW JOHNSON, 2017-2020
"""Classes for simple file processing"""

import re

__all__ = ['KeywordParser', 'PatternReader']


class _TextProcessor(object):
    """Parent class for text processors."""

    def __init__(self, stream):
        self.stream = stream
        self.line = ''

    def _step(self):
        self.line = self.stream.readline()
        return self.line

    def _match(self, regexp):
        return re.match(regexp, self.line)

    def _search(self, regexp):
        return re.search(regexp, self.line)

    def seekToTop(self):
        """Reset the file pointer to the start of the file."""
        self.stream.seek(0)


class KeywordParser(_TextProcessor):
    r"""
    Class for parsing a file for chunks separated by various keywords.

    Parameters
    ----------
    stream : readable buffer
        Stream to be processed.
    keys : iterable of str
        List of keywords/phrases that will indicate the start of a chunk
    separators : iterable of str, optional
        List of additional phrases that can separate two chunks.
        If not given, will default to empty line ``'\n'``.
    eof : str, optional
        String to indicate the end of the file

    Attributes
    ----------
    line : str
        Most recently read line
    stream : readable buffer
        Stream that is currently processed

    """

    def __init__(self, stream, keys, separators=None, eof=''):
        super().__init__(stream)
        self._startMatch = re.compile('|'.join([str(arg) for arg in keys]))
        separators = set(keys).union(separators or {"\n"})
        self._endMatch = re.compile('|'.join([str(arg) for arg in separators]))
        self._end = eof

    def yieldChunks(self):
        """
        Return each chunk of text as a generator.

        .. deprecated:: 0.2.0
            Use :meth:`__iter__` instead

        Yields
        ------
        list of str
            Successive chunks of text

        """
        return iter(self)

    def __iter__(self):
        """Yield all chunks in the stream

        Yields
        ------
        list of str
            Successive chunks of text

        """
        chunk = []
        while self._step() != self._end:
            if self._match(self._endMatch):
                if chunk:
                    yield chunk
                chunk = [self.line] if self._match(self._startMatch) else []
            elif chunk:
                chunk.append(self.line)
        if chunk:
            yield chunk

    def parse(self):
        """
        Parse the file and return a list of keyword blocks.

        Returns
        -------
        list
            List of key word argument chunks.

        """
        return list(self)

    @classmethod
    def iterateOverFile(cls, filePath, *args, **kwargs):
        """Iterate over all chunks in the file

        Additional arguments will be passed to the constructor,
        e.g. ``keys`` and ``separators``

        Parameters
        ----------
        filepath : str
            Name of file to be opened.

        Yields
        ------
        list of str
            Chunks of text bounded by input arguments

        """
        with open(filePath, "r") as stream:
            parser = cls(stream, *args, **kwargs)
            for item in parser:
                yield item


class PatternReader(_TextProcessor):
    """
    Class that can read over a file looking for patterns.

    Parameters
    ----------
    stream : readable
        Stream of content to be processed

    Attributes
    ----------
    line : str
        Most recently read line
    match : regular expression match or None
        Match from the most recently read line

    """

    def __init__(self, stream):
        super().__init__(stream)
        self.match = None

    def searchFor(self, pattern):
        """
        Return true if the pattern is found.

        Parameters
        ----------
        pattern : str or compiled regular expression
            Pattern to be found in the stream. Will consume
            lines in the stream until a match is found
            or all lines have been exhausted

        Returns
        -------
        bool
            True if the pattern was found

        """
        regexp = re.compile(pattern) if isinstance(pattern, str) else pattern
        while self._step():
            self.match = self._search(regexp)
            if self.match:
                return True
        return False

    def yieldMatches(self, pattern):
        """
        Generator that returns all match groups that match pattern.

        Parameters
        ----------
        pattern : str or compiled regular expression
            Seek through the file and yield all match groups for lines that
            contain this patten.

        Yields
        ------
        regular expression match

        """
        while self.searchFor(pattern):
            yield self.match
