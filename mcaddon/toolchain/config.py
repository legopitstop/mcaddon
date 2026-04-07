from mcaddon import BaseModel, PackageFormat, VersionBump
from pydantic import Field
from typing import List, Optional, Dict, Any
from argparse import Namespace
import os
import commentjson


class PackagerConfig(BaseModel):
    resource_packs: List[str] = Field(default_factory=list)
    behavior_packs: List[str] = Field(default_factory=list)
    skin_packs: List[str] = Field(default_factory=list)
    marketing_art: List[str] = Field(default_factory=list)
    store_art: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    world: Optional[str] = None
    format: Optional[PackageFormat] = None
    bump: Optional[VersionBump] = None

    minify: bool = False
    flatten: bool = False
    obfuscate: bool = False
    verify: bool = Field(default=False)

    @staticmethod
    def from_namespace(value: Namespace) -> "PackagerConfig":
        keys = [
            "resource_packs",
            "behavior_packs",
            "skin_packs",
            "marketing_art",
            "store_art",
            "world",
            "format",
            "minify",
            "flatten",
            "verify",
            "bump",
            "obfuscate",
            "encrypt",
        ]
        data = {k: v for [k, v] in value.__dict__.items() if k in keys}
        return PackagerConfig(**data)

    @staticmethod
    def from_file(filename: Optional[str] = None) -> "PackagerConfig":
        config = PackagerConfig()
        if filename is None:
            if os.path.isfile("mcaddon.config.json"):
                filename = "mcaddon.config.json"
        if filename:
            with open(filename) as fd:
                config.update(commentjson.load(fd))
        return config

    def update(self, data: Dict[str, Any] | "PackagerConfig") -> "PackagerConfig":
        config = (
            data
            if isinstance(data, PackagerConfig)
            else PackagerConfig.model_validate(data)
        )
        # content
        if not self.resource_packs:
            self.resource_packs = config.resource_packs

        if not self.behavior_packs:
            self.behavior_packs = config.behavior_packs

        if not self.skin_packs:
            self.skin_packs = config.skin_packs

        if not self.marketing_art:
            self.marketing_art = config.marketing_art

        if not self.store_art:
            self.store_art = config.store_art

        if not self.world:
            self.world = config.world

        if self.format is None:
            self.format = config.format

        if not self.bump:
            self.bump = config.bump

        if not self.tools:
            self.tools = config.tools

        # if not self.minify:
        #     self.minify = config.minify

        # if not self.flatten:
        #     self.flatten = config.flatten

        # if not self.verify:
        #     self.verify = config.verify

        # if not self.obfuscate:
        #     self.obfuscate = config.obfuscate

        return self
