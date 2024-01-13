from . import Lang

class LANGEncoder:
    def __init__(self, **kw):
        pass
    
    def encode(self, obj:Lang|dict) -> str:
        lines = []
        if isinstance(obj, dict):
            for k,v in obj.items():
                lines.append(f"{k}={v}")
        else:
            raise TypeError(f"Expected dict or Lang but got '{obj.__class__.__name__}' instead.")
        
        # Comments
        if isinstance(obj, Lang):
            l = len(lines)
            i = 0
            for c in obj.comments:
                lines.insert(c['line']+i, '## '+c['text'])
                i +=1
        return '\n'.join(lines)