import re
import os
import json
import locale

__version__ = '0.0.1'
__lang__ = None
__root__ = None

class LangError(Exception): pass

class Lang(dict):
    def format(self, s:str, *subs):
        # replace %#
        i=1
        for rep in subs:
            s = s.replace('%'+str(i), str(rep))
            i+=1

        # replace %s
        i = 0
        regex = r'%s'
        match = re.search(regex, s)
        while match is not None:
            try:
                rep = list(subs)[i]
            except IndexError:
                try: rep = list(subs)[-1]
                except IndexError: rep = ''
            s = s.replace('%s', str(rep), 1)
            match = re.search(regex, s)
            i +=1

        # clean up
        s = re.sub(r'%[1-9]+', '', s)
        s = re.sub(r'%s', '', s)

        return s

    def translate(self, __key:str, *subs:str, fallback:str=None):
        if fallback is None: fallback = str(__key)
        result = self.get(str(__key), str(fallback))
        # return self.format(re.sub(r'\s+', '', re.sub(r'#.*', '', result)), *subs)
        return self.format(result, *subs)
    tl = translate

    @property
    def comments(self) -> list:
        return getattr(self, '_comments', [])
    
    @comments.setter
    def comments(self, value:list) :
        if isinstance(value, list):
            setattr(self, '_comments', value)
        else:
            raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead.")

    def insert_comment(self, line:int, s:str):
        """
        Inserts a comment to the file at a specified line before the key/value if any.

        Arguments
        ---
        `line` - The line to insert at.

        `s` - The content of the comment.
        """
        com = {'line': line, 'text': s}
        try:
            self._comments.append(com)
        except AttributeError:
            self._comments = [com]
        return self
    
    def remove_comment(self, index:int):
        """
        Removes a comment at the specified index.

        Arguments
        ---
        `line` - The comment to remove.
        """
        try:
            del self._comments[index]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_comments(self):
        """
        Removes all comments from this file.
        """
        try:
            self._comments.clear()
        except AttributeError:
            self._comments = []
        return self

    def __setitem__(self, __key:str, __value:str):
        super().__setitem__(str(__key), str(__value))

    def __getitem__(self, __key:str) -> str:
        return self.get(__key, __key)

from .decoder import LANGDecoder
from .encoder import LANGEncoder

def set_language(lang:str):
    """
    Override the locale language.

    Arguments
    ---
    `lang` - The lang to use.
    """
    global __lang__
    __lang__ = str(lang)

def get_language() -> str:
    """
    Returns the configured langauge code
    """
    global __lang__
    if __lang__ is None:
        __lang__ = locale.getdefaultlocale()[0]
    return __lang__

def init(path:str, default:str='en_US'):
    """
    Load lang file from the directory path.

    Arguments
    ---
    `path` - Directory path to the .lang files

    `default` - The default lang file to use if the locale lang does not exist.
    """
    # get languages
    LANGS = os.path.join(path, 'languages.json')
    if os.path.exists(LANGS): # get list from languages.json
        with open(LANGS) as r:
            langs = json.load(r)
            if isinstance(langs, list) == False: raise TypeError(f"Expected list but got '{langs.__class__.__name__}' insteead.")
    else: # get list from dir
        langs = []
        for file in os.listdir(path):
            if file.endswith('.lang'):
                langs.append(file.replace('.lang', ''))

    # get lang file
    locale = get_language()
    if locale in langs:
        with open(os.path.join(path, locale+'.lang'), encoding='utf8') as r: load(r)
    else:
        fp = os.path.join(path, default+'.lang')
        if os.path.exists(fp):
            with open(fp, encoding='utf8') as r: load(r)

def translate(key:str, *subs, fallback:str=None) -> str:
    """
    Use the root translator.

    Arguments
    ---
    `key` - The key to translate.

    `subs` - List of values to substitut these can either be ordered (`%1`, `%2`, etc.) or not ordered (`%s`)

    `fallback` - The fallback text if key can't be found. Returns key by default.
    """
    if __root__ is None:
        raise LangError('A language file has not been loaded yet.')
    return __root__.translate(key, *subs, fallback=fallback)

tl = translate

def dump(obj:Lang|dict, fp:str, **kw) -> None:
    """Serialize obj as a LANG formatted stream to fp (a `.write()`-supporting file-like object)."""
    iterable = LANGEncoder(**kw).encode(obj)
    fp.write(iterable)

def dumps(obj:Lang|dict, **kw) -> str:
    """Serialize obj to a LANG formatted str."""
    return LANGEncoder(**kw).encode(obj)

def load(fp:str|bytes, **kw) -> Lang:
    """Deserialize fp (a `.read()`-supporting file-like object containing a LANG document) to a Python object."""
    return loads(fp.read(), **kw)

def loads(s:str|bytes|bytearray, **kw) -> Lang:
    """Deserialize s (a str, bytes or bytearray instance containing a LANG document) to a Python object."""
    if not isinstance(s, (str, bytes, bytearray)):
        raise TypeError(f'the LANG object must be str, bytes or bytearray, not {s.__class__.__name__}')
    result = LANGDecoder(**kw).decode(s)
    global __root__
    __root__ = result
    return result
