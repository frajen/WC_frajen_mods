from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id


class Field(field_result.Result):
    def src(self, shield):
        return [
            field.AddItem(item_name_id[shield]),
        ]

class Battle(battle_result.Result):
    def src(self, shield):
        return [
            battle_result.AddItem(item_name_id[shield]),
        ]

class Result(ObjectiveResult):
    NAME = "Elemental Shield"
    def __init__(self):
        import random
        shields = ["Flame Shld", "Ice Shld", "Thunder Shld"]
        shield = random.choice(shields)
        super().__init__(Field, Battle, shield)
