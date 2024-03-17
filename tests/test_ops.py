from mcaddon import *

blocks = [Block("test1"), Block("test2"), Block("test3")]

for b in blocks:
    if b == Block("test3"):
        print("EQUAL", b)

    if b != Block("test3"):
        print("NOT", b)

    if "components" in b:
        print("HAS COMPONENTS", b)
