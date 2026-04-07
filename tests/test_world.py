from mcaddon import LevelFile


def test_open_level():

    with LevelFile.open("tests/worlds/example/level.dat") as lvl:
        print(lvl)
