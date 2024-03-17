import glob
import time
from mcaddon import BehaviorPack, Addon
from multiprocessing import Pool


def callback(path):
    try:
        pack = BehaviorPack.load(path)
        print(pack, path)
        return pack
    except Exception as err:
        import traceback

        print("Error: {}\n{}".format(path, traceback.format_exc()))


if __name__ == "__main__":

    start = time.time()

    # BEHAVIOR_PACKS

    gofast = True
    if gofast:
        # This should be used in Addon class to load packs.
        with Pool(20) as p:
            packs = p.map(callback, glob.glob("tests/units/behavior_packs/*"))

    else:
        packs = []
        for path in glob.glob("tests/units/behavior_packs/*"):
            pack = callback(path)
            packs.append(pack)

    print(round(time.time() - start, 2), "ms")
    addon = Addon()
    addon.extend(packs)
    print("Saving...")
    addon.save("build/", zipped=False, overwrite=True)
