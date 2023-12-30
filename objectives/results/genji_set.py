from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

class Field(field_result.Result):
    def src(self):
        return [
            field.AddItem(item_name_id["Genji Armor"]),
            field.AddItem(item_name_id["Genji Shld"]),
            field.AddItem(item_name_id["Genji Helmet"]),
            field.AddItem(item_name_id["Genji Glove"]),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            battle_result.AddItem(item_name_id["Genji Armor"]),
            battle_result.AddItem(item_name_id["Genji Shld"]),
            battle_result.AddItem(item_name_id["Genji Helmet"]),
            battle_result.AddItem(item_name_id["Genji Glove"]),
        ]

class Result(ObjectiveResult):
    NAME = "Genji Set"
    def __init__(self):
        super().__init__(Field, Battle)
