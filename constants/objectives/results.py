from constants.blitzes import id_blitz
from constants.dances import id_dance
from constants.lores import id_lore
from constants.rages import id_rage
from constants.swdtechs import id_swdtech
from constants.spells import id_spell

from collections import namedtuple
ResultType = namedtuple("ResultType", ["id", "name", "format_string", "value_range"])

category_types = {
    "Random" : [
        ResultType(0, "Random", "Random", None),
    ],
    "Kefka's Tower" : [
        ResultType(1, "Kefka's Tower", "Random", None),
        ResultType(2, "Unlock Final Kefka", "Unlock Final Kefka", None),
        ResultType(3, "Unlock KT Skip", "Unlock KT Skip", None),
    ],
    "Auto" : [
        ResultType(4, "Auto", "Random", None),
        ResultType(5, "Auto Berserk", "Auto Berserk", None),
        ResultType(6, "Auto Condemned", "Auto Condemned", None),
        ResultType(7, "Auto Float", "Auto Float", None),
        ResultType(8, "Auto Haste", "Auto Haste", None),
        ResultType(9, "Auto Image", "Auto Image", None),
        ResultType(10, "Auto Muddle", "Auto Muddle", None),
        ResultType(11, "Auto Mute", "Auto Mute", None),
        ResultType(12, "Auto Reflect", "Auto Reflect", None),
        ResultType(13, "Auto Regen", "Auto Regen", None),
        ResultType(14, "Auto Safe", "Auto Safe", None),
        ResultType(15, "Auto Seizure", "Auto Seizure", None),
        ResultType(16, "Auto Shell", "Auto Shell", None),
        ResultType(17, "Auto Sleep", "Auto Sleep", None),
        ResultType(18, "Auto Slow", "Auto Slow", None),
    ],
    "Battle" : [
        ResultType(20, "Battle", "Random", None),
        ResultType(21, "Add Enemy Levels", "Enemy Levels {:+d}", list(range(1, 100))),
        ResultType(22, "Add Boss Levels", "Boss Levels {:+d}", list(range(1, 100))),
        ResultType(23, "Add Dragon Levels", "Dragon Levels {:+d}", list(range(1, 100))),
        ResultType(24, "Add Final Levels", "Final Levels {:+d}", list(range(1, 100))),
    ],
    "Command" : [
        ResultType(25, "Command", "Random", None),
        ResultType(26, "Learn Blitzes", "Learn {} Blitzes", list(range(1, len(id_blitz) + 1))),
        ResultType(27, "Learn Dances", "Learn {} Dances", list(range(1, len(id_dance) + 1))),
        ResultType(28, "Learn Lores", "Learn {} Lores", list(range(1, len(id_lore) + 1))),
        ResultType(29, "Learn Rages", "Learn {} Rages", list(range(1, len(id_rage) + 1))),
        ResultType(30, "Learn SwdTechs", "Learn {} SwdTechs", list(range(1, len(id_swdtech) + 1))),
        ResultType(31, "Learn Spells", "Learn {} Spells", list(range(1, len(id_spell) + 1))),
        ResultType(32, "Forget Spells", "Forget {} Spells", list(range(1, len(id_spell) + 1))),
        ResultType(33, "Max Morph Duration", "Max Morph Duration", None),
    ],
    "Item" : [
        ResultType(34, "Item", "Random", None),
        ResultType(35, "Breakable Rods", "Breakable Rods", None),
        ResultType(36, "Dragoon", "Dragoon", None),
        ResultType(37, "Dried Meat", "Dried Meat", None),
        ResultType(38, "Exp. Egg", "Exp. Egg", None),
        ResultType(58, "High Tier Item", "High Tier Item", None),
        ResultType(40, "Illumina", "Illumina", None),
        ResultType(39, "Imp Set", "Imp Set", None),
        ResultType(41, "Rename Cards", "Rename Cards", None),
        ResultType(42, "Ribbon", "Ribbon", None),
        ResultType(43, "Tools", "Tools", None),

        ### Ultimate items mods
        ResultType(63, "Ultimate Items", "Ultimate Items", None),  #includes Dueling Mask/Bone Wrist
        ResultType(64, "Angel Brush", "Angel Brush", None),
        ResultType(65, "Apocalypse", "Apocalypse", None),
        ResultType(66, "Bone Wrist", "Bone Wrist", None),
        ResultType(67, "Dueling Mask", "Dueling Mask", None),
        ResultType(68, "Final Trump", "Final Trump", None),
        ResultType(69, "Godhand", "Godhand", None),
        ResultType(70, "Gungnir", "Gungnir", None),
        ResultType(71, "Longinus", "Longinus", None),
        ResultType(72, "Oborozuki", "Oborozuki", None),
        ResultType(73, "Save The Queen", "Save The Queen", None),
        ResultType(74, "Scorpion Tail", "Scorpion Tail", None),
        ResultType(75, "Stardust Rod", "Stardust Rod", None),
        ResultType(76, "Zanmato", "Zanmato", None),
        ResultType(77, "ZwillXBlade", "ZwillXBlade", None),

        ### Starter kit mods
        ResultType(78, "Full Starter Kit", "Full Starter Kit", None),
        ResultType(79, "Basic Starter Kit", "Basic Starter Kit", None),
        ResultType(80, "Better Starter Kit", "Better Starter Kit", None),
        ResultType(81, "Hat Trick Kit", "Hat Trick Kit", None),

        ### Other item sets
        ResultType(82, "Better Tier Item", "Better Tier Item", None),
        ResultType(83, "Elemental Shield", "Elemental Shield", None),
        ResultType(84, "Elemental Swords", "Elemental Swords", None),
        ResultType(85, "Hero Ring", "Hero Ring", None),
        ResultType(86, "Earrings", "Earrings", None),
        ResultType(87, "Wind God", "Wind God", None),
        ResultType(88, "Diamond Set", "Diamond Set", None),
        ResultType(89, "Crystal Set", "Crystal Set", None),
        ResultType(90, "Genji Set", "Genji Set", None),
        ResultType(91, "Gold Set", "Gold Set", None),
        ResultType(92, "Force Set", "Force Set", None),
        ResultType(93, "Heal Pack", "Heal Pack", None),
    ],
    "Stat" : [
        ResultType(44, "Stat", "Random", None),
        ResultType(45, "MagPwr All", "{:+d} Mag.Pwr All", list(range(-99, 100))),
        ResultType(46, "Speed All", "{:+d} Speed All", list(range(-99, 100))),
        ResultType(47, "Stamina All", "{:+d} Stamina All", list(range(-99, 100))),
        ResultType(48, "Vigor All", "{:+d} Vigor All", list(range(-99, 100))),
        ResultType(49, "MagPwr Random", "{:+d} Mag.Pwr {}", list(range(-99, 100))),
        ResultType(50, "Speed Random", "{:+d} Speed {}", list(range(-99, 100))),
        ResultType(51, "Stamina Random", "{:+d} Stamina {}", list(range(-99, 100))),
        ResultType(52, "Vigor Random", "{:+d} Vigor {}", list(range(-99, 100))),
    ],
    "Status" : [
        ResultType(53, "Status", "Random", None),
        ResultType(54, "Fallen One", "Fallen One", None),
        ResultType(55, "Full Heal", "Full Heal", None),
        ResultType(56, "Imp Song", "Imp Song", None),
        ResultType(57, "Sour Mouth", "Sour Mouth", None),
    ],
}

#Additional results
category_types["Command"].append(ResultType(59, "Magitek Upgrade", "Magitek Upgrade", None))
category_types["Item"].append(ResultType(60, "Sprint Shoes", "Sprint Shoes", None))
category_types["Auto"].append(ResultType(61, "Auto Dog Block", "Auto Dog Block", None))
category_types["Auto"].append(ResultType(62, "Auto Life 3", "Auto Life 3", None))

categories = list(category_types.keys())

id_type = {}
name_type = {}
name_category = {}
for category in category_types:
    for _type in category_types[category]:
        id_type[_type.id] = _type
        name_type[_type.name] = _type
        name_category[_type.name] = category

names = list(name_type.keys())

types = [_type for name, _type in name_type.items()]
