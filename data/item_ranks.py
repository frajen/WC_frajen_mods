### An item ranking system borrowed from Beyond Chaos
### A similar system was used in the development of WC's item prices

ranked_items = {
    222 : 10,   # Moogle Charm is lowest rank -> when 3 are given at the start
    65 : 30,    # Shuriken
    105 : 50,    # Leather Hat
    232 : 50,    # Tonic
    242 : 50,    # Antidote
    243 : 50,    # Eyedrop
    251 : 120,    # Echo Screen
    0 : 150,    # Dirk
    106 : 150,    # Hair Band
    132 : 150,    # LeatherArmor
    248 : 150,    # Green Cherry
    254 : 150,    # Dried Meat
    90 : 200,    # Buckler
    133 : 200,    # Cotton Robe
    174 : 200,    # Inviz Edge
    244 : 200,    # Soft
    107 : 250,    # Plumed Hat
    134 : 250,    # Kung Fu Suit
    170 : 250,    # AutoCrossbow
    1 : 300,    # MithrilKnife
    233 : 300,    # Potion
    241 : 300,    # Revivify
    252 : 300,    # Smoke Bomb
    91 : 400,    # Heavy Shld
    175 : 400,    # Shadow Edge
    10 : 450,    # MithrilBlade
    43 : 500,    # Ashura
    52 : 500,    # Mithril Rod
    66 : 500,    # Ninja Star
    83 : 500,    # MetalKnuckle
    163 : 500,    # NoiseBlaster
    171 : 500,    # Fire Skean
    172 : 500,    # Water Edge
    173 : 500,    # Bolt Edge
    176 : 500,    # Goggles
    177 : 500,    # Star Pendant
    183 : 500,    # Barrier Ring
    240 : 500,    # Fenix Down
    246 : 500,    # Sleeping Bag
    37 : 600,    # Imperial
    61 : 600,    # Chocobo Brsh
    109 : 600,    # Magus Hat
    136 : 600,    # Silk Robe
    135 : 700,    # Iron Armor
    184 : 700,    # MithrilGlove
    253 : 700,    # Warp Stone
    164 : 750,    # Bio Blaster
    11 : 800,    # RegalCutlass
    29 : 800,    # Mithril Pike
    44 : 800,    # Kotetsu
    84 : 800,    # Mithril Claw
    110 : 800,    # Bandana
    3 : 950,    # Air Lancet
    77 : 1000,    # Cards
    85 : 1000,    # Kaiser
    111 : 1000,    # Iron Helmet
    165 : 1000,    # Flash
    181 : 1000,    # Jewel Ring
    190 : 1000,    # True Knight
    245 : 1000,    # Remedy
    138 : 1100,    # Ninja Gear
    38 : 1200,    # Kodachi
    45 : 1200,    # Forged
    92 : 1200,    # Mithril Shld
    137 : 1200,    # Mithril Vest
    247 : 1200,    # Tent
    56 : 1500,    # Poison Rod
    182 : 1500,    # Fairy Ring
    230 : 1500,    # Sprint Shoes
    235 : 1500,    # Tincture
    115 : 1600,    # Head Band
    30 : 1700,    # Trident
    68 : 2000,    # Flail
    116 : 2000,    # Mithril Helm
    166 : 2000,    # Chain Saw
    139 : 2200,    # White Dress
    69 : 2500,    # Full Moon
    86 : 2500,    # Poison Claw
    93 : 2500,    # Gold Shld
    119 : 2500,    # Tiger Mask
    16 : 3000,    # Epee
    53 : 3000,    # Fire Rod
    54 : 3000,    # Ice Rod
    55 : 3000,    # Thunder Rod
    113 : 3000,    # Bard's Hat
    114 : 3000,    # Green Beret
    117 : 3000,    # Tiara
    168 : 3000,    # Drill
    178 : 3000,    # Peace Ring
    193 : 3000,    # Czarina Ring
    199 : 3000,    # Sneak Ring
    227 : 3000,    # Sniper Sight
    39 : 3200,    # Blossom
    95 : 3500,    # Diamond Shld
    108 : 3500,    # Beret
    140 : 3500,    # Mithril Mail
    118 : 4000,    # Gold Helmet
    212 : 4000,    # Beads
    71 : 4500,    # Boomerang
    70 : 5000,    # Morning Star
    81 : 5000,    # Dice
    144 : 5000,    # Power Sash
    167 : 5000,    # Debilitator
    179 : 5000,    # Amulet
    180 : 5000,    # White Cape
    185 : 5000,    # Guard Ring
    195 : 5000,    # Earrings
    196 : 5000,    # Atlas Armlet
    213 : 5000,    # Black Belt
    121 : 5500,    # Mystery Veil
    73 : 6000,    # Hawk Eye
    141 : 6000,    # Gaia Gear
    187 : 6000,    # Wall Ring
    188 : 6300,    # Cherub Down
    13 : 7000,    # Flame Sabre
    14 : 7000,    # Blizzard
    15 : 7000,    # ThunderBlade
    62 : 7000,    # DaVinci Brsh
    99 : 7000,    # Crystal Shld
    122 : 7000,    # Circlet
    186 : 7000,    # RunningShoes
    192 : 7000,    # Zephyr Cape
    225 : 7000,    # Back Guard
    12 : 7500,    # Rune Edge
    125 : 7500,    # Dark Hood
    46 : 8000,    # Tempest
    124 : 8000,    # Diamond Helm
    189 : 8000,    # Cure Ring
    210 : 8000,    # Hyper Wrist
    226 : 8000,    # Gale Hairpin
    47 : 9000,    # Murasame
    127 : 9000,    # Oath Veil
    191 : 9000,    # DragoonBoots
    19 : 10000,    # Enhancer
    31 : 10000,    # Stout Spear
    63 : 10000,    # Magical Brsh
    78 : 10000,    # Darts
    87 : 10000,    # Fire Knuckle
    126 : 10000,    # Crystal Helm
    143 : 10000,    # Gold Armor
    231 : 10000,    # Rename Card
    234 : 10000,    # X-Potion
    249 : 10000,    # Magicite
    250 : 10000,    # Super Ball
    6 : 11000,    # Man Eater
    145 : 11000,    # Light Robe
    17 : 12000,    # Break Blade
    34 : 12000,    # Gold Lance
    57 : 12000,    # Pearl Rod
    146 : 12000,    # Diamond Vest
    236 : 12500,    # Ether
    32 : 13000,    # Partisan
    58 : 13000,    # Gravity Rod
    80 : 13000,    # Trump
    150 : 13000,    # Dark Gear
    151 : 13000,    # Tao Robe
    131 : 14200,    # Titanium
    20 : 15000,    # Crystal
    75 : 15000,    # Sniper
    149 : 15000,    # DiamondArmor
    7 : 16000,    # SwordBreaker
    21 : 17000,    # Falchion
    152 : 17000,    # Crystal Mail
    74 : 20000,    # Bone Club
    155 : 20000,    # Imp's Armor
    194 : 20000,    # Cursed Ring
    237 : 20000,    # X-Ether
    130 : 23800,    # Thornlet
    169 : 25000,    # Air Anchor
    197 : 25000,    # Blizzard Orb
    198 : 25000,    # Rage Ring
    202 : 25000,    # Ribbon
    205 : 25000,    # Gold Hairpin
    207 : 25000,    # Thief Glove
    208 : 25000,    # Gauntlet
    214 : 25000,    # Coin Toss
    215 : 25000,    # FakeMustache
    219 : 25000,    # Memento Ring
    220 : 25000,    # Safety Bit
    221 : 25000,    # Relic Ring
    223 : 25000,    # Charm Bangle
    229 : 25000,    # Tintinabar
    238 : 25000,    # Elixir
    36 : 25300,    # Imp Halberd
    112 : 27300,    # Coronet
    123 : 27400,    # Regal Crown
    129 : 27800,    # Genji Helmet
    142 : 28600,    # Mirage Vest
    201 : 29800,    # Hero Ring
    203 : 30000,    # Muscle Belt
    204 : 30000,    # Crystal Orb
    2 : 30000,    # Guardian
    153 : 30900,    # Czarina Gown
    160 : 32000,    # Nutkin Suit
    5 : 33600,    # Assassin
    59 : 34000,    # Punisher
    72 : 34400,    # Rising Sun
    18 : 35000,    # Drainer
    40 : 35000,    # Hardened
    22 : 35600,    # Soul Sabre
    64 : 36100,    # Rainbow Brsh
    157 : 36700,    # Tabby Suit
    158 : 37100,    # Chocobo Suit
    159 : 37100,    # Moogle Suit
    48 : 37500,    # Aura
    23 : 39500,    # Ogre Nix
    79 : 39600,    # Doom Darts
    4 : 40400,    # ThiefKnife
    88 : 40600,    # Dragon Claw
    41 : 40800,    # Striker
    67 : 41200,    # Tack Star
    76 : 42800,    # Wing Edge
    49 : 43200,    # Strato
    51 : 43700,    # Heal Rod
    200 : 43800,    # Pod Bracelet
    8 : 43800,    # Graedus
    239 : 44000,    # Megalixir
    89 : 44000,    # Tiger Fangs
    101 : 44400,    # TortoiseShld
    120 : 44800,    # Red Cap
    25 : 44900,    # Scimitar
    33 : 45000,    # Pearl Lance
    147 : 45000,    # Red Jacket
    42 : 45000,    # Stunner
    50 : 45400,    # Sky Render
    35 : 45800,    # Aura Lance
    24 : 46500,    # Excalibur
    100 : 47000,    # Genji Shld
    102 : 50400,    # Cursed Shld
    209 : 50500,    # Genji Glove
    217 : 53300,    # Dragon Horn
    154 : 55000,    # Genji Armor
    224 : 55000,    # Marvel Shoes
    60 : 56500,    # Magus Rod
    161 : 56700,    # BehemothSuit
    216 : 59100,    # Gem Box
    218 : 59200,    # Merit Award
    28 : 60300,    # Atma Weapon
    128 : 61600,    # Cat Hood
    148 : 64300,    # Force Armor
    162 : 64300,    # Snow Muffler
    94 : 65000,    # Aegis Shld
    206 : 66900,    # Economizer
    104 : 75000,    # Force Shld
    96 : 77700,    # Flame Shld
    97 : 79600,    # Ice Shld
    98 : 83800,    # Thunder Shld
    82 : 91600,    # Fixed Dice
    9 : 95500,    # ValiantKnife
    211 : 125000,    # Offering
    156 : 125000,    # Minerva
    27 : 125100,    # Ragnarok
    228 : 137500,    # Exp. Egg
    26 : 175500,    # Illumina
    103 : 190900,    # Paladin Shld
}
