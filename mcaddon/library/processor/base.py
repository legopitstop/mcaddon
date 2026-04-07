__all__ = ["ProcessorList"]

from typing import List
from pydantic import Field

from mcaddon.core.file import ResourceFile
from mcaddon.library.common import BaseDescription
from mcaddon.library.pack import behaviorpack

from .processor_type import Processor


@behaviorpack("worldgen/processors")
class ProcessorList(ResourceFile):
    TYPE_ID = "minecraft:processor_list"

    description: BaseDescription = BaseDescription(identifier="minecraft:processor")
    processors: List[Processor] = Field(default_factory=list)

    @property
    def id(self) -> str:
        return self.description.identifier
