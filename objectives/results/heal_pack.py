from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

ITEM_COUNT = 255

class Field(field_result.Result):
    def src(self, item_list):
        src = []
        for x in range(ITEM_COUNT):
            src += [
                field.AddItem(item_name_id[item_list[x]]),
            ]
        return src

class Battle(battle_result.Result):
    def src(self, item_list):
        src = []
        for x in range(ITEM_COUNT):
            src += [
                battle_result.AddItem(item_name_id[item_list[x]]),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Heal Pack"
    def __init__(self):        
        from data.item_names import name_id
        from data.item_names import id_name
        import random
        id_list = []
        item_list = []
##        items = ["Tonic", "Potion", "X-Potion", "Tincture", "Ether", _
##                 "X-Ether", "Elixir", "Megalixir", "Fenix Down", "Revivify", _
##                 "Antidote", "Eyedrop", "Soft", "Remedy", "Sleeping Bag", _
##                 "Tent", "Green Cherry", "Echo Screen"]        
        tiers = [
            [ # 25%
                name_id["Potion"],
            ],
            [ # 10%
                name_id["Ether"],
                name_id["Fenix Down"],
                name_id["Sleeping Bag"],
            ],
            [ # 6%
                name_id["Tincture"],
            ],
            [ # 5%
                name_id["Tonic"],
                name_id["X-Potion"],
                name_id["Elixir"],
                name_id["Revivify"],
                name_id["Remedy"],
                name_id["Tent"],
            ],
            [ # 3.5%
                name_id["X-Ether"],
            ],
            [ # 1%
                name_id["Antidote"],
                name_id["Echo Screen"],
                name_id["Eyedrop"],
                name_id["Green Cherry"],
                name_id["Soft"],
              ],
            [ # 0.5%
                name_id["Megalixir"],
            ],
        ]
        item_weights = [0.25, 0.1, 0.06, 0.05, 0.035, 0.01, 0.005]
        from utils.weighted_random import weighted_random

        for _ in range(ITEM_COUNT):
            random_tier = weighted_random(item_weights)
            random_tier_index = random.randrange(len(tiers[random_tier]))
            selection = tiers[random_tier][random_tier_index]
            id_list.append(selection)
            item_list.append(id_name[selection])

        #print(id_list)
        #print(item_list)

        super().__init__(Field, Battle, item_list)
