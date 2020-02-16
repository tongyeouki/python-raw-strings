# Python Raw Strings

[![pipeline status](https://gitlab.com/p2m3ng/python-raw-strings/badges/master/pipeline.svg)](https://gitlab.com/p2m3ng/python-raw-strings/-/commits/master)
[![coverage report](https://gitlab.com/p2m3ng/python-raw-strings/badges/master/coverage.svg)](https://gitlab.com/p2m3ng/python-raw-strings/-/commits/master)

A common way to make escape some chars is to prefix the hardcoded string with "r" or "R":

```python
chain = r"\bHello world\n"
'\\bHello world\\n'
```

This library allows you to generate raw strings dynamically, especially regex, from and through various python built in 
data structures: 
* Dictionaries
* Lists
* Sets
* Strings
* Tuples

It can handle exceptions for integers, floats and datetime objects. 

## Install 

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    
Or:  

    $ python3 setup.py install
    
## Usage

```python
from raw_strings.formatter import DataFormatter


data = {"a": "\bHello World\n", "b": "\tBrand name", "c": "John\6Doe"}
raw_data = DataFormatter(data=data).raw()

{'a': '\\bHello World\\n', 'b': '\\tBrand name', 'c': 'John\\6Doe'}
```

Table can be modified through DataFormatter:

```python
data = {'\nHello World\n', "\nBrand name\n", "\nJohn Doe\n"}
formatter = DataFormatter(data=data)
formatter.table.delete("\n")

{'\nHello World\n', '\nJohn Doe\n', '\nBrand name\n'}
```

```python
data = {'\nHello World\n', "\nBrand name\n", "\nJohn Doe\n"}
formatter = DataFormatter(data=data)
formatter.table.add("\n", r"\n")

{'\nHello World\n', '\nJohn Doe\n', '\nBrand name\n'}
```

## Example

```python
from raw_strings.formatter import DataFormatter
import datetime
import re

regex_list = [
    {
        "id": 1,
        "created": datetime.datetime.now(),
    },
    {
        "a": "\bHello World\n",
        "b": "\bBrand name",
        "c": "John Doe",
        "d": "c:\\\\temp\\\\.*",
        "e": "([\d\w\+\-\.\_]+)@([\w\_\-\.]+[a-zA-Z])",
    }
]

print(regex_list)

raw = DataFormatter(data=regex_list).raw()

print(raw)

text = r"""
Hello World
   Brand name    John Doe
c:\temp\myfiles
john.doe@example.com
"""

for regex in raw[1].values():
    re.compile(regex)
    result = re.search(regex, text, re.IGNORECASE)
    print(result)
```

Output: 

```log
[{'id': 1, 'created': datetime.datetime(2020, 1, 1, 0, 0, 30, 123456)}, {'a': '\x08Hello World\n', 'b': '\x08Brand name', 'c': 'John Doe', 'd': 'c:\\\\temp\\\\.*', 'e': '([\\d\\w\\+\\-\\.\\_]+)@([\\w\\_\\-\\.]+[a-zA-Z])'}]
[{'id': 1, 'created': datetime.datetime(2020, 1, 1, 0, 0, 30, 123456)}, {'a': '\\bHello World\\n', 'b': '\\bBrand name', 'c': 'John Doe', 'd': 'c:\\\\temp\\\\.*', 'e': '([\\d\\w\\+\\-\\.\\_]+)@([\\w\\_\\-\\.]+[a-zA-Z])'}]
<_sre.SRE_Match object; span=(1, 13), match='Hello World\n'>
<_sre.SRE_Match object; span=(16, 26), match='Brand name'>
<_sre.SRE_Match object; span=(30, 38), match='John Doe'>
<_sre.SRE_Match object; span=(39, 54), match='c:\\temp\\myfiles'>
<_sre.SRE_Match object; span=(55, 75), match='john.doe@example.com'>
```

## Contributing

Feel free to contribute to this project or to raise an issue. See `.gitlab/ISSUE_TEMPLATE.md`
