from mcaddon import *

vol = Volume("test:sample_volume")
vol.add_component(FogComponent("fog_savanna", 1))
vol.add_component(OnActorEnterComponent([Trigger("on_enter")]))
vol.add_component(OnActorLeaveComponent([Trigger("on_leave")]))
vol.add_event("on_enter", RunCommand("say on_enter"))
vol.add_event("on_leave", RunCommand("say on_leave"))

vol.save("build/")
