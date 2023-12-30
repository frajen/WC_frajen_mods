def name():
    return "Characters"

def parse(parser):
    characters = parser.add_argument_group("Characters")

    characters.add_argument("-sal", "--start-average-level", action = "store_true",
                            help = "Recruited characters start at the average character level")
    characters.add_argument("-stl", "--start-level", default = 3, type = int, choices = range(3, 100), metavar = "COUNT",
                            help = "Start game at level %(metavar)s.")
    characters.add_argument("-sn", "--start-naked", action = "store_true",
                            help = "Recruited characters start with no equipment")
    characters.add_argument("-eu", "--equipable-umaro", action = "store_true",
                            help = "Umaro can access equipment menu")
    characters.add_argument("-csrp", "--character-stat-random-percent", default = [100, 100], type = int,
                            nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                            help = "Each character stat set to random percent of original within given range ")

    ### initial stat swap
    characters.add_argument("-swapstats", "--character-swap-stats", action = "store_true",
                            help = "Character initial stats swapped")
    ### flag to set character starting level (will not override level averaging)
    characters.add_argument("-cstartlvl", "--force-character-starting-levels",  type = str,
                            help = "Force character starting levels")
    ### flag to set character starting level (will not override level averaging)
    characters.add_argument("-cexcludeavg", "--exclude-character-from-level-averaging",  type = str,
                            help = "Exclude characters from level averaging calculations")
    ### flag to equip characters with ultimate items
    characters.add_argument("-startulti", "--start_ultimates", action = "store_true",
                            help = "Start with ultimate items")

def process(args):
    args._process_min_max("character_stat_random_percent")

    # check for valid starting levels
    args.start_levels = []
    if args.force_character_starting_levels is not None:
        args.start_levels = args.force_character_starting_levels.split('.')
        if len(args.start_levels) != Characters.CHARACTER_COUNT:
            raise ValueError(f"Invalid number of level arguments ({len(args.start_levels)} should be {Characters.CHARACTER_COUNT})")
        for i in range(len(args.start_levels)):
            if int(args.start_levels[i]) < 1:
                args.start_levels[i] = "1"
            elif int(args.start_levels[i]) > 99:
                args.start_levels[i] = "99"
        # end of check for valid levels
    else:
        args.start_levels = ["3" for i in range(14)]

    # validate character avg level exclusion list
    args.excluded_characters_from_avg = []
    if args.exclude_character_from_level_averaging is not None:
        args.excluded_characters_from_avg = args.exclude_character_from_level_averaging.split('.')
        if len(args.excluded_characters_from_avg) != Characters.CHARACTER_COUNT:
            raise ValueError(f"Invalid number of level arguments ({len(args.excluded_characters_from_avg)} should be {Characters.CHARACTER_COUNT})")
        for i in range(len(args.excluded_characters_from_avg)):
            if args.excluded_characters_from_avg[i] != "0" and args.excluded_characters_from_avg[i] != "1":
                raise ValueError(f"Exclude from level averaging input should only be 0 or 1")
    else:
        args.excluded_characters_from_avg = ["0" for i in range(14)]


def flags(args):
    flags = ""

    if args.start_average_level:
        flags += " -sal"
    if args.start_level != 3:
        flags += f" -stl {args.start_level}"
    if args.start_naked:
        flags += " -sn"
    if args.equipable_umaro:
        flags += " -eu"
    if args.character_stat_random_percent_min != 100 or args.character_stat_random_percent_max != 100:
        flags += f" -csrp {args.character_stat_random_percent_min} {args.character_stat_random_percent_max}"

    ### character mods
    if args.character_swap_stats:
        flags += " -swapstats"
    if args.force_character_starting_levels:
        flags += " -cstartlvl " + args.force_character_starting_levels
    if args.exclude_character_from_level_averaging:
        flags += " -cexcludeavg " + args.exclude_character_from_level_averaging
    if args.start_ultimates:
        flags += " -startulti"

    return flags

def options(args):
    character_stats = f"{args.character_stat_random_percent_min}-{args.character_stat_random_percent_max}%"

    force_flag = False
    exclude_flag = False
    if args.force_character_starting_levels is not None:
        force_flag = True
    if args.exclude_character_from_level_averaging is not None:
        exclude_flag = True

    return [
        ("Start Average Level", args.start_average_level),
        ("Start Level", args.start_level),
        ("Start Naked", args.start_naked),
        ("Equipable Umaro", args.equipable_umaro),
        ("Character Stats", character_stats),
        ("Swap initial stats", args.character_swap_stats),
        ("Start w/ultimates", args.start_ultimates),
        ("Force Start Lvls", force_flag),
        ("Exclude from Avg Calc", exclude_flag),
    ]

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        if key == "Character Stats":
            entries[index] = ("Stats", entry[1])
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
