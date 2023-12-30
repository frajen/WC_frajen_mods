from multiprocessing.sharedctypes import Value
from constants.commands import *
import random
import args

class Commands:
    def __init__(self, characters):
        self.characters = characters

    def mod_commands(self):
        command_set = set(name_id[name] for name in RANDOM_POSSIBLE_COMMANDS)
        command_list = list(command_set)

        allowed_commands = command_set | set([name_id["Fight"], RANDOM_COMMAND, RANDOM_UNIQUE_COMMAND, NONE_COMMAND])

        # if morph was explicitly selected remove from available command list
        morph_id = name_id["Morph"]
        for command in args.character_commands:
            if command == morph_id:
                command_list.remove(morph_id)

        for exclude_command in args.random_exclude_commands:
            try:
                command_set.discard(exclude_command)
                command_list.remove(exclude_command)
            except ValueError:
                pass

        from data.characters import Characters
        # Give the Moogles for Moogle Defense randomized commands
        # Copy the list minus any exclusions
        possible_moogle_commands = command_list.copy()
        # randomize commands for Moogles during Moogle Defense from the non-excluded set
        # Remove Morph to ensure only 1 character gets Morph
        # Remove Rage to avoid any issues with Randomized Atma weapon
        # Remove X-Magic as they won't have any Magic
        # Remove Blitz, SwdTech, Dance, and Lore because they won't have abilities within unless a party member does
        moogle_exclusions = [morph_id, name_id["Rage"], name_id["X Magic"], name_id["Blitz"], name_id["SwdTech"], name_id["Lore"], name_id["Dance"]]
        for exclude in moogle_exclusions:
            try:
                possible_moogle_commands.remove(exclude)
            except ValueError:
                pass
        if len(possible_moogle_commands) > 0:
            for index in range(Characters.FIRST_MOOGLE, Characters.LAST_MOOGLE + 1):
                self.characters[index].commands[1] = random.choice(possible_moogle_commands)

        # if suplex a train condition exists, guarantee blitz
        import objectives
        blitz_id = name_id["Blitz"]
        if objectives.suplex_train_condition_exists and blitz_id not in args.character_commands:
            # try to replace a random "Random" or "Random Unique" command with Blitz (even if blitz in excluded commands)
            possible_indices = []
            for index, command in enumerate(args.character_commands):
                if command == RANDOM_COMMAND or command == RANDOM_UNIQUE_COMMAND:
                    possible_indices.append(index)

            if not possible_indices:
                # suplex a train explicitly picked and all commands explicitly picked (but none are blitz)
                # force a random command to be blitz instead
                possible_indices = list(range(len(args.character_commands)))

            random_index = random.choice(possible_indices)
            args.character_commands[random_index] = blitz_id
            command_set.discard(blitz_id)

        for index, command in enumerate(args.character_commands):
            if command not in allowed_commands and (index != 0 or command != name_id["Morph"]) and (index != 12 or command != name_id["Leap"]):
                raise ValueError(f"Invalid character command {command}")
            elif command == RANDOM_COMMAND:
                args.character_commands[index] = random.choice(command_list)
                if args.character_commands[index] == morph_id:
                    command_list.remove(morph_id) # only one character gets morph
            elif command == NONE_COMMAND:
                args.character_commands[index] = name_id["None"]

            command_set.discard(args.character_commands[index])

        # added for guaranteeing Gau has an offensive command
        if args.gau_offense:
            first_gau_unique = False
            second_gau_unique = False
        for index, command in enumerate(args.character_commands):
            if command == RANDOM_UNIQUE_COMMAND:
                if args.gau_offense:
                    if index == 11:
                        first_gau_unique = True
                    if index == 12:
                        second_gau_unique = True                    
                args.character_commands[index] = random.choice(tuple(command_set))
                command_set.discard(args.character_commands[index])

        # apply the commands to the characters
        for index in range(len(args.character_commands[ : -2])):
            self.characters[index].commands[1] = args.character_commands[index]
        self.characters[Characters.GAU].commands[0] = args.character_commands[-2] # rage
        self.characters[Characters.GAU].commands[1] = args.character_commands[-1] # leap

        ### Mod for ensuring Gau has an offensive command
        if args.gau_offense:
            print_debug = False
            # build list of offensive commands that don't require items to work:
            # 0 #Fight, 6 #Capture, 7 #SwdTech, 10,  #Blitz, 13,  #Sketch, 14,  #Control, 15,  #Slot, 16,  #Rage, 18,  #Mimic, 22,  #Jump, 27,  #Shock 29,  #MagiTek
            allowed = [0, 6, 7, 10, 13, 14, 15, 16, 18, 22, 27, 29]
            no_offense = True
            for command in self.characters[Characters.GAU].commands:
                if command in allowed:
                    no_offense = False
            # after looping through commands, if no_offense is True, randomly replace
            if no_offense:
                if print_debug:
                    print("Gau originally has: " + str(self.characters[Characters.GAU].commands[0])
                          + ", " + str(self.characters[Characters.GAU].commands[1]))
                # get any offensive commands from remaining available commands
                for command in command_set:
                    if command in allowed:
                        self.characters[Characters.GAU].commands[0] = command # set for Gau
                        no_offense = False
                        if print_debug:
                            print("Gau given offensive command")
                        break
            # if no_offense is still True, no offensive commands left in command_set
            if no_offense:
                # if the player asked for both of Gau's commands to be unique
                # give up and set Gau's first command to Fight            
                if first_gau_unique and second_gau_unique:
                    self.characters[Characters.GAU].commands[0] = 0 # rage
                    if print_debug:
                        print("Gau given Fight")
                else:
                    #otherwise just pick something from the offensive command list
                    if first_gau_unique:
                        self.characters[Characters.GAU].commands[1] = random.choice(allowed)
                    else:
                        self.characters[Characters.GAU].commands[0] = random.choice(allowed)
                    if print_debug:
                        print("Gau given offensive command")


    def shuffle_commands(self):
        from data.characters import Characters

        commands = []
        for index in range(len(COMMAND_OPTIONS) - 1):
            commands.append(self.characters[index].commands[1])
        commands.append(self.characters[Characters.GAU].commands[0]) # rage

        random.shuffle(commands)

        for index in range(len(COMMAND_OPTIONS) - 1):
            self.characters[index].commands[1] = commands[index]
        self.characters[Characters.GAU].commands[0] = commands[-1] # rage

    ### Mod for Fanatic's Tower command safety: guarantee Fight or Item
    ### Also helps with Imp status, although Imp has a wider range of
    ### allowed commands: Fight, Item, Jump, Magic, X Magic, Mimic, Health, Shock
    def fanatics_safety_mod(self):
        print_debug = False
        if not args.scan_all:
            args.scan_all = True
            
        for character in self.characters:
            if character.id <= 11: #skip Umaro/Gogo
                if print_debug:
                    print(character.name)
                    print(id_name[character.commands[0]] + ", " + id_name[character.commands[1]] + ", " +
                          id_name[character.commands[2]] + ", " + id_name[character.commands[3]])
                ft_ok = False
                #### guarantee Fight, Item, or Mimic
                # loop thru commands
                for command in character.commands:
                    if command == 0 or command == 1 or command == 18:
                        ft_ok = True
                # end of loop thru 1 character's commands
                if ft_ok:
                    pass
                    # no need to do anything if they have Fight/Item/Mimic already
                else:
                    ft_safe_cmd = random.randint(1, 10)
                    if ft_safe_cmd < 3:
                        character.commands[0] = 18 # 20% chance Mimic
                    elif ft_safe_cmd < 7:
                        character.commands[0] = 0 # 40% chance Fight
                    else:
                        character.commands[3] = 1  # 40% chance Item
                # end of check if character had Fight/Item/Mimic
            # end of character ID check
                if print_debug:
                    print(id_name[character.commands[0]] + ", " + id_name[character.commands[1]] + ", " +
                          id_name[character.commands[2]] + ", " + id_name[character.commands[3]])
            
        # end of loop thru characters
    ### End of: Mod for Fanatic's Tower command safety

    ### Mod for Fight/Magic/Item command randomization
    ### 3 swap chances:
    ### chance to remove Fight - fight_swap_chance
    ### chance to remove Magic - magic_swap_chance
    ### chance to remove Item - item_swap_chance
    ### Note that if a character cannot use Fight, Magic, or Item and becomes and Imp, they may 
    ### soft-lock the game due to being unable to do anything. This may hard-lock the game
    ### if Muddled/Zombie
    def vanilla_command_mod(self, fight_swap_chance=0, magic_swap_chance=0, item_swap_chance=0, minimize_dupes=True):
        print_debug = False
        command_set = set(name_id[name] for name in RANDOM_POSSIBLE_COMMANDS)
        command_list = list(command_set)

        allowed_commands = command_set | set([name_id["Fight"], RANDOM_COMMAND, RANDOM_UNIQUE_COMMAND, NONE_COMMAND])

        morph_id = name_id["Morph"]

        # if any commands have been dictated to be excluded in args, add them to the command list:
        if args.commands:
            for exclude_command in args.random_exclude_commands:
                try:
                    command_set.discard(exclude_command)
                    command_list.remove(exclude_command)
                except ValueError:
                    pass

        # attempt to minimize the number of duplicates
        # by tracking which commands have been picked in commands_remaining
        # commands_remaining initially holds 
        #minimize_dupes = True
        commands_remaining = []
        if minimize_dupes:
            commands_remaining = command_list.copy()

        # apply the commands to the characters
        from data.characters import Characters

        if args.commands:
            command_range = range(len(args.character_commands[ : -2]))
            # range(len(args.character_commands[ : -2]))   always seems to turn into range(0,11) so not sure this is necessary
            if command_range != range(0,11):
                print(command_range)
                input("command_range not equal to range(0,11)")
        else:
            command_range = range(0, 11)

        ### Pick from a list of commands
        def generate_random_command(minimize_dupes, commands_remaining, command_list):
            if minimize_dupes:
                return random.choice(commands_remaining)
            else:
                return random.choice(command_list)

        ### run this after every command assignment to check for:
        ### 1. Only 1 character gets Morph - not required but same philosophy as WC
        ### 2. Ensure there are available commands to be picked from a list
        def after_assignment(command_list, commands_remaining):
            if random_command == morph_id: 
                command_list.remove(morph_id) # only one character gets morph
            if minimize_dupes:
                commands_remaining.remove(random_command) # remove from commands_remaining
                if commands_remaining == []:
                    commands_remaining = command_list.copy() #re-initialize command list if there are none left to pick from

        # loop through 12 characters' commands
        for index in command_range:
            fight_swapped = False
            # chance to swap Fight for something
            if random.randint(1, 100) <= fight_swap_chance:
                #print("fight swap")
                fight_swapped = True
                random_command = generate_random_command(minimize_dupes, commands_remaining, command_list)

                #make sure the command isn't a duplicate of the WC rolled command (which is always in slot commands[1])
                while (self.characters[index].commands[1] == random_command):
                    random_command = generate_random_command(minimize_dupes, commands_remaining, command_list)
                    # if there's only 1 command left and it matches one of the other existing ones,
                    # reset the commands remaining
                    if len(commands_remaining) == 1:
                        if random_command == self.characters[index].commands[0]:
                            commands_remaining = command_list.copy()

                self.characters[index].commands[0] = random_command

                after_assignment(command_list, commands_remaining)

            # double check you have commands leftover
            if commands_remaining == []:
                #print("No more commands left to randomize, re-initialize")
                commands_remaining = command_list.copy()
                                        
            magic_swapped = False
            # chance to swap Magic for something
            if random.randint(1, 100) <= magic_swap_chance:
                #print("magic swap")
                magic_swapped = True
                random_command = generate_random_command(minimize_dupes, commands_remaining, command_list)

                #make sure the command isn't a duplicate of previously rolled commands
                while (self.characters[index].commands[0] == random_command or
                       self.characters[index].commands[1] == random_command):
                    random_command = generate_random_command(minimize_dupes, commands_remaining, command_list)
                    # if there's only 1 command left and it matches one of the other existing ones,
                    # reset the commands remaining
                    if len(commands_remaining) == 1:
                        if random_command in [self.characters[index].commands[0], self.characters[index].commands[1]]:
                            commands_remaining = command_list.copy()

                self.characters[index].commands[2] = random_command

                after_assignment(command_list, commands_remaining)

            # double check you have commands leftover
            if commands_remaining == []:
                #print("No more commands left to randomize, re-initialize")
                commands_remaining = command_list.copy()

            item_swapped = False
            # chance to swap Item for something
            if random.randint(1, 100) <= item_swap_chance:
                #print("item swap")
                item_swapped = True
                random_command = generate_random_command(minimize_dupes, commands_remaining, command_list)

                #make sure the command isn't a duplicate of the WC rolled command
                while (self.characters[index].commands[0] == random_command or
                       self.characters[index].commands[1] == random_command or
                       self.characters[index].commands[2] == random_command):
                    random_command = generate_random_command(minimize_dupes, commands_remaining, command_list)
                    # if there's only 1 command left and it matches one of the other existing ones,
                    # reset the commands remaining
                    if len(commands_remaining) == 1:
                        if random_command in [self.characters[index].commands[0], self.characters[index].commands[1],
                                              self.characters[index].commands[2]]:
                            commands_remaining = command_list.copy()

                self.characters[index].commands[3] = random_command

                after_assignment(command_list, commands_remaining)

            # double check you have commands leftover
            if commands_remaining == []:
                if print_debug:
                    print("No more commands left to randomize, re-initialize")
                commands_remaining = command_list.copy()

        #end loop through characters
    ### End of: Mod for Fight/Magic/Item command randomization

    ### Mod to force commands on characters
    def force_commands(self):
#    DEFAULT_NAME = ["TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN", "CELES", "STRAGO", "RELM", "SETZER", "MOG", "GAU", "GOGO", "UMARO"]
#     0: "Fight", 1: "Item", 2: "Magic", 3: "Morph", 4: "Revert", 5: "Steal", 6: "Capture", 7: "SwdTech", 8: "Throw", 9: "Tools",
#10  : "Blitz", 11  : "Runic", 12  : "Lore", 13  : "Sketch", 14  : "Control", 15  : "Slot", 16  : "Rage", 17  : "Leap", 18  : "Mimic", 19  : "Dance",
#20  : "Row", 21  : "Def", 22  : "Jump", 23  : "X Magic", 24  : "GP Rain", 25  : "Summon", 26  : "Health", 27  : "Shock", 28  : "Possess", 29  : "MagiTek",
#30  : "Empty?", # broken? selecting with cursor crashes game, 31  : "Empty",  # cursor can hover over empty but not select, 255 : "None",

## WC discord wk 2 seed
##        self.characters[4].commands[1] = 10
##        self.characters[4].commands[2] = 9
##        self.characters[6].commands[1] = 23
##        self.characters[6].commands[2] = 2
##        self.characters[6].commands[3] = 11
##        self.characters[9].commands[1] = 15
##        self.characters[9].commands[2] = 5

## WC discord wk 3 seed
        #Gau - Rage/Dance/Magic/Item

        #self.characters[11].commands[0] = 3
        #self.characters[11].commands[1] = 12
        
        #self.characters[11].commands[2] = 2
        #self.characters[11].commands[3] = 1
        #Cyan - Throw/Steal/GP Rain/Item
        #self.characters[2].commands[0] = 3
        #self.characters[2].commands[1] = 8
        #self.characters[2].commands[2] = 24
        #self.characters[3].commands[1] = 16
        
        #self.characters[2].commands[3] = 1
    
        #Mog - Dance/Control/Magic/Item
        #self.characters[0].commands[0] = 0
        #self.characters[0].commands[1] = 14
        #self.characters[0].commands[2] = 19
        #self.characters[0].commands[3] = 1
        pass
    ### End of: Mod to force commands on characters


    def mod(self):
        import data.characters_asm as characters_asm
        from data.characters import Characters

        if args.commands:
            self.mod_commands()
        if args.shuffle_commands:
            self.shuffle_commands()

        ### Mod to randomize Fight/Magic/Item
        if args.fight_swap_chance > 0 or args.magic_swap_chance > 0 or args.item_swap_chance > 0:
            self.vanilla_command_mod(args.fight_swap_chance, args.magic_swap_chance,
                                       args.item_swap_chance, minimize_dupes=True)
            # only need to check this if Fight/Magic/Item randomization is active
            if args.random_cmd_safety_check:
                self.fanatics_safety_mod()

        self.force_commands() #general command forcing
        ### Mod to randomize Fight/Magic/Item

        if args.commands or args.shuffle_commands:
            characters_asm.update_morph_character(self.characters[ : Characters.CHARACTER_COUNT])

    def log(self):
        from log import section, format_option
        from data.characters import Characters

##        lcolumn = []
##        for index, option in enumerate(COMMAND_OPTIONS[ : -2]):
##            lcolumn.append(format_option(option, id_name[self.characters[index].commands[1]]))
##        lcolumn.append(format_option(COMMAND_OPTIONS[-2], id_name[self.characters[Characters.GAU].commands[0]]))
##        lcolumn.append(format_option(COMMAND_OPTIONS[-1], id_name[self.characters[Characters.GAU].commands[1]]))

        # update for Fight/Magic/Item command randomization
        vanilla_command_show = False
        lcolumn = []
        if args.fight_swap_chance > 0 or args.magic_swap_chance > 0 or args.item_swap_chance > 0:
            if args.spoiler_log:
                vanilla_command_show = True
                
        if vanilla_command_show:
            for index, option in enumerate(COMMAND_OPTIONS[ : -1]):
                lcolumn.append(self.characters[index].name + ": " + id_name[self.characters[index].commands[0]] + ", " +
                    id_name[self.characters[index].commands[1]]  + ", " + id_name[self.characters[index].commands[2]]  + ", " +
                    id_name[self.characters[index].commands[3]])
        else:
            for index, option in enumerate(COMMAND_OPTIONS[ : -2]):
                lcolumn.append(format_option(option, id_name[self.characters[index].commands[1]]))
            lcolumn.append(format_option(COMMAND_OPTIONS[-2], id_name[self.characters[Characters.GAU].commands[0]]))
            lcolumn.append(format_option(COMMAND_OPTIONS[-1], id_name[self.characters[Characters.GAU].commands[1]]))
        
        section("Commands", lcolumn, [])

    ### Mod to guarantee commands for random starting characters
    ### by default, this will do nothing if Gogo/Umaro is picked
    ### assume these guarantees override all other command options
    ### this is the simplest way to approach this, could be done in other ways
    def mod_starting_slot_commands(self, pathingdict):
        # get the starting characters
        starting_chars = [char for char, event in pathingdict.items() if event == "Start"]

        # get the desired commands
        forced_commands = args.starting_slot_commands
        #print(forced_commands)
        #print(starting_chars)
        from data.characters import Characters
        #print(Characters.DEFAULT_NAME)

        # this applies starting slot commands to characters
        # in the order which they were listed
        # for example, characters in the first slot (e.g. -sc1 terra) will
        # always have forced commands applied to them first
        # could use args.start_chars to determine which specific slots, if any,
        # were randomly picked, and apply these forced commands onto the random ones
        for character in starting_chars:
            # get index of starting character
            char_id = Characters.DEFAULT_NAME.index(character)
            if char_id != 12 and char_id != 13: #skip Gogo/Umaro
                self.characters[char_id].commands[1] = forced_commands.pop(0)
                # exit if there aren't any more commands to force
                if len(forced_commands) == 0:
                    break


    ### mod to tier character commands based on depth
    def mod_tiered_commands(self, character_depth):
        
        ### get max depths
        max_depth = 0
        sum_depth = 0
        avg_depth = 0
        for x, depth in character_depth.items():
            sum_depth += depth
            if depth > max_depth:
                max_depth = depth
        avg_depth = sum_depth / 14
        #print(character_depth)
        #print("Max depth: " + str(max_depth))
        # Depth levels
        import math
        highest_depth = math.ceil(max_depth * 0.9)
        high_depth = (max_depth + avg_depth) / 2
        if high_depth > highest_depth:
            high_depth = max_depth * 0.6
        #print("Highest: " + str(highest_depth))
        #print("High: " + str(high_depth))
        #print("Avg depth: " + str(avg_depth))

        command_rank = {
            0 : 5,  #Fight
            1 : 5,  #Item
            2 : 4,  #Magic
            3 : 3,  #Morph
            4 : 0,  #Revert
            5 : 1,  #Steal
            6 : 1,  #Capture
            7 : 3,  #SwdTech
            8 : 3,  #Throw
            9 : 3,  #Tools
            10: 3,  #Blitz
            11: 2,  #Runic
            12: 2,  #Lore
            13: 1,  #Sketch
            14: 1,  #Control
            15: 2,  #Slot
            16: 2,  #Rage
            17: 0,  #Leap
            18: 3,  #Mimic
            19: 2,  #Dance
            20: 0,  #Row
            21: 0,  #Def
            22: 3,  #Jump
            23: 4,  #X Magic
            24: 2,  #GP Rain
            25: 0,  #Summon
            26: 2,  #Health
            27: 4,  #Shock
            28: 5,  #Possess
            29: 5,  #MagiTek
            30: 0,  #Empty
            31: 0,  #Empty
            255: 0, #None
        }

        ### re-randomize commands based on depth
        command_list = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                        15, 16, 18, 19, 22, 23, 24, 26, 27, 28, 29]
        maincommands = [0, 1, 2]
        ### apply commands to the characters
        for character in self.characters:
            if character.id <= 11:
                print(character.name)
                print(id_name[character.commands[0]] + ", " + id_name[character.commands[1]] + ", " +
                      id_name[character.commands[2]] + ", " + id_name[character.commands[3]])
                ### handle the highest characters
                if character_depth[character.name] >= highest_depth:
                    for x in range(4):
                        tempcommand = character.commands[x]
                        # commands must be rank 3 or higher
                        if command_rank[tempcommand] < 3:
                            swapped = True
                            while (swapped):
                                tempcommand = random.choice(command_list)
                                if command_rank[tempcommand] < 3:
                                    swapped = True
                                else:
                                    swapped = False
                                if tempcommand in character.commands:  #prevent duplicate commands
                                    swapped = True
                            character.commands[x] = tempcommand
                ### handle high depth
                elif character_depth[character.name] >= high_depth:
                    for x in range(4):
                        tempcommand = character.commands[x]
                        swap = 0
                        # commands must be rank 3 or 4. Allow Fight, Magic, Item
                        if ((command_rank[tempcommand] < 3) or
                            ((command_rank[tempcommand] == 5) and
                            (tempcommand not in maincommands))):
                            swap = 1
                        if swap == 1:
                            swapped = True
                            while (swapped):
                                tempcommand = random.choice(command_list)
                                if command_rank[tempcommand] < 3:
                                    swapped = True
                                elif ((command_rank[tempcommand] == 5) and
                                (tempcommand not in maincommands)):
                                    swapped = True
                                else:
                                    swapped = False
                                if tempcommand in character.commands:  #prevent duplicate commands
                                    swapped = True
                            character.commands[x] = tempcommand
                ### handle avg depth
                elif character_depth[character.name] >= avg_depth:
                    for x in range(4):
                        tempcommand = character.commands[x]
                        swap = 0
                        # commands must be rank 2, 3 or 4. Allow Fight, Magic, Item
                        if ((command_rank[tempcommand] < 2) or
                            ((command_rank[tempcommand] == 5) and
                            (tempcommand not in maincommands))):
                            swap = 1
                        if swap == 1:
                            swapped = True
                            while (swapped):
                                tempcommand = random.choice(command_list)
                                if command_rank[tempcommand] < 2:
                                    swapped = True
                                elif ((command_rank[tempcommand] == 5) and
                                (tempcommand not in maincommands)):
                                    swapped = True
                                else:
                                    swapped = False
                                if tempcommand in character.commands:  #prevent duplicate commands
                                    swapped = True
                            character.commands[x] = tempcommand
                ### handles starting party and other low depth characters
                else:
                    for x in range(4):
                        tempcommand = character.commands[x]
                        swap = 0
                        # commands must be rank 1, 2, or 3. Allow Fight 2/5, Item 1/2, Magic 1/3
                        if command_rank[tempcommand] < 1:
                            swap = 1
                        if (command_rank[tempcommand] > 3):
                            swap = 1
                            if ((tempcommand == 0) and
                                (random.randint(1,100) <= 40)):
                                    swap = 0
                            if ((tempcommand == 1) and
                                (random.randint(1,100) <= 50)):
                                    swap = 0
                            if ((tempcommand == 2) and
                                (random.randint(1,100) <= 33)):
                                    swap = 0
                        if swap == 1:
                            swapped = True
                            while (swapped):
                                tempcommand = random.choice(command_list)
                                if command_rank[tempcommand] < 1:
                                    swapped = True
                                elif command_rank[tempcommand] > 3:
                                    if ((tempcommand == 0 and random.randint(1, 100) <= 33) or
                                   (tempcommand == 1 and random.randint(1, 100) <= 20) or
                                   (tempcommand == 2 and random.randint(1, 100) <= 50)):
                                        swapped = False
                                    else:
                                        swapped = True
                                else:
                                    swapped = False
                                if tempcommand in character.commands:  #prevent duplicate commands
                                    swapped = True
                            character.commands[x] = tempcommand
                            
                ### end of block to handle character depth
                ### see new results
                print(id_name[character.commands[0]] + ", " + id_name[character.commands[1]] + ", " +
                    id_name[character.commands[2]] + ", " + id_name[character.commands[3]])
                #input("Z")
            ### end of character.id <= 11 loop
        ### go to next character

        ### guarantee every character has Fight or Item
        ### guarantee characters that naturally learn Magic have Magic or X Magic
        for character in self.characters:
            if character.id <= 11:
                print(character.name)
                print(id_name[character.commands[0]] + ", " + id_name[character.commands[1]] + ", " +
                      id_name[character.commands[2]] + ", " + id_name[character.commands[3]])
                if ((0 not in character.commands) and (1 not in character.commands)):
                    if random.randint(1, 2) == 1:
                        character.commands[3] = 1  #50% chance set the last command to Item
                    else:
                        character.commands[0] = 0

                # natural magic section
                #if character.natural_magic_user == 1:
                    #input("X")
                #print(character.natural_magic_user)
                if ((character.natural_magic_user == 1) and
                    (2 not in character.commands) and (23 not in character.commands)):
                    if random.randint(1, 10) == 1:
                        character.commands[2] = 23  #10% chance to set the command to X Magic
                    else:
                        character.commands[2] = 2
                        
                print(id_name[character.commands[0]] + ", " + id_name[character.commands[1]] + ", " +
                      id_name[character.commands[2]] + ", " + id_name[character.commands[3]])
            ### end of character.id <= 11 loop
        ### go to next character

        ### guarantee someone in starting party can use Item
        start_chars_no_item = []
        for character in self.characters:
            if character.id <= 11:
                if character_depth[character.name] == 1:
                    if character.commands[3] != 1:
                        start_chars_no_item.append(character.id)

        if len(start_chars_no_item) > 0:
            itemchar = random.choice(start_chars_no_item)
            for character in self.characters:
                if character.id == itemchar:
                    character.commands[3] = 1
        ### end of guarantee someone in starting party can use Item
