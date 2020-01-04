========
Examples
========

.. currentmodule:: drewtils

Keyword Parser
^^^^^^^^^^^^^^

The :class:`KeywordParser` is designed to seek out and return
chunks of text with specified start and end characters.
This class takes three arguments that specify strings that begin and end each
chunk of text, and the end of the file.

.. testsetup:: *

    import drewtils

.. doctest::

    >>> kwargInput = ("""// This a comment line\nset goodrun True\nmultiline line0
    ... line1\nline2\n//Comment inside
    ... multiline\nother1\nother2\nset done True""")
    >>> with open('kwargs.txt', 'w') as kwargFile:
    ...    _x = kwargFile.write(kwargInput)
    >>> chunkGen = drewtils.KeywordParser.iterateOverFile(
    ...     "kwargs.txt", keys=["set", "multiline"],
    ...     separators=["\n", "//"])
    >>> for c in chunkGen:
    ...     break
    >>> c
    ['set goodrun True\n']
    >>> chunks = list(chunkGen)
    >>> len(chunks)
    3
    >>> chunks[0]
    ['multiline line0\n', 'line1\n', 'line2\n']
    >>> chunks[1]
    ['multiline\n', 'other1\n', 'other2\n']
    >>> chunks[2]
    ['set done True']


The :class:`KeywordParser` can also be used directly with a readable buffer,
like an opened file. 

.. testsetup:: *

    import drewtils
    import io

.. doctest::

    >>> stream = io.StringIO("""// This a comment line\nset goodrun True\nmultiline line0
    ... line1\nline2\n//Comment inside
    ... multiline\nother1\nother2\nset done True""")
    >>> parser = drewtils.KeywordParser(
    ...     stream, keys=["set", "multiline"],
    ...     separators=["\n", "//"])
    >>> for c in parser:
    ...     print(c)
    ['set goodrun True\n']
    ['multiline line0\n', 'line1\n', 'line2\n']
    ['multiline\n', 'other1\n', 'other2\n']
    ['set done True']


Pattern Reader
^^^^^^^^^^^^^^

The :class:`PatternReader` is designed to repeatedly return
lines that match specified strings or regular expressions.
The functionality is similar to grep, but with powerful features like
:meth:`~PatternReader.yieldMatches`, shown below.

.. testsetup:: *

  from drewtils import PatternReader

.. doctest::

  >>> from io import StringIO
  >>> stream = StringIO("""22:20:02:INFO    :root : Initializing ---------
  ... 22:20:10:DEBUG   :prepr: Prepping files to be uploaded
  ... 22:20:14:WARN    :prepr: FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING
  ... 22:20:20:DEBUG   :compr: compressing 4 files
  ... 22:21:31:DEBUG   :compr: compression complete - 60 % compression ratio
  ... 22:22:05:DEBUG   :cnctr: Opening connection
  ... 22:22:09:INFO    :root : Beginning upload -------
  ... 22:22:11:DEBUG   :upldr: Launching upload of 1.21 Gb to destination
  ... 22:24:35:DEBUG   :closr: Experienced keyboard interupt
  ... 22:24:40:CRITICAL:upldr: LOST CONNECTION. ATTEMPTING CLEAN FAIL
  ... 22:24:42:DEBUG   :upldr: Launching clean fail routines
  ... 22:25:06:DEBUG   :upldr: Clean fail routines sucessful
  ... 22:25:56:INFO    :inspt: Likely source of error - keyboard interupt
  ... 22:26:23:INFO    :closr: Exiting processes ---------
  ... 22:26:41:INFO    :root : Process complete
  ... 22:26:42:DEBUG   :root : Error code: 1""")
  >>> regexp = r'(\d{2}:\d{2}:\d{2}):(WARN|CRITICAL)\s*:([a-z]{5}):\s*(.*)'
  >>> parser = PatternReader(stream)
  >>> parser.searchFor('compr')
  True
  >>> parser.line
  '22:20:20:DEBUG   :compr: compressing 4 files\n'
  >>> parser.searchFor(regexp)
  True
  >>> parser.line
  '22:24:40:CRITICAL:upldr: LOST CONNECTION. ATTEMPTING CLEAN FAIL\n'


The :class:`~drewtils.PatternReader` can also be used to produce matches on-the-fly
and with little memory overhead as a generator

.. testsetup:: *

    from drewtils import PatternReader

.. doctest::

  >>> from io import StringIO
  >>> stream = StringIO("""22:20:02:INFO    :root : Initializing ---------
  ... 22:20:10:DEBUG   :prepr: Prepping files to be uploaded
  ... 22:20:14:WARN    :prepr: FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING
  ... 22:20:20:DEBUG   :compr: compressing 4 files
  ... 22:21:31:DEBUG   :compr: compression complete - 60 % compression ratio
  ... 22:22:05:DEBUG   :cnctr: Opening connection
  ... 22:22:09:INFO    :root : Beginning upload -------
  ... 22:22:11:DEBUG   :upldr: Launching upload of 1.21 Gb to destination
  ... 22:24:35:DEBUG   :closr: Experienced keyboard interupt
  ... 22:24:40:CRITICAL:upldr: LOST CONNECTION. ATTEMPTING CLEAN FAIL
  ... 22:24:42:DEBUG   :upldr: Launching clean fail routines
  ... 22:25:06:DEBUG   :upldr: Clean fail routines sucessful
  ... 22:25:56:INFO    :inspt: Likely source of error - keyboard interupt
  ... 22:26:23:INFO    :closr: Exiting processes ---------
  ... 22:26:41:INFO    :root : Process complete
  ... 22:26:42:DEBUG   :root : Error code: 1""")
  >>> regexp = r'(\d{2}:\d{2}:\d{2}):(WARN|CRITICAL)\s*:([a-z]{5}):\s*(.*)'
  >>> parser = PatternReader(stream)
  >>> for match in parser.yieldMatches(regexp):
  ...     print(match.groups())
  ('22:20:14', 'WARN', 'prepr', 'FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING')
  ('22:24:40', 'CRITICAL', 'upldr', 'LOST CONNECTION. ATTEMPTING CLEAN FAIL')

A great resource for building and testing python regular expressions is
`pythex.org <https://pythex.org/>`_.

See Also
--------
* `Python 3 - regular expression library <https://docs.python.org/3/library/re.html>`_

