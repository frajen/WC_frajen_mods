from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

### 6 of consumable items
FULL_STARTER = ["Heal Rod", "Megalixir", "Super Ball", "Elixir", "Dried Meat", "X-Ether", "X-Potion",
                "Ether", "Tent", "Remedy", "Sleeping Bag", "Warp Stone", "Fenix Down",
                "Smoke Bomb", "Antidote", "Bolt Edge", "Echo Screen", "Eyedrop",
                "Fire Skean", "Green Cherry", "Inviz Edge", "Magicite", "Potion",
                "Rename Card", "Revivify", "Shadow Edge", "Soft", "Tincture", "Tonic",
                "Water Edge",
                "Megalixir", "Super Ball", "Elixir", "Dried Meat", "X-Ether", "X-Potion",
                "Ether", "Tent", "Remedy", "Sleeping Bag", "Warp Stone", "Fenix Down",
                "Smoke Bomb", "Antidote", "Bolt Edge", "Echo Screen", "Eyedrop",
                "Fire Skean", "Green Cherry", "Inviz Edge", "Magicite", "Potion",
                "Rename Card", "Revivify", "Shadow Edge", "Soft", "Tincture", "Tonic",
                "Water Edge",
                "Megalixir", "Super Ball", "Elixir", "Dried Meat", "X-Ether", "X-Potion",
                "Ether", "Tent", "Remedy", "Sleeping Bag", "Warp Stone", "Fenix Down",
                "Smoke Bomb", "Antidote", "Bolt Edge", "Echo Screen", "Eyedrop",
                "Fire Skean", "Green Cherry", "Inviz Edge", "Magicite", "Potion",
                "Rename Card", "Revivify", "Shadow Edge", "Soft", "Tincture", "Tonic",
                "Water Edge",
                "Megalixir", "Super Ball", "Elixir", "Dried Meat", "X-Ether", "X-Potion",
                "Ether", "Tent", "Remedy", "Sleeping Bag", "Warp Stone", "Fenix Down",
                "Smoke Bomb", "Antidote", "Bolt Edge", "Echo Screen", "Eyedrop",
                "Fire Skean", "Green Cherry", "Inviz Edge", "Magicite", "Potion",
                "Rename Card", "Revivify", "Shadow Edge", "Soft", "Tincture", "Tonic",
                "Water Edge",
                "Megalixir", "Super Ball", "Elixir", "Dried Meat", "X-Ether", "X-Potion",
                "Ether", "Tent", "Remedy", "Sleeping Bag", "Warp Stone", "Fenix Down",
                "Smoke Bomb", "Antidote", "Bolt Edge", "Echo Screen", "Eyedrop",
                "Fire Skean", "Green Cherry", "Inviz Edge", "Magicite", "Potion",
                "Rename Card", "Revivify", "Shadow Edge", "Soft", "Tincture", "Tonic",
                "Water Edge",
                "Megalixir", "Super Ball", "Elixir", "Dried Meat", "X-Ether", "X-Potion",
                "Ether", "Tent", "Remedy", "Sleeping Bag", "Warp Stone", "Fenix Down",
                "Smoke Bomb", "Antidote", "Bolt Edge", "Echo Screen", "Eyedrop",
                "Fire Skean", "Green Cherry", "Inviz Edge", "Magicite", "Potion",
                "Rename Card", "Revivify", "Shadow Edge", "Soft", "Tincture", "Tonic",
                "Water Edge"]

FULL_STARTER_IDS = [item_name_id[item_name] for item_name in FULL_STARTER]

class Field(field_result.Result):
    def src(self):
        src = []
        for item_id in FULL_STARTER_IDS:
            src += [
                field.AddItem(item_id),
            ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id in FULL_STARTER_IDS:
            src += [
                battle_result.AddItem(item_id),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Full Starter Kit"
    def __init__(self):
        super().__init__(Field, Battle)
