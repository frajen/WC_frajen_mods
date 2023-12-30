def name():
    return "Items"

def parse(parser):
    from data.characters import Characters
    items = parser.add_argument_group("Items")

    items_equipable = items.add_mutually_exclusive_group()
    items_equipable.add_argument("-ier", "--item-equipable-random",
                                 default = None, type = int, nargs = 2, metavar = ("MIN", "MAX"),
                                 choices = range(Characters.CHARACTER_COUNT + 1),
                                 help = "Each item equipable by between %(metavar)s random characters")
    items_equipable.add_argument("-iebr", "--item-equipable-balanced-random",
                                 default = None, type = int, metavar = "VALUE",
                                 choices = range(Characters.CHARACTER_COUNT + 1),
                                 help = "Each item equipable by %(metavar)s random characters. Total number of items equipable by each character is balanced")
    items_equipable.add_argument("-ieor", "--item-equipable-original-random",
                                 default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                 help = "Characters have a %(metavar)s chance of being able to equip each item they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each item they could previously equip")
    items_equipable.add_argument("-iesr", "--item-equipable-shuffle-random",
                                 default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                 help = "Shuffle character equipment. After randomization, characters have a %(metavar)s chance of being able to equip each item they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each item they could previously equip")

    items_equipable_relic = items.add_mutually_exclusive_group()
    items_equipable_relic.add_argument("-ierr", "--item-equipable-relic-random",
                                       default = None, type = int, nargs = 2, metavar = ("MIN", "MAX"),
                                       choices = range(Characters.CHARACTER_COUNT + 1),
                                       help = "Each relic equipable by between %(metavar)s random characters")
    items_equipable_relic.add_argument("-ierbr", "--item-equipable-relic-balanced-random",
                                       default = None, type = int, metavar = "VALUE",
                                       choices = range(Characters.CHARACTER_COUNT + 1),
                                       help = "Each relic equipable by %(metavar)s random characters. Total number of relics equipable by each character is balanced")
    items_equipable_relic.add_argument("-ieror", "--item-equipable-relic-original-random",
                                       default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                       help = "Characters have a %(metavar)s chance of being able to equip each relic they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each relic they could previously equip")
    items_equipable_relic.add_argument("-iersr", "--item-equipable-relic-shuffle-random",
                                       default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                       help = "Shuffle character relics. After randomization, characters have a %(metavar)s chance of being able to equip each item they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each item they could previously equip")

    items.add_argument("-csb", "--cursed-shield-battles", default = [256, 256], type = int,
                       nargs = 2, metavar = ("MIN", "MAX"), choices = range(257),
                       help = "Number of battles required to uncurse the cursed shield")

    items.add_argument("-mca", "--moogle-charm-all", action = "store_true",
                       help = "All characters can wear Moogle Charm relics which prevent random battles. Overrides Equipable option")
    items.add_argument("-stra", "--swdtech-runic-all", action = "store_true",
                       help = "All weapons enable swdtech and runic")

    items.add_argument("-saw", "--stronger-atma-weapon", action = "store_true",
                       help = "Atma Weapon moved to higher tier and divisor reduced from 64 to 32")

    ### item mods
    items.add_argument("-ultis", "--ultimate-items", action = "store_true",
                        help = "14 low tier items converted to FF6 Advance Ultimate Items")
    items.add_argument("-iteach", "--item-teacher", default = None, type = int,
                        choices = range(101), metavar = "COUNT", 
                        help = "Randomize spells that items teach")
    items.add_argument("-irstat", "--item-rand-stat", default = None, type = int,
                        choices = range(101), metavar = "COUNT", 
                        help = "Randomly boost item stats")
    items.add_argument("-irrdrstch", "--random-ranked-drops-steals-chance", default = 0, type = int,
                       choices = range(101),
                       help = "Chance to randomize enemy item drops/steals using item ranks")
    items.add_argument("-irrdrstvar", "--random-ranked-drops-steals-variation", default = 0, type = int,
                       choices = range(101),
                       help = "Range of random variation for enemy item drops/steals using indexed item ranks")
    items.add_argument("-idesc", "--adjusted-item-descriptions", action = "store_true",
                       help = "Shortens vanilla item descriptions")

def process(args):
    args._process_min_max("item_equipable_random")
    if args.item_equipable_balanced_random is not None:
        args.item_equipable_balanced_random_value = args.item_equipable_balanced_random
        args.item_equipable_balanced_random = True
    if args.item_equipable_original_random is not None:
        args.item_equipable_original_random_percent = args.item_equipable_original_random
        args.item_equipable_original_random = True
    if args.item_equipable_shuffle_random is not None:
        args.item_equipable_shuffle_random_percent = args.item_equipable_shuffle_random
        args.item_equipable_shuffle_random = True

    args._process_min_max("item_equipable_relic_random")
    if args.item_equipable_relic_balanced_random is not None:
        args.item_equipable_relic_balanced_random_value = args.item_equipable_relic_balanced_random
        args.item_equipable_relic_balanced_random = True
    if args.item_equipable_relic_original_random is not None:
        args.item_equipable_relic_original_random_percent = args.item_equipable_relic_original_random
        args.item_equipable_relic_original_random = True
    if args.item_equipable_relic_shuffle_random is not None:
        args.item_equipable_relic_shuffle_random_percent = args.item_equipable_relic_shuffle_random
        args.item_equipable_relic_shuffle_random = True

    args._process_min_max("cursed_shield_battles")
    args.cursed_shield_battles_original = args.cursed_shield_battles_min == 256 and\
                                          args.cursed_shield_battles_max == 256

    ### item mods
    if args.item_teacher is not None:
        args.item_teacher_chance = args.item_teacher
    if args.item_rand_stat is not None:
        args.item_rand_stat_chance = args.item_rand_stat

def flags(args):
    flags = ""

    if args.item_equipable_random:
        flags += f" -ier {args.item_equipable_random_min} {args.item_equipable_random_max}"
    elif args.item_equipable_balanced_random:
        flags += f" -iebr {args.item_equipable_balanced_random_value}"
    elif args.item_equipable_original_random:
        flags += f" -ieor {args.item_equipable_original_random_percent}"
    elif args.item_equipable_shuffle_random:
        flags += f" -iesr {args.item_equipable_shuffle_random_percent}"

    if args.item_equipable_relic_random:
        flags += f" -ierr {args.item_equipable_relic_random_min} {args.item_equipable_relic_random_max}"
    elif args.item_equipable_relic_balanced_random:
        flags += f" -ierbr {args.item_equipable_relic_balanced_random_value}"
    elif args.item_equipable_relic_original_random:
        flags += f" -ieror {args.item_equipable_relic_original_random_percent}"
    elif args.item_equipable_relic_shuffle_random:
        flags += f" -iersr {args.item_equipable_relic_shuffle_random_percent}"

    if args.cursed_shield_battles_min != 256 or args.cursed_shield_battles_max != 256:
        flags += f" -csb {args.cursed_shield_battles_min} {args.cursed_shield_battles_max}"

    if args.moogle_charm_all:
        flags += " -mca"
    if args.swdtech_runic_all:
        flags += " -stra"

    if args.stronger_atma_weapon:
        flags += " -saw"

    ### item mods
    if args.ultimate_items:
        flags += " -ultis"
    if args.item_teacher:
        flags += f" -iteach {args.item_teacher_chance}"
    if args.item_rand_stat:
        flags += f" -irstat {args.item_rand_stat_chance}"
    if args.random_ranked_drops_steals_chance:
        flags += f" -irrdrstch {args.random_ranked_drops_steals_chance}"
    if args.random_ranked_drops_steals_variation:
        flags += f" -irrdrstvar {args.random_ranked_drops_steals_variation}"
    if args.adjusted_item_descriptions:
        flags += " -idesc"

    return flags

def options(args):
    equipable = "Original"
    if args.item_equipable_random:
        equipable = f"Random {args.item_equipable_random_min}-{args.item_equipable_random_max}"
    elif args.item_equipable_balanced_random:
        equipable = f"Balanced Random {args.item_equipable_balanced_random_value}"
    elif args.item_equipable_original_random:
        equipable = f"Original + Random {args.item_equipable_original_random_percent}%"
    elif args.item_equipable_shuffle_random:
        equipable = f"Shuffle + Random {args.item_equipable_shuffle_random_percent}%"

    equipable_relics = "Original"
    if args.item_equipable_relic_random:
        equipable_relics = f"Random {args.item_equipable_relic_random_min}-{args.item_equipable_relic_random_max}"
    elif args.item_equipable_relic_balanced_random:
        equipable_relics = f"Balanced Random {args.item_equipable_relic_balanced_random_value}"
    elif args.item_equipable_relic_original_random:
        equipable_relics = f"Original + Random {args.item_equipable_relic_original_random_percent}%"
    elif args.item_equipable_relic_shuffle_random:
        equipable_relics = f"Shuffle + Random {args.item_equipable_relic_shuffle_random_percent}%"

    cursed_shield_battles = f"{args.cursed_shield_battles_min}-{args.cursed_shield_battles_max}"

    return [
        ("Equipable", equipable),
        ("Equipable Relics", equipable_relics),
        ("Cursed Shield Battles", cursed_shield_battles),
        ("Moogle Charm All", args.moogle_charm_all),
        ("SwdTech Runic All", args.swdtech_runic_all),
        ("Stronger Atma Weapon", args.stronger_atma_weapon),
        ("Ultimate Items", args.ultimate_items),
        ("Teach Spells", args.item_teacher),
        ("Stat Boosts", args.item_rand_stat),
        ("Random Drop/Steal %", args.random_ranked_drops_steals_chance),
        ("Random Drop/Steal Var", args.random_ranked_drops_steals_variation),
        ("Adjusted item desc", args.adjusted_item_descriptions),
    ]

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        try:
            if key == "Equipable":
                key = "Equip"
            elif key == "Equipable Relics":
                key = "EquipR"
            elif key == "Cursed Shield Battles":
                key = "Cursed Shield"
            value = value.replace("Balanced Random", "Balanced")
            value = value.replace("Original + Random", "Original + ")
            value = value.replace("Shuffle + Random", "Shuffle + ")
            entries[index] = (key, value)
        except:
            pass
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
