from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

class Field(field_result.Result):
    def src(self):
        return [
            field.AddItem(item_name_id["ThunderBlade"]),
            field.AddItem(item_name_id["Flame Sabre"]),
            field.AddItem(item_name_id["Blizzard"]),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            battle_result.AddItem(item_name_id["ThunderBlade"]),
            battle_result.AddItem(item_name_id["Flame Sabre"]),
            battle_result.AddItem(item_name_id["Blizzard"]),
        ]

class Result(ObjectiveResult):
    NAME = "Elemental Swords"
    def __init__(self):
        super().__init__(Field, Battle)
