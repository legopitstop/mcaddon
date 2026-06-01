__all__ = [
    "LevelFile",
    "Abilities",
    "EduSharedResource",
    "FlatWorldLayers",
    "BlockLayer",
]

from typing import ClassVar, List, Optional, Dict, Any, Tuple
from datetime import datetime
from uuid import UUID
from pydantic import Field

from mcaddon.core.base import BaseModel
from mcaddon.core.file import NbtFile


class Abilities(BaseModel):
    attackmobs: bool = True
    attackplayers: bool = True
    build: bool = True
    doorsandswitches: bool = True
    flySpeed: float = 0.05
    flying: bool = False
    instabuild: bool = False
    invulnerable: bool = False
    lightning: bool = False
    mayfly: bool = False
    mine: bool = True
    op: bool = False
    opencontainers: bool = True
    teleport: bool = False
    verticalFlySpeed: float = 1
    walkSpeed: float = 0.1


class EduSharedResource(BaseModel):
    ButtonName: str
    linkUri: str


class BlockLayer(BaseModel):
    block_name: str
    count: int


class FlatWorldLayers(BaseModel):
    biome_id: int = 1
    encoding_version: int = 6
    structure_options: Optional[str] = None
    block_layers: List[BlockLayer] = Field(default_factory=list)
    world_version: str = "version.post_1_18"


class LevelFile(NbtFile):
    extension: ClassVar[str] = ".dat"

    BiomeOverride: str
    CenterMapsToOrigin: bool
    ConfirmedPlatformLockedContent: bool
    Difficulty: int
    FlatWorldLayers: str
    ForceGameType: bool
    GameType: int
    Generator: int
    HasUncompleteWorldFileOnDisk: bool
    InventoryVersion: str
    IsHardcore: bool = False
    LANBroadcast: bool
    LANBroadcastIntent: bool
    LastPlayed: datetime
    LevelName: str = ""
    LimitedWorldOriginX: int = 0
    LimitedWorldOriginY: int = 0
    LimitedWorldOriginZ: int = 0
    MinimumCompatibleClientVersion: Tuple[int, int, int, int, int]
    MultiplayerGame: bool
    MultiplayerGameIntent: bool
    NetherScale: int
    NetworkVersion: int
    Platform: int
    PlatformBroadcastIntent: int
    PlayerHasDied: bool
    RandomSeed: int
    SpawnV1Villagers: bool
    SpawnX: int = 0
    SpawnY: int = 0
    SpawnZ: int = 0
    StorageVersion: int
    Time: int
    WorldVersion: int
    XBLBroadcastIntent: int
    abilities: Abilities
    baseGameVersion: str = "*"
    bonusChestEnabled: bool
    bonusChestSpawned: bool
    cheatsEnabled: bool
    commandblockoutput: bool
    commandblocksenabled: bool
    commandsEnabled: bool
    currentTick: int

    editorWorldType: int
    eduOffer: int
    educationFeaturesEnabled: bool
    experiments: Dict[str, bool] = Field(default_factory=dict)
    functioncommandlimit: int = 10000
    hasBeenLoadedInCreative: bool
    hasLockedBehaviorPack: bool
    hasLockedResourcePack: bool
    immutableWorld: bool
    isCreatedInEditor: bool
    isExportedFromEditor: bool
    isFromLockedTemplate: bool
    isFromWorldTemplate: bool
    isRandomSeedAllowed: bool
    isSingleUseWorld: bool
    isWorldTemplateOptionLocked: bool
    keepinventory: bool
    lastOpenedWithVersion: Tuple[int, int, int, int, int]
    lightningLevel: int
    lightningTime: int
    limitedWorldDepth: int
    limitedWorldWidth: int
    locatorbar: bool = True
    maxcommandchainlength: int = 65535
    mobgriefing: bool
    naturalregeneration: bool
    permissionsLevel: int
    playerPermissionsLevel: int
    playerssleepingpercentage: int
    prid: str
    projectilescanbreakblocks: bool
    pvp: bool
    rainLevel: int
    rainTime: int
    requiresCopiedPackRemovalCheck: bool
    respawnblocksexplode: bool
    sendcommandfeedback: bool
    serverChunkTickRange: int
    showbordereffect: bool
    showcoordinates: bool
    showdaysplayed: bool
    showdeathmessages: bool
    showrecipemessages: bool
    startWithMapEnabled: bool
    texturePacksRequired: bool
    useMsaGamertagsOnly: bool
    worldStartCount: int
    world_policies: Dict[str, Any] = Field(default_factory=dict)

    # World Template

    UseAllowList: Optional[bool] = None
    worldTemplateUUID: Optional[UUID] = None
    worldTemplateVersion: Optional[str] = None

    # Game Rules

    randomtickspeed: int
    recipesunlock: bool
    showtags: bool
    spawnMobs: bool
    spawnradius: int
    tntexplodes: bool
    tntexplosiondropdecay: bool
    falldamage: bool
    firedamage: bool
    freezedamage: bool
    daylightCycle: int
    dodaylightcycle: bool
    doentitydrops: bool
    dofiretick: bool
    doimmediaterespawn: bool
    doinsomnia: bool
    dolimitedcrafting: bool
    domobloot: bool
    domobspawning: bool
    dotiledrops: bool
    doweathercycle: bool
    drowningdamage: bool
