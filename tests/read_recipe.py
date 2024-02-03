from mcaddon import *

rpe = Recipe.load("build/brewing_container.json")
print(rpe.identifier)

rpe = Recipe.load("build/brewing_mix.json")
print(rpe.identifier)

rpe = Recipe.load("build/furnace.json")
print(rpe.identifier)

rpe = Recipe.load("build/shaped.json")
print(rpe.identifier)

rpe = Recipe.load("build/shapeless.json")
print(rpe.identifier)

rpe = Recipe.load("build/smithing_transform.json")
print(rpe.identifier)

rpe = Recipe.load("build/smithing_trim.json")
print(rpe.identifier)
