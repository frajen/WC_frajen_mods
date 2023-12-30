from objectives.results._objective_result import *

class Field(field_result.Result):
    def src(self, item_id):
        return [
            field.AddItem(item_id),
        ]

class Battle(battle_result.Result):
    def src(self, item_id):
        return [
            battle_result.AddItem(item_id),
        ]

class Result(ObjectiveResult):
    NAME = "Better Tier Item"
    def __init__(self):
        import random
        from data.items import id_name as item_id_names
        ##BETTER_TIER = [
##    "Megalixir", "Hero Ring", "Merit Award", "Blizzard Orb",
##    "Czarina Gown", "Moogle Suit", "Nutkin Suit", "Red Jacket",
##    "Mirage Vest", "Tao Robe", "TortoiseShld", "Striker",
##    "Sniper", "Excalibur", "Stunner", "Wing Edge", "Doom Darts",
##]
        BETTER_TIER = [239, 201, 218, 197, 153, 159, 160, 147, 142, 151, 101, 41, 75, 24, 42, 76, 79]
        random_item = random.choice(BETTER_TIER)
        print("Better tier item: " + item_id_names[random_item])
        super().__init__(Field, Battle, random_item)
