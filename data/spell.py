from data.ability_data import AbilityData
import data.text as text

class Spell(AbilityData):
    def __init__(self, id, name_data, ability_data):
        super().__init__(id, ability_data)

        self.id = id
        self.name = text.get_string(name_data, text.TEXT2).rstrip('\0')

    def name_data(self):
        from data.spells import Spells
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Spells.NAME_SIZE - len(data)))
        return data

    def get_name(self):
        name = self.name
        first_pos = name.find('<')
        while first_pos >= 0:
            second_pos = name.find('>')
            name = name.replace(name[first_pos:second_pos + 1], "")
            first_pos = name.find('<')
        return name.strip('\0')

    def print(self):
        print(f"{self.id} {self.get_name()}")

    # Added to be able to modify non black/white/effect magic
    # Requires adding ESPER_ATTACK_NAME_SIZE and OTHER_ABILITY_NAME_SIZE in data\spells.py
    def esper_name_data(self):
        from data.spells import Spells
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Spells.ESPER_ABILITY_NAME_SIZE - len(data)))
        return data

    def other_ability_name_data(self):
        from data.spells import Spells
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Spells.OTHER_ABILITY_NAME_SIZE - len(data)))
        return data
    # Added to be able to modify non black/white/effect magic
