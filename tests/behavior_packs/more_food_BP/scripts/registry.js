import { CropComponent } from "./block/CropComponent";
import { SpileComponent } from "./block/SpileComponent";
import { BushComponent } from "./block/BushComponent";
import { SaplingComponent } from "./block/SaplingComponent";
import * as gen from "./classes/SaplingGenerator";
import { CauldronComponent } from "./block/CauldronComponent";
import { HangingCropComponent } from "./block/HangingCropComponent";
import { CakeComponent } from "./block/CakeComponent";
import { CandleCakeComponent } from "./block/CandleCakeComponent";
import { TallCropComponent } from "./block/TallCropComponent";

import { PourableComponent } from "./item/PourableComponent";
import { MREComponent } from "./item/MREComponent";
import { MintyComponent } from "./item/MintyComponent";
import { PottableComponent } from "./item/PottableComponent";
import { PottedFlowerComponent } from "./block/PottedFlowerComponent";
import { CANDLES } from "./classes/utils";

function registerCakes(registry, name) {
  const chocolateCake = new CakeComponent();
  for (const candle of CANDLES) {
    chocolateCake.addCandleCake(
      "minecraft:" + candle,
      `lpsm_morefood:${candle}_${name}`,
    );
    registry.registerCustomComponent(
      `lpsm_morefood:${candle}_${name}`,
      new CandleCakeComponent(
        "minecraft:" + candle,
        `lpsm_morefood:${name}_block`,
      ),
    );
  }
  registry.registerCustomComponent("lpsm_morefood:" + name, chocolateCake);
}

export function registerBlockComponents(registry) {
  registry.registerCustomComponent(
    "lpsm_morefood:bean_bush",
    new BushComponent("lpsm_morefood:beans"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:raspberry_bush",
    new BushComponent("lpsm_morefood:raspberry"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:poison_berry_bush",
    new BushComponent("lpsm_morefood:poison_berries"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:soybean_bush",
    new BushComponent("lpsm_morefood:soybeans"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:strawberry_bush",
    new BushComponent("lpsm_morefood:strawberry"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:tea_bush",
    new BushComponent("lpsm_morefood:tea_leaves"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:tomato_bush",
    new BushComponent("lpsm_morefood:tomato"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:vanilla_bush",
    new BushComponent("lpsm_morefood:vanilla_pod"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pepper_bush",
    new BushComponent("lpsm_morefood:pepper"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:peppermint_bush",
    new BushComponent("lpsm_morefood:peppermint"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:coffee_bush",
    new BushComponent("lpsm_morefood:coffee_beans"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:cranberry_bush",
    new BushComponent("lpsm_morefood:cranberries"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:eggplant_bush",
    new BushComponent("lpsm_morefood:eggplant"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:gherkin_bush",
    new BushComponent("lpsm_morefood:gherkin"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:grape_bush",
    new BushComponent("lpsm_morefood:grape"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:blueberry_bush",
    new BushComponent("lpsm_morefood:blueberries"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_apple",
    new HangingCropComponent("minecraft:apple"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_orange",
    new HangingCropComponent("lpsm_morefood:orange"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_olive",
    new HangingCropComponent("lpsm_morefood:olives"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_lemon",
    new HangingCropComponent("lpsm_morefood:lemon"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_coconut",
    new HangingCropComponent("lpsm_morefood:coconut"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_cherry",
    new HangingCropComponent("lpsm_morefood:cherry"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_avocado",
    new HangingCropComponent("lpsm_morefood:avocado"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_banana",
    new HangingCropComponent("lpsm_morefood:banana"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_plum",
    new HangingCropComponent("lpsm_morefood:plum"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:hanging_almond",
    new HangingCropComponent("lpsm_morefood:almonds"),
  );
  registry.registerCustomComponent(CropComponent.typeId, new CropComponent());
  registry.registerCustomComponent(
    TallCropComponent.typeId,
    new TallCropComponent(),
  );
  registry.registerCustomComponent(SpileComponent.typeId, new SpileComponent());

  registry.registerCustomComponent(
    "lpsm_morefood:apple_sapling",
    new SaplingComponent(gen.APPLE_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:almond_sapling",
    new SaplingComponent(gen.ALMOND_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:avocado_sapling",
    new SaplingComponent(gen.AVOCADO_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:banana_sapling",
    new SaplingComponent(gen.BANANA_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:lemon_sapling",
    new SaplingComponent(gen.LEMON_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:olive_sapling",
    new SaplingComponent(gen.OLIVE_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:orange_sapling",
    new SaplingComponent(gen.ORANGE_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:palm_sapling",
    new SaplingComponent(gen.PALM_SAPLING),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:plum_sapling",
    new SaplingComponent(gen.PLUM_SAPLING),
  );

  const sapCauldron = new CauldronComponent();
  sapCauldron.addBucket("minecraft:bucket", "lpsm_morefood:maple_sap_bucket");
  registry.registerCustomComponent("lpsm_morefood:sap_cauldron", sapCauldron);

  // registerCakes(registry, "chocolate_cake");
  // registerCakes(registry, "rainbow_cake");
  // registerCakes(registry, "pound_cake");
  // registerCakes(registry, "redwhiteblue_cake");
  // registerCakes(registry, "cake_with_cherries");

  registry.registerCustomComponent(
    "lpsm_morefood:potted_almond_sapling",
    new PottedFlowerComponent("lpsm_morefood:almond_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_avocado_sapling",
    new PottedFlowerComponent("lpsm_morefood:avocado_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_lemon_sapling",
    new PottedFlowerComponent("lpsm_morefood:lemon_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_apple_sapling",
    new PottedFlowerComponent("lpsm_morefood:apple_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_banana_sapling",
    new PottedFlowerComponent("lpsm_morefood:banana_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_olive_sapling",
    new PottedFlowerComponent("lpsm_morefood:olive_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_orange_sapling",
    new PottedFlowerComponent("lpsm_morefood:orange_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_palm_sapling",
    new PottedFlowerComponent("lpsm_morefood:palm_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_plum_sapling",
    new PottedFlowerComponent("lpsm_morefood:plum_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_spearmint",
    new PottedFlowerComponent("lpsm_morefood:spearmint"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:potted_water_mint",
    new PottedFlowerComponent("lpsm_morefood:water_mint"),
  );
}

export function registerItemComponents(registry) {
  registry.registerCustomComponent(MintyComponent.typeId, new MintyComponent());
  registry.registerCustomComponent(
    "lpsm_morefood:bottled_beer",
    new PourableComponent("lpsm_morefood:beer_mug", "lpsm_morefood:beer"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:bottled_cider",
    new PourableComponent("lpsm_morefood:tumbler_glass", "lpsm_morefood:cider"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:bottled_red_wine",
    new PourableComponent("lpsm_morefood:wine_glass", "lpsm_morefood:red_wine"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:bottled_white_wine",
    new PourableComponent(
      "lpsm_morefood:wine_glass",
      "lpsm_morefood:white_wine",
    ),
  );
  registry.registerCustomComponent(MREComponent.typeId, new MREComponent());
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_almond_sapling",
    new PottableComponent("lpsm_morefood:potted_almond_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_avocado_sapling",
    new PottableComponent("lpsm_morefood:potted_avocado_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_lemon_sapling",
    new PottableComponent("lpsm_morefood:potted_lemon_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_apple_sapling",
    new PottableComponent("lpsm_morefood:potted_apple_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_banana_sapling",
    new PottableComponent("lpsm_morefood:potted_banana_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_olive_sapling",
    new PottableComponent("lpsm_morefood:potted_olive_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_orange_sapling",
    new PottableComponent("lpsm_morefood:potted_orange_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_palm_sapling",
    new PottableComponent("lpsm_morefood:potted_palm_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_plum_sapling",
    new PottableComponent("lpsm_morefood:potted_plum_sapling"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_spearmint",
    new PottableComponent("lpsm_morefood:potted_spearmint"),
  );
  registry.registerCustomComponent(
    "lpsm_morefood:pottable_water_mint",
    new PottableComponent("lpsm_morefood:potted_water_mint"),
  );
}
