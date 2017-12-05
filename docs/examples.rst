========
Examples
========

Keyword Parser
^^^^^^^^^^^^^^

The :class:`~drewtils.parsers.KeywordParser` is designed to seek out and return
chunks of text with specified start and end characters.
This class takes three arguments that specify strings that begin and end each
chunk of text, and the end of the file.

.. testsetup:: *

    from drewtils import parsers

.. doctest::

    >>> kwargInput = ("// This a comment line\nset goodrun True\nmultiline line0\n"
    >>>               "line1\nline2\n//Comment inside\n"
    >>>               "multiline\nother1\nother2\nset done True\n")
    >>> with open('kwargs.txt', 'w') as kwargFile:
    >>>    kwargFile.write(kwargInput)
    >>> with parsers.KeywordParser('kwargs.txt', keys=['set', 'multiline'],
    >>>                            separators=['\n', '//']) as parser:
    >>>    chunks = parser.parse()
    >>> for num, chunk in enumerate(chunks):
    >>>     print(num, ''.join(chunk)
    0, 'set goodrun True'
    1, 'multiline line0'
    'line 1'
    'line 2'
    2, 'multiline'
    'other1'
    'other2'
    3, 'set done True'

Pattern Reader
^^^^^^^^^^^^^^

The :class:`~drewtils.parsers.PatternReader` is designed to repeatedly return
lines that match specified strings or regular expressions.
The functionality is similar to grep, but with powerful features like
:py:meth:`~drewtils.parsers.PatternReader.yieldMatches`, shown below.

.. testsetup:: *

  from drewtils.parsers import PatternReader

.. doctest::

  >>> lines = ("22:20:02:INFO    :root : Initializing ---------\n"
  >>>          "22:20:10:DEBUG   :prepr: Prepping files to be uploaded\n"
  >>>          "22:20:14:WARN    :prepr: FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING\n"
  >>>          "22:20:20:DEBUG   :compr: compressing 4 files\n"
  >>>          "22:21:31:DEBUG   :compr: compression complete - 60 % compression ratio\n"
  >>>          "22:22:05:DEBUG   :cnctr: Opening connection\n"
  >>>          "22:22:09:INFO    :root : Beginning upload -------\n"
  >>>          "22:22:11:DEBUG   :upldr: Launching upload of 1.21 Gb to destination\n"
  >>>          "22:24:35:DEBUG   :closr: Experienced keyboard interupt\n"
  >>>          "22:24:40:CRITICAL:upldr: LOST CONNECTION. ATTEMPTING CLEAN FAIL\n""
  >>>          "22:24:42:DEBUG   :upldr: Launching clean fail routines\n"
  >>>          "22:25:06:DEBUG   :upldr: Clean fail routines sucessful\n"
  >>>          "22:25:56:INFO    :inspt: Likely source of error - keyboard interupt\n"
  >>>          "22:26:23:INFO    :closr: Exiting processes ---------\n"
  >>>          "22:26:41:INFO    :root : Process complete\n"
  >>>          "22:26:42:DEBUG   :root : Error code: 1")
  >>> filePath = 'patterntesting.txt'
  >>>regexp = r'(\d{2}:\d{2}:\d{2}):(WARN|CRITICAL)\s*:([a-z]{5}):\s*(.*)'
  >>>with open(filePath, 'w') as output:
  >>>    output.write(lines)
  >>>with PatternReader(filePath) as parser:
  >>>    parser.searchFor('compr')
  True
  >>>    parser.line
  '22:20:20:DEBUG   :compr: compressing 4 files'
  >>>    parser.searchFor(regexp)
  True
  >>>    parser.line
  '22:24:40:CRITICAL:upldr: LOST CONNECTION. ATTEMPTING CLEAN FAIL'


The :class:`~drewtils.parsers.PatternReader` can also be used to produce matches on-the-fly
and with little memory overhead as a generator

.. testsetup::*

    from drewtils.parsers import PatternReader
    lines = ("22:20:02:INFO    :root : Initializing ---------\n"
             "22:20:10:DEBUG   :prepr: Prepping files to be uploaded\n"
             "22:20:14:WARN    :prepr: FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING\n"
             "22:20:20:DEBUG   :compr: compressing 4 files\n"
             "22:21:31:DEBUG   :compr: compression complete - 60 % compression ratio\n"
             "22:22:05:DEBUG   :cnctr: Opening connection\n"
             "22:22:09:INFO    :root : Beginning upload -------\n"
             "22:22:11:DEBUG   :upldr: Launching upload of 1.21 Gb to destination\n"
             "22:24:35:DEBUG   :closr: Experienced keyboard interupt\n"
             "22:24:40:CRITICAL:upldr: LOST CONNECTION. ATTEMPTING CLEAN FAIL\n""
             "22:24:42:DEBUG   :upldr: Launching clean fail routines\n"
             "22:25:06:DEBUG   :upldr: Clean fail routines sucessful\n"
             "22:25:56:INFO    :inspt: Likely source of error - keyboard interupt\n"
             "22:26:23:INFO    :closr: Exiting processes ---------\n"
             "22:26:41:INFO    :root : Process complete\n"
             "22:26:42:DEBUG   :root : Error code: 1")
    filePath = 'patterntesting.txt'
    regexp = r'(\d{2}:\d{2}:\d{2}):(WARN|CRITICAL)\s*:([a-z]{5}):\s*(.*)'
    with open(filePath, 'w') as output:
        output.write(lines)
    parser = PatterReader(filePath)

.. doctest::

  >> with parser:
  >>     for match in parser.yieldMatches(regexp):
  >>         print(match.groups()[0])
  ('22:20:14', 'WARN', 'prepr', 'FOUND 4 FILES, NOT 6 SPECIFIED, PROCEEDING')
  ('22:24:40', 'CRITICAL', 'upldr', 'LOST CONNECTION. ATTEMPTING CLEAN FAIL')

A great resource for building and testing python regular expressions is
`pythex.org <https://pythex.org/>`_.

See Also
--------
* `Python 2.7 - regular expression library <https://docs.python.org/2/library/re.html>`_
* `Pyhton 3.6 - regular expression library <https://docs.python.org/3.6/library/re.html>`_

