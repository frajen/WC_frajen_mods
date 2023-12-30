from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

class Field(field_result.Result):
    def src(self):
        return [
            field.AddItem(item_name_id["Gold Lance"]),
            field.AddItem(item_name_id["Gold Armor"]),
            field.AddItem(item_name_id["Gold Shld"]),
            field.AddItem(item_name_id["Gold Helmet"]),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            battle_result.AddItem(item_name_id["Gold Lance"]),
            battle_result.AddItem(item_name_id["Gold Armor"]),
            battle_result.AddItem(item_name_id["Gold Shld"]),
            battle_result.AddItem(item_name_id["Gold Helmet"]),
        ]

class Result(ObjectiveResult):
    NAME = "Gold Set"
    def __init__(self):
        super().__init__(Field, Battle)
