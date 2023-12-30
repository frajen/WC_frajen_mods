from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

### 6 of consumable items
BASIC_STARTER = ["Tonic", "Tonic", "Tonic", "Tonic", "Tonic", "Tonic", "Tonic", "Tonic", "Tonic", "Tonic",
                "Potion", "Potion", "Potion", "Potion", "Potion", "Potion", "Potion", "Potion", "Potion",
                "Sleeping Bag", "Sleeping Bag", "Sleeping Bag", "Sleeping Bag", "Sleeping Bag", "Sleeping Bag",
                "Sleeping Bag", "Sleeping Bag", "Sleeping Bag", "Sleeping Bag", "Sleeping Bag", "Sleeping Bag",
                "Tent", "Dried Meat",
                 "Rename Card", "Rename Card", "Rename Card", "Rename Card", "Rename Card", "Rename Card",
                 "Rename Card", "Rename Card", "Rename Card", "Rename Card", "Rename Card", "Rename Card",
                 "Rename Card", "Rename Card"]

BASIC_STARTER_IDS = [item_name_id[item_name] for item_name in BASIC_STARTER]

class Field(field_result.Result):
    def src(self):
        src = []
        for item_id in BASIC_STARTER_IDS:
            src += [
                field.AddItem(item_id),
            ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id in BASIC_STARTER_IDS:
            src += [
                battle_result.AddItem(item_id),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Basic Starter Kit"
    def __init__(self):
        super().__init__(Field, Battle)
