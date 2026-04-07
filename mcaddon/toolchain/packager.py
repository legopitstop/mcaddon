__all__ = [
    "Packager",
    "register_tool",
    "Tool",
    "FlattenTool",
    "ObfuscateTool",
    "MinifyTool",
    "VerifyTool",
]

from typing import List, Dict, Optional, Type, Any
import os
import logging
import tempfile
import mcpath
import shutil
import glob
import commentjson
import hashlib
import mclang

from mcaddon import (
    __version__,
    ResourcePack,
    BehaviorPack,
    SkinPack,
    BasePack,
    PackageFormat,
)
from .config import PackagerConfig


class Tool:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def build(self, path: str, resource_type: str, format: PackageFormat) -> None: ...


__tools__: Dict[str, Type[Tool]] = {}


class Packager:
    def __init__(self, logger: bool = False, tools: Dict[str, Type[Tool]] = {}):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tools: Dict[str, Type[Tool]] = tools if tools else __tools__
        if not logger:
            self.logger.disabled = True

        self.logger.info("Starting packager %s", __version__)

    def verify_config(self, config: PackagerConfig) -> None:
        if not config.format:
            return

        pack_count = (
            len(config.resource_packs)
            + len(config.behavior_packs)
            + len(config.skin_packs)
        )

        match config.format:
            case PackageFormat.MCADDON:
                if pack_count < 2:
                    raise Exception(
                        f"Need at least 2 packs for {config.format._value_}, got {pack_count}"
                    )
                if config.world:
                    raise Exception(f"{config.format._value_} cannot have a world")

            case PackageFormat.MCPACK:
                if pack_count > 1:
                    raise Exception(
                        f"{config.format._value_} can only have 1 pack, got {pack_count}"
                    )
                if config.world:
                    raise Exception(f"{config.format._value_} cannot have a world")

            case PackageFormat.MCWORLD:
                if not config.world:
                    raise Exception(f"{config.format._value_} must have a world")

            case PackageFormat.MCTEMPLATE:
                if not config.world:
                    raise Exception(f"{config.format._value_} must have a world")

            case PackageFormat.PARTNER:
                if not config.world and pack_count == 0:
                    raise Exception(
                        f"{config.format._value_} must have a world or pack"
                    )

    def guess_format(self, output: str, config: PackagerConfig) -> None:
        if config.format:
            return

        fp, ext = os.path.splitext(output)
        match ext:
            case ".mcaddon":
                config.format = PackageFormat.MCADDON
            case ".mcpack":
                config.format = PackageFormat.MCPACK
            case ".mcworld":
                config.format = PackageFormat.MCWORLD
            case ".mctemplate":
                config.format = PackageFormat.MCTEMPLATE
            case ".zip":
                config.format = PackageFormat.PARTNER

    def archive(self, archive_name: str, content_path: str) -> None:
        shutil.make_archive(archive_name, "zip", content_path)
        if os.path.isfile(archive_name):
            os.remove(archive_name)
        os.rename(f"{archive_name}.zip", archive_name)

    def _rp(self, packs: List[str]) -> List[str]:
        result = []
        for pack in packs:
            for p in [
                *mcpath.bedrockGDK.get_resource_packs(),
                *mcpath.bedrockGDK.get_development_resource_packs(),
            ]:
                if p.endswith(pack):
                    result.append(p)
        return result

    def _bp(self, packs: List[str]) -> List[str]:
        result = []
        for pack in packs:
            for p in [
                *mcpath.bedrockGDK.get_behavior_packs(),
                *mcpath.bedrockGDK.get_development_behavior_packs(),
            ]:
                if p.endswith(pack):
                    result.append(p)
        return result

    def _sp(self, packs: List[str]) -> List[str]:
        result = []
        for pack in packs:
            for p in mcpath.bedrockGDK.get_development_skin_packs():
                if p.endswith(pack):
                    result.append(p)
        return result

    def _world(self, world: str) -> Optional[str]:
        for p in mcpath.bedrockGDK.get_worlds():
            if p.endswith(world):
                return p
        return None

    def build_pack(
        self, path: str, resource_type: str, config: PackagerConfig
    ) -> tempfile.TemporaryDirectory[Any]:
        self.logger.info("Running with config %s", config)
        name = os.path.basename(path)
        self.logger.info('Processing "%s" %s', name, resource_type.upper())
        temp = tempfile.TemporaryDirectory(prefix=f"{resource_type}_", delete=False)
        shutil.copytree(path, temp.name, dirs_exist_ok=True)

        for t in config.tools:
            tool = self.tools.get(t)
            if not tool:
                self.logger.warning("Tool '%s' not found!", t)
                continue
            if not config.format:
                self.logger.warning("Format not defined!", t)
                continue
            self.logger.info('%s "%s" %s', t.title(), name, resource_type.upper())
            tool().build(temp.name, resource_type, config.format)

        return temp

    def build_world(
        self, path: str, config: PackagerConfig
    ) -> tempfile.TemporaryDirectory[Any]:
        temp = tempfile.TemporaryDirectory(prefix="world_", delete=False)
        shutil.copytree(path, temp.name, dirs_exist_ok=True)
        return temp

    def _build(
        self,
        root: tempfile.TemporaryDirectory[Any],
        output: str,
        config: PackagerConfig,
    ) -> List[tempfile.TemporaryDirectory[Any]]:
        temp: List[tempfile.TemporaryDirectory[Any]] = []
        resource_packs: Dict[str, str] = {}
        behavior_packs: Dict[str, str] = {}
        skin_packs: Dict[str, str] = {}
        world: Optional[str] = None
        # Resource packs
        for pack in self._rp(config.resource_packs):
            tdir = self.build_pack(pack, "rp", config)
            temp.append(tdir)
            name = os.path.basename(pack)
            resource_packs[name] = tdir.name
        # Behavior packs
        for pack in self._bp(config.behavior_packs):
            tdir = self.build_pack(pack, "bp", config)
            temp.append(tdir)
            name = os.path.basename(pack)
            behavior_packs[name] = tdir.name
        # Skin packs
        for pack in self._sp(config.skin_packs):
            tdir = self.build_pack(pack, "sp", config)
            temp.append(tdir)
            name = os.path.basename(pack)
            skin_packs[name] = tdir.name
        # World
        if config.world:
            world = self._world(config.world)
            if world:
                tdir = self.build_world(world, config)
                temp.append(tdir)
                world = tdir.name
        match config.format:
            case PackageFormat.MCADDON:
                for name, rp in resource_packs.items():
                    self.archive(os.path.join(root.name, f"{name}_RP.mcpack"), rp)
                for name, bp in behavior_packs.items():
                    self.archive(os.path.join(root.name, f"{name}_BP.mcpack"), bp)
                for name, sp in skin_packs.items():
                    self.archive(os.path.join(root.name, f"{name}_SP.mcpack"), sp)
            case PackageFormat.MCPACK:
                for name, rp in resource_packs.items():
                    shutil.copytree(rp, root.name, dirs_exist_ok=True)
                for name, bp in behavior_packs.items():
                    shutil.copytree(bp, root.name, dirs_exist_ok=True)
                for name, sp in skin_packs.items():
                    shutil.copytree(sp, root.name, dirs_exist_ok=True)

            case PackageFormat.MCWORLD:
                print("mcworld")

            case PackageFormat.MCTEMPLATE:
                print("mctemplate")

            case PackageFormat.PARTNER:
                # TODO: Store art
                store_art = os.path.join(root.name, "Store Art")
                os.makedirs(store_art, exist_ok=True)

                # TODO: Marketing art
                marketing_art = os.path.join(root.name, "Marketing Art")
                os.makedirs(marketing_art, exist_ok=True)

                content = os.path.join(root.name, "Content")
                os.makedirs(content, exist_ok=True)

                if world:
                    # TODO: Add packs to world JSON files.
                    shutil.copytree(
                        world,
                        os.path.join(content, "world_template"),
                        dirs_exist_ok=True,
                    )
                    for name, rp in resource_packs.items():
                        shutil.copytree(
                            rp,
                            os.path.join(
                                content, "world_template", "resource_packs", "RP"
                            ),
                            dirs_exist_ok=True,
                        )

                    for name, bp in behavior_packs.items():
                        shutil.copytree(
                            bp,
                            os.path.join(
                                content, "world_template", "behavior_packs", "BP"
                            ),
                            dirs_exist_ok=True,
                        )

                else:
                    for name, rp in resource_packs.items():
                        shutil.copytree(
                            rp,
                            os.path.join(content, "resource_packs", "RP"),
                            dirs_exist_ok=True,
                        )

                    for name, bp in behavior_packs.items():
                        shutil.copytree(
                            bp,
                            os.path.join(content, "behavior_packs", "BP"),
                            dirs_exist_ok=True,
                        )

                    for name, sp in skin_packs.items():
                        shutil.copytree(
                            sp, os.path.join(content, "skins", "SP"), dirs_exist_ok=True
                        )

        self.logger.info("Archiving output...")
        print(root.name)
        self.archive(output % {}, root.name)
        return temp

    def build(self, output: str, config: PackagerConfig) -> None:
        self.guess_format(output, config)
        self.verify_config(config)

        root: tempfile.TemporaryDirectory[Any] = tempfile.TemporaryDirectory(
            delete=False
        )
        temp: List[tempfile.TemporaryDirectory[Any]] = []

        try:
            temp = self._build(root, output, config)
        finally:
            # Cleanup
            self.logger.info("Cleaning up!")
            for x in temp:
                x.cleanup()
            root.cleanup()


def register_tool(tool_id: str):
    def wrapper(cls):
        __tools__[tool_id] = cls
        return cls

    return wrapper


# Only flatten /type/creator/name/path/to/file.json -> /type/creator/name/file.json for addons
# directories = []
# TODO: Flatten
@register_tool("flatten")
class FlattenTool(Tool):
    def _flatten(self, input_dir: str, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        for root, _, files in os.walk(input_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, input_dir)
                flat_name = rel_path.replace(os.sep, "_")
                out_path = os.path.join(output_dir, flat_name)
                shutil.copy2(full_path, out_path)
                os.remove(full_path)
        os.removedirs(input_dir)

    def get_dirs(self, path: str) -> List[str]:
        return [root for root, subdirs, _ in os.walk(path) if not subdirs]

    def flat(self, path: str) -> None:
        print("FLAT", path)
        for dir in self.get_dirs(path):
            print(dir)
            self._flatten(dir, path)

    # TODO: Ignore last 2 paths
    def namespaced(self, path: str) -> None:
        print("NAMESPACED", self.get_dirs(path), path)

    def flatten_folder(self, path: str, format: PackageFormat) -> None:
        # return self.flat(path)

        match format:
            case (
                PackageFormat.MCADDON
                | PackageFormat.MCWORLD
                | PackageFormat.MCTEMPLATE
                | PackageFormat.PARTNER
            ):
                self.flat(path)

            case PackageFormat.MCPACK:
                self.namespaced(path)

    def build(self, path: str, resource_type: str, format: PackageFormat) -> None:
        loaders = {}
        exclude: List[str] = []
        match resource_type:
            case "rp":
                loaders = ResourcePack.loaders
                exclude = []
            case "bp":
                loaders = BehaviorPack.loaders
                exclude = ["scripts"]
            case _:
                return

        # Check if it exists in loaders
        for d in os.listdir(path):
            dir = os.path.join(path, d)
            if os.path.isdir(dir) and d in loaders and d not in exclude:
                self.flatten_folder(dir, format)


@register_tool("obfuscate")
class ObfuscateTool(Tool):
    def hash_name(self, name: str) -> str:
        return hashlib.sha256(name.encode()).hexdigest()[:10]

    def build(self, path: str, resource_type: str, format: PackageFormat) -> None:
        files = []
        paths = []
        match resource_type:
            case "rp":
                paths = [
                    "animation_controllers",
                    "animations",
                    "attachables",
                    "biomes",
                    "entity",
                    "fogs",
                    "particles",
                    "render_controllers",
                ]
            case "bp":
                paths = [
                    "animation_controllers",
                    "blocks",
                    "items",
                    "recipes",
                    "biomes",
                    "entities",
                    "spawn_groups",
                    "spawn_rules",
                    "worldgen",
                ]

        for x in paths:
            files.extend(
                glob.glob(os.path.join(path, x, "**", "*.json"), recursive=True)
            )

        for file in files:
            x, ext = os.path.splitext(file)
            name = os.path.basename(x)
            os.rename(
                file,
                os.path.join(os.path.dirname(file), f"{self.hash_name(name)}{ext}"),
            )


@register_tool("minify")
class MinifyTool(Tool):
    def build(self, path: str, resource_type: str, format: PackageFormat) -> None:
        # JSON
        for file in glob.glob(os.path.join(path, "**/*.json"), recursive=True):
            try:
                with open(file, "r") as f:
                    txt = f.read().replace("ï»¿", "")
                    data = commentjson.loads(txt)

                with open(file, "w") as f:
                    commentjson.dump(data, f, separators=(",", ":"))

            except Exception as err:
                self.logger.warning('Failed to format "%s": %s', file, err)

        # Lang
        for file in glob.glob(os.path.join(path, "texts", "*.lang")):
            with open(file, "r") as fd:
                try:
                    lang = mclang.loads(fd.read().replace("ï»¿", ""))
                    lang.comments = []
                    with open(file, "w") as f:
                        f.write(mclang.dumps(lang))
                except Exception as err:
                    self.logger.warning('Failed to load lang "%s": %s', file, err)


# TODO: Run scripting to validate custom components.
@register_tool("verify")
class VerifyTool(Tool):
    def build(self, path: str, resource_type: str, format: PackageFormat) -> None:
        pack: Optional[BasePack] = None
        match resource_type:
            case "rp":
                pack = ResourcePack.open(path)
            case "bp":
                pack = BehaviorPack.open(path)
            case "sp":
                pack = SkinPack.open(path)
        if pack:
            pack.verify()
