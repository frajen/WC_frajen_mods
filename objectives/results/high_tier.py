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
    NAME = "High Tier Item"
    def __init__(self):
        import random
        from data.items import Items

        random_item = random.choice(Items.GOOD)

        # debug - show picked objective item
        print_debug = False
        if print_debug:
            from data.items import id_name as item_id_names        
            print("High tier item: " + item_id_names[random_item])
        
        super().__init__(Field, Battle, random_item)
