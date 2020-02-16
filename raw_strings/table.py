class Table:
    chars = {
        '\'': r'\'',
        '\"': r'\"',
        '\a': r'\a',
        '\b': r'\b',
        '\f': r'\f',
        '\n': r'\n',
        '\r': r'\r',
        '\t': r'\t',
        '\\u': r'\u',
        '\\U': r'\U',
        '\\-': r'\-',
        '\v': r'\v',
        '\0': r'\0',
        '\2': r'\2',
        '\3': r'\3',
        '\4': r'\4',
        '\5': r'\5',
        '\6': r'\6',
        # '\\t': r'\\t',
    }

    @classmethod
    def add(cls, key, value):
        cls.chars[key] = value
        return cls.chars

    @classmethod
    def delete(cls, key):
        del cls.chars[key]
        return cls.chars
