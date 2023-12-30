import args, random
from data.item import Item

from constants.items import good_items
from constants.items import id_name, name_id

import data.items_asm as items_asm

# Mod for item descriptions
from data.structures import DataBits, DataArray, DataList

# Mod for ultimate items
import data.text as text
from data.text.text3 import text_value, value_text
ULTS_ID = [11, 20, 44, 38, 31, 84, 45, 59, 62, 78, 16, 111, 71, 223]


class Items():
    # For logging randomized item spells and stats
    TOLOG = ""
    STATLOG = ""
    
    ITEM_COUNT = 256
    EMPTY = 0xff # item 255 is empty

    BREAKABLE_RODS = range(53, 59)
    ELEMENTAL_SHIELDS = range(96, 99)

    ### Mod for ultimate items, reference list: 11, 20, 31, 84, 38, 44, 45, 78, 16, 59, 62, 71, 111, 223
    ULTS = ["RegalCutlass", "Crystal", "Kotetsu", "Kodachi", "Stout Spear", "Mithril Claw",
            "Forged", "Punisher", "DaVinci Brsh", "Darts", "Epee", "Iron Helmet", 
            "Boomerang", "Charm Bangle"]
    #TERRA, LOCKE, CYAN, SHADOW 0-3
    #EDGAR, SABIN, CELES, STRAGO, RELM 4-8
    #SETZER, MOG, GAU, GOGO, UMARO 9-13
    #RegalCutlass -> Apocalypse, Terra
    #Crystal -> ZwillXBlade, Locke
    #Kotetsu -> Zanmato, Cyan
    #Kodachi -> Oborozuki, Shadow
    #Stout Spear -> Longinus, Edgar
    #Mithril Claw -> Godhand, Sabin
    #Forged -> SaveTheQueen, Celes
    #Punisher -> Stardust Rod, Strago
    #DaVinci Brsh -> Angel Brush, Relm
    #Darts -> Final Trump, Setzer
    #Epee -> Gungnir, Mog
    #Iron Helmet -> Dueling Mask, Gau
    #Boomerang -> ScorpionTail, Gogo
    #Charm Bangle -> Bone Wrist, Umaro

    GOOD = [name_id[name] for name in good_items]
    if args.stronger_atma_weapon:
        GOOD.append(name_id["Atma Weapon"])
    if args.no_free_paladin_shields:
        GOOD.remove(name_id["Paladin Shld"])
    if args.no_exp_eggs:
        GOOD.remove(name_id["Exp. Egg"])
    if args.no_illuminas:
        GOOD.remove(name_id["Illumina"])

    ### Remove GOOD items here if desired:
    #GOOD.remove(name_id["ValiantKnife"])
    #GOOD.remove(name_id["Illumina"])
    #GOOD.remove(name_id["Ragnarok"])
    #GOOD.remove(name_id["Aura Lance"])
    #GOOD.remove(name_id["Magus Rod"])
    #GOOD.remove(name_id["Fixed Dice"])        

    # Mod for item descriptions
    ITEM_DESCRIPTION_PTR_START = 0x2D7AA0
    ITEM_DESCRIPTION_PTR_END = 0x2D7C9F
    ITEM_DESCRIPTION_START = 0x2D6400
    ITEM_DESCRIPTION_END = 0x2D779F

    def __init__(self, rom, args, dialogs, characters):
        self.rom = rom
        self.args = args
        self.dialogs = dialogs
        self.characters = characters

        self.read()

    def read(self):
        self.items = []
        self.type_items = {Item.TOOL : [], Item.WEAPON : [], Item.ARMOR : [],
                           Item.SHIELD : [], Item.HELMET : [], Item.RELIC : [], Item.ITEM : []}

        # Mod for descriptions
        self.desc_data = DataList(self.rom, self.ITEM_DESCRIPTION_PTR_START, self.ITEM_DESCRIPTION_PTR_END,
                                    self.rom.SHORT_PTR_SIZE, self.ITEM_DESCRIPTION_START,
                                    self.ITEM_DESCRIPTION_START, self.ITEM_DESCRIPTION_END)                

        for item_index in range(self.ITEM_COUNT):
            #item = Item(item_index, self.rom)
            # Mod for descriptions
            item = Item(item_index, self.rom, self.desc_data[item_index])

            self.items.append(item)

            if item.id != self.EMPTY:
                self.type_items[item.type].append(item)

    ### Mod for item descriptions
    def adjust_item_descriptions(self):
        from data.item_shortened_descriptions import id_desc
        for item in self.items:
            if item.id in id_desc.keys():
                item.desc = id_desc[item.id] + "<end>"

    def equipable_random(self, type_condition, rand_min, rand_max):
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                item.remove_all_equipable_characters()
                num_chars = random.randint(rand_min, rand_max)
                rand_chars = random.sample(self.characters.playable, num_chars)
                for character in rand_chars:
                    item.add_equipable_character(character)

    def equipable_balanced_random(self, type_condition, characters_per_item):
        # assign each item satisfying given type_condition exactly characters_per_item unique characters
        # the total number of items each character can equip should also be balanced
        # e.g. given 160 equipable items and 3 characters_per_item:
        #      160 * 3 = 480 total equipable slots to assign, the 3 characters should be unique for each item
        #      480 // 14 = 34, each character can equip 34 different items
        #      480  % 14 = 4, 4 characters can equip 1 additional item (35 items total for those 4)

        from data.characters import Characters
        possible_characters = list(range(Characters.CHARACTER_COUNT))
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                item.remove_all_equipable_characters()

                if len(possible_characters) < characters_per_item:
                    # fewer possibilities left than number of characters needed for each item
                    character_group = possible_characters # add remaining possible characters to current group
                    possible_characters = list(range(Characters.CHARACTER_COUNT)) # add all characters back into pool

                    # select characters at random from possible pool until
                    # character_group contains characters_per_item unique characters
                    while len(character_group) < characters_per_item:
                        candidate = random.choice(possible_characters)
                        if candidate not in character_group:
                            character_group.append(candidate)
                            possible_characters.remove(candidate)

                    # assign character group to current item
                    for character in character_group:
                        item.add_equipable_character(self.characters.playable[character])
                else:
                    character_group = random.sample(possible_characters, characters_per_item)
                    for character in character_group:
                        possible_characters.remove(character)
                        item.add_equipable_character(self.characters.playable[character])

    def equipable_original_random(self, type_condition, percent):
        if percent == 0:
            return

        from data.characters import Characters
        percent = percent / 100.0
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                for character in self.characters.playable:
                    if percent < 0 and item.equipable_by(character) and random.random() < -percent:
                        item.remove_equipable_character(character)
                    elif percent > 0 and not item.equipable_by(character) and random.random() < percent:
                        item.add_equipable_character(character)

    def equipable_shuffle_random(self, type_condition, percent):
        from data.characters import Characters
        equipable = [[] for _ in range(Characters.CHARACTER_COUNT)]
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                for character in range(Characters.CHARACTER_COUNT):
                    if item.equipable_by(self.characters.playable[character]):
                        equipable[character].append(item)
                item.remove_all_equipable_characters()

        random.shuffle(equipable)

        for character in range(Characters.CHARACTER_COUNT):
            for item in equipable[character]:
                item.add_equipable_character(self.characters.playable[character])

        self.equipable_original_random(type_condition, percent)

    def moogle_charm_all(self):
        # make moogle charm equipable by everyone
        moogle_charm = self.items[name_id["Moogle Charm"]]
        for character in self.characters.playable:
            moogle_charm.add_equipable_character(character)

    def swdtech_runic_all(self):
        for item in self.items:
            if item.type == Item.WEAPON:
                item.enable_swdtech = 1
                item.enable_runic = 1

    def prevent_atma_weapon_rage(self):
        # prevent atma weapon from being equipped by anyone with rage to avoid bug
        rage_characters = self.characters.get_characters_with_command("Rage")
        atma_weapon = self.items[name_id["Atma Weapon"]]
        for character in rage_characters:
            atma_weapon.remove_equipable_character(self.characters.playable[character])

    def get_price(self, id):
        return self.items[id].price

    def random_prices_value(self):
        for item in self.items:
            item.price = random.randint(self.args.shop_prices_random_value_min,
                                        self.args.shop_prices_random_value_max)

    def random_prices_percent(self):
        for item in self.items:
            price_percent = random.randint(self.args.shop_prices_random_percent_min,
                                           self.args.shop_prices_random_percent_max) / 100.0
            value = int(item.price * price_percent)
            item.price = max(min(value, 2**16 - 1), 0)

    def expensive_breakable_rods(self):
        self.items[name_id["Poison Rod"]].scale_price(3)
        self.items[name_id["Fire Rod"]].scale_price(4)
        self.items[name_id["Ice Rod"]].scale_price(4)
        self.items[name_id["Thunder Rod"]].scale_price(4)
        self.items[name_id["Gravity Rod"]].scale_price(1.2)
        self.items[name_id["Pearl Rod"]].scale_price(1.2)

    def expensive_super_balls(self):
        self.items[name_id["Super Ball"]].scale_price(2)

    def assign_values(self):
        from data.item_custom_values import custom_values
        for item in self.items:
            if item.id in custom_values:
                item.price = custom_values[item.id]

    def remove_learnable_spell(self, spell):
        for item in self.items:
            if item.learnable_spell == spell:
                item.remove_learnable_spell()

    def moogle_starting_equipment(self):
        # Give the moogles in Moogle Defense starting armor and helmets. Keeping vanilla weapons
        from data.shop_item_tiers import tiers
        from data.item import Item
        from data.characters import Characters

        for index in range(Characters.FIRST_MOOGLE, Characters.LAST_MOOGLE + 1):
            self.characters.characters[index].init_body = random.choice(tiers[Item.ARMOR][1])
            self.characters.characters[index].init_head = random.choice(tiers[Item.HELMET][1])

    ### Mod to have items randomly teach spells
    def randomize_item_learnables_spells(self, chance_to_learn=0):
        if chance_to_learn == 0:
            exit
        print_debug = False
        from data.spell_names import id_name as spell_id_names
        from data.spell_names import name_id as spell_name_id

        if print_debug:
            from data.spell import get_name as spell_get_name
            print(spell_id_names)
            print(spell_id_names[0])
        
        #LEARN_RATES = [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 16, 20]
        LEARN_RATES = [1, 2, 3, 4, 5]  #reduce learn rates

        original_good = self.GOOD
        picked_spells = []
        picked_items = []
        best_items = []
        for item in self.items:
            # BLACK_MAGIC_COUNT = 24  #0 to 23
            # EFFECT_MAGIC_COUNT = 21  #24 to 44
            # WHITE_MAGIC_COUNT = 9  #45 to 53
            # best spells:  5-7 (lvl 2's), 8 (Bio), 9-11 (lvl 3's), 14 (Pearl), 15 (Flare), 18 (X-Zone), 19 (Meteor), 21 (Quake), 23 (Merton)
            # 27 (Mute), 32 (Stop), 33 (Bserk), 41 (Osmose), 43 (Quick),
            # 46, 47, 48, 49,  (Cure2/3, Life/Life 2), 51 (Remedy), 53 (Life 3)
            #best_spells = [5, 6, 7, 8, 9, 10, 11, 14, 15, 18, 19, 21, 23, 27, 32, 33, 41, 43, 46, 47, 48, 49, 51, 53]
            # make it easier to find lvl 2's and Remedy on random items

            #best_spells = [8, 9, 10, 11, 14, 15, 18, 19, 21, 23, 27, 32, 33, 41, 43, 46, 47, 48, 49, 53]
            # ^ original best_spells ^
            best_spells = [9, 10, 11, 15, 23, 43, 53]

            # if item is not part of the high tier item list and the item doesn't naturally have a learn rate
            # weapons detail page can't show spells that teach stuff
            if ((item.id not in original_good) and (item.learnable_spell_rate == 0) and
                (item.id > 89) and ((item.id < 163) or (item.id > 176)) and (item.id != 222) and (item.id < 230)):
                # if item is selected to randomly learn
                if random.randint(1, 100) <= chance_to_learn:
                    # pick a spell
                    selected_spell = random.randint(0,53)

                    ### need to update this section for new spell exclusion lists
                    # no Ultimas
                    if self.args.no_ultima:
                        while selected_spell == 20:
                            selected_spell = random.randint(0,53)
                    # if spell has already been selected, 50% chance to pick another one
                    if selected_spell in picked_spells and len(picked_spells) < 53:
                        if random.randint(1,2) == 1:
                            while selected_spell not in picked_spells:
                                selected_spell = random.randint(0,53)
                                if self.args.no_ultima:
                                    while selected_spell == 20:
                                        selected_spell = random.randint(0,53)
                    
                    item.learnable_spell = selected_spell
                    item.learnable_spell_rate = random.choice(LEARN_RATES)
                    picked_spells.append(selected_spell)

                    # reset picked spells if all have been exhausted
                    if len(picked_spells) >= 53:
                        picked_spells = []

                    picked_items.append(item)
                    if selected_spell in best_spells:
                        best_items.append(item)

                    if print_debug:
                        print(str(item.name) + " | " + str(spell_id_names[selected_spell]) + ": x" + str(item.learnable_spell_rate))

                    if (selected_spell != 20 and self.args.no_ultima) or (not self.args.no_ultima):
                        self.TOLOG = self.TOLOG + "\n" + (str(item.name) + " | " + str(spell_id_names[selected_spell]) + ": x" + str(item.learnable_spell_rate))
                    item.write()

                    # name modifier
                    # remove spaces if the name is going to chop off the last letter to add the X
                    if len(item.name) == 12 and (item.name.find(" ") != -1):
                        splititemname = item.name.split(" ")
                        if print_debug:
                            print(splititemname)
                        item.name = ""
                        for x in range(len(splititemname)):
                            item.name = item.name + splititemname[x]
                        if print_debug:
                            print(item.name)

                    item.name = item.name[:11] + 'X'    #append X to item name if it teaches a spell
                    
                    # update price
                    price_boost = random.randint(50, 200) / 100
                    value = int(item.price * (1 + price_boost))
                    item.price = min(value, 2**16 - 1)

                    #replace item description with new one
                    item.desc = "L: " + str(spell_id_names[selected_spell]) + " x" + str(item.learnable_spell_rate) + "<end>"
                    
                # end of add spell chance
            # end of check for item with learn rate

        if print_debug:
            print(best_items)
        ##### getting self.GOOD = [] forces a complete reset of the high tier item pool when used from data/items.py
        #self.GOOD = []
        #for items in best_items:
            #self.GOOD.append(items.id)
            
    ### End of: Mod to have items randomly teach spells

    ### add section to check if item descriptions are too long, and add newline if so

    ### Mod to randomize item stats
    def randomize_stats(self,chance_to_mod=0):
        if chance_to_mod == 0:
            exit

        print_debug = False            
        from constants.items import good_items

        for item in self.items:
            item_changed = False
            item_changes = ""
            itemrank_modifier = 0
            ### skip: Shuriken, Ninja/Tack Star, Cursed Shld, Empty
            ### Tools (Item Type 0), Throws (Item Type 6)
            if ((item.name not in good_items) and item.id != 65 and item.id != 66 and item.id != 67 and
                item.id != 102 and item.id != 255 and item.type != 0 and item.type != 6):
                if random.randint(1, 100) <= chance_to_mod:
                    #item.vigor = max(min(item.vigor + random.randint(1, 5), 7), item.vigor)
                    item.vigor = max(min(item.vigor + random.randint(1, 7), 7), item.vigor)
                    item_changes = item_changes + "Vigor: " + str(item.vigor) + ", "
                    item_changed = True
                    itemrank_modifier += 2
                if random.randint(1, 100) <= chance_to_mod:
                    #item.speed = max(min(item.speed + random.randint(1, 5), 7), item.speed)
                    item.speed = max(min(item.speed + random.randint(1, 7), 7), item.speed)
                    item_changes = item_changes + "Speed: " + str(item.speed) + ", "
                    item_changed = True
                    itemrank_modifier += 1
                if random.randint(1, 100) <= chance_to_mod:
                    item.stamina = max(min(item.stamina  + random.randint(1, 5), 7), item.stamina)
                    item_changes = item_changes + "Stamina: " + str(item.stamina) + ", "
                    item_changed = True
                    itemrank_modifier += 1
                if random.randint(1, 100) <= chance_to_mod:
                    #item.magic = max(min(item.magic + random.randint(1, 3), 7), item.magic)
                    item.magic = max(min(item.magic + random.randint(1, 7), 7), item.magic)
                    item_changes = item_changes + "Magic: " + str(item.magic) + ", "
                    item_changed = True
                    itemrank_modifier += 4
                if random.randint(1, 100) <= chance_to_mod:
                    #item.evade = max(min(item.evade + random.randint(1, 2), 4), item.evade)
                    item.evade = max(min(item.evade + random.randint(1, 3), 5), item.evade)
                    item_changes = item_changes + "Evade: " + str(item.evade) + ", "
                    item_changed = True
                    itemrank_modifier += 3
                if random.randint(1, 100) <= chance_to_mod:
                    #item.mblock = max(min(item.mblock + random.randint(1, 2), 4), item.mblock)
                    item.mblock = max(min(item.mblock + random.randint(1, 3), 5), item.mblock)
                    item_changes = item_changes + "MBlock: " + str(item.mblock) + ", "
                    item_changed = True
                    itemrank_modifier += 3

                if item_changed:
                    # update price
                    price_boost = (random.randint(1, 10) * itemrank_modifier) / 100
                    value = int(item.price * (1 + price_boost))
                    item.price = min(value, 2**16 - 1)

                    #item.name = item.name[:11] + '+'    #append a + to an item if it received stat buffs 
                    item_changes = item_changes[:-2]  #take out last ", "                    
                    self.STATLOG = self.STATLOG + "\n" + (str(item.name) + ": " + item_changes)
                    if print_debug:
                        print(str(item.name) + ": " + str(item.vigor) + " | " + str(item.speed) + " | " + str(item.stamina) + " | " + str(item.magic) + " | " +
                            str(item.evade) + " | " + str(item.mblock))
    ### End of: Mod to randomize item stats


    ### Mod to swap out vanilla items for ultimate items
    #TERRA, LOCKE, CYAN, SHADOW 0-3
    #EDGAR, SABIN, CELES, STRAGO, RELM 4-8
    #SETZER, MOG, GAU, GOGO, UMARO 9-13
    def ultimates(self):
        print_debug = False
        for item in self.items:
            if print_debug:
                vigorsign = ""
                speedsign = ""
                staminasign = ""
                magicsign = ""
                if item.vigorsign == 1:
                    vigorsign = "-"
                if item.speedsign == 1:
                    speedsign = "-"
                if item.staminasign == 1:
                    staminasign = "-"
                if item.magicsign == 1:
                    magicsign = "-"
                
                print(item.name + " | " + str(item.type) + " | " + vigorsign + str(item.vigor) + " | " + speedsign + 
                      str(item.speed) + " | " + staminasign + str(item.stamina) + " | " +
                      magicsign + str(item.magic) + " | " + str(item.specialeffect) +
                      " | " + str(item.enable_swdtech) + " | " + str(item.same_damage_back_row) +
                      " | " + str(item.allow_two_hands) + " | " + str(item.enable_runic) +
    " | " + str(item.field_effect) + " | " + str(item.status_protect1) + " | " +
    str(item.status_protect2) + " | " + str(item.statusacquire1) + " | " +
    str(item.elementtype) + " | " + str(item.usable_in_battle) + " | " +
    str(item.weaponspellcasting) + " | " + str(item.allowproc) + " | " + str(item.breakswhenused) +
    " | " + str(item.targeting) + " | " + str(item.powerdef) + " | " + str(item.hitmdef) +
    " | " + str(item.elemabsorbs) + " | " + str(item.elemnulls) + " | " + str(item.elemweaks) +
    " | " + str(item.statusacquire2) + " | " + str(item.evade) + " | " + str(item.mblock)
+ " | " + str(item.mblockevade) + " | " + str(item.flags1) + " | " + str(item.flags2) +
" | " + str(item.flags3) + " | " + str(item.flags4) + " | " + str(item.flags5))
            # end debug print section for ultimates

            # perform item mods
            if item.name == "RegalCutlass":
                item.vigor = 7
                item.magic = 7
                item.powerdef = 250
                item.hitmdef = 150
                item.mblock = 2
                item.evade = 2
                item.specialeffect = 112
                item.name = "Apocalypse"
                item.animation = [92, 92, 32, 1, 55, 0, 164 ,0]
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[0])
                item.write()
            if item.name == "Crystal":
                item.elementtype = 16
                item.weaponspellcasting = 29
                item.allowproc = 1
                item.vigor = 3
                item.speed = 7
                item.stamina = 3
                item.powerdef = 220
                item.hitmdef = 180
                item.mblock = 3
                item.evade = 2
                item.name = "ZwillXBlade"
                item.animation = [39, 39, 24, 62, 54, 0, 148, 0]
                item.icon = "<dirk icon>"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[1])
                item.write()
            if item.name == "Stout Spear":
                item.vigor = 7
                item.speed = 3
                item.stamina = 3
                item.powerdef = 235
                item.hitmdef = 150
                item.name = "Longinus"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[4])
                item.write()
            if item.name == "Mithril Claw":
                item.elementtype = 32
                item.vigor = 7
                item.stamina = 7
                item.powerdef = 245
                item.hitmdef = 150
                item.mblock = 3
                item.name = "Godhand"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[5])
                item.write()
            if item.name == "Kodachi":
                item.vigor = 7
                item.speed = 7
                item.powerdef = 225
                item.hitmdef = 180
                item.mblock = 5
                item.evade = 1
                item.name = "Oborozuki"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[3])
                item.write()
            if item.name == "Kotetsu":
                item.elementtype = 32
                item.vigor = 7
                item.stamina = 7
                item.powerdef = 245
                item.hitmdef = 150
                item.mblock = 3
                item.name = "Zanmato"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[2])
                item.write()
            if item.name == "Forged":
                item.speed = 4
                item.magic = 7
                item.stamina = 3
                item.powerdef = 240
                item.hitmdef = 150
                item.mblock = 4
                item.evade = 4
                item.name = "SaveTheQueen"
                item.animation = [30, 30, 32, 0, 55, 0, 164, 0]
                item.icon = "<sword icon>"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[6])
                item.write()
            if item.name == "Darts":
                item.speed = 4
                item.stamina = 4
                item.powerdef = 215
                item.hitmdef = 230
                item.specialeffect = 112
                item.name = "Final Trump"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[9])
                item.write()
            if item.name == "Epee":
                item.magic = 7
                item.stamina = 7
                item.powerdef = 240
                item.hitmdef = 150
                item.name = "Gungnir"
                item.animation = [93, 93, 43, 5, 51, 0, 168, 0]
                item.icon = "<lance icon>"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[10])
                item.write()
            if item.name == "Punisher":
                item.weaponspellcasting = 19
                item.allowproc = 1
                item.magic = 7
                item.stamina = 4
                item.powerdef = 180
                item.hitmdef = 135
                item.name = "Stardust Rod"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[7])
                item.write()
            if item.name == "DaVinci Brsh":
                item.weaponspellcasting = 30
                item.allowproc = 1
                item.speed = 7
                item.magic = 7
                item.powerdef = 170
                item.hitmdef = 135
                item.name = "Angel Brush"
                item.animation = [22, 22, 37, 4, 55, 0, 148, 0]
                item.icon = "<brush icon>"
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[8])
                item.write()
            if item.name == "Boomerang":
                item.elementtype = 8
                item.weaponspellcasting = 8
                item.allowproc = 1
                item.vigor = 4
                item.speed = 4
                item.stamina = 4
                item.magic = 4
                item.powerdef = 225
                item.hitmdef = 150
                item.allow_two_hands = 1
                item.name = "ScorpionTail"
                item.animation = [25, 25, 25, 8, 25, 0, 218, 0]
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[12])
                item.write()
            if item.name == "Iron Helmet":
                item.vigor = 6
                item.speed = 6
                item.stamina = 6
                item.magic = 6
                item.powerdef = 40
                item.hitmdef = 40
                item.mblock = 1
                item.evade = 1               
                item.flags1 = 4   #Red Cap
                item.elementtype = 255  #halves all elements
                item.name = "Dueling Mask"
                #in order to get this description to be written in 
                #change the ptr to new space
                #item.description_ptr = [135, 19]
                #item.description_length = 5
                #name_bytes = text.get_bytes("Test", text.TEXT3)
                #name_bytes.append(0)
                #item.description_array = name_bytes
                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[11])
                item.write()
            if item.name == "Charm Bangle":
                item.vigor = 5
                item.speed = 5
                item.stamina = 5
                item.magic = 5
                item.powerdef = 10
                item.hitmdef = 10
                item.mblock = 1
                item.evade = 1
                item.field_effect = 0
                item.flags1 = 11   #Muscle Belt 8, Hero Ring 3
                item.flags3 = 144  #Hyper Wrist 128, Sniper Sight 16
                item.name = "Bone Wrist"

                new_desc = f'Carved bone wristband<end>'
                item.desc = new_desc

                item.remove_all_equipable_characters()
                item.add_equipable_character(self.characters.characters[13])
                item.write()
    ### End of: Mod to swap out vanilla items for ultimate items


    def mod(self):
        ### Shorten item descriptions
        if self.args.adjusted_item_descriptions:
            self.adjust_item_descriptions()

        ### Equippability                    
        not_relic_condition = lambda x : x != Item.RELIC
        if self.args.item_equipable_random:
            self.equipable_random(not_relic_condition, self.args.item_equipable_random_min,
                                                       self.args.item_equipable_random_max)
        elif self.args.item_equipable_balanced_random:
            self.equipable_balanced_random(not_relic_condition, self.args.item_equipable_balanced_random_value)
        elif self.args.item_equipable_original_random:
            self.equipable_original_random(not_relic_condition, self.args.item_equipable_original_random_percent)
        elif self.args.item_equipable_shuffle_random:
            self.equipable_shuffle_random(not_relic_condition, self.args.item_equipable_shuffle_random_percent)

        relic_condition = lambda x : x == Item.RELIC
        if self.args.item_equipable_relic_random:
            self.equipable_random(relic_condition, self.args.item_equipable_relic_random_min,
                                                   self.args.item_equipable_relic_random_max)
        elif self.args.item_equipable_relic_balanced_random:
            self.equipable_balanced_random(relic_condition, self.args.item_equipable_relic_balanced_random_value)
        elif self.args.item_equipable_relic_original_random:
            self.equipable_original_random(relic_condition, self.args.item_equipable_relic_original_random_percent)
        elif self.args.item_equipable_relic_shuffle_random:
            self.equipable_shuffle_random(relic_condition, self.args.item_equipable_relic_shuffle_random_percent)

        if self.args.moogle_charm_all:
            self.moogle_charm_all()

        if self.args.swdtech_runic_all:
            self.swdtech_runic_all()

        if self.args.no_priceless_items:
            self.assign_values()

        if self.args.shops_expensive_breakable_rods:
            self.expensive_breakable_rods()

        if self.args.shops_expensive_super_balls:
            self.expensive_super_balls()

        if self.args.shop_prices_random_value:
            self.random_prices_value()
        elif self.args.shop_prices_random_percent:
            self.random_prices_percent()

        ### Move all price assignments prior to name changing
        ### Mod for ultimate items
        if self.args.ultimate_items:
            self.ultimates()

        ### Mod for items to randomly teach spells
        if self.args.item_teacher:
            self.randomize_item_learnables_spells(self.args.item_teacher_chance)
            
        ### Mod for items stat boosts
        if self.args.item_rand_stat:
            self.randomize_stats(self.args.item_rand_stat_chance)


        for a_spell_id in self.args.remove_learnable_spell_ids:
            self.remove_learnable_spell(a_spell_id)

        if self.args.cursed_shield_battles_original:
            self.cursed_shield_battles = 256
        else:
            self.cursed_shield_battles = random.randint(self.args.cursed_shield_battles_min,
                                                        self.args.cursed_shield_battles_max)
            items_asm.cursed_shield_mod(self.cursed_shield_battles)
            cursed_shld = self.items[name_id["Cursed Shld"]]
            cursed_shld.desc = "Battles: " + str(self.cursed_shield_battles) + "<line>"

        if self.args.stronger_atma_weapon:
            items_asm.stronger_atma_weapon()
        self.prevent_atma_weapon_rage()

        # overwrite imperial banquet dialogs (1769-1830) with receive item dialogs
        # skip banquet dialogs that are too short (must be >=23 for longest item names)
        self.available_dialogs = list(range(1769, 1777))
        self.available_dialogs.extend(list(range(1782, 1801)))
        self.available_dialogs.extend(list(range(1802, 1804)))
        self.available_dialogs.extend(list(range(1805, 1818)))
        self.available_dialogs.extend(list(range(1820, 1822)))
        self.available_dialogs.append(1823)
        self.available_dialogs.extend(list(range(1825, 1830)))

        # generate receive item dialogs for good items
        self.receive_dialogs = {}
        for item_id in self.GOOD:
            self.add_receive_dialog(item_id)

        self.moogle_starting_equipment()

    def write(self):
        # Mod to show more item details
        if self.args.spoiler_log:
            self.log()
            
##        for item in self.items:
##            item.write()
        # Mod for item descriptions
        for item_index, item in enumerate(self.items):
            item.write()
            self.desc_data[item_index] = item.desc_data()
        self.desc_data.write()


    def get_id(self, name):
        return name_id[name]

    def get_name(self, id):
        name = self.items[id].name
        first_pos = name.find('<')
        while first_pos >= 0:
            second_pos = name.find('>')
            name = name.replace(name[first_pos:second_pos + 1], "")
            first_pos = name.find('<')
        return name.strip('\0')

    def get_type(self, id):
        return self.items[id].type

    def get_items(self, exclude = None, item_types = None):
        if exclude is None:
            exclude = []
        exclude.append(self.EMPTY)

        if item_types is None:
            item_list = [item.id for item in self.items]
        else:
            try:
                assert(item_types >= 0 and item_types < Item.ITEM_TYPE_COUNT)
                item_list = [item.id for item in self.type_items[item_types]]
            except ValueError:
                item_list = []
                for item_type in item_types:
                    assert(item_type >= 0 and item_type < Item.ITEM_TYPE_COUNT)
                    item_list.extend([item.id for item in self.type_items[item_type]])

        item_list = [item_id for item_id in item_list if item_id not in exclude]
        return item_list

    def get_excluded(self):
        exclude = []

        if self.args.no_moogle_charms:
            exclude.append(name_id["Moogle Charm"])
        if self.args.no_exp_eggs:
            exclude.append(name_id["Exp. Egg"])
        if self.args.no_illuminas:
            exclude.append(name_id["Illumina"])

        from data.movement import AUTO_SPRINT, B_DASH
        # Sprint Shoes are a literal dead item if any of these options
        if self.args.no_sprint_shoes or self.args.movement in [AUTO_SPRINT, B_DASH]:
            exclude.append(name_id["Sprint Shoes"])
        if self.args.no_free_paladin_shields:
            exclude.append(name_id["Paladin Shld"])
            exclude.append(name_id["Cursed Shld"])
        if self.args.permadeath:
            exclude.append(name_id["Fenix Down"])

        ### Mod for ultimate items
        if self.args.ultimate_items:
            for item_name in self.ULTS:
                exclude.append(name_id[item_name])

        return exclude

    def get_random(self, exclude = None, item_types = None):
        if exclude is None:
            exclude = []
        exclude.extend(self.get_excluded())

        try:
            # pick random type if multiple provided
            item_type = random.choice(item_types)
        except TypeError:
            item_type = item_types

        return random.choice(self.get_items(exclude, item_type))

    def get_good_random(self):
        print_debug = True
        ### Mod to apply "one of" concept for good items/check rewards
        if args.one_of:
            one_ofs = [
                "Paladin Shld",
                "Illumina",
                "Exp. Egg",
                "Fixed Dice",
                "Ragnarok",
                "ValiantKnife",
                "Offering",
                #"Dragon Horn",
                #"Gem Box",
                #"Flame Shld",
                #"Ice Shld",
                #"Thunder Shld",
                #"Minerva",
            ]
            selected_good_item = random.choice(self.GOOD)
            if id_name[selected_good_item] in one_ofs:
                if print_debug:
                    print("1 " + id_name[selected_good_item])
                self.GOOD.remove(selected_good_item)
            return selected_good_item
        else:  # "one of" logic not applied, normal WC
            return random.choice(self.GOOD)


    ### Mod to select random item with location tiering
    def get_tiered_good_random(self, event_depth, event):
        ### get max and summed depth
        max_depth = 0
        summed_depth = 0
        for x, depth in event_depth.items():
            summed_depth += depth
            if depth > max_depth:
                max_depth = depth

        avg_depth = summed_depth / len(event_depth.items())

        ### more straight-forward approach:
        ### don't allow highest tiered items when event has
        ### eventdepth of less than half the avg depth
        best_items = [
            "Paladin Shld",
            "Illumina",
            "Exp. Egg",
            "Fixed Dice",
            "Ragnarok",
            "ValiantKnife",
            "Offering",
            "Dragon Horn",
            "Gem Box",
            "Flame Shld",
            "Ice Shld",
            "Thunder Shld",
            "Minerva",
        ]
        selected_good_item = self.get_good_random()
        ### if the event's depth is less than the avg depth
        if event_depth[event.name()] < avg_depth:
            ### keep picking items until the selected item is not in best_items
            while id_name[selected_good_item] in best_items:
                #print("depth too low")
                selected_good_item = self.get_good_random()

        ### experimental section w/tiering table
        ### currently throws errors
        if 0 == 1:
            ### include tiering table
            ### could apply variation to these rank values if desired
            high_tier_item_rank = {
                9 : 39500, # ValiantKnife
                26 : 175500, # Illumina
                27 : 95500, # Ragnarok
                33 : 44400, # Pearl Lance
                35 : 47700, # Aura Lance
                60 : 64300, # Magus Rod
                82 : 77700, # Fixed Dice
                94 : 69000, # Aegis Shld originally 79600
                96 : 69100, # Flame Shld originally 59100
                97 : 69200, # Ice Shld originally 59200
                98 : 74300, # Thunder Shld originally 64300
                100 : 50400, # Genji Shld
                103 : 190900, # Paladin Shld
                104 : 72500, # Force Shld originally 137500
                120 : 27400, # Red Cap
                128 : 53300, # Cat Hood
                129 : 28600, # Genji Helmet
                148 : 66900, # Force Armor
                154 : 34000, # Genji Armor
                156 : 83800, # Minerva
                161 : 34400, # BehemothSuit
                162 : 60300, # Snow Muffler
                206 : 125100, # Economizer
                209 : 35000, # Genji Glove
                211 : 125000, # Offering
                216 : 75000, # Gem Box
                217 : 35000, # Dragon Horn
                224 : 65000, # Marvel Shoes
                228 : 90000, # Exp. Egg originally 55000
            }
            if args.stronger_atma_weapon:
                high_tier_item_rank[28] = 37500
            if args.no_free_paladin_shields:
                high_tier_item_rank.pop(103)
            if args.no_exp_eggs:
                high_tier_item_rank.pop(228)
            if args.no_illuminas:
                high_tier_item_rank.pop(26)
                
            temprank = {k: v for k, v in sorted(high_tier_item_rank.items(), key=lambda item: item[1])}
            gooditemrank = list(temprank.items())

            # tier sizes were turning out to be very small, expand tier sizes by 2
            tier_size = int(len(gooditemrank) / max_depth) + 2
            x = 0
            rank = 1
            while(x < len(gooditemrank)):
                gooditemrank[x] = (gooditemrank[x][0], rank)
                x = x + 1
                if x % tier_size == 0:
                    rank = rank + 1

            max_tier = rank  #store the highest tier value
            #print(gooditemrank)
            #input("Z")

            # get event depth: subtract tier sizes by 2, minimum of 1
            eventdepth = max(event_depth[event.name()] - 2, 1)
            import random
            roll = random.randint(1, 100)
            ### apply variation to depth
            ### original: -2 10%, -1 25%, 0 35%, +1 25%, +2 5%
            ### new: -2 5%, -1 15%, 0 35%, +1 25%, +2 20%
            if roll <= 5:
                eventdepth = max(1, eventdepth-2)
                eventdepth = min(eventdepth, max_tier)
            elif roll <= 20:
                eventdepth = max(1, eventdepth-1)
                eventdepth = min(eventdepth, max_tier)
            elif roll <= 55:
                eventdepth = min(eventdepth, max_tier)
            elif roll <= 80:
                eventdepth = min(eventdepth + 1, max_tier)
            elif roll <= 100:
                eventdepth = min(eventdepth + 2, max_tier)
            ### get all the items that match the eventdepth
            possible_items = []

            #print(roll)
            #print(eventdepth)
            for x in range(len(gooditemrank)):
                if gooditemrank[x][1] == eventdepth:
                    possible_items.append(gooditemrank[x][0])

            #print(possible_items)
            try:
                selected_good_item = random.choice(possible_items)
            except IndexError:
                print(gooditemrank)
                print(eventdepth)
                print(max_tier)
                input("tiered item problem")

            print(str(event.name()) + ": " + str(eventdepth) +
                  " / Item: " + str(id_name[selected_good_item]))
        ### end of experimental ranked item tiering section

        return selected_good_item
    ### End of: Mod to select random item with location tiering


    ### Experimental: Mod to randomly pick new item attributes
    def randomize_item_attributes(self, chance_to_mod=10, number_of_mods=1):
        if chance_to_mod == 0:
            exit
        # item attribute categories:
        # apply chance to have a category
        # apply separate chance within category
        # field effects
        if random.randint(1, 100) <= chance_to_mod:
            pass
        # status protect1
        if random.randint(1, 100) <= chance_to_mod:
            #dark, zombie, poison, magitek, vanish, imp, petrify, magic death
            sp1 = [0, 1, 2, 3, 4, 5, 6]
            chosen = random.choice(sp1)
            if chosen == 0:
                no_dark = True
            elif chosen == 1:
                no_zombie = True
    ### End of: Mod to randomly pick new item attributes


    def get_receive_dialog(self, item):
        return self.receive_dialogs[item]

    def add_receive_dialog(self, item_id):
        dialog_id = self.available_dialogs.pop()
        self.receive_dialogs[item_id] = dialog_id

        # item names are stored as TEXT2, dialogs are TEXT1
        import data.text
        item_name = data.text.convert(self.items[item_id].name, data.text.TEXT1)

        self.dialogs.set_text(dialog_id, '<line><     >Received “' + item_name + '”!<end>')

    def print(self):
        for item in self.items:
            item.print()

    ### Mod for detailed item log output
    def log(self):
        from log import section, format_option, SECTION_WIDTH                                                          
        from data.characters import Characters                                                                         
                                                                                                                       
        lcolumn = []
        #print(good_items)
        #print(self.items)

        ### comment out for testing 
        #fulllist = []
        #for item in self.items:
            #fulllist.append(item.name)
        
        #for item_name in sorted(fulllist):
        ### comment out for testing
        
        for item in self.items:    # uncommented
            #item = self.items[name_id[item_name]] - comment out for testing
                                                                                                                       
            equipable = []                                                                                             
            for character in self.characters.playable:                                                                 
                if item.equipable_by(character):                                                                       
                    equipable.append(f"{character.name:<{Characters.NAME_SIZE}}")                                      
                else:                                                                                                  
                    equipable.append(' ' * Characters.NAME_SIZE)
                    
            item_name = item.name                                                                                                   
            lcolumn.append(f"{item_name:<{Item.NAME_LENGTH}}{' '.join(equipable):>{SECTION_WIDTH - Item.NAME_LENGTH}}")

        ### section for new item learn rates
        lcolumn.append("\n")            
        lcolumn.append("---------------------- ITEM SPELLS ---------------------- ")
        lcolumn.append(self.TOLOG)

        ### section for new item stats
        lcolumn.append("\n")            
        lcolumn.append("---------------------- NEW ITEM STATS ---------------------- ")
        lcolumn.append(self.STATLOG)
        
        section("Equipable", lcolumn, [])
