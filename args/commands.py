from constants.commands import COMMAND_OPTIONS, RANDOM_COMMAND, RANDOM_UNIQUE_COMMAND, NONE_COMMAND, RANDOM_EXCLUDE_COMMANDS, id_name, name_id

def name():
    return "Commands"

def parse(parser):
    commands = parser.add_argument_group("Commands")
    commands.add_argument("-com", "--commands", type = str, help = "Character commands")
    commands.add_argument("-scc", "--shuffle-commands", action = "store_true", help = "Shuffle selected/randomized commands")
    commands.add_argument("-rec1", "--random-exclude-command1", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec2", "--random-exclude-command2", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec3", "--random-exclude-command3", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec4", "--random-exclude-command4", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec5", "--random-exclude-command5", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec6", "--random-exclude-command6", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")

    ### Command mods
    commands.add_argument("-fightrand", "--fight-swap-chance", default = 0, type = int,
                          choices = range(101), metavar = "COUNT", 
                          help = "Chance of replacing Fight command with another command")  #that this affects Gau's first command regardless of whether it's Fight or not
    commands.add_argument("-magicrand", "--magic-swap-chance", default = 0, type = int,
                          choices = range(101), metavar = "COUNT", 
                          help = "Chance of replacing Magic command with another command")
    commands.add_argument("-itemrand", "--item-swap-chance", default = 0, type = int,
                          choices = range(101), metavar = "COUNT", 
                          help = "Chance of replacing Item  command with another command")
    commands.add_argument("-cmdsafety", "--random-cmd-safety-check", action = "store_true",
                        help = "Guarantee every character has Fight or Item and enforce Scan All (-scan) is on to ensure they can always cast a spell")
    commands.add_argument("-gauoff", "--gau_offense", action = "store_true",
                          help = "Guarantee Gau has a command which allows him to damage enemies without requiring items/GP")
    commands.add_argument("-fscom", "--force_start_commands", type = str, help = "Forced commands for starting party (applies to non-Gogo/Umaro random)")


def process(args):
    if not args.commands:
        args.blitz_command_possible = True
        return

    digits = 2 # number of digits each command id substring is
    args.character_commands = [int(args.commands[index : index + digits]) for index in range(0, len(args.commands), digits)]

    args.command_strings = []
    for index, command in enumerate(args.character_commands):
        if command == RANDOM_COMMAND:
            args.command_strings.append("Random")
        elif command == RANDOM_UNIQUE_COMMAND:
            args.command_strings.append("Random Unique")
        elif command == NONE_COMMAND:
            args.command_strings.append("None")
        else:
            args.command_strings.append(id_name[command])

    ### Mod for forcing starting commands
    if args.force_start_commands is not None:
        args.starting_slot_commands = [int(args.force_start_commands[index : index + digits]) for index in range(0, len(args.force_start_commands), digits)]
        args.force_start_command_strings = []
        for index, command in enumerate(args.starting_slot_commands):
            args.force_start_command_strings.append(id_name[command])


    args.random_exclude_commands = []
    if args.random_exclude_command1 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command1)
    if args.random_exclude_command2 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command2)
    if args.random_exclude_command3 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command3)
    if args.random_exclude_command4 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command4)
    if args.random_exclude_command5 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command5)
    if args.random_exclude_command6 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command6)

    random_exists = "Random" in args.command_strings or "Random Unique" in args.command_strings
    blitz_excluded = name_id["Blitz"] in args.random_exclude_commands
    args.blitz_command_possible = ("Blitz" in args.command_strings) or (random_exists and not blitz_excluded)

def flags(args):
    flags = ""

    if args.commands:
        flags += " -com " + args.commands

    if args.shuffle_commands:
        flags += " -scc"

    if args.force_start_commands:
        flags += " -fscom " + args.force_start_commands

    if args.random_exclude_command1 != NONE_COMMAND:
        flags += f" -rec1 {args.random_exclude_command1}"
    if args.random_exclude_command2 != NONE_COMMAND:
        flags += f" -rec2 {args.random_exclude_command2}"
    if args.random_exclude_command3 != NONE_COMMAND:
        flags += f" -rec3 {args.random_exclude_command3}"
    if args.random_exclude_command4 != NONE_COMMAND:
        flags += f" -rec4 {args.random_exclude_command4}"
    if args.random_exclude_command5 != NONE_COMMAND:
        flags += f" -rec5 {args.random_exclude_command5}"
    if args.random_exclude_command6 != NONE_COMMAND:
        flags += f" -rec6 {args.random_exclude_command6}"

    ### command mods
    if args.fight_swap_chance > 0:
        flags += f" -fightrand {args.fight_swap_chance}"
    if args.magic_swap_chance > 0:
        flags += f" -magicrand {args.magic_swap_chance}"
    if args.item_swap_chance > 0:
        flags += f" -itemrand {args.item_swap_chance}"
    if args.random_cmd_safety_check:
        flags += " -cmdsafety"
    if args.gau_offense:
        flags += " -gauoff"

    return flags

def options(args):
    result = []
    if args.commands is not None:
        for index, command_string in enumerate(args.command_strings):
            result.append((COMMAND_OPTIONS[index], command_string))
    else:
        for option in COMMAND_OPTIONS:
            result.append((option, option))

    result.append(("", ""))
    result.append(("Shuffle Commands", args.shuffle_commands))

    ### Mod for force start commands
    if args.force_start_commands is not None:
        for index, command_string in enumerate(args.force_start_command_strings):
            result.append(("Forced cmd " + str(index+1), command_string))        


    add_exclude_command = lambda command : result.append(("Random Exclude", "None" if command == NONE_COMMAND else id_name[command]))

    add_exclude_command(args.random_exclude_command1)
    add_exclude_command(args.random_exclude_command2)
    add_exclude_command(args.random_exclude_command3)
    add_exclude_command(args.random_exclude_command4)
    add_exclude_command(args.random_exclude_command5)
    add_exclude_command(args.random_exclude_command6)

    ### command mods
    if args.fight_swap_chance > 0:
        result.append(("Fight Swap %", args.fight_swap_chance))
    if  args.magic_swap_chance > 0:
        result.append(("Magic Swap %", args.magic_swap_chance))
    if args.item_swap_chance > 0:
        result.append(("Item Swap %", args.item_swap_chance))
    if args.random_cmd_safety_check > 0:
        result.append(("Fanatic's Cmd Safe", args.random_cmd_safety_check))
    if args.gau_offense > 0:
        result.append(("Gau offense", args.gau_offense))
    
    return result

def menu(args):
    return (name(), options(args))

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
