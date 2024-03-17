# TODO
- Add method to convert an mcaddon to a python script to convert already existing packs to python. (w/ cli)
- Cache build UUID's so it can use the same UUID when re-built
- Use js2py to convert Python to JavaScript for Scripting API to create custom components and other custom features.

- Rename "BlockState" to "BlockPermutation" to match Minecraft API. BlockPermutation('id', {state: value})
    - Could cause conflict issues w/ the minecraft:block.permutations objects
    - BlockPermutation.get_state()
    - BlockPermutation.add_state()
    - BlockPermutation.remove_state()
    - BlockPermutation.clear_states()

- args that use default [] or {} should use None. Create a new {} or [] in the prop if None is passed.
    - Migrate dict and list attrs to use util.setattr2

## Extensions
- AI Creator
    - Block-like interface defining the component's priority ![](https://miro.medium.com/v2/resize:fit:1400/1*EOM__0efT1Dy7_YCvNQ6ow.png)
    - Run button at the top corner to simulate the entity behavior (Lights up each Block)

