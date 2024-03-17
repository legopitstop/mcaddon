from mcaddon import *

geo = Geometry("cube.geo")
model = EntityModel("geometry.cube", 64, 64, 2, 2.5, Vector3(0, 0.75, 0))
bone = Bone("bb_main", pivot=Vector3(0, 0, 0))
bone.add_cube(Cube(Vector3(-8, 0, -8), Vector3(16, 16, 16), Vector2(0, 0)))
model.add_bone(bone)
geo.add_model(model)
geo.save("build/")
