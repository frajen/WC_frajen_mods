from data.character import Character
from data.natural_magic import NaturalMagic
from data.commands import Commands
from data.menu_character_sprites import MenuCharacterSprites
from data.character_sprites import CharacterSprites
from data.character_palettes import CharacterPalettes
from data.party_battle_scripts import PartyBattleScripts
from data.structures import DataArray

import data.characters_asm as characters_asm

class Characters():
    CHARACTER_COUNT = 14   # 14 playable characters
    TERRA, LOCKE, CYAN, SHADOW, EDGAR, SABIN, CELES, STRAGO, RELM, SETZER, MOG, GAU, GOGO, UMARO = range(CHARACTER_COUNT)
    SOLDIER, IMP, GENERAL_LEO, BANON_DUNCAN, ESPER_TERRA, MERCHANT, GHOST, KEFKA = range(CHARACTER_COUNT, 22)

    # Moogle character indexes
    FIRST_MOOGLE = 0x12
    LAST_MOOGLE = 0x1B

    DEFAULT_NAME = ["TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN", "CELES", "STRAGO", "RELM", "SETZER", "MOG", "GAU", "GOGO", "UMARO"]

    INIT_DATA_START = 0x2d7ca0
    INIT_DATA_END = 0x2d821f
    INIT_DATA_SIZE = 22

    NAMES_START = 0x478c0
    NAMES_END = 0x47a3f
    NAME_SIZE = 6

    def __init__(self, rom, args, spells):
        self.rom = rom
        self.args = args

        self.init_data = DataArray(self.rom, self.INIT_DATA_START, self.INIT_DATA_END, self.INIT_DATA_SIZE)
        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)

        self.characters = []
        for character_index in range(len(self.name_data)):
            character = Character(character_index, self.init_data[character_index], self.name_data[character_index])
            self.characters.append(character)

        self.playable = self.characters[:self.CHARACTER_COUNT]

        self.natural_magic = NaturalMagic(self.rom, self.args, self, spells)
        self.commands = Commands(self.characters)

        self.menu_character_sprites = MenuCharacterSprites(self.rom, self.args)
        self.character_sprites = CharacterSprites(self.rom, self.args)
        self.character_palettes = CharacterPalettes(self.rom, self.args, self.menu_character_sprites)

        self.battle_scripts = PartyBattleScripts(self.rom, self.args, self)

        self.available_characters = list(range(self.CHARACTER_COUNT))

        # path of characters required to unlock each character
        # e.g. self.character_paths[self.TERRA] = all characters required for terra (in order)
        self.character_paths = [[] for char_index in range(self.CHARACTER_COUNT)]

    def get_available_count(self):
        return len(self.available_characters)

    def set_unavailable(self, character):
        self.available_characters.remove(character)

    def get_random_available(self, exclude = None):
        if exclude is None:
            exclude = []

        import random
        possible_characters = [character_id for character_id in self.available_characters if character_id not in exclude]
        random_character = random.choice(possible_characters)
        self.set_unavailable(random_character)
        return random_character

    def set_character_path(self, character, required_character):
        if required_character is not None:
            self.character_paths[character].extend(self.character_paths[required_character])
            self.character_paths[character].append(required_character)

    def get_character_path(self, character):
        return self.character_paths[character]


    ### Mod to specify character starting levels on a character-by-character basis
    ### Mod to exclude characters from level averaging
    ### Maybe move this to characters_asm.py
    def mod_init_levels(self):
        if self.args.force_character_starting_levels:

##org $C0A10B
##; we are hijacking a JSR to "get the level average of the party"
##; simply because we are going to manually set the level of this character
##; but then there's the level factoring code as well
##; it no longer serves a purpose, so let's get rid of it
##LDA $EC  ; get our character from our event argument
##STA $1600,Y  ; save it as ID
##TAX
##LDA C0get_level,X
##BNE level_not_zero
##LDA #$01  ; enfore a minimum level of 1
##level_not_zero:
##CMP #$63  ; 99 or higher?
##BCC level_not_99
##LDA #$63
##level_not_99:
##STA $1608,Y
##JSR $A27E  ; get max HP
##REP #$20
##LDA $160B,Y  ; max HP
##STA $1609,Y  ; save as current
##SEP #$20
##TDC
##JSR $A2BC  ; get max MP
##REP #$20
##LDA $160F,Y  ; max MP
##STA $160D,Y  ; save as current
##SEP #$20
##TDC
##JSR $A235  ; determine experience needed for next level
##TYX
##JSR $9DF0
##LDA $087C,Y
##AND #$F0
##ORA #$01
##STA $087C,Y
##LDA $0868,Y
##ORA #$01
##STA $0868,Y
##TDC
##STA $0867,Y
##TXY
##JSR $A17F  ; natural magic and abilities
##LDA #$03
##JMP $9B5C  ; advance event queue 3 bytes
## 
##C0get_level:
##DB $00  ; Terra
##DB $00  ; Locke
##DB $00  ; Cyan
##DB $00  ; Shadow
##DB $00  ; Edgar
##DB $00  ; Sabin
##DB $00  ; Celes
##DB $00  ; Strago
##DB $00  ; Relm
##DB $00  ; Setzer
##DB $00  ; Mog
##DB $00  ; Gau
##DB $00  ; Gogo
##DB $00  ; Umaro
## 
##padbyte $EA : pad $C0A17F
            
            space = Reserve(0xa10b, 0xa17e, "set_char_levels", asm.NOP())
            space.write(
                #use asm.DIR for $EC
                asm.LDA(0xEC, asm.DIR),    #get character
                asm.STA(0x1600, asm.ABS_Y), #save it as ID
                asm.TAX(),
                asm.LDA(0xa164, asm.LNG_X),  #can't use string here, had to put A164 directly
                asm.BNE("level_not_zero"),
                #use asm.IMM for #$01
                asm.LDA(0x01, asm.IMM8),   # enforce min level of 1
                "level_not_zero",
                asm.CMP(0x63, asm.IMM8),  #99 or higher?
                asm.BCC("level_not_99"),
                asm.LDA(0x63, asm.IMM8),
                "level_not_99",
                asm.STA(0x1608, asm.ABS_Y),
                asm.JSR(0xA27E, asm.ABS),  #get max HP
                asm.REP(0x20),
                asm.LDA(0x160B, asm.ABS_Y),  #max HP
                asm.STA(0x1609, asm.ABS_Y),  #save as current
                asm.SEP(0x20),
                asm.TDC(),
                asm.JSR(0xA2BC, asm.ABS),  #get max MP
                asm.REP(0x20),
                asm.LDA(0x160F, asm.ABS_Y),  #max MP
                asm.STA(0x160D, asm.ABS_Y),  #save as current
                asm.SEP(0x20),
                asm.TDC(),
                asm.JSR(0xA235, asm.ABS),   #determine XP needed for next level
                asm.TYX(),
                asm.JSR(0x9DF0, asm.ABS),
                asm.LDA(0x087C, asm.ABS_Y),
                asm.AND(0xF0, asm.IMM8),
                asm.ORA(0x01, asm.IMM8),
                asm.STA(0x087C, asm.ABS_Y),
                asm.LDA(0x0868, asm.ABS_Y),
                asm.ORA(0x01, asm.IMM8),
                asm.STA(0x0868, asm.ABS_Y),
                asm.TDC(),
                asm.STA(0x0867, asm.ABS_Y),
                asm.TXY(),
                asm.JSR(0xA17F, asm.ABS),  #jump to natural magic and abilities
                asm.LDA(0x03, asm.IMM8),
                asm.JMP(0x9B5C, asm.ABS),  #advance event queue 3 bytes
                "C0get_level",
                # character starting level values
                int(self.args.start_levels[0]), #Terra
                int(self.args.start_levels[1]), #Locke
                int(self.args.start_levels[2]), #Cyan
                int(self.args.start_levels[3]), #Shadow
                int(self.args.start_levels[4]), #Edgar
                int(self.args.start_levels[5]), #Sabin
                int(self.args.start_levels[6]), #Celes
                int(self.args.start_levels[7]), #Strago
                int(self.args.start_levels[8]), #Relm
                int(self.args.start_levels[9]), #Setzer
                int(self.args.start_levels[10]), #Mog
                int(self.args.start_levels[11]), #Gau
                int(self.args.start_levels[12]), #Gogo
                int(self.args.start_levels[13]), #Umaro
            )
            #space.printr()            

        #end of forced level value

        if self.args.exclude_character_from_level_averaging:
##hirom
## 
##org $C09F78
##; we are going to hijack the "get average level" routine
##; to remove *specific* characters from the factoring
##; the characters excluded will be a simple bitfield
##JSR factor_out
## 
##org $C0D630
##exclude_finish:
##; the state of M, A, X, and Y are actually irrelevant here for a change
##LDX $1EDE
##RTS
## 
##factor_out:
##REP #$21
##LDA C0_characters_to_exclude  ; load the character bitfield for those we don't want to factor into level averaging
##BIT $1EDE  ; have we recruited any of these characters?
##BEQ exclude_finish  ; branch if not, this is a simple safety measure to make sure we don't accidently un-factor someone we don't want to.
##; in theory, this shouldn't matter, but it never hurts to have checks in
##LDA C0_characters_to_exclude  ; load the bit(s) of characters we want excluded
##STA $1E
##LDA $1EDE  ; load our roster
##STA $20
##TDC
##TAY  ; set Y to 0
##INC A  ; set A to 1
##STA $1B  ; save it to scatch
##character_check_loop:
##LDA $1B
##BIT $20  ; have we recruited this character?
##BEQ character_next_iteration
##; now we check to make sure whether or not we should include this character into level averaging
##BIT $1E  ; is this character excluded?
##BEQ character_next_iteration  ; branch if not
##LDA $20  ; load roster
##EOR $1E  ; flip off the bit for this character
##STA $20  ; and save it to the roster
##LDA $1B
##character_next_iteration:
##ASL $1B  ; move on to the next character to check
##INY
##CPY #$000E  ; have we done all 14 characters yet?
##BNE character_check_loop
##LDA $20  ; load our now factored-out roster
##TAX
##RTS
## 
##C0_characters_to_exclude:
##DW $0000
##; below is the bitfield of characters, it is in binary
##; set the bit in the word above to remove that character from being factored into leveling
##; 0000 0000 0000 0001 - Terra ($01)
##; 0000 0000 0000 0010 - Locke ($02)
##; 0000 0000 0000 0100 - Cyan ($04)
##; 0000 0000 0000 1000 - Shadow ($08)
##; 0000 0000 0001 0000 - Edgar ($10)
##; 0000 0000 0010 0000 - Sabin ($20)
##; 0000 0000 0100 0000 - Celes ($40)
##; 0000 0000 1000 0000 - Strago ($80)
##; 0000 0001 0000 0000 - Relm ($0100)
##; 0000 0010 0000 0000 - Setzer ($0200)
##; 0000 0100 0000 0000 - Mog ($0400)
##; 0000 1000 0000 0000 - Gau ($0800)
##; 0001 0000 0000 0000 - Gogo ($1000)
##; 0010 0000 0000 0000 - Umaro ($2000)
##; the highest bit is used in character data for the Merit award and is ignored here
## 

            ##; we are going to hijack the "get average level" routine
            ##; to remove *specific* characters from the factoring
            ##; the characters excluded will be a simple bitfield
            space = Reserve(0x9f78, 0x9f7a, "factor_out_jump")
            space.write(
                asm.JSR(0xd634, asm.ABS), 
            )
            #space.printr()

            # reverse the argument input, which expects Terra->Umaro
            exclude_bitfield = self.args.excluded_characters_from_avg[::-1]

            val2 = ""
            val1 = ""
            val4 = ""
            val3 = ""
            val3 = "".join(exclude_bitfield[0:2])
            val4 = "".join(exclude_bitfield[2:6])
            val1 = "".join(exclude_bitfield[6:10])
            val2 = "".join(exclude_bitfield[10:14])
##            for i in range(2):
##                val3 = val3 + exclude_bitfield[i]                           
##            for i in range(4):
##                val4 = val4 + exclude_bitfield[i+2]
##            for i in range(4):
##                val1 = val1 + exclude_bitfield[i+6]
##            for i in range(4):
##                val2 = val2 + exclude_bitfield[i+10]
            exclflags0 = int(val1 + val2, 2)
            exclflags1 = int(val3 + val4, 2)
            #print(exclflags0)
            #print(exclflags1)
            #input("X")

            space = Reserve(0xd630, 0xd66e, "factor_out")
            space.write(
                "exclude_finish",  #the state of M, A, X, and Y are actually irrelevant here for a change
                asm.LDX(0x1EDE, asm.ABS),
                asm.RTS(),
                "factor_out",
                asm.REP(0x21),
                asm.LDA(0xc0d66d, asm.LNG),  #load the character bitfield for those we don't want to factor into level averaging
                asm.BIT(0x1EDE, asm.ABS),  #have we recruited any of these characters?
                asm.BEQ("exclude_finish"),  #branch if not, this is a simple safety measure to make sure we don't accidently un-factor someone we don't want to.
                #in theory, this shouldn't matter, but it never hurts to have checks in
                asm.LDA(0xc0d66d, asm.LNG),  #load the bit(s) of characters we want excluded
                asm.STA(0x1e, asm.DIR),
                asm.LDA(0x1EDE, asm.ABS),  #load our roster
                asm.STA(0x20, asm.DIR),
                asm.TDC(),
                asm.TAY(),  #set Y to 0
                asm.INC(),  #set A to 1
                asm.STA(0x1B, asm.DIR),  #save it to scatch
                "character_check_loop",
                asm.LDA(0x1B, asm.DIR),
                asm.BIT(0x20, asm.DIR),  #have we recruited this character?
                asm.BEQ("character_next_iteration"),
                #now we check to make sure whether or not we should include this character into level averaging
                asm.BIT(0x1e, asm.DIR),  #is this character excluded?
                asm.BEQ("character_next_iteration"),  #branch if not
                asm.LDA(0x20, asm.DIR),   #load roster
                asm.EOR(0x1b, asm.DIR),   #flip off the bit for this character
                asm.STA(0x20, asm.DIR),   #and save it to the roster
                asm.LDA(0x1b, asm.DIR),
                "character_next_iteration",
                asm.ASL(0x1b, asm.DIR),  #move on to the next character to check
                asm.INY(),
                asm.CPY(0x000E, asm.IMM16),  #have we done all 14 characters yet?
                asm.BNE("character_check_loop"),
                asm.LDA(0x20, asm.DIR),  #load our now factored-out roster
                asm.TAX(),
                asm.RTS(),
                "C0_characters_to_exclude",
                exclflags0,
                exclflags1,
                #below is the bitfield of characters, it is in binary
                #set the bit in the word above to remove that character from being factored into leveling
                #0000 0000 0000 0001 - Terra ($01)
                #0000 0000 0000 0010 - Locke ($02)
                #0000 0000 0000 0100 - Cyan ($04)
                #0000 0000 0000 1000 - Shadow ($08)
                #0000 0000 0001 0000 - Edgar ($10)
                #0000 0000 0010 0000 - Sabin ($20)
                #0000 0000 0100 0000 - Celes ($40)
                #0000 0000 1000 0000 - Strago ($80)
                #0000 0001 0000 0000 - Relm ($0100)
                #0000 0010 0000 0000 - Setzer ($0200)
                #0000 0100 0000 0000 - Mog ($0400)
                #0000 1000 0000 0000 - Gau ($0800)
                #0001 0000 0000 0000 - Gogo ($1000)
                #0010 0000 0000 0000 - Umaro ($2000)
                #the highest bit is used in character data for the Merit award and is ignored here

                #0x00, 0x00 causes all characters to be level averaged
                #0x0F, 0x00 causes Terra/Locke/Cyan/Shadow to not be used in the level averaging calc
                #little endian means we needed to swap the order of this
                #0x0F,
                #0x00,
            )
            #space = Write(Bank.C0, src, "asdf")
            #space.printr()

        ### end of character exclusion from lvl averaging
            
        if self.args.start_average_level:
            # remove all variation in leveling, since we're controlling level directly
            for character in self.characters:
                character.init_level_factor = 0

            characters_asm.set_starting_level(self.args.start_level)

    def stats_random_percent(self):
        import random
        stats = ["init_extra_hp", "init_extra_mp", "init_vigor", "init_speed", "init_stamina", "init_magic",
                 "init_attack", "init_defense", "init_magic_defense", "init_evasion", "init_magic_evasion"]
        for character in self.characters:
            for stat in stats:
                stat_value = getattr(character, stat)
                if stat_value != 0:
                    character_stat_percent = random.randint(self.args.character_stat_random_percent_min,
                                                            self.args.character_stat_random_percent_max) / 100.0
                    value = int(stat_value * character_stat_percent)
                    setattr(character, stat, max(min(value, 255), 0))

    def get_characters_with_command(self, command_name):
        from constants.commands import name_id
        command_id = name_id[command_name]

        result = []
        for character in self.characters:
            if command_id in character.commands:
                result.append(character.id)
        return result

    def mod_names(self):
        for character_id, name in enumerate(self.args.names):
            self.characters[character_id].name = name

    ### Mod to have characters equipped with ultimate items when recruited
    def start_with_ultimates(self):
        self.characters[0].init_right_hand = 11
        self.characters[1].init_right_hand = 20
        self.characters[2].init_right_hand = 44
        self.characters[3].init_right_hand = 38
        self.characters[4].init_right_hand = 31
        self.characters[5].init_right_hand = 84
        self.characters[6].init_right_hand = 45
        self.characters[7].init_right_hand = 59
        self.characters[8].init_right_hand = 62
        self.characters[9].init_right_hand = 78
        self.characters[10].init_right_hand = 16
        self.characters[11].init_head = 111
        self.characters[12].init_right_hand = 71
        self.characters[13].init_relic1 = 223
        ### ult mod reference list
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

    ### Mod to swap initial stats between characters
    ### Exclude Umaro for now - they are really good
    def swap_stats(self):
        extra_hp_list = []
        extra_mp_list = []
        vigor_list = []
        speed_list = []
        stamina_list = []
        magic_list = []
        attack_list = []
        defense_list = []
        magic_defense_list = []
        evasion_list = []
        magic_evasion_list = []
        for char in self.characters:
            if char.id < 13:  #skip Umaro
                extra_hp_list.append(char.init_extra_hp)
                extra_mp_list.append(char.init_extra_mp)
                vigor_list.append(char.init_vigor)
                speed_list.append(char.init_speed)
                stamina_list.append(char.init_stamina)
                magic_list.append(char.init_magic)
                attack_list.append(char.init_attack)
                defense_list.append(char.init_defense)
                magic_defense_list.append(char.init_magic_defense)
                evasion_list.append(char.init_evasion)
                magic_evasion_list.append(char.init_magic_evasion)

        import random
        for char in self.characters:
            if char.id < 13:  #skip Umaro
                char.init_extra_hp = extra_hp_list.pop(random.randrange(len(extra_hp_list)))
                char.init_extra_mp = extra_mp_list.pop(random.randrange(len(extra_mp_list)))
                char.init_vigor = vigor_list.pop(random.randrange(len(vigor_list)))
                char.init_speed = speed_list.pop(random.randrange(len(speed_list)))
                char.init_stamina = stamina_list.pop(random.randrange(len(stamina_list)))
                char.init_magic = magic_list.pop(random.randrange(len(magic_list)))
                char.init_attack = attack_list.pop(random.randrange(len(attack_list)))
                char.init_defense = defense_list.pop(random.randrange(len(defense_list)))
                char.init_magic_defense = magic_defense_list.pop(random.randrange(len(magic_defense_list)))
                char.init_evasion = evasion_list.pop(random.randrange(len(evasion_list)))
                char.init_magic_evasion = magic_evasion_list.pop(random.randrange(len(magic_evasion_list)))
    ### End of: Mod to swap initial stats between characters

    def mod(self):
        if self.args.start_naked:
            for char in self.characters:
                char.clear_init_equip()

        if self.args.equipable_umaro:
            characters_asm.equipable_umaro(self.CHARACTER_COUNT)

        ### Mod for characters starting with ultimates
        if self.args.ultimate_items and self.args.start_ultimates:
            self.start_with_ultimates()

        self.mod_init_levels()

        ### Mod to swap character initial stats
        if self.args.character_swap_stats:
            self.swap_stats()

        if self.args.character_stat_random_percent:
            self.stats_random_percent()

        self.commands.mod()

        if self.args.character_names:
            self.mod_names()

        if self.args.original_name_display:
            characters_asm.show_original_names()

        ### Note: natural_magic.mod reserves C0 space. if command tiering
        ### then you have to wait until after Events to know who can use Magic/X Magic
        ### seems to have problems if this is the case though
        self.natural_magic.mod()

        self.character_sprites.mod()
        self.character_palettes.mod()
        self.battle_scripts.mod()

    def write(self):
        if self.args.spoiler_log:
            self.commands.log()

        for character_index in range(len(self.characters)):
            self.init_data[character_index] = self.characters[character_index].init_data()
            self.name_data[character_index] = self.characters[character_index].name_data()

        self.init_data.write()
        self.name_data.write()

        self.natural_magic.write()

        self.menu_character_sprites.write()
        self.character_sprites.write()
        self.character_palettes.write()
        self.battle_scripts.write()

    def print_character_paths(self):
        for char_index in range(self.CHARACTER_COUNT):
            path = self.get_character_path(char_index)
            for req_char_index in path:
                print(f"{self.DEFAULT_NAME[req_char_index]} -> ", end = '')
            print(f"{self.DEFAULT_NAME[char_index]}")

    def print(self):
        for char in self.characters:
            char.print()

    def get(self, character):
        for char in self.characters:
            if char.id == character:
                return char

    def get_by_name(self, name):
        for char in self.characters:
            if self.DEFAULT_NAME[char.id].lower() == name.lower():
                return char

    def get_name(self, character):
        return self.characters[character].name.rstrip('\0')

    def get_default_name(self, character):
        return self.DEFAULT_NAME[character]

    def get_sprite(self, character):
        return self.character_sprites.character_sprites[character].id

    def get_random_esper_item_sprite(self):
        sprites = [self.SOLDIER, self.IMP, self.MERCHANT, self.GHOST]

        import random
        return sprites[random.randrange(len(sprites))]

    def get_palette(self, character):
        return self.character_palettes.get(character)


    ### Display character stats
    def log(self):                          
        from log import section, format_option
        stat_labels = ["Extra HP", "Extra MP", "Vigor", "Speed", "Stamina", "MagPwr",
                       "Bat.Pwr", "Def", "MDef", "Evade", "MBlock"]
        stat_attributes = ["init_extra_hp", "init_extra_mp", "init_vigor", "init_speed", "init_stamina", "init_magic", 
                           "init_attack", "init_defense", "init_magic_defense", "init_evasion", "init_magic_evasion"]


        display_stats = False
        # Only display changed initial stats IF spoiler log is on
        if self.args.character_swap_stats or self.args.character_stat_random_percent:
            if self.args.spoiler_log:
                display_stats = True
        else:
            # display vanilla stats
            display_stats = True

        if display_stats:
            lcolumn = []                   
            lcolumn.append(format_option("Name", '  '.join(stat_labels)))                                                  
                                                  
            for character in self.playable:                                                                                
                line = []                                                                                                  
                for label, attribute in zip(stat_labels, stat_attributes):                                                 
                    line.append(f"{getattr(character, attribute):<{len(label)}}")                                          
                lcolumn.append(format_option(character.name, '  '.join(line)))                                             
                                                                                                                           
            section("Character Stats", lcolumn, [])    


    ### Experimental section:
    ### mod to tier character levels based on depth
    ### 2022-11-28: this mod might be outdated due to being able to directly set
    ### character start levels with the flag -cstartlvl
        
    ### for the starting party, level is calculated in order of the party:
    ### Char 1 = 3 + C1LF
    ### Char 2 = max(3 + C1LF, 3 + C2LF)
    ### Char 3 = max(avg(Char 1 and Char 2), 3 + C3LF)
    ### Char 4 = max(avg(Char 1 and Char 2 and Char 3), 3 + C4LF)
        
    ### Char 1 will be given level 3 + Char 1's level factor

    ### Char 2's lowest possible level will be Char 1's level (level 3 + Char 1's level factor)
    ### If 3 + Char 2's level factor is greater than 3 + Char 1's level factor, use that instead

    ### Char 3's lowest possible level will be the average of the first 2 characters' levels
    ### If 3 + Char 3's level factor is greater than this average, it will use that instead

    ### If the next character has a higher level factor, that character's level will use that higher level factor
    ### otherwise it will use the average level of the party
    #
    ### somewhat wonky with low max depth seeds (<=6)
    def mod_tiered_init_levels(self, character_depth):
        ### get max depths
        max_depth = 0
        sum_depth = 0
        avg_depth = 0
        for x, depth in character_depth.items():
            sum_depth += depth
            if depth > max_depth:
                max_depth = depth
        avg_depth = sum_depth / 14
        print(character_depth)
        print("Max depth: " + str(max_depth))
        # Depth levels: highest for last 25%
        import math
        highest_depth = math.ceil(max_depth * 0.9)
        high_depth = (max_depth + avg_depth) / 2
        if high_depth > highest_depth:
            high_depth = max_depth * 0.6
        #avg_depth = math.floor(avg_depth)
        print("Highest: " + str(highest_depth))
        print("High: " + str(high_depth))
        print("Avg depth: " + str(avg_depth))
        
        for characters in self.characters:
            if characters.id <= 13:
                if character_depth[characters.name] >= highest_depth:
                    print("3: " + str(characters.name))
                    characters._init_level_factor = 3
                elif character_depth[characters.name] >= high_depth:
                    print("2: " + str(characters.name))
                    characters._init_level_factor = 2
                elif character_depth[characters.name] >= avg_depth:
                    print("1: " + str(characters.name))
                    characters._init_level_factor = 1
                else:
                    characters._init_level_factor = 0

        low_factor = math.floor(avg_depth * 5)
        mid_factor = math.floor(high_depth * 6)
        high_factor = min(math.floor(highest_depth * 7), 96)
        print("Low: " + str(low_factor+3) + " | Mid: " +
              str(mid_factor+3) + " | High: " + str(high_factor+3))
        characters_asm.mod_level_factor_adjustment(mod0=0x0, mod1=hex(low_factor),
                                                   mod2=hex(mid_factor), mod3=hex(high_factor))


