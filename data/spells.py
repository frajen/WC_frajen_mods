from data.spell import Spell
from data.spell_names import id_name, name_id
from data.ability_data import AbilityData
from data.structures import DataArray

class Spells:
    BLACK_MAGIC_COUNT = 24  #0 to 23
    EFFECT_MAGIC_COUNT = 21  #24 to 44
    WHITE_MAGIC_COUNT = 9  #45 to 53
    SPELL_COUNT = BLACK_MAGIC_COUNT + EFFECT_MAGIC_COUNT + WHITE_MAGIC_COUNT

    NAMES_START = 0x26f567
    NAMES_END = 0x26f6e0
    NAME_SIZE = 7

    ABILITY_DATA_START = 0x046ac0
    ABILITY_DATA_END = 0x046db3

    ### added to be able to mod all abilities in a single module
    ESPER_ABILITY_NAMES_START = 0x26FE8F
    ESPER_ABILITY_NAMES_END = 0x26FF9C
    ESPER_ABILITY_NAME_SIZE = 10
    ESPER_ABILITY_COUNT = 27

    OTHER_ABILITY_NAMES_START = 0x26F7B9
    OTHER_ABILITY_NAMES_END = 0x26FE8E
    OTHER_ABILITY_NAME_SIZE = 10
    OTHER_ABILITY_COUNT = 174

    SPELL_DATA_END = 0x0478BF

    # other addresses that might be useful
##    ABILITY_DATA_SIZE = 0xE  # equivalent to AbilityData.DATA_SIZE
    ESPER_ABILITY_DATA_START    = 0x046DB4    #27 espers
    ESPER_ABILITY_DATA_END      = 0x046F2D    #46DB4 + (0xE * 27) - 1
    SHADOW_SCROLLS_START        = 0x046F2E
##    SHADOW_SCROLLS_END          = 0X046F57
##    SWDTECH_DATA_START          = 0x046F66
##    SWDTECH_DATA_END            = 0x046FD5
##    BLITZ_DATA_START            = 0X046FD6
##    BLITZ_DATA_END              = 0X047053
##    DANCE_DATA_START            = 0X047054
##    DANCE_DATA_END              = 0X047195
##    MAGITEK_DATA_START          = 0X0471EA
##    MAGITEK_DATA_END            = 0X04724F
##    LORES_DATA_START            = 0X04725A
##    LORES_DATA_END              = 0X0X0479F
    OTHER_ABILITY_DATA_START    = 0x0473AA
    OTHER_ABILITY_DATA_END      = 0x0478BF

    ### added to be able to mod all abilities in a single module


    # (default) order spells appear in menu going left to right, top to bottom
    # put white magic before black and effect magic
    import itertools
    spell_menu_order = itertools.chain(range(45, 54), range(45))

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)

        self.ability_data = DataArray(self.rom, self.ABILITY_DATA_START, self.ABILITY_DATA_END, AbilityData.DATA_SIZE)
        self.spells = []
        for spell_index in range(len(self.name_data)):
            spell = Spell(spell_index, self.name_data[spell_index], self.ability_data[spell_index])
            self.spells.append(spell)


        ### WC typically likes to separate spells to their vanilla use function
        ### it may someday be desired to be able to randomize spells across use functions
        ### at minimum, these mods allow for name changes to Esper ability names and other spells
        # add Esper ability names
        self.esper_name_data = DataArray(self.rom, self.ESPER_ABILITY_NAMES_START, self.ESPER_ABILITY_NAMES_END, self.ESPER_ABILITY_NAME_SIZE)

        self.esper_ability_data = DataArray(self.rom, self.ESPER_ABILITY_DATA_START, self.ESPER_ABILITY_DATA_END, AbilityData.DATA_SIZE)
        self.esper_spells = []
        for spell_index in range(len(self.esper_name_data)):
            esper_spell = Spell(spell_index+54, self.esper_name_data[spell_index], self.esper_ability_data[spell_index])
            self.esper_spells.append(esper_spell)

        # add other spells
        self.other_ability_name_data = DataArray(self.rom, self.OTHER_ABILITY_NAMES_START, self.OTHER_ABILITY_NAMES_END, self.OTHER_ABILITY_NAME_SIZE)

        self.other_ability_data = DataArray(self.rom, self.SHADOW_SCROLLS_START, self.OTHER_ABILITY_DATA_END, AbilityData.DATA_SIZE)
        self.other_abilities = []
        for spell_index in range(len(self.other_ability_name_data)):
            other_spell = Spell(spell_index+81, self.other_ability_name_data[spell_index], self.other_ability_data[spell_index])
            self.other_abilities.append(other_spell)

        # for debugging: verify which abilities have been read in
##        for ability in self.spells:
##                print(ability.name + " | " + str(ability.targets) + " | " + str(ability.elements) +
##        " | " + str(ability.flags1) + " | " + str(ability.flags2) + " | " + str(ability.flags3) +
##        " | " + str(ability.mp) + " | " + str(ability.power) + " | " + str(ability.flags4) + 
##        " | " + str(ability.accuracy) + " | " + str(ability.effect) + " | " + str(ability.status1) + 
##        " | " + str(ability.status2) + " | " + str(ability.status3) + " | " + str(ability.status4))
        ### mod to read in all spells, not just black/white/effect


    def get_id(self, name):
        return name_id[name]

    def get_name(self, id):
        if id == 0xff:
            return ""
        return self.spells[id].get_name()

    def get_random(self, count = 1, exclude = None):
        if exclude is None:
            exclude = []

        import random
        possible_spell_ids = [spell.id for spell in self.spells if spell.id not in exclude]
        count = min(len(possible_spell_ids), count)
        return random.sample(possible_spell_ids, count)

    ### returns a spell based on the tiering system for Random Tiered Espers
    ### there could be other conceptions of this idea using something more
    ### akin to a ranked spell list instead of spell frequency buckets
    def get_random_tiered(self, count = 1, exclude = None):
        import random
        def get_spell():
            from data.esper_spell_tiers import tiers, weights, tier_s_distribution
            from utils.weighted_random import weighted_random

            random_tier = weighted_random(weights)
            if random_tier < len(weights) - 1: # not s tier, use equal distribution
                random_tier_index = random.randrange(len(tiers[random_tier]))
                return tiers[random_tier][random_tier_index]

            weights = [entry[1] for entry in tier_s_distribution]
            random_s_index = weighted_random(weights)
            return tier_s_distribution[random_s_index][0]

        if exclude is None:
            exclude = []

        x = 0
        spell_list = []
        for x in range(count):
            tiered_spell = get_spell()  #get a random tiered spell
            #loop if excluded, or in existing spell list
            while ((tiered_spell in exclude) or
                    (tiered_spell in spell_list)):  
                tiered_spell = get_spell()
            spell_list.append(tiered_spell)
        return spell_list
    ### end of mod for random tiered spell  

    def get_replacement(self, spell_id, exclude):
        ''' get a random spell from the same tier as the given spell_id '''
        import random
        from data.esper_spell_tiers import tiers

        same_tier = next((tier for tier in tiers if spell_id in tier), [])
        replacements = [i for i in same_tier if i not in exclude]
        replacement = random.choice(replacements) if len(replacements) else None
        return replacement

    def no_mp_scan(self):
        scan_id = name_id["Scan"]
        self.spells[scan_id].mp = 0

    def no_mp_warp(self):
        warp_id = name_id["Warp"]
        self.spells[warp_id].mp = 0

    def ultima_254_mp(self):
        ultima_id = name_id["Ultima"]
        self.spells[ultima_id].mp = 254

    def shuffle_mp(self):
        mp = []
        for spell in self.spells:
            mp.append(spell.mp)

        import random
        random.shuffle(mp)
        for spell in self.spells:
            spell.mp = mp.pop()

    def random_mp_value(self):
        import random
        for spell in self.spells:
            spell.mp = random.randint(self.args.magic_mp_random_value_min, self.args.magic_mp_random_value_max)

    def random_mp_percent(self):
        import random
        for spell in self.spells:
            mp_percent = random.randint(self.args.magic_mp_random_percent_min,
                                        self.args.magic_mp_random_percent_max) / 100.0
            value = int(spell.mp * mp_percent)
            spell.mp = max(min(value, 254), 0)

    def mod(self):
        if self.args.magic_mp_shuffle:
            self.shuffle_mp()
        elif self.args.magic_mp_random_value:
            self.random_mp_value()
        elif self.args.magic_mp_random_percent:
            self.random_mp_percent()

        # Apply No MP Scan after any MP shuffle/rando
        if self.args.scan_all:
            self.no_mp_scan()
        if self.args.warp_all:
            self.no_mp_warp()

        # Apply Ultima 254 MP after any MP shuffle/rando
        if self.args.ultima_254_mp:
            self.ultima_254_mp()

    def write(self):
        if self.args.spoiler_log:
            self.log()
            
        for spell_index, spell in enumerate(self.spells):
            self.name_data[spell_index] = spell.name_data()
            self.ability_data[spell_index] = spell.ability_data()

        ### because the Espers mod is run after this (Spells) mod,
        ### changes to Esper ability data will be overwritten in data\espers.py
        ### changes can be made by a per-Esper basis
        ### see the following example for Phoenix:        
    ##    # change phoenix behavior to cast life 3 on party instead of life
    ##        self.espers[self.PHOENIX].flags1 = 0
    ##        self.espers[self.PHOENIX].flags3 = 0x20
    ##        self.espers[self.PHOENIX].power = 0
    ##        self.espers[self.PHOENIX].status1 = 0
    ##        self.espers[self.PHOENIX].status4 = 0x04
        ### note that changing the ability name (e.g. "Bolt Fist" for Ramuh) still works here
        for spell_index, spell in enumerate(self.esper_spells):
            self.esper_name_data[spell_index] = spell.esper_name_data()
            self.esper_ability_data[spell_index] = spell.ability_data()
        self.esper_name_data.write()
        self.esper_ability_data.write()

        ### Similarly, other modules will overwrite numeric changes done here for specific abilities
        ### Shadow's throws, Storm, Swdtech, Magitek, Lores will be overwritten by other modules
        ### Blitz, Dance, Slots, Shock, and other abilities can be changed
        ### Name changes will work for everything but Magitek and Lores
        ### (there is a bug with 12 extra spells after Lores being read by data\lores.py        
        for spell_index, spell in enumerate(self.other_abilities):
            self.other_ability_name_data[spell_index] = spell.other_ability_name_data()
            self.other_ability_data[spell_index] = spell.ability_data()
        self.other_ability_name_data.write()
        self.other_ability_data.write()
        
        self.name_data.write()
        self.ability_data.write()

    def log(self):
        from log import section
        
        lcolumn = []
        for spell in self.spells:
            spell_name = spell.get_name()

            lcolumn.append(f"{spell_name:<{self.NAME_SIZE}} {spell.mp:>3} MP")
        
        section("Spells", lcolumn, [])

    def print(self):
        for spell in self.spells:
            spell.print()
