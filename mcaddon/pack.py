from typing import Self
from zipfile import ZipFile
import mclang
import os

from .manifest import Manifest
from .util import Identifier
from .block import Block
from .item import Item

__all__ = ['Pack', 'BehaviorPack', 'ResourcePack', 'Addon']

class Pack:
    def __init__(self):
        pass

class __CommonPack(Pack):
    def __init__(self, manifest:Manifest):
        super().__init__()
        self.texts = mclang.Lang()
        self.texts[manifest.header.name_key] = manifest.header.name
        self.texts[manifest.header.description_key] = manifest.header.description

        self.manifest = manifest
        self.blocks:dict[Identifier, Block] = {}
        self.items:dict[Identifier, Item] = {}
        self.name = self.texts.translate(self.manifest.header.name)

    @property
    def manifest(self) -> Manifest:
        return getattr(self, '_manifest')
    
    @manifest.setter
    def manifest(self, value:Manifest):
        if not isinstance(value, Manifest): raise TypeError(f"Expected Manifest but got '{value.__class__.__name__}' instead")
        setattr(self, '_manifest', value)

    @property
    def texts(self) -> mclang.Lang:
        return getattr(self, '_texts')
    
    @texts.setter
    def texts(self, value:mclang.Lang):
        if not isinstance(value, mclang.Lang): raise TypeError(f"Expected mclang.Lang but got '{value.__class__.__name__}' instead")
        setattr(self, '_texts', value)

    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @classmethod
    def load(cls, fp:str) -> Self:
        self = cls.__new__(cls)
        return self
    
    # Block

    def get_block(self) -> Block|None:
        return self.blocks.get()

    def add_block(self, block:Block) -> Block:
        self.blocks[block.identifier] = block
        return block

    def remove_block(self, identifier:Identifier|str) -> Block|None:
        return self.blocks.pop(Identifier(identifier))

    def clear_blocks(self):
        self.blocks = {}
        return self
    
    # Item
    
    def get_item(self) -> Item|None:
        return self.items.get()

    def add_item(self, item:Item) -> Item:
        self.items[item.identifier] = item
        return item

    def remove_item(self, identifier:Identifier|str) -> Item|None:
        return self.items.pop(Identifier(identifier))

    def clear_items(self):
        self.items = {}
        return self
        
    def save(self, fp: str) -> Self:
        name, ext = os.path.splitext(fp)
        if ext == '':
            return self.save_folder(name+ext)
        return self.save_zipfile(fp)
    
    def save_zipfile(self, fp:str) -> Self:
        with ZipFile(fp, 'w') as z: self.writezip(z)
        return self
    
    def writezip(self, z:ZipFile, path:str='', **kw) -> Self:
        """
        Save pack as a ZIPFILE

        :param fp: The file path to save as
        :type fp: str
        """
        raise NotImplementedError()
    
    def save_folder(self, path:str, **kw) -> Self:
        """
        Save pack as a FOLDER

        :param path: The directory to save to
        :type path: str
        """
        raise NotImplementedError()

class BehaviorPack(__CommonPack):
    def __init__(self, manifest:Manifest=None):
        m = Manifest.behavior() if manifest is None else manifest
        super().__init__(m)

    def writezip(self, zip:ZipFile, path:str='', **kw) -> Self:
        props = {'separators': (',', ':')}
        props.update(kw)
        # MANIFEST

        zip.writestr(os.path.join(path, 'manfiest.json'), self.manifest.json(**props))

        # BLOCK

        for id, block in self.blocks.items():
            zip.writestr(os.path.join(path, 'blocks', id.path+'.json'), block.json(**props))

        # ITEM
            
        for id, item in self.items.items():
            zip.writestr(os.path.join(path, 'items', id.path+'.json'), item.json(**props))

        # TEXTS

        zip.writestr(os.path.join(path, 'texts', 'en_US.lang'), mclang.dumps(self.texts))
        return self

    def save_folder(self, path:str, **kw) -> Self:
        props = {'indent': 2}
        props.update(kw)

        # MANIFEST

        fp = os.path.join(path, 'manifest.json')
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w') as f:
            f.write(self.manifest.json(**props))

        # BLOCK
            
        for id, block in self.blocks.items():
            fp = os.path.join(path, 'blocks', f'{id.path}.json')
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, 'w') as f:
                f.write(block.json(**props))

        # ITEM
                
        for id, item in self.items.items():
            fp = os.path.join(path, 'items', f'{id.path}.json')
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, 'w') as f:
                f.write(item.json(**props))

        # TEXTS
                
        fp = os.path.join(path, 'texts', 'en_US.lang')
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w') as f: mclang.dump(self.texts, f)
        return self
    
class ResourcePack(__CommonPack):
    def __init__(self, manifest:Manifest=None):
        m = Manifest.resource() if manifest is None else manifest
        super().__init__(m)
    
    def writezip(self, zip:ZipFile, path:str='', **kw) -> Self:
        props = {'separators': (',', ':')}
        props.update(kw)

        # MANIFEST

        zip.writestr(os.path.join(path, 'manfiest.json'), self.manifest.json(**props))

        # TEXTS

        zip.writestr(os.path.join(path, 'texts', 'en_US.lang'), mclang.dumps(self.texts))
        return self

    def save_folder(self, path: str, **kw) -> Self:
        props = {'indent': 2}
        props.update(kw)

        # MANIFEST

        fp = os.path.join(path, 'manifest.json')
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w') as f:
            f.write(self.manifest.json(**props))

        # TEXTS
                
        fp = os.path.join(path, 'texts', 'en_US.lang')
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w') as f: mclang.dump(self.texts, f)

        return self
    
class Addon:
    def __init__(self, resources:ResourcePack=None, behaviors:BehaviorPack=None):
        self.resources = resources
        self.behaviors = behaviors

    @property
    def resources(self) -> ResourcePack|None:
        return getattr(self, '_resources', None)
    
    @resources.setter
    def resources(self, value:ResourcePack|None):
        if value is None: self.resources = ResourcePack()
        elif isinstance(value, ResourcePack):
            setattr(self, '_resources', value)
        else:
            raise TypeError(f"Expected ResourcePack or None but got '{value.__class__.__name__}' instead")
    
    @property
    def behaviors(self) -> BehaviorPack|None:
        return getattr(self, '_behaviors', None)
    
    @behaviors.setter
    def behaviors(self, value:BehaviorPack|None):
        if value is None: self.behaviors = BehaviorPack()
        elif isinstance(value, BehaviorPack):
            setattr(self, '_behaviors', value)
        else:
            raise TypeError(f"Expected BehaviorPack or None but got '{value.__class__.__name__}' instead")
    
    def add_block(self, block:Block) -> Block:
        self.resources.add_block(block)
        self.behaviors.add_block(block)
        return block

    def remove_block(self, identifier:Identifier|str) -> Block|None:
        self.resources.remove_block(identifier)
        blk = self.behaviors.remove_block(identifier)
        return blk

    def clear_blocks(self):
        self.resources.clear_blocks()
        self.behaviors.clear_blocks()
        return self
    
    def add_item(self, item:Item) -> Item:
        self.resources.add_item(item)
        self.behaviors.add_item(item)
        return item

    def remove_item(self, identifier:Identifier|str) -> Item|None:
        self.resources.remove_item(identifier)
        itm = self.behaviors.remove_item(identifier)
        return itm

    def clear_items(self):
        self.resources.clear_items()
        self.behaviors.clear_items()
        return self
    
    def save(self, fp:str):
        name, ext = os.path.splitext(fp)
        if ext == '':
            return self.save_folder(name+ext)
        return self.save_zipfile(fp)

    def save_zipfile(self, fp:str):
        path =os.path.join(os.path.dirname(fp), '.cache')
        os.makedirs(path, exist_ok=True)
        rp_name = self.resources.name[:16]+'_RP.mcpack'
        bp_name = self.behaviors.name[:16]+'_BP.mcpack'
        rp_path = os.path.join(path, rp_name)
        bp_path = os.path.join(path, bp_name)
        self.resources.save_zipfile(rp_path)
        self.behaviors.save_zipfile(bp_path)
        with ZipFile(fp, 'w') as zip:
            zip.write(rp_path, rp_name)
            zip.write(bp_path, bp_name)
    
    def save_folder(self, path:str):
        self.resources.save_folder(os.path.join(path, self.resources.name[:16]+'_RP'))
        self.behaviors.save_folder(os.path.join(path, self.behaviors.name[:16]+'_BP'))
