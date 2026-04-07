from mcaddon import Jigsaw, __format_version__


def test_dump_jigsaw():
    result = {
        "format_version": __format_version__,
        "minecraft:jigsaw": {
            "description": {"identifier": "minecraft:jigsaw"},
            "biome_filters": [],
            "step": "underground_structures",
            "terrain_adaptation": "bury",
            "start_pool": "minecraft:default",
            "max_depth": 7,
            "heightmap_projection": "world_surface",
            "start_height": {"type": "constant"},
            "max_distance_from_center": {"horizontal": 1, "vertical": 1},
        },
    }
    obj = Jigsaw()
    assert obj.model_dump() == result, obj.model_dump()


def test_open_jigsaws():
    # for file in glob.glob("tests/behavior_packs/vanilla/worldgen/structures/*.json"):
    #     print(file)
    #     with Jigsaw.open(file) as structure:
    #         print(structure.id)

    #         data = structure.model_dump()
    #         result = Jigsaw.model_validate(data)
    #         assert data == result.model_dump()
    ...
