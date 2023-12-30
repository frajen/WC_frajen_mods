from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

HAT_TRICK_GREEN = ["Green Beret", "Green Beret", "Green Beret"]
HAT_TRICK_BARD = ["Bard's Hat", "Bard's Hat", "Bard's Hat"]

HAT_TRICK_GREEN_IDS = [item_name_id[item_name] for item_name in HAT_TRICK_GREEN]
HAT_TRICK_BARD_IDS = [item_name_id[item_name] for item_name in HAT_TRICK_BARD]

class Field(field_result.Result):
    def src(self):
        src = []
        import random
        green = random.randint(0, 1)
        if green == 1:
            for item_id in HAT_TRICK_GREEN_IDS:
                src += [
                    field.AddItem(item_id),
                ]
        else:
            for item_id in HAT_TRICK_BARD_IDS:
                src += [
                    field.AddItem(item_id),
                ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        import random
        green = random.randint(0, 1)
        if green == 1:
            for item_id in HAT_TRICK_GREEN_IDS:
                src += [
                    battle_result.AddItem(item_id),
                ]
        else:
            for item_id in HAT_TRICK_BARD_IDS:
                src += [
                    battle_result.AddItem(item_id),
                ]
        return src

class Result(ObjectiveResult):
    NAME = "Hat Trick Kit"
    def __init__(self):
        super().__init__(Field, Battle)
