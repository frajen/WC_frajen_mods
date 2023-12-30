import data.text as text
from data.text.text2 import text_value, value_text

class Item():
    NAME_LENGTH = 13
    NAMES_START_ADDR = 0x12b300

    DATA_SIZE = 30
    DATA_START_ADDR = 0x185000

    ITEM_TYPE_COUNT = 7
    TOOL, WEAPON, ARMOR, SHIELD, HELMET, RELIC, ITEM = range(ITEM_TYPE_COUNT)

    # Mods for animation
    ANIMATION_START_ADDR = 0x2CE408

    # Mod to pass in description parameter via desc_data in data\items.py
    #def __init__(self, id, rom):
    def __init__(self, id, rom, desc_data):
        self.rom = rom

        self.id = id
        self.name_addr = self.NAMES_START_ADDR + self.id * self.NAME_LENGTH
        self.data_addr = self.DATA_START_ADDR + self.id * self.DATA_SIZE

        # Mods for animation 
        self.animation_addr = self.ANIMATION_START_ADDR + self.id * 8

        # Mods for descriptions
        self.desc = text.get_string(desc_data, text.TEXT2).rstrip('\0')

        self.read()

    def is_equipable(self):
        return self.equipable_characters

    def equipable_by(self, character):
        char_bit = 0x01 << character.id
        return self.equipable_characters & char_bit

    def add_equipable_character(self, character):
        char_bit = 0x01 << character.id
        self.equipable_characters = self.equipable_characters | char_bit

    def remove_equipable_character(self, character):
        char_bit = 0x01 << character.id
        self.equipable_characters = self.equipable_characters & ~char_bit

    def remove_all_equipable_characters(self):
        self.equipable_characters = 0

    def remove_learnable_spell(self):
        self.learnable_spell = 0
        self.learnable_spell_rate = 0

    def scale_price(self, factor):
        self.price = int(self.price * factor)
        self.price = max(min(self.price, 2**16 - 1), 0)

    def read(self):
        name_bytes = self.rom.get_bytes(self.name_addr, self.NAME_LENGTH)
        self.icon = value_text[name_bytes[0]]
        self.name = text.get_string(name_bytes[1:], text.TEXT2).rstrip('\0')

        data = self.rom.get_bytes(self.data_addr, self.DATA_SIZE)
        self.type                   = data[0] & 0x07
        self.throwable              = (data[0] & 0x10) >> 4
        self.usable_in_battle       = (data[0] & 0x20) >> 5
        self.usable_in_menu         = (data[0] & 0x40) >> 6
        self.equipable_characters   = (data[1] & 0xff)
        self.equipable_characters  |= (data[2] & 0x3f) << 8
        self.imp_equipment          = (data[2] & 0x40) >> 6
        self.merit_awardable        = (data[2] & 0x80) >> 7
        self.learnable_spell_rate   = data[3]
        self.learnable_spell        = data[4]
        self.weapon_flag_unknown1   = (data[19] & 0x01) >> 0
        self.enable_swdtech         = (data[19] & 0x02) >> 1   #Tonic/Potion/X-Potion/Elixir/Megalixir/Fenix Down/Revivify: dmg on undead = 1
        self.weapon_flag_unknown2   = (data[19] & 0x04) >> 2
        self.weapon_flag_unknown3   = (data[19] & 0x08) >> 3   #items: affects HP
        self.weapon_flag_unknown4   = (data[19] & 0x10) >> 4   #items: affets MP
        self.same_damage_back_row   = (data[19] & 0x20) >> 5   #items: removes status effect, including Wound, Sleeping Bag, Tent
        self.allow_two_hands        = (data[19] & 0x40) >> 6
        self.enable_runic           = (data[19] & 0x80) >> 7   #X-Potion, X-Ether, Elixir, Megalixir, Fenix Down, Revivify, Sleeping Bag, Tent: items: max out
        self.price                  = int.from_bytes(data[28:30], "little")

        ### Mods for item parameters
        #note that these are decimal representations
        #Charm Bangle = 1, Moogle Charm = 2, Sprint Shoes = 32, Tintinabar = 128
        self.field_effect           = data[5]
        self.fewer_encounters       = (data[5] & 0x01) >> 0
        self.no_encounters          = (data[5] & 0x02) >> 1
        self.sprintshoes            = (data[5] & 0x10) >> 4
        self.stepregen              = (data[5] & 0x80) >> 7
        #Dark = 1, Zombie = 2, Poison = 4, Dark+Zombie+Poison = 7, White Cape = 32 (either Imp/Mute), Petrify = 64, Ribbon = 103, Safety Bit/Memento Ring = 194 
        #from BC: No magitek = 8, No vanish = 16, No imp = 32, Death protection = 128 (Safety Bit = 128+64+2)
        self.status_protect1        = data[6]
        self.no_dark                = (data[6] & 0x01) >> 0
        self.no_zombie              = (data[6] & 0x02) >> 1
        self.no_poison              = (data[6] & 0x04) >> 2
        self.no_magitek             = (data[6] & 0x08) >> 3
        self.no_vanish              = (data[6] & 0x10) >> 4
        self.no_imp                 = (data[6] & 0x20) >> 5
        self.no_petrify             = (data[6] & 0x40) >> 6
        self.no_magic_death         = (data[6] & 0x80) >> 7    
        #White Cape = 8 (Imp/Mute), Peace Ring = 48 (Bserk/Confuse), Ribbon = 248
        #from BC: No condemned = 1, Near fatal always = 2, No image = 4, No mute = 8, No berserk = 16, No muddle = 32, No seizure = 64, No sleep = 128
        # test what "near fatal always" means
        self.status_protect2        = data[7]
        self.no_condemned           = (data[7] & 0x01) >> 0
        self.once_near_fatal_always = (data[7] & 0x02) >> 1  #unused in vanilla
        self.no_image               = (data[7] & 0x04) >> 2
        self.no_mute                = (data[7] & 0x08) >> 3
        self.no_berserk             = (data[7] & 0x10) >> 4
        self.no_muddle              = (data[7] & 0x20) >> 5
        self.no_seizure             = (data[7] & 0x40) >> 6
        self.no_sleep               = (data[7] & 0x80) >> 7
        #AutoFloat = 1, AutoRegen = 2, AutoHaste = 8, AutoShell = 32, AutoSafe = 64, AutoRflect = 128
        self.statusacquire1         = data[8]
        self.auto_float             = (data[8] & 0x01) >> 0
        self.auto_regen             = (data[8] & 0x02) >> 1
        self.auto_haste             = (data[8] & 0x08) >> 3
        self.auto_shell             = (data[8] & 0x20) >> 5
        self.auto_safe              = (data[8] & 0x40) >> 6
        self.auto_reflect           = (data[8] & 0x80) >> 7
        #Atlas Armlet = 1, Earrings = 2, Hero Ring = 3, Red Cap = 4, Muscle Belt = 8, Green Beret = 16, Minerva = 32, Crystal Orb = 64, Bard's Hat = 128
        self.flags1                 = data[9]
        self.raise_atk              = (data[9] & 0x01) >> 0
        self.raise_mag              = (data[9] & 0x02) >> 1
        self.hp_1_4                 = (data[9] & 0x04) >> 2
        self.hp_1_2                 = (data[9] & 0x08) >> 3
        self.hp_1_8                 = (data[9] & 0x10) >> 4
        self.mp_1_4                 = (data[9] & 0x20) >> 5
        self.mp_1_2                 = (data[9] & 0x40) >> 6
        self.mp_1_8                 = (data[9] & 0x80) >> 7
        #Gale Hairpin = 1, Back Guard = 2, DragoonBoots = 4, Gem Box = 8, FakeMustache = 16, Coin Toss = 32, Thief Glove = 64, Dragon Horn = 128
        self.flags2                 = data[10]
        self.preemptive_strike      = (data[10] & 0x01) >> 0
        self.prevent_back_pincer    = (data[10] & 0x02) >> 1
        self.jump                   = (data[10] & 0x04) >> 2
        self.xmagic                 = (data[10] & 0x08) >> 3
        self.control                = (data[10] & 0x10) >> 4
        self.gprain                 = (data[10] & 0x20) >> 5
        self.capture                = (data[10] & 0x40) >> 6
        self.better_jump            = (data[10] & 0x80) >> 7
        #Sneak Ring = 1, Beret = 4 (Better Sketch), Coronet = 8 (Better Control), Sniper Sight = 16, Gold Hairpin = 32, Economizer = 64, Hyper Wrist = 128
        self.flags3                 = data[11]
        self.better_steal           = (data[11] & 0x01) >> 0
        self.better_sketch          = (data[11] & 0x04) >> 2
        self.better_control         = (data[11] & 0x08) >> 3
        self.always_hits            = (data[11] & 0x10) >> 4
        self.mp_consumption_1_2     = (data[11] & 0x20) >> 5
        self.mp_consumption_one     = (data[11] & 0x40) >> 6
        self.raise_vigor_50_percent = (data[11] & 0x80) >> 7
        #Offering = 1, Black Belt = 2, Beads = 4, Gauntlet = 8, Genji Glove = 16, Merit Award = 32, True Knight = 64
        self.flags4                 = data[12]
        self.x_fight                = (data[12] & 0x01) >> 0
        self.counter_75_percent     = (data[12] & 0x02) >> 1
        self.evade_boost            = (data[12] & 0x04) >> 2
        self.two_handed_weapon      = (data[12] & 0x08) >> 3
        self.dual_wield             = (data[12] & 0x10) >> 4
        self.better_equip           = (data[12] & 0x20) >> 5
        self.cover                  = (data[12] & 0x40) >> 6
        self.mp_1_8                 = (data[12] & 0x80) >> 7
        #Barrier Ring = 1, MithrilGlove = 2, Czarina Ring = 3, Exp. Egg = 8, Cat Hood = 16, Relic Ring = 128
        self.flags5                 = data[13]
        self.shell_low_HP           = (data[13] & 0x01) >> 0
        self.safe_low_HP            = (data[13] & 0x02) >> 1
        self.reflect_low_HP         = (data[13] & 0x04) >> 2  #unused in vanilla
        self.doubles_xp             = (data[13] & 0x08) >> 3
        self.doubles_gold           = (data[13] & 0x10) >> 4
        self.become_undead          = (data[13] & 0x80) >> 7
        #Self = 1, Single Enemy = 65, Fire/Ice/Thunder Rod/Shields = 105
        #Inviz/Shadow Edge = 2, Rename Card = 3, Megalixir/Smoke Bomb/Warp Stone = 46
        #Chain Saw/Debilitator/Drill/Air Anchor/Magicite = 67
        #NoiseBlaster/BioBlaster/Flash/AutoCrossbow = 106
        #Fire Skean/Water Edge/Bolt Edge/Super Ball = 110
        self.targeting              = data[14]
        self.target_one             = (data[14] & 0x01) >> 0
        self.target_one_side_only   = (data[14] & 0x02) >> 1
        self.target_everyone        = (data[14] & 0x04) >> 2
        self.target_group_default   = (data[14] & 0x08) >> 3
        self.target_auto            = (data[14] & 0x10) >> 4
        self.target_group           = (data[14] & 0x20) >> 5
        self.target_enemy_default   = (data[14] & 0x40) >> 6
        self.target_random          = (data[14] & 0x80) >> 7

        #Fire = 1, Ice = 2, Bolt = 4, Poison = 8, Wind = 16, Pearl = 32, Earth = 64, Water = 128
        self.elementtype            = data[15]
        self.fire                   = (data[15] & 0x01) >> 0
        self.ice                    = (data[15] & 0x02) >> 1
        self.bolt                   = (data[15] & 0x04) >> 2
        self.poison                 = (data[15] & 0x08) >> 3
        self.wind                   = (data[15] & 0x10) >> 4
        self.pearl                  = (data[15] & 0x20) >> 5
        self.earth                  = (data[15] & 0x40) >> 6
        self.water                  = (data[15] & 0x80) >> 7
        self.vigorspeed             = data[16]
        self.vigor                  = (data[16] & 0x07) >> 0
        self.vigorsign              = (data[16] & 0x08) >> 3  #1 is negative
        self.speed                  = (data[16] & 0x70) >> 4
        self.speedsign              = (data[16] & 0x80) >> 7  #1 is negative
        self.staminamagic           = data[17]
        self.stamina                = (data[17] & 0x07) >> 0
        self.staminasign            = (data[17] & 0x08) >> 3   #1 is negative
        self.magic                  = (data[17] & 0x70) >> 4
        self.magicsign              = (data[17] & 0x80) >> 7     #1 is negative

        self.weaponspellcasting     = (data[18] & 0x3F) >> 0  #spell ID for proc/break stored here
        self.allowproc              = (data[18] & 0x40) >> 6
        self.breakswhenused         = (data[18] & 0x80) >> 7  #"break" = remove from inventory

        self.powerdef               = data[20]  # items: heal power
        self.hitmdef                = data[21]
        self.elemabsorbs            = data[22]
        self.absorbs_fire           = (data[22] & 0x01) >> 0
        self.absorbs_ice            = (data[22] & 0x02) >> 1
        self.absorbs_bolt           = (data[22] & 0x04) >> 2
        self.absorbs_poison         = (data[22] & 0x08) >> 3
        self.absorbs_wind           = (data[22] & 0x10) >> 4
        self.absorbs_pearl          = (data[22] & 0x20) >> 5
        self.absorbs_earth          = (data[22] & 0x40) >> 6
        self.absorbs_water          = (data[22] & 0x80) >> 7        
        self.elemnulls              = data[23]
        self.nullifies_fire         = (data[23] & 0x01) >> 0
        self.nullifies_ice          = (data[23] & 0x02) >> 1
        self.nullifies_bolt         = (data[23] & 0x04) >> 2
        self.nullifies_poison       = (data[23] & 0x08) >> 3
        self.nullifies_wind         = (data[23] & 0x10) >> 4
        self.nullifies_pearl        = (data[23] & 0x20) >> 5
        self.nullifies_earth        = (data[23] & 0x40) >> 6
        self.nullifies_water        = (data[23] & 0x80) >> 7
        self.elemweaks              = data[24]
        self.weak_to_fire           = (data[24] & 0x01) >> 0
        self.weak_to_ice            = (data[24] & 0x02) >> 1
        self.weak_to_bolt           = (data[24] & 0x04) >> 2
        self.weak_to_poison         = (data[24] & 0x08) >> 3
        self.weak_to_wind           = (data[24] & 0x10) >> 4
        self.weak_to_pearl          = (data[24] & 0x20) >> 5
        self.weak_to_earth          = (data[24] & 0x40) >> 6
        self.weak_to_water          = (data[24] & 0x80) >> 7
        #Cursed Ring = 1, Mirage Vest = 4, Thornlet = 64, Cursed Shld - 121
        #from BC: Near fatal = 2, Mute = 8, Bserk = 16, Muddle = 32, Seizure = 64, Sleep = 128
        self.statusacquire2         = data[25]
        self.auto_condemned         = (data[25] & 0x01) >> 0
        self.auto_near_fatal        = (data[25] & 0x02) >> 1    #unused in vanilla
        self.auto_image             = (data[25] & 0x04) >> 2
        self.auto_mute              = (data[25] & 0x08) >> 3
        self.auto_berserk           = (data[25] & 0x10) >> 4
        self.auto_muddle            = (data[25] & 0x20) >> 5
        self.auto_seizure           = (data[25] & 0x40) >> 6
        self.auto_sleep             = (data[25] & 0x80) >> 7
        self.mblockevade            = data[26]
        self.evade                  = self.mblockevade & 0x0F
        self.mblock                 = (self.mblockevade & 0xF0) >> 4

        #first four bits (from ff3usME):
        #1: Magicite
        #2: Super Ball
        #3: Smoke Bomb
        #4: Knife evade animation (also Elixir/Megalixir)
        #5: Sword evade animation (also Warp Stone)
        #6: Buckler/shield evade animation (also Dried Meat)
        #7: Red cape evade animation (Zephyr Cape)
        #10 Buckler/shield mblock animation
        #14: Buckler/shield evade & mblock animation
        #next four bits:
        #16: Random steal (ThiefKnife)
        #32: Atma Weapon
        #48: Random X kill (e.g. Assassin, Trump, Wing Edge)
        #64: 2x dmg on humans (Man Eater)
        #80: Drain HP (Drainer)
        #96: Drain MP (Soul Sabre)
        #112: MP crit
        #128: Throw proc (Hawk Eye/Sniper)
        #144: Dice graphic
        #160: Vknife
        #176: 50% Wind Slash (Tempest)
        #192: Heal Rod
        #208: Random slice kill (Scimitar)
        #224: Ogre Nix
        #255: Many consumables, Inviz and Shadow Edge
        self.specialeffect = data[27]
        if (data[27] & 0xF) == 4:
            self.knife_evade_animation = 1
        elif (data[27] & 0xF) == 5:
            self.sword_evade_animation = 1
        elif (data[27] & 0xF) == 6:
            self.buckler_evade_animation = 1
        elif (data[27] & 0xF) == 7:
            self.red_cape_evade_animation = 1
        elif (data[27] & 0xF) == 10:
            self.buckler_mblock_animation = 1
        elif (data[27] & 0xF) == 14:
            self.buckler_evade_mblock_animation = 1

        if ((data[27] & 0xF0) >> 4) == 1:
            self.random_steal = 1
        elif ((data[27] & 0xF0) >> 4) == 2:
            self.atma_weapon_graphic = 1
        elif ((data[27] & 0xF0) >> 4) == 3:
            self.random_x_kill = 1
        elif ((data[27] & 0xF0) >> 4) == 4:
            self.double_dmg_on_humans = 1
        elif ((data[27] & 0xF0) >> 4) == 5:
            self.drain_HP = 1
        elif ((data[27] & 0xF0) >> 4) == 6:
            self.drain_MP = 1
        elif ((data[27] & 0xF0) >> 4) == 7:
            self.mp_crit = 1
        elif ((data[27] & 0xF0) >> 4) == 8:
            self.throw_proc = 1
        elif ((data[27] & 0xF0) >> 4) == 9:
            self.dice_graphic = 1
        elif ((data[27] & 0xF0) >> 4) == 10:
            self.stronger_on_low_HP = 1
        elif ((data[27] & 0xF0) >> 4) == 11:
            self.wind_slash_proc = 1
        elif ((data[27] & 0xF0) >> 4) == 12:
            self.heal_rod = 1
        elif ((data[27] & 0xF0) >> 4) == 13:
            self.random_slice_kill = 1
        elif ((data[27] & 0xF0) >> 4) == 14:
            self.ogre_nix_breakable = 1

        animation_data = self.rom.get_bytes(self.animation_addr, 8)
        self.animation = animation_data
        ### End of: Mods for item parameters
        
    def write(self):
        name_bytes = [text_value[self.icon]]
        name_bytes += text.get_bytes(self.name, text.TEXT2)
        name_bytes += [text_value['\0']] * (self.NAME_LENGTH - len(name_bytes))
        self.rom.set_bytes(self.name_addr, name_bytes)

        data = [0x00] * self.DATA_SIZE

        data[1]     = (self.equipable_characters & 0x00ff)
        data[2]     = (self.equipable_characters & 0x3f00)  >> 8
        data[2]    |= self.imp_equipment                    << 6
        data[2]    |= self.merit_awardable                  << 7

        data[19]    = self.weapon_flag_unknown1             << 0
        data[19]   |= self.enable_swdtech                   << 1
        data[19]   |= self.weapon_flag_unknown2             << 2
        data[19]   |= self.weapon_flag_unknown3             << 3
        data[19]   |= self.weapon_flag_unknown4             << 4
        data[19]   |= self.same_damage_back_row             << 5
        data[19]   |= self.allow_two_hands                  << 6
        data[19]   |= self.enable_runic                     << 7

        self.rom.set_byte(self.data_addr + 1, data[1])
        self.rom.set_byte(self.data_addr + 2, data[2])
        self.rom.set_byte(self.data_addr + 3, self.learnable_spell_rate)
        self.rom.set_byte(self.data_addr + 4, self.learnable_spell)
        self.rom.set_byte(self.data_addr + 19, data[19])
        self.rom.set_short(self.data_addr + 28, self.price)

        ### Mods for item parameters
        data[5] = self.field_effect

        data[6]  = self.no_dark         << 0
        data[6] |= self.no_zombie       << 1
        data[6] |= self.no_poison       << 2
        data[6] |= self.no_magitek      << 3
        data[6] |= self.no_vanish       << 4
        data[6] |= self.no_imp          << 5
        data[6] |= self.no_petrify      << 6
        data[6] |= self.no_magic_death  << 7

        data[7]  = self.no_condemned                << 0
        data[7] |= self.once_near_fatal_always      << 1
        data[7] |= self.no_image                    << 2
        data[7] |= self.no_mute                     << 3
        data[7] |= self.no_berserk                  << 4
        data[7] |= self.no_muddle                   << 5
        data[7] |= self.no_seizure                  << 6
        data[7] |= self.no_sleep                    << 7

        data[9] = self.flags1
        data[11] = self.flags3

        data[14]    = self.target_one << 0
        data[14]   |= self.target_one_side_only << 1
        data[14]   |= self.target_everyone << 2
        data[14]   |= self.target_group_default << 3
        data[14]   |= self.target_auto << 4
        data[14]   |= self.target_group << 5
        data[14]   |= self.target_enemy_default << 6
        data[14]   |= self.target_random << 7

        data[15] = self.elementtype
        #data[16] = self.vigorspeed
        data[16] = ((self.vigor | self.vigorsign << 3) | self.speed << 4) | self.speedsign << 7
        #data[17] = self.staminamagic
        data[17] = ((self.stamina | self.staminasign << 3) | self.magic << 4) | self.magicsign << 7

        data[18] = self.weaponspellcasting << 0
        data[18] |= self.allowproc << 6
        data[18] |= self.breakswhenused << 7

        data[20] = self.powerdef
        data[21] = self.hitmdef
        
        #data[26] = self.mblockevade
        data[26] = self.evade | (self.mblock << 4)
        data[27] = self.specialeffect

        self.rom.set_byte(self.data_addr + 5, data[5])
        self.rom.set_byte(self.data_addr + 9, data[9])
        self.rom.set_byte(self.data_addr + 11, data[11])
        self.rom.set_byte(self.data_addr + 14, data[14])  #targeting

        self.rom.set_byte(self.data_addr + 15, data[15])
        self.rom.set_byte(self.data_addr + 16, data[16])
        self.rom.set_byte(self.data_addr + 17, data[17])
        self.rom.set_byte(self.data_addr + 18, data[18])
        self.rom.set_byte(self.data_addr + 20, data[20])
        self.rom.set_byte(self.data_addr + 21, data[21])
        self.rom.set_byte(self.data_addr + 26, data[26])
        self.rom.set_byte(self.data_addr + 27, data[27])

        animation_data = self.animation
        self.rom.set_bytes(self.animation_addr, animation_data)
        ### End of: Mods for item parameters

    ### Added for itme description mods
    def desc_data(self):
        from data.items import Items
        data = text.get_bytes(self.desc, text.TEXT3)
        return data

    def get_desc(self):
        return self.desc.strip('\0')
    ### Added for itme description mods


    def print(self):
        type_string = {self.TOOL : "TOOL", self.WEAPON : "WEAPON", self.ARMOR : "ARMOR",
                       self.SHIELD : "SHIELD", self.HELMET : "HELMET", self.RELIC : "RELIC", self.ITEM : "ITEM"}
        print("{}: {} {}: {} {}".format(self.id, self.name, type_string[self.type], hex(self.equipable_characters), self.price))
