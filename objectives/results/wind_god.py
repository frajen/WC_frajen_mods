from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

class Field(field_result.Result):
    def src(self):
        return [
            field.AddItem(item_name_id["Tempest"]),
            field.AddItem(item_name_id["Offering"]),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            battle_result.AddItem(item_name_id["Tempest"]),
            battle_result.AddItem(item_name_id["Offering"]),
        ]

class Result(ObjectiveResult):
    NAME = "Wind God"
    def __init__(self):
        super().__init__(Field, Battle)
