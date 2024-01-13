import re
from . import Lang

class LANGDecoderError(Exception): pass

class LANGDecoder:
    def __init__(self, **kw):
        pass

    def decode(self, s) -> Lang:
        remove = [r'\t', r'#.*'] # 
        result = {}
        lines = str(s).split('\n')
        num = 1
        for ln in lines:
            text = ln.lstrip('\ufeff ')
            if text.startswith('##'): pass # ignore comments
            elif text == '': pass # ignore empty lines
            elif text.startswith('#'): 
                raise LANGDecoderError(f"Line: {num} - Invalid lang file format. New line character was found while parsing key: '{text}'.")
            else:
                kv = text.split('=',1)
                if len(kv) == 2:
                    v = kv[1]
                    for r in remove:
                        v = re.sub(r, '', v)
                    result[kv[0]] = v
                else:
                    raise LANGDecoderError(f"Line: {num} - Invalid lang file format. New line character was found while parsing key: '{text}'.")


            num+=1
        return Lang(result)