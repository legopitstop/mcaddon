from mcaddon import ResourcePack, BehaviorPack

BP = BehaviorPack.open("build/addon/addon_BP")
print(BP)

RP = ResourcePack.open("build/addon/addon_RP")
print(RP)
