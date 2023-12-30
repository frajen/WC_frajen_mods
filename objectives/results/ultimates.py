from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

#Ultimate weapons
#ULTS = ["RegalCutlass", "Crystal", "Stout Spear", "Mithril Claw", "Kodachi", "Kotetsu", "Forged", "Darts", "Epee", "Punisher", "DaVinci Brsh", "Boomerang"]

#Ultimate items (includes Gau's Dueling Mask (Iron Helmet) and Umaro's Bone Wrist (Charm Bangle)
ULTS = ["RegalCutlass", "Crystal", "Stout Spear", "Mithril Claw",
        "Kodachi", "Kotetsu", "Forged", "Darts", "Epee", "Punisher",
        "DaVinci Brsh", "Boomerang", "Iron Helmet", "Charm Bangle"]
ULT_IDS = [item_name_id[item_name] for item_name in ULTS]

class Field(field_result.Result):
    def src(self):
        src = []
        for item_id in ULT_IDS:
            src += [
                field.AddItem(item_id),
            ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id in ULT_IDS:
            src += [
                battle_result.AddItem(item_id),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Ultimate Items"
    def __init__(self):
        super().__init__(Field, Battle)
