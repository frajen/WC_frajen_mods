from data.enemy_script import EnemyScript
from data.enemy_script_custom_commands import EnemyScriptCommands
from data.enemy_script_dialogs import EnemyScriptDialogs
from data.enemy_script_abilities import EnemyScriptAbilities
from data.structures import DataMap

import data.enemy_script_commands as ai_instr

### used for script-to-English
from constants.commands import id_name as commands_id_name
from data.spell_names import id_name as spells_id_name
from data.item_names import id_name as items_id_name


class EnemyScripts():
    SCRIPT_PTRS_START = 0xf8400
    SCRIPT_PTRS_END   = 0xf86ff
    SCRIPTS_START = 0xf8700
    SCRIPTS_END   = 0xfc04f

    def __init__(self, rom, args, enemies):
        self.rom = rom
        self.args = args
        self.enemies = enemies

        self.script_data = DataMap(self.rom, self.SCRIPT_PTRS_START, self.SCRIPT_PTRS_END,
                                   self.rom.SHORT_PTR_SIZE, self.SCRIPTS_START,
                                   self.SCRIPTS_START, self.SCRIPTS_END)

        self.scripts = []
        for script_index in range(len(self.script_data)):
            script = EnemyScript(script_index, self.script_data[script_index])
            self.scripts.append(script)


        if 0 == 1:
            def check_slots(slot_str):
                slots_binary = str(bin(slot_str)[2:])   
                slots_binary = reversed(slots_binary)
                output_str = ""
                for index, x in enumerate(slots_binary):
                    if x == "1":
                        output_str = output_str + "#" + str(index+1) + ", "
                output_str = output_str[:-2]
                return output_str

        #script english decoder
            for index, script in enumerate(self.scripts):
                enemy = self.enemies.enemies[index]
                print("Name: " + enemy.name + " | ID: " + str(enemy.id))
                for instruction in script.instructions:
                    if type(instruction) is ai_instr.Spell:
                        if str(instruction) == "Battle":
                            print("Battle")
                        elif str(instruction) == "Special":
                            print("Special")
                        else:
                            print("Ability: " + str(instruction))
                    elif type(instruction) is ai_instr.RandomAttack:
                        print("1/3 chance " + str(instruction))
                        #print(str(instruction))
                    elif type(instruction) is ai_instr.If:
                        codes = str(instruction).split(" ")
                        x = codes[1]
                        y = codes[2]
                        z = codes[3]
                        if x == "1":
                            print("If the last attack was either of the commands: " + 
                                    commands_id_name[int(y)] + " or " +
                                    commands_id_name[int(z)])
                        elif x == "2":
                            print("If monster was targeted by either of the abilities: " + 
                                    spells_id_name[int(y)] + " or " +
                                    spells_id_name[int(z)])
                        elif x == "3":
                            print("If monster was targeted by either of the items: " + 
                                    items_id_name[int(y)] + " or " +
                                    items_id_name[int(z)])
                        elif x == "4":
                            element_slots = check_slots(int(y))
                            element_slots = element_slots.replace("#1", "Fire")
                            element_slots = element_slots.replace("#2", "Ice")
                            element_slots = element_slots.replace("#3", "Bolt")
                            element_slots = element_slots.replace("#4", "Poison")
                            element_slots = element_slots.replace("#5", "Wind")
                            element_slots = element_slots.replace("#6", "Pearl")
                            element_slots = element_slots.replace("#7", "Earth")
                            element_slots = element_slots.replace("#8", "Water")
                            print("If monster was targeted by the following element(s): " + element_slots)
                        elif x == "5":
                            print("If monster has been attacked: ")
                        elif x == "6":
                            print("If target " + str(int(y)) + " HP is below: " + str(int(z)))
                            #note this is possibly modded, see data/enemy_script_abilities.py
                        elif x == "7":
                            print("If target " + str(int(y)) + " MP is below: " + str(int(z)))
                            #note this is possibly modded, see data/enemy_script_abilities.py
                        elif x == "8":
                            print("If target " + str(int(y)) + " has statuses: " + str(int(z)))
                        elif x == "9":
                            print("If target " + str(int(y)) + " does not have statuses: " + str(int(z)))
                        #elif x == "10":
                            #print("The following commands are never executed.")
                        elif x == "11":
                            print("If monster's battle timer is more than " + str(int(y)))
                        elif x == "12":
                            print("If VAR " + str(int(y)) + " is less than VAR " + str(int(z)))
                        elif x == "13":
                            print("If VAR " + str(int(y)) + " is greater than VAR " + str(int(z)))
                        elif x == "14":
                            print("If target " + str(int(y)) + " level is less than " + str(int(z)))
                        elif x == "15":
                            print("If target " + str(int(y)) + " level is greater than " + str(int(z)))
                        elif x == "16":
                            print("If only 1 type of monster is alive:")
                        elif x == "17":
                            print("If the monster(s) in slot(s) " + check_slots(int(y)) + " are alive:")
                        elif x == "18":
                            if y == "0":
                                print("If monster has died: ")
                            else:
                                print("If the monster(s) in slot(s) " + check_slots(int(y)) + " have died: ")
                                # the byte here determines which monsters to 
                                # check, with each bit for each monster
                                # a value of 0x01 means monster in slot 1
                                # a value of 0x02 means monster in slot 2
                                # a value of 0x03 means monsters in slots 1 and 2
                                # a value of 0x04 means monster in slot 3
                                # a value of 0x07 means monsters in slots 1, 2, 3
                                # a value of 0x3F means monsters in slots 1, 2, 3, 4, 5, 6

##                        elif x == "19":
##                            #certain # of monsters/characters are alive
##                        elif x == "20":
##                            #certain bit of certain variable is set
##                        elif x == "21":
##                            #certain bit of certain variable is NOT set
##                        elif x == "22":
##                            #if global battle timer is larger than value in int(y)
##                        elif x == "23":
##                            #sets the target of the next attack
##                        elif x == "24":
##                            #if Gau has not joined the party (not seen)
##                        elif x == "25":
##                            #if monster is certain # in the formation
##                        elif x == "26":
##                            #if target is weak vs an element
##                        elif x == "27":
##                            #if battle formation is = to int(y)
##                        elif x == "28":
##                            #always execute even if Quick is in effect
                        else:
                            print(str(instruction))
                    else:
                        print(str(instruction))
                    

        # if a script begins with
        # an attack, there must be an accompanying 0xFF to signal
        # the "End first wave of attack" (EndMainLoop ? )
        # afterwards, conditinals may be cut off by
        # scripts simplying ending with 1 0xFF (EndScript ? )

        self.enemy_script_custom_commands = EnemyScriptCommands(self.rom, self.args, self, self.enemies)
        self.enemy_script_dialogs = EnemyScriptDialogs(self.args, self)
        self.enemy_script_abilities = EnemyScriptAbilities(self.args, self, self.enemies)

    def __len__(self):
        return len(self.scripts)

    def get_script(self, enemy_name):
        enemy_id = self.enemies.get_enemy(enemy_name)
        return self.scripts[enemy_id]

    def cleanup_mod(self):
        terra_kefka_burn_soldiers_script = self.scripts[366]
        terra_kefka_burn_soldiers_script.delete()

        # this script is used for sealed gate bridge battles and kefka vs gestahl fc battle
        sealed_gate_and_floating_continent_script = self.scripts[379]
        sealed_gate_and_floating_continent_script.delete()

    def mag_roader_wild_cat_fix(self):
        # fix small brown mag roader missing end script byte
        mag_roader_id = 243
        mag_roader_script = self.scripts[mag_roader_id]
        mag_roader_script.append(ai_instr.EndScript())

    def rizopas_timer_mod(self):
        # randomize time until rizopas appears to prevent doing nothing until 60 seconds passes
        piranha_script = self.get_script("Piranha")

        import random
        random_time = random.randint(5, 55) # average of 30

        original_time = 60
        if random_time == original_time:
            return

        rizopas_timer_check = ai_instr.If(0x16, 0x3c, 0x00) # if timer is larger than 0x3c (60)
        rizopas_timer_check_new = ai_instr.If(0x16, random_time, 0x00) # if timer is larger than random_time

        piranha_script.replace(rizopas_timer_check, rizopas_timer_check_new)

    def ifrit_shiva_death_mod(self):
        ifrit_script = self.get_script("Ifrit")
        shiva_script = self.get_script("Shiva")

        # there are 2 versions of ifrit/shiva, do not show the event one for whichever was killed or no exp received
        show_both = ai_instr.ChangeEnemies(0x00, 0x00, 0x03)    # show shiva/ifrit, restore their hp
        show_ifrit = ai_instr.ChangeEnemies(0x00, 0x00, 0x01)   # show ifrit, restore hp
        show_shiva = ai_instr.ChangeEnemies(0x00, 0x00, 0x02)   # show shiva, restore hp

        ifrit_script.replace(show_both, show_shiva)
        shiva_script.replace(show_both, show_ifrit)

        end_battle = ai_instr.Misc(0x02, 0x00)                  # end battle
        boss_death = ai_instr.ChangeEnemies(0x0c, 0x01, 0xff)   # kill all enemies with boss death animation

        ifrit_script.replace(end_battle, boss_death)
        shiva_script.replace(end_battle, boss_death)

    def doom_gaze_no_escape_mod(self):
        from data.spell_names import name_id

        doom_gaze_script = self.get_script("Doom Gaze")
        escape_turn = [
            ai_instr.EndTurn(),         # wait until next turn
            ai_instr.SetTarget(0x36),   # set target: self
            ai_instr.RandomAttack(name_id["Nothing"], name_id["Escape"], name_id["Escape"]),
        ]
        doom_gaze_script.remove(escape_turn)

    def doom_gaze_event_bit_mod(self):
        doom_gaze_script = self.get_script("Doom Gaze")

        # instructions which set doom gaze defeated event bit
        set_defeated_bit = ai_instr.Bits(0x01, 0x0d, 0x00) # set bit 0x00 in byte 13 (1dd2, bit 0)
        doom_gaze_script.remove(set_defeated_bit)

    def wrexsoul_no_zinger_mod(self):
        from data.spell_names import name_id

        wrexsoul_script = self.get_script("Wrexsoul")

        # first turn, executes dialog and zinger
        dialog_zinger = [
            ai_instr.If(0x15, 0x00, 0x01),      # if byte 0 bit 0x01 clear
            ai_instr.Bits(0x01, 0x00, 0x01),    # set bit 0x01 in byte 0
            ai_instr.Event(0x1f),               # trigger event 0x1f (dialog)
            ai_instr.Spell(name_id["Zinger"]),
            ai_instr.EndIf(),
        ]
        wrexsoul_script.remove(dialog_zinger)

        # zinger's after the first
        zinger_turn = [
            ai_instr.EndTurn(),                 # wait until next turn
            ai_instr.SetTarget(0x44),           # set target: random ally
            ai_instr.RandomAttack(name_id["Nothing"], name_id["Zinger"], name_id["Zinger"])
        ]
        wrexsoul_script.remove(zinger_turn)

    def srbehemoth_no_back_attack_mod(self):
        srbehemoth_id = 281 # first battle
        srbehemoth_script = self.scripts[srbehemoth_id]

        # move allies from right side to left side for second srbehemoth
        party_move = ai_instr.Animate(0x06, 0x00, 0x00)
        srbehemoth_script.remove(party_move)

    def chadarnook_flashing_mod(self):
        chadarnook_painting_script = self.get_script("Chadarnook")

        switch_animation = 0x0d # enemies flash in and out rapidly

        switch_to_demon = [
            ai_instr.ChangeEnemies(0x0e, 0x02, 0x02),   # lightning flash, add enemy 2 at current hp
            ai_instr.ChangeEnemies(0x0e, 0x01, 0x01),   # lightning flash, remove enemy 1
        ]
        switch_to_demon_new = [
            ai_instr.ChangeEnemies(switch_animation, 0x02, 0x02), # change animation
            ai_instr.ChangeEnemies(switch_animation, 0x01, 0x01), # change animation
        ]
        chadarnook_painting_script.replace(switch_to_demon, switch_to_demon_new, count = 2)

        chadarnook_demon_id = 328
        chadarnook_demon_script = self.scripts[chadarnook_demon_id]

        switch_to_painting = [
            ai_instr.ChangeEnemies(0x0e, 0x02, 0x01),   # lightning flash, add enemy 1 at current hp
            ai_instr.ChangeEnemies(0x0e, 0x01, 0x02),   # lightning flash, remove enemy 2
        ]
        switch_to_painting_new = [
            ai_instr.ChangeEnemies(switch_animation, 0x02, 0x01), # change animation
            ai_instr.ChangeEnemies(switch_animation, 0x01, 0x02), # change animation
        ]
        chadarnook_demon_script.replace(switch_to_painting, switch_to_painting_new, count = 2)

    def chadarnook_more_demon_mod(self):
        chadarnook_demon_id = 328
        chadarnook_demon_script = self.scripts[chadarnook_demon_id]

        # NOTE: if the painting returns and only takes one action, the switch was triggered by number of attacks
        #       if the painting returns and takes 2 or 3 actions, the switch was triggered by the timer

        # timer until demon turns back to painting (default is 40)
        time_until_switch = 48
        timer_check = ai_instr.If(0x0b, 0x28, 0x00)
        timer_check_new = ai_instr.If(0x0b, time_until_switch, 0x00)

        # number of times demon attacked before turning back to painting (default is 5 times)
        # NOTE, the threshold is (value + 1), e,g, if set to 4 demon will switch after the 5th attack
        attacks_until_switch = 6 # switch after being targeted 6 times
        attacks_check = ai_instr.If(0x0d, 0x00, 0x04)
        attacks_check_new = ai_instr.If(0x0d, 0x00, attacks_until_switch - 1)

        # when chadarnook demon timer runs out the number of times attacked counter is not reset
        # also, when the number of attacks threshold is reached, the timer is not reset to zero
        # this can cause demon to appear and immediately switch back to the painting
        # change it so both the timer and attack counter are reset before switching
        reset_timer = ai_instr.Misc(0x00, 0x00)                 # reset timer for current enemy
        timer_switch_flag = ai_instr.Arithmetic(0x03, 0x01)     # set a flag telling painting enemy that time ran out
        reset_attacked_count = ai_instr.Arithmetic(0x00, 0x00)  # reset attack counter (var 0000)
        attacked_switch_flag = ai_instr.Arithmetic(0x03, 0x00)  # clear flag telling painting enemy that attack threshold reached (not timer)

        time_up_switch = [
            timer_check,
            reset_timer,
            timer_switch_flag,
        ]
        time_up_switch_new = [
            timer_check_new,
            reset_attacked_count,
            reset_timer,
            timer_switch_flag,
        ]
        chadarnook_demon_script.replace(time_up_switch, time_up_switch_new)

        attacked_enough_switch = [
            attacks_check,
            reset_attacked_count,
            attacked_switch_flag,
        ]
        attacked_enough_switch_new = [
            attacks_check_new,
            reset_attacked_count,
            reset_timer,
            attacked_switch_flag,
        ]
        chadarnook_demon_script.replace(attacked_enough_switch, attacked_enough_switch_new)

    def magimaster_no_ultima_mod(self):
        from data.spell_names import name_id

        magimaster_script = self.get_script("MagiMaster")

        # removing the if/end if causes him to use wallchange before dying so leave them in
        ultima = [
            ai_instr.SetTarget(0x47), # set target: default
            ai_instr.Spell(name_id["Ultima"]),
        ]
        magimaster_script.remove(ultima)

    def hidon_no_chokesmoke(self):
        from data.spell_names import name_id

        hidon_script = self.get_script("Hidon")

        chokesmoke = []
        for character in range(4):
            chokesmoke.extend([
                ai_instr.If(8, 72 + character, 7),
                ai_instr.If(9, 72 + character, 1),
                ai_instr.SetTarget(72 + character),
                ai_instr.Spell(name_id["ChokeSmoke"]),
                ai_instr.EndIf(),
            ])
        hidon_script.remove(chokesmoke)

    def magic_urn_no_life(self):
        from data.spell_names import name_id

        magic_urn_script = self.get_script("Magic Urn")

        life = [
            ai_instr.If(8, 67, 7),
            ai_instr.RandomAttack(name_id["Life"], name_id["Life"], name_id["Life 2"]),
            ai_instr.SetTarget(54),
            ai_instr.RandomAttack(name_id["Escape"], name_id["Nothing"], name_id["Nothing"]),
            ai_instr.EndIf(),
        ]
        magic_urn_script.remove(life)

    def chupon_sneeze_all(self):
        # Make Chupon 64 (Coliseum) target all allies with initial sneeze
        chupon_id = 64
        chupon_script = self.scripts[chupon_id]
        chupon_script.delete()
        chupon_script.insert(0, ai_instr.SetTarget(0x43)) # Target: Allies
        chupon_script.insert(1, ai_instr.Spell(0x02)) # Target: Allies
        chupon_script.insert(2, ai_instr.Spell(0x03)) # Target: Allies
        chupon_script.insert(3, ai_instr.RandomAttack(0x00, 0x01, 0x02)) # Target: Allies
        chupon_script.insert(4, ai_instr.EndScript()) # Target: Allies

    def mod(self):
        # first free up some space for other mods
        self.cleanup_mod()

        # remove dialogs
        self.enemy_script_dialogs.cleanup_mod()

        self.enemy_script_custom_commands.mod()

        self.mag_roader_wild_cat_fix()
        self.rizopas_timer_mod()

        if self.args.boss_experience:
            self.ifrit_shiva_death_mod()

        if self.args.doom_gaze_no_escape:
            self.doom_gaze_no_escape_mod()

            if self.args.boss_battles_shuffle or self.args.boss_battles_random:
                self.doom_gaze_event_bit_mod()

        if self.args.wrexsoul_no_zinger:
            self.wrexsoul_no_zinger_mod()

        if self.args.boss_battles_shuffle or self.args.boss_battles_random:
            # the animation chadarnook uses to switch between demon and painting
            # breaks with other battle backgrounds, they turn weird colors and look very glitchy
            self.chadarnook_flashing_mod()

            self.srbehemoth_no_back_attack_mod()

        if self.args.chadarnook_more_demon:
            self.chadarnook_more_demon_mod()

        if self.args.magimaster_no_ultima:
            self.magimaster_no_ultima_mod()

        if self.args.permadeath:
            self.hidon_no_chokesmoke()
            self.magic_urn_no_life()

        if self.args.random_encounters_chupon:
            self.chupon_sneeze_all()

        if self.args.ability_scaling:
            self.enemy_script_abilities.scale_abilities_mod()

        ### experimental section for AI script randomization
        # update scripts with modded version
        # list of scripts that have been previously modded:
        #366 deleted
        #379 deleted
        #243 mag roader
        #340 piranha
        #264 shiva 265 ifrit
        #285 doom gaze
        #290 wrexsoul
        #281 srbehemoth undead
        #286 chadarnook girl
        #328 chadarnook demon
        #358 magimaster
        #291 hidon
        #85 magic urn
        # list of other random scripts?
        # 367, 368
        # 369 - zone eater
        # 370 - Gau
        # 371 - kefka vs leo
        # 372
        # 373 - SF officer
        # 374 - Cadet
        # 375, 376, 377, 378
        # 379, 380
        # 382, 383
        if 0 == 1:
            modded_scripts = [366, 379, 243, 340, 264, 265, 285, 290, 281, 286, 328, 358, 291, 85,
                              367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 380, 382, 383]
            script_ids = list(range(0, len(self.scripts)))
            updated_script_ids = list((i for i in script_ids if i not in modded_scripts))
            import random

            #print(len(updated_script_ids))
            #print(len(modded_scripts))
            #print(len(self.scripts))

            tlen=[]
            for script in self.scripts:
                tlen.append(len(script.data()))
            #print(tlen)
            #print(sum(tlen))
            # sum up values in here to make sure they're all the same as the next tlen usage

            initial_script_ids = updated_script_ids.copy()
            temp_scripts = []
            if 1 == 1:
                for script_index in range(len(self.scripts)):
                    #print(script_index)
                    #script = self.scripts[script_index]
                    #print(script)
                    #input("Z")
                    #script = ""
                    #if script_index < 2:
                        #script = EnemyScript(3, self.script_data[3])
                        #self.scripts[script_index] = script
                    if script_index in initial_script_ids:
                        if 1 == 1:
                            new_id = random.choice(updated_script_ids)
                            updated_script_ids.remove(new_id)
                            #print(script_index)
                            #print(new_id)
                            #script = EnemyScript(script_index, self.script_data[new_id])
                            script = EnemyScript(script_index, self.script_data[new_id])
                            self.scripts[script_index] = script
                            print(str(script_index) + " | " + str(new_id))
                            #input("X")
                    else:
                        pass
    ##                    script = EnemyScript(script_index, self.script_data[script_index])
    ##                    self.scripts[script_index] = script
    ##                    print(str(script_index) + " | " + str(script_index))

                    #self.scripts[script_index] = script
                    temp_scripts.append(script)
                #end of for loop
                #print(updated_script_ids)
                #input("Y")
                

                    ##### print enemy scripts
                    #print()                                                                                                    
                    #print(self.enemies.get_name(script_index))                                                                 
                    #print(repr(script))    
                    ##### print enemy scripts
                #import sys
                #print(sys.getsizeof([script.data() for script in temp_scripts]))
                #print(sys.getsizeof([script.data() for script in self.scripts]))
                #input("X")
                  
            
    def write(self):
        ### experimental section for AI script randomization
        #for script in self.scripts:
            #print(script.data())
            #input("Z")
        #self.script_data.assign([[0] for script in self.scripts])
        #print(self.script_data[0])
        #print(self.script_data[1])
        #print(self.script_data[2])
        #input("Z")
        #self.script_data.write()
        #tlen = []
        #for script in self.scripts:
            #tlen.append(len(script.data()))
        #print(tlen)
        #print(sum(tlen))

        self.script_data.assign([script.data() for script in self.scripts])
        self.script_data.write()
