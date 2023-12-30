def name():
    return "Chests"

def parse(parser):
    chests = parser.add_argument_group("Chests")

    chests_contents = chests.add_mutually_exclusive_group()
    chests_contents.add_argument("-ccsr", "--chest-contents-shuffle-random", default = None, type = int,
                                 metavar = "PERCENT", choices = range(101),
                                 help = "Chest contents shuffled and given percent randomized")
    chests_contents.add_argument("-ccrt", "--chest-contents-random-tiered", action = "store_true",
                                 help = "Chest contents randomized by tier")
    chests_contents.add_argument("-ccrs", "--chest-contents-random-scaled", action = "store_true",
                                 help = "Chest contents randomized by tier. Probability of higher tiers begins low and increases as more chests are opened")
    chests_contents.add_argument("-cce", "--chest-contents-empty", action = "store_true",
                                 help = "Chest contents empty")

    chests.add_argument("-cms", "--chest-monsters-shuffle", action = "store_true",
                        help = "Monsters-in-a-box shuffled but locations unchanged")

    ### chest mods
    chests.add_argument("-ecs", "--empty-chest-shuffle", default = None, type = int,
                                 metavar = "PERCENT", choices = range(101),
                                 help = "Percentage of chests empty")
    chests.add_argument("-gcs", "--gold-chest-shuffle", default = None, type = int,
                                 metavar = "PERCENT", choices = range(101),
                                 help = "Percentage of chests with GP")

    chests.add_argument("-nogoodchests", "--no-good-chests", action = "store_true",
                        help = "Exclude more high tier items from chests")
    chests.add_argument("-rxi", "--replace-with-items", action = "store_true",
                        help = "Replace excluded items with items and not empties")

def process(args):
    if args.chest_contents_shuffle_random is not None:
        args.chest_contents_shuffle_random_percent = args.chest_contents_shuffle_random
        args.chest_contents_shuffle_random = True
    ### added % empty chests
    if args.empty_chest_shuffle is not None:
        args.empty_chest_shuffle_percent = args.empty_chest_shuffle
        args.empty_chest_shuffle = True
    ### added % GP chests
    if args.gold_chest_shuffle is not None:
        args.gold_chest_shuffle_percent = args.gold_chest_shuffle
        args.gold_chest_shuffle = True
    if (args.empty_chest_shuffle is not None) and (args.gold_chest_shuffle is not None):
        total = args.empty_chest_shuffle_percent + args.gold_chest_shuffle_percent
        if total > 100:
            raise ValueError(f"Sum of random % empty and % GP chests is over 100% - value: {total}")

def flags(args):
    flags = ""

    if args.chest_contents_shuffle_random:
        flags += f" -ccsr {args.chest_contents_shuffle_random_percent}"
    elif args.chest_contents_random_tiered:
        flags += " -ccrt"
    elif args.chest_contents_random_scaled:
        flags += " -ccrs"
    elif args.chest_contents_empty:
        flags += " -cce"

    if args.chest_monsters_shuffle:
        flags += " -cms"

    ### chest mods
    if args.empty_chest_shuffle:
        flags += f" -ecs {args.empty_chest_shuffle_percent}"
    if args.gold_chest_shuffle:
        flags += f" -gcs {args.gold_chest_shuffle_percent}"
    if args.no_good_chests:
        flags += " -nogoodchests"
    if args.replace_with_items:
        flags += " -rxi"

    return flags

def options(args):
    result = []

    contents_value = "Original"
    if args.chest_contents_shuffle_random:
        contents_value = "Shuffle + Random"
    elif args.chest_contents_random_tiered:
        contents_value = "Random Tiered"
    elif args.chest_contents_random_scaled:
        contents_value = "Random Scaled"
    elif args.chest_contents_empty:
        contents_value = "Empty"

    result.append(("Contents", contents_value))
    if args.chest_contents_shuffle_random:
        result.append(("Random Percent", f"{args.chest_contents_shuffle_random_percent}%"))
    result.append(("Monsters-In-A-Box Shuffled", args.chest_monsters_shuffle))

    ### chest mods
    if args.empty_chest_shuffle:
        result.append(("Random Empty Percent", f"{args.empty_chest_shuffle_percent}%"))
    if args.gold_chest_shuffle:
        result.append(("Random GP Percent", f"{args.gold_chest_shuffle_percent}%"))
    if args.no_good_chests:
        result.append(("No good chests", f"{args.no_good_chests}"))
    if args.replace_with_items:
        result.append(("Excluded become items", f"{args.replace_with_items}"))

    return result

def menu(args):
    entries = options(args)

    if args.chest_contents_shuffle_random:
        entries[0] = ("Shuffle + Random", entries[1][1]) # put percent on same line
        del entries[1]                                   # delete random percent line
    else:
        entries[0] = (entries[0][1], "")
    entries[1] = ("MIAB Shuffled", entries[1][1])
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
