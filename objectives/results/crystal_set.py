from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

class Field(field_result.Result):
    def src(self):
        return [
            field.AddItem(item_name_id["Crystal Mail"]),
            field.AddItem(item_name_id["Crystal Shld"]),
            field.AddItem(item_name_id["Crystal Helm"]),
            field.AddItem(item_name_id["Crystal"]),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            battle_result.AddItem(item_name_id["Crystal Mail"]),
            battle_result.AddItem(item_name_id["Crystal Shld"]),
            battle_result.AddItem(item_name_id["Crystal Helm"]),
            battle_result.AddItem(item_name_id["Crystal"]),
        ]

class Result(ObjectiveResult):
    NAME = "Crystal Set"
    def __init__(self):
        super().__init__(Field, Battle)
