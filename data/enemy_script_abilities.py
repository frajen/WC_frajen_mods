from data.spell_names import name_id
from data.enemy_script_custom_commands import *
import data.enemy_script_commands as ai_instr

class EnemyScriptAbilities:
    # spell to replace -> randomization category and +tier
    SPELL_CATEGORY = {
        "Fire"       : FIRE0,
        "Fire 2"     : FIRE0,
        "Fire Ball"  : FIRE0,
        "Blaze"      : FIRE0,
        "Fire Wall"  : FIRE0,
        "Fire Skean" : FIRE1,
        "Elf Fire"   : FIRE1,
        "Fire 3"     : FIRE1,
        "Flare Star" : FIRE1,
        "Merton"     : FIRE2,
        "S. Cross"   : FIRE2,

        "Ice"        : ICE0,
        "Blizzard"   : ICE0,
        "Ice 2"      : ICE0,
        "Storm"      : ICE1,
        "Ice 3"      : ICE1,
        "Absolute 0" : ICE1,
        "Surge"      : ICE1,

        "Bolt"       : BOLT0,
        "Mega Volt"  : BOLT0,
        "Bolt 2"     : BOLT0,
        "Bolt Edge"  : BOLT1,
        "Plasma"     : BOLT1,
        "Bolt 3"     : BOLT1,
        "Giga Volt"  : BOLT1,

        "Lifeshaver" : EARTH0,
        "Slide"      : EARTH0,
        "Magnitude8" : EARTH1,
        "Quake"      : EARTH2,

        "Gale Cut"   : WIND0,
        "Wind Slash" : WIND1,
        "Sand Storm" : WIND1,
        "Aero"       : WIND2,

        "Acid Rain"  : WATER0,
        "Flash Rain" : WATER0,
        "Aqua Rake"  : WATER0,
        "Water Edge" : WATER1,
        "CleanSweep" : WATER1,
        "El Nino"    : WATER1,

        "Poison"     : POISON0,
        "Virite"     : POISON0,
        "Bio"        : POISON0,
        "Pois. Frog" : POISON0,

        "L? Pearl"   : PEARL0,
        "Scar Beam"  : PEARL0,
        "Pearl"      : PEARL1,

        "Shock Wave" : NON_ELEMENTAL0,
        "Heart Burn" : NON_ELEMENTAL0,
        "Stone"      : NON_ELEMENTAL0,
        "L4 Flare"   : NON_ELEMENTAL0,
        "Blow Fish"  : NON_ELEMENTAL1,
        "Rage"       : NON_ELEMENTAL1,
        "Cokatrice"  : NON_ELEMENTAL1,
        "Quasar"     : NON_ELEMENTAL1,
        "Flare"      : NON_ELEMENTAL1,
        "Whump"      : NON_ELEMENTAL1,
        "Meteor"     : NON_ELEMENTAL1,
        "Land Slide" : NON_ELEMENTAL1,
        "GrandTrain" : NON_ELEMENTAL1,
        "Wombat"     : NON_ELEMENTAL2,
        "Meteo"      : NON_ELEMENTAL2,
        "HyperDrive" : NON_ELEMENTAL2,
        "Ultima"     : NON_ELEMENTAL2,

        "Tek Laser"  : TEK0,
        "Diffuser"   : TEK0,
        "Atomic Ray" : TEK0,
        "WaveCannon" : TEK1,
        "Shrapnel"   : TEK1,

        "Cure"       : CURE0,
        "Cure 2"     : CURE0,
        "Sun Bath"   : CURE1,
        "Ice Rabbit" : CURE1,
        "Cure 3"     : CURE1,
    }

    def __init__(self, args, enemy_scripts, enemies):
        self.args = args
        self.enemy_scripts = enemy_scripts
        self.enemies = enemies

    def piranha_scale_mod(self):
        piranha_script = self.enemy_scripts.get_script("Piranha")

        # add a possible scaled special attack to piranhas to increase their difficulty
        battle = [
            ai_instr.Spell(name_id["Battle"]),
            ai_instr.EndMainLoop(),
        ]
        battle_battle_special = [
            ai_instr.RandomAttack(name_id["Battle"], name_id["Battle"], SPECIAL0),
            ai_instr.EndMainLoop(),
        ]

        piranha_script.replace(battle, battle_battle_special)

    def leader_scale_mod(self):
        leader_script = self.enemy_scripts.get_script("Leader")

        # make leader special counter attack one tier stronger
        nothing_nothing_special0 = ai_instr.RandomAttack(name_id["Nothing"], name_id["Nothing"], SPECIAL0)
        nothing_nothing_special1 = ai_instr.RandomAttack(name_id["Nothing"], name_id["Nothing"], SPECIAL1)

        leader_script.replace(nothing_nothing_special0, nothing_nothing_special1)

    def marshal_scale_mod(self):
        marshal_script = self.enemy_scripts.get_script("Marshal")

        # make Marshal special attack one tier stronger
        battle_special0_special0 = ai_instr.RandomAttack(name_id["Battle"], SPECIAL0, SPECIAL0)
        battle_special1_special1 = ai_instr.RandomAttack(name_id["Battle"], SPECIAL1, SPECIAL1)
        marshal_script.replace(battle_special0_special0, battle_special1_special1)

    def whelk_scale_mod(self):
        whelk_script = self.enemy_scripts.get_script("Whelk")

        # increase tier offset of shell counter
        shell_counter = []
        shell_counter_new = []
        if self.args.ability_scaling_element:
            shell_counter.append(ai_instr.Spell(BOLT0))
            shell_counter_new.append(ai_instr.Spell(BOLT1))
        elif self.args.ability_scaling_random:
            shell_counter.append(ai_instr.Spell(DAMAGE0))
            shell_counter_new.append(ai_instr.Spell(DAMAGE1))
        shell_counter.append(ai_instr.EndIf())
        shell_counter_new.append(ai_instr.EndIf())

        whelk_script.replace(shell_counter, shell_counter_new)

    def _scale_special(self, spell_id, enemy):
        if spell_id != name_id["Special"] or enemy.special_effect < 0x20 or enemy.special_effect > 0x2f:
            return spell_id # not a special attack or does not have a damage effect

        if enemy.special_effect >= 0x28:
            return SPECIAL2
        elif enemy.special_effect >= 0x24:
            return SPECIAL1
        return SPECIAL0

    def _scale_ability(self, ability_id, enemy):
        from data.spell_names import id_name
        name = id_name[ability_id]

        if name not in self.SPELL_CATEGORY:
            return self._scale_special(ability_id, enemy)

        if self.args.ability_scaling_element:
            return self.SPELL_CATEGORY[name]

        if self.args.ability_scaling_random:
            category = self.SPELL_CATEGORY[name]
            tier = get_custom_ability_tier(category)
            if category >= CURE0 and category <= CURE2:
                return CURE0 + tier
            return DAMAGE0 + tier

        return ability_id

    def _scale_spell_instruction(self, instruction, enemy):
        from data.spell_names import id_name
        instruction.spell_id = self._scale_ability(instruction.spell_id, enemy)

    def _scale_random_attack_instruction(self, instruction, enemy):
        from data.spell_names import id_name

        instruction.attack1 = self._scale_ability(instruction.attack1, enemy)
        instruction.attack2 = self._scale_ability(instruction.attack2, enemy)
        instruction.attack3 = self._scale_ability(instruction.attack3, enemy)

    def flameeater_reflect_mod(self):
        # after being damaged 6 times, starts reflecting spells off itself
        flameeater_script = self.enemy_scripts.get_script("FlameEater")

        if_reflect_target_self = [
            ai_instr.If(0x08, 0x36, 0x17),  # if reflect on self (also sets target self)
        ]
        if_reflect_target_default = [
            ai_instr.If(0x08, 0x36, 0x17),  # if reflect on self,
            ai_instr.SetTarget(0x47),       # set target default
        ]

        flameeater_script.replace(if_reflect_target_self, if_reflect_target_default)

    def stooges_reflect_mod(self):
        # stooges begin reflecting spells off self after being attacked by magic 3 times (except larry, bug?)
        curley_script = self.enemy_scripts.get_script("Curley")
        larry_script = self.enemy_scripts.get_script("Larry")
        moe_script = self.enemy_scripts.get_script("Moe")

        if_reflect_target_self = [
            ai_instr.If(0x08, 0x36, 0x17),  # if reflect on self (also sets target self)
            ai_instr.SetTarget(0x36),       # set target self (redundant?)
        ]
        if_reflect_target_default = [
            ai_instr.If(0x08, 0x36, 0x17),  # if reflect on self,
            ai_instr.SetTarget(0x47),       # set target default
        ]

        curley_script.replace(if_reflect_target_self, if_reflect_target_default)
        larry_script.replace(if_reflect_target_self, if_reflect_target_default)
        moe_script.replace(if_reflect_target_self, if_reflect_target_default)

    def wrexsoul_reflect_mod(self):
        # wrexsoul casts spells on soulsavers with reflect
        wrexsoul_script = self.enemy_scripts.get_script("Wrexsoul")

        target_reflect_enemies = [
            ai_instr.SetTarget(0x41),       # target enemies with reflect
        ]
        target_default = [
            ai_instr.SetTarget(0x47),       # target default
        ]

        wrexsoul_script.replace(target_reflect_enemies, target_default, count = 2)

    def gold_dragon_reflect_mod(self):
        # gold dragon casts spells on self with reflect if any party member has reflect
        gold_dragon_script = self.enemy_scripts.get_script("Gold Drgn")

        target_self = [
            ai_instr.SetTarget(0x36),       # target self
        ]
        target_default = [
            ai_instr.SetTarget(0x47),       # target default
        ]

        gold_dragon_script.replace(target_self, target_default, count = 2)

    def scale_abilities_mod(self):
        print_debug = False
        import data.bosses as bosses

        for index, script in enumerate(self.enemy_scripts.scripts):
            enemy = self.enemies.enemies[index]
            if not self.args.scale_final_battles and enemy.id in bosses.final_battle_enemy_name:
                continue
            if not self.args.scale_eight_dragons and enemy.id in bosses.dragon_enemy_name:
                continue

            for instruction in script.instructions:
                if type(instruction) is ai_instr.Spell:
                    if print_debug:
                        print("Spell: " + str(instruction))
                    self._scale_spell_instruction(instruction, enemy)
                elif type(instruction) is ai_instr.RandomAttack:
                    self._scale_random_attack_instruction(instruction, enemy)
                    if print_debug:
                        print("RandomAttack : " + str(instruction))
                else:
                    if print_debug:
                        print(instruction)
                        if enemy.name == debugName:
                            print(instruction.attack1)


        self.piranha_scale_mod()
        self.leader_scale_mod()
        self.whelk_scale_mod()
        self.marshal_scale_mod()

        self.flameeater_reflect_mod()
        self.stooges_reflect_mod()
        self.wrexsoul_reflect_mod()
        self.gold_dragon_reflect_mod()

        ### Experimental section
        if 0 == 1:
            ### BC - style script modification can go here, note the following mods and make sure
            ### they don't get messed up from WC assumptions
            modded_scripts = [366, 379, 243, 340, 264, 265, 285, 290, 281, 286, 328, 358, 291, 85,
                              367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 380, 382, 383,
                              334, 256, 278, 287, 288, 289, 336]
            script_ids = list(range(0, len(self.enemy_scripts.scripts)))
            updated_script_ids = list((i for i in script_ids if i not in modded_scripts))
            import random

            initial_script_ids = updated_script_ids.copy()
            initial_scripts = self.enemy_scripts.scripts.copy()
            #print(initial_script_ids)
            #print(len(initial_script_ids))
            #print(modded_scripts)
            #print(len(modded_scripts))
            #input("Z")
            temp_scripts = []
            #print(self.enemy_scripts.scripts[0])
            #input("Z")
            #for script_index in range(len(self.scripts)):
            def get_size(scripts):
                tlen = []
                for script in self.enemy_scripts.scripts:
                    tlen.append(len(script.data()))        
                print(tlen)
                print(str(sum(tlen)) + " " + str(len(tlen)))
                a = 0
                return a

            #b = get_size(self.enemy_scripts.scripts)
            #input("A")

            
            #for index, script in enumerate(self.enemy_scripts.scripts):
                #if index in initial_script_ids:
                    #self.enemy_scripts.scripts[index] = [0]

            #print(self.enemy_scripts.scripts[0])
            #b = get_size(self.enemy_scripts.scripts)
            #input("A")
            
            for index, script in enumerate(initial_scripts):
                #if index == 256:
                    #print(script)
                    #input("Z")
                if index in initial_script_ids:
                    new_id = random.choice(updated_script_ids)
                    updated_script_ids.remove(new_id)
                    #print(str(index) + " | " + str(new_id))
                    #print(self.enemy_scripts.scripts[new_id].data())
                    script = initial_scripts[new_id]
                    self.enemy_scripts.scripts[index] = script
                    #print(self.enemy_scripts.scripts[index].data())
                    #input("X")
                    #self.scripts[script_index] = script
                    print(str(index) + " | " + str(new_id))
            #print(updated_script_ids)
            #b = get_size(self.enemy_scripts.scripts)
            #input("A")
            
    ##        tlen = []
    ##        for script in self.enemy_scripts.scripts:
    ##            tlen.append(len(script.data()))        
    ##        print(tlen)
    ##        print(str(sum(tlen)) + " " + str(len(tlen)))
    ##        input("A")
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
            # 334 - leader
            # 256 - whelk
            # 278 - flameeater
            # 287, 288, 289 - stooges
            # 336 - gold drgn
