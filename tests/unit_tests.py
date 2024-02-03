import glob
import time
from mcaddon import BehaviorPack, ResourcePack
from multiprocessing import Pool


def callback(path):
    pack = BehaviorPack.load(path)
    print(pack)
    return pack


if __name__ == "__main__":

    start = time.time()

    # BEHAVIOR_PACKS

    gofast = False
    if gofast:  # 5.59 ms
        # This should be used in Addon class to load packs.
        with Pool() as p:
            packs = p.map(callback, glob.glob("tests/units/behavior_packs/*"))

    else:  # 11.43 ms
        packs = []
        for path in glob.glob("tests/units/behavior_packs/*"):
            pack = callback(path)
            packs.append(pack)

    # RESOURCE_PACKS
    # for path in glob.glob('tests/units/resource_packs/*'):
    #     pack = ResourcePack.load(path)
    #     print('RP',pack)
    print(round(time.time() - start, 2), "ms")
