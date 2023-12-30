#rooms - series of doors.  [ [2-way doors], [1-way exits], [1-way entrances], require_world?]

room_data = {
    # 'root-code' rooms are terminal entrance rooms for randomizing individual sections.
    # They are also used in Dungeon Crawl mode.
##    'root-u' : [ [], [2010], [3009], None], # Root map for -door-randomize-umaro
##    'root-unb' : [ [1138], [], [], 0], # Root map for -door-randomize-upper-narshe-wob
##    'root-unr' : [ [1146], [], [], 1], # Root map for -door-randomize-upper-narshe-wor
##    'root-em' : [ [44], [], [], 0], # Root map for -door-randomize-esper-mountain
##    'root-ob' : [ [593], [], [], 1], # Root map for -door-randomize-owzer's basement
##    'root-mf' : [ [1229], [ ], [3028], 0],     # Magitek Factory root entrance in Vector
##    'root_sg': [[1058, 1263], [], [], 0],  # Root entrance = imperial base
    
    0 : [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 44], [ ], [ ], None], #World of Balance
    1 : [[41, 43], [ ], [ ], None], #World of Balance Cave to Sealed Gate Bridge
    2 : [[45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79], [ ], [ ], None], #World of Ruin
    3 : [[81], [ ], [ ], None], #Blackjack Outside
    4 : [[82, 83], [ ], [ ], None], #Blackjack Gambling Room
    5 : [[84, 85, 87], [ ], [ ], None], #Blackjack Party Room
    6 : [[86], [ ], [ ], None], #Blackjack Shop Room
    7 : [[88, 89], [ ], [ ], None], #Blackjack Engine Room
    8 : [[90], [ ], [ ], None], #Blackjack Parlor Room
    9 : [[91], [ ], [ ], None], #Falcon Outside
    10 : [[92, 93, 95], [ ], [ ], None], #Falcon Main Room
    11 : [[94], [ ], [ ], None], #Falcon Small Room
    12 : [[96], [ ], [ ], None], #Falcon Engine Room
    13 : [[1129], [ ], [ ], None], #Chocobo Stable Exterior WoB
    14 : [[1131], [ ], [ ], None], #Chocobo Stable Interior
    15 : [[1132], [ ], [ ], None], #Chocobo Stable Exterior WoR

    17 : [[97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 108, 112, 1135, 1136], [ ], [ ], None], #Narshe Outside WoB
    18 : [[107, 111], [ ], [ ], None], #Narshe Outside Behind Arvis to Mines WoB
    19 : [[109, 110], [ ], [ ], None], #Narshe South Caves Secret Passage Outside WoB
    20 : [[113, 114], [ ], [ ], None], #Narshe Northern Mines 2nd/3rd Floor Outside WoB
    21 : [[115, 1139], [ ], [ ], None], #Narshe Northern Mines 3rd Floor Outside WoB
    22 : [[1137, 1138], [ ], [ ], None], #Narshe Northern Mines 1st Floor Outside WoB
    23 : [[1140, 1141], [ ], [ ], None], #Snow Battlefield WoB
    24 : [[1142], [ ], [ ], None], #Narshe Peak WoB
    25 : [[116, 117], [ ], [ ], None], #Narshe Weapon Shop
    26 : [[118], [ ], [ ], None], #Narshe Weapon Shop Back Room
    27 : [[119, 120], [ ], [ ], None], #Narshe Armor Shop
    28 : [[121], [ ], [ ], None], #Narshe Item Shop
    29 : [[122], [ ], [ ], None], #Narshe Relic Shop
    30 : [[123], [ ], [ ], None], #Narshe Inn
    31 : [[124, 125], [ ], [ ], None], #Narshe Arvis House
    32 : [[126], [ ], [ ], None], #Narshe Elder House
    33 : [[127], [ ], [ ], None], #Narshe Cursed Shld House
    34 : [[128], [ ], [ ], None], #Narshe Treasure Room
    35 : [[129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 140, 144, 1143, 1144], [ ], [ ], None], #Narshe Outside WoR
    36 : [[139, 143], [ ], [ ], None], #Narshe Outside Behind Arvis to Mines WoR
    37 : [[141, 142], [ ], [ ], None], #Narshe South Caves Secret Passage Outside WoR
    38 : [[145, 146], [ ], [ ], None], #Narshe Northern Mines 2nd/3rd Floor Outside WoR
    39 : [[147, 1147], [ ], [ ], None], #Narshe Northern Mines 3rd Floor Outside WoR
    40 : [[1145, 1146], [ ], [ ], None], #Narshe Northern Mines 1st Floor Outside WoR
    41 : [[1148, 1149], [ ], [ ], None], #Snow Battlefield WoR
    42 : [[1150], [ ], [ ], None], #Narshe Peak WoR
    43 : [[148, 149], [ ], [ ], None], #Narshe Northern Mines 1F Side/East Room WoR
    44 : [[150, 151], [ ], [ ], None], #Narshe Northern Mines 2F Inside WoR
    45 : [[152, 153], [ ], [ ], None], #Narshe Northern Mines 3F Inside WoR
    46 : [[154, 155], [ ], [ ], None], #Narshe South Caves Secret Passage 1F WoR
    47 : [[156, 157, 1151], [ ], [ ], None], #Narshe Northern Mines Main Hallway WoR
    48 : [[158], [ ], [ ], None], #Narshe Northern Mines Tritoch Room WoR
    49 : [[159, 160], [ ], [ ], None], #Narshe 3-Party Cave WoR
    50 : [[161, 162, 163, 164], [ ], [ ], None], #Narshe South Caves WoR
    51 : [[165, 166], [ ], [ ], None], #Narshe Checkpoint Room WoR
    52 : [[167, 168], [ ], [ ], None], #Narshe South Caves Secret Passage 3F WoR

    54 : [[169, 170], [ ], [ ], None], #Narshe Northern Mines Side Room 1F WoB
    55 : [[171, 172], [ ], [ ], None], #Narshe Northern Mines Side Room 2F WoB
    56 : [[173, 174], [ ], [ ], None], #Narshe Northern Mines Inside 3F WoB
    57 : [[175, 176], [ ], [ ], None], #Narshe South Caves Secret Passage 1F WoB


    60 : [[178, 179, 1155], [ ], [ ], None], #Narshe Northern Mines Main Hallway WoB
    61 : [[180], [ ], [ ], None], #Narshe Northern Mines Tritoch Room WoB
    62 : [[181, 182], [ ], [ ], None], #Narshe Moogle Cave WoR
    63 : [[183, 184], [ ], [ ], None], #Narshe South Caves Secret Passage 3F WoB
    64 : [[185, 186], [ ], [ ], None], #Narshe Checkpoint Room WoB
    65 : [[187, 188, 189, 190], [ ], [ ], None], #Narshe South Caves WoB
    66 : [[191, 192], [ ], [ ], None], #Narshe 3-Party Cave WoB
    67 : [[193, 194], [ ], [ ], None], #Narshe Moogle Cave WoB
    68 : [[195], [ ], [ ], None], #Cave to South Figaro Siegfried Tunnel
    69 : [[197], [ ], [ ], None], #Figaro Castle Entrance
    70 : [[198, 199, 201, 204], [ ], [ ], None], #Figaro Castle Outside Courtyard
    71 : [[200], [ ], [ ], None], #Figaro Castle Center Tower Outside
    72 : [[202, 205, 207, 208], [ ], [ ], None], #Figaro Castle Desert Outside
    73 : [[203], [ ], [ ], None], #Figaro Castle West Tower Outside
    74 : [[206], [ ], [ ], None], #Figaro Castle East Tower Outside
    75 : [[209, 210], [ ], [ ], None], #Figaro Castle King's Bedroom
    76 : [[1160], [ ], [ ], None], #Figaro Castle Throne Room
    77 : [[211, 212, 213, 214], [ ], [ ], None], #Figaro Castle Foyer
    78 : [[215, 216, 217, 218, 219, 220], [ ], [ ], None], #Figaro Castle Main Hallway
    79 : [[221, 222, 223], [ ], [ ], None], #Figaro Castle Behind Throne Room
    80 : [[224, 225], [ ], [ ], None], #Figaro Castle East Bedroom
    81 : [[226, 227], [ ], [ ], None], #Figaro Castle Inn
    82 : [[228], [ ], [ ], None], #Figaro Castle West Shop
    83 : [[229], [ ], [ ], None], #Figaro Castle East Shop
    84 : [[230, 231], [ ], [ ], None], #Figaro Castle Below Inn
    85 : [[232, 233], [ ], [ ], None], #Figaro Castle Below Library
    86 : [[234, 235], [ ], [ ], None], #Figaro Castle Library
    87 : [[236, 238], [ ], [ ], None], #Figaro Castle Switch Room
    88 : [[237], [ ], [ ], None], #Figaro Castle Prison
    89 : [[239, 240], [ ], [ ], None], #Figaro Castle B1 Hallway East
    90 : [[241, 242], [ ], [ ], None], #Figaro Castle B1 Hallway West
    91 : [[243, 244], [ ], [ ], None], #Figaro Castle B2 Hallway
    92 : [[245, 247], [ ], [ ], None], #Figaro Castle B2 East Hallway
    93 : [[246, 248], [ ], [ ], None], #Figaro Castle B2 West Hallway
    94 : [[249, 250, 251], [ ], [ ], None], #Figaro Castle B2 4 Chest Room
    95 : [[252, 253], [ ], [ ], None], #Figaro Castle Engine Room
    96 : [[254], [ ], [ ], None], #Figaro Castle Treasure Room Behind Engine Room
    97 : [[255], [ ], [ ], None], #Figaro Castle B1 Single Chest Room
    98 : [[256, 257], [ ], [ ], None], #Cave to South Figaro Small Hallway WoR
    99 : [[258, 259, 260], [ ], [ ], None], #Cave to South Figaro Big Room WoR
    100 : [[261, 262], [ ], [ ], None], #Cave to South Figaro South Entrance WoR
    101 : [[263, 264], [ ], [ ], None], #Cave to South Figaro Small Hallway WoB
    102 : [[265, 266, 267], [ ], [ ], None], #Cave to South Figaro Big Room WoB
    103 : [[268], [ ], [ ], None], #Cave to South Figaro South Entrance WoB
    104 : [[270], [ ], [ ], None], #Cave to South Figaro Single Chest Room WoB
    105 : [[271], [ ], [ ], None], #Cave to South Figaro Turtle Room WoB
    106 : [[1161], [ ], [ ], None], #Cave to South Figaro Outside WoB
    107 : [[283, 286, 287, 288, 289, 290, 291, 292, 293, 294, 1162, 1163, 1164, 1165, 1166], [ ], [ ], None], #South Figaro Outside WoR
    108 : [[284, 285], [ ], [ ], None], #South Figaro Rich Man's House Side Outside WoR
    109 : [[295, 299, 300, 301, 302, 303, 304, 305, 306, 1167, 1169, 1170, 1171], [ ], [ ], None], #South Figaro Outside WoB
    110 : [[296, 297], [ ], [ ], None], #South Figaro Rich Man's House Side Outside WoB
    111 : [[298], [ ], [ ], None], #South Figaro East Side
    112 : [[1168], [ ], [ ], None], #South Figaro Outside East Side WoB
    113 : [[307, 308], [ ], [ ], None], #South Figaro Relics
    114 : [[309, 310], [ ], [ ], None], #South Figaro Inn
    115 : [[311, 312], [ ], [ ], None], #South Figaro Armory
    116 : [[313, 314, 316], [ ], [ ], None], #South Figaro Pub
    117 : [[315], [ ], [ ], None], #South Figaro Pub Basement
    118 : [[1172], [ ], [ ], None], #South Figaro Chocobo Stable
    119 : [[317, 318, 319], [ ], [ ], None], #South Figaro Rich Man's House 1F
    120 : [[320, 321, 324], [ ], [ ], None], #South Figaro Rich Man's House 2F Hallway
    121 : [[322, 325], [ ], [ ], None], #South Figaro Rich Man's Master Bedroom
    122 : [[323], [ ], [ ], None], #South Figaro Rich Man's House Kids' Room
    123 : [[326, 327], [ ], [ ], None], #South Figaro Rich Man's House Bedroom Secret Stairwell
    124 : [[328, 329, 331, 332, 333], [ ], [ ], None], #South Figaro Rich Man's House B1
    125 : [[330], [ ], [ ], None], #South Figaro Celes Cell
    126 : [[334, 335], [ ], [ ], None], #South Figaro Clock Room
    127 : [[336], [ ], [ ], None], #South Figaro Duncan's House Basement
    128 : [[337], [ ], [ ], None], #South Figaro Item Shop
    129 : [[338], [ ], [ ], None], #South Figaro Rich Man's House Secret Back Door Room
    130 : [[346], [ ], [ ], None], #South Figaro Cider House Secret Room
    131 : [[339, 344], [ ], [ ], None], #South Figaro Cider House Upstairs
    132 : [[340, 343, 348], [ ], [ ], None], #South Figaro Cider House Downstairs
    133 : [[341, 342], [ ], [ ], None], #South Figaro Behind Duncan's House
    134 : [[345, 347], [ ], [ ], None], #South Figaro Duncan's House Upstairs
    135 : [[349, 350, 351], [ ], [ ], None], #South Figaro Escape Tunnel
    136 : [[352], [ ], [ ], None], #South Figaro Rich Man's House Save Point Room
    137 : [[353], [ ], [ ], None], #South Figaro B2 3 Chest Room
    138 : [[354], [ ], [ ], None], #South Figaro B2 2 Chest Room
    139 : [[355], [ ], [ ], None], #Cave to South Figaro Single Chest Room WoR
    140 : [[356], [ ], [ ], None], #Cave to South Figaro Turtle Room WoR
    141 : [[357], [ ], [ ], None], #Cave to South Figaro Turtle Door WoR
    142 : [[1173], [ ], [ ], None], #South Figaro Docks
    143 : [[358, 359], [ ], [ ], None], #Cave to South Figaro Behind Turtle
    144 : [[360, 361, 1174], [ ], [ ], None], #Sabin's House Outside
    145 : [[362], [ ], [ ], None], #Sabin's House Inside
    146 : [[363, 1175], [ ], [ ], None], #Mt. Kolts South Entrance
    147 : [[364, 365, 366], [ ], [ ], None], #Mt. Kolts 1F Outside
    148 : [[367], [ ], [ ], None], #Mt Kolts Outside Chest 1 Room
    149 : [[368, 1176], [ ], [ ], None], #Mt Kolts Outside Cliff West
    150 : [[369], [ ], [ ], None], #Mt Kolts Outside Chest 2 Room
    151 : [[370, 371], [ ], [ ], None], #Mt. Kolts Outside Bridge
    152 : [[372, 373], [ ], [ ], None], #Mt. Kolts Vargas Spiral
    153 : [[375], [ ], [ ], None], #Mt. Kolts First Inside Room
    154 : [[376, 377, 378, 385], [ ], [ ], None], #Mt. Kolts 4-Way Split Room
    155 : [[379, 380], [ ], [ ], None], #Mt. Kolts 2F Inside Room
    156 : [[381, 382], [ ], [ ], None], #Mt. Kolts Inside Bridges Room
    157 : [[383], [ ], [ ], None], #Mt. Kolts After Vargas Room
    158 : [[386], [ ], [ ], None], #Mt Kolts Inside Chest Room
    159 : [[1177, 1178], [ ], [ ], None], #Mt. Kolts North Exit
    160 : [[387, 388, 389, 1179], [ ], [ ], None], #Mt. Kolts Back Side
    161 : [[390, 391], [ ], [ ], None], #Mt. Kolts Save Point Room
    162 : [[392, 393, 394, 395], [ ], [ ], None], #Narshe School Main Room
    163 : [[396], [ ], [ ], None], #Narshe School Left Room
    164 : [[397], [ ], [ ], None], #Narshe School Middle Room
    165 : [[398], [ ], [ ], None], #Narshe School Right Room
    166 : [[1180, 1181], [ ], [ ], None], #Returners Hideout Outside
    167 : [[399, 400, 401, 402, 403], [ ], [ ], None], #Returners Hideout Main Room
    168 : [[404], [ ], [ ], None], #Returners Hideout Back Room
    169 : [[405, 406], [ ], [ ], None], #Returners Hideout Banon's Room
    170 : [[407], [ ], [ ], None], #Returner's Hideout Bedroom
    171 : [[408], [ ], [ ], None], #Returner's Hideout Inn
    172 : [[409, 410], [ ], [ ], None], #Returner's Hideout Secret Passage
    173 : [[1182], [ ], [ ], None], #Lete River Jumpoff
    174 : [[411, 1183], [ ], [ ], None], #Crazy Old Man's House Outside WoB
    175 : [[412], [ ], [ ], None], #Crazy Old Man's House Inside

    177 : [[417, 432], [ ], [ ], None], #Doma 3F Inside
    178 : [[418, 419, 424, 428, 430, 431, 433], [ ], [ ], None], #Doma Main Room
    179 : [[420], [ ], [ ], None], #Doma 2F Treasure Room
    180 : [[421], [ ], [ ], None], #Doma Right Side Bedroom
    181 : [[422, 425, 427, 429], [ ], [ ], None], #Doma Inner Room
    182 : [[423], [ ], [ ], None], #Doma Throne Room
    183 : [[426], [ ], [ ], None], #Doma Left Side Bedroom
    184 : [[434], [ ], [ ], None], #Doma Cyan's Room
    185 : [[435], [ ], [ ], None], #Doma Dream 3F Outside
    186 : [[436], [ ], [ ], None], #Doma Dream 1F Outside
    187 : [[437, 438], [ ], [ ], None], #Doma Dream 2F Outside
    188 : [[439, 453], [ ], [ ], None], #Doma Dream 3F Inside
    189 : [[440, 441, 445, 449, 451, 452, 454], [ ], [ ], None], #Doma Dream Main Room
    190 : [[442], [ ], [ ], None], #Doma Dream Treasure Room
    191 : [[443], [ ], [ ], None], #Doma Dream Right Side Bedroom
    192 : [[444, 446, 448, 450], [ ], [ ], None], #Doma Dream Inner Room
    193 : [[447], [ ], [ ], None], #Doma Dream Side Bedroom
    194 : [[455], [ ], [ ], None], #Doma Dream Cyan's Room
    195 : [[456], [ ], [ ], None], #Doma Dream Throne Room
    196 : [[457, 458, 1186], [ ], [ ], None], #Duncan's House Outside
    197 : [[459], [ ], [ ], None], #Duncan's House
    198 : [[460, 1187], [ ], [ ], None], #Crazy Old Man's House WoR




    203 : [[469], [ ], [ ], None], #Phantom Train Station
    204 : [[470, 471, 472, 473], [ ], [ ], None], #Phantom Train Outside 4th Section

    206 : [[474, 475, 476], [ ], [ ], None], #Phantom Train Outside 1st Section



    210 : [[477, 483], [ ], [ ], None], #Doma Dream Train Outside 3rd Section
    211 : [[478, 479, 480, 481], [ ], [ ], None], #Doma Dream Train Outside 2nd Section
    212 : [[482], [ ], [ ], None], #Doma Dream Train Outside 1st Section
    213 : [[484, 485, 486, 487], [ ], [ ], None], #Doma Dream Train 2nd Car

    215 : [[488], [ ], [ ], None], #Phantom Train Caboose Inner Room

    217 : [[489, 490, 491, 492], [ ], [ ], None], #Phantom Train Dining Room
    218 : [[493, 494], [ ], [ ], None], #Phantom Train Seating Car with Switch Left Side



    222 : [[496, 497, 498, 499, 500, 501], [ ], [ ], None], #Phantom Train Caboose
    223 : [[502], [ ], [ ], None], #Phantom Train Final Save Point Room



    227 : [[503], [ ], [ ], None], #Mobliz Kids' Hideaway
    228 : [[504, 505], [ ], [ ], None], #Baren Falls Inside
    229 : [[1189], [ ], [ ], None], #Baren Falls Cliff
    230 : [[506, 507, 508, 512, 1190, 1191], [ ], [ ], None], #Mobliz Outside WoB
    231 : [[1192, 1193], [ ], [ ], None], #Mobliz Outside WoR

    233 : [[516], [ ], [ ], None], #Mobliz Inn
    234 : [[517, 518], [ ], [ ], None], #Mobliz Arsenal

    236 : [[519], [ ], [ ], None], #Mobliz Mail Room Upstairs
    237 : [[520], [ ], [ ], None], #Mobliz Item Shop
    238 : [[521], [ ], [ ], None], #Mobliz Mail Room Basement WoB


    241 : [[1196, 1197], [ ], [ ], None], #Baren Falls Outside
    242 : [[523, 524], [ ], [ ], None], #Crescent Mountain
    243 : [[1198], [ ], [ ], None], #Serpent Trench Cliff
    244 : [[525, 526, 1201, 1202], [ ], [ ], None], #Nikeah Outside WoB
    245 : [[527], [ ], [ ], None], #Nikeah Inn
    246 : [[528], [ ], [ ], None], #Nikeah Pub
    247 : [[1203], [ ], [ ], None], #Nikeah Chocobo Stable
    248 : [[529], [ ], [ ], None], #Serpent Trench Cave 2nd Part 1st Room
    249 : [[530], [ ], [ ], None], #Serpent Trench Cave 2nd Part 2nd Room


    252 : [[531, 532, 533], [ ], [ ], None], #Mt Zozo Outside Bridge
    253 : [[534], [ ], [ ], None], #Mt Zozo Outside Single Chest Room
    254 : [[535, 536], [ ], [ ], None], #Mt Zozo Outside Cliff to Cyan's Cave
    255 : [[537, 538, 539], [ ], [ ], None], #Mt Zozo Inside First Room
    256 : [[540, 541], [ ], [ ], None], #Mt Zozo Inside Dragon Room
    257 : [[542, 543], [ ], [ ], None], #Mt Zozo Cyan's Cave
    258 : [[1204], [ ], [ ], None], #Mt Zozo Cyan's Cliff
    259 : [[544, 1205, 1206, 1207], [ ], [ ], None], #Coliseum Guy's House Outside
    260 : [[545], [ ], [ ], None], #Coliseum Guy's House Inside
    261 : [[1208], [ ], [ ], None], #Nikeah Docks
    262 : [[546, 547, 548, 549, 550, 551, 1209, 1210], [ ], [ ], None], #Kohlingen Outside WoB
    263 : [[552, 553, 554, 555, 556, 557, 1211, 1212], [ ], [ ], None], #Kohlingen Outside WoR
    264 : [[558], [ ], [ ], None], #Kohlingen Inn Inside
    265 : [[559, 560], [ ], [ ], None], #Kohlingen General Store Inside
    266 : [[561, 563], [ ], [ ], None], #Kohlingen Chemist's House Upstairs
    267 : [[562], [ ], [ ], None], #Kohlingen Chemist's House Downstairs
    268 : [[564], [ ], [ ], None], #Kohlingen Chemist's House Back Room
    269 : [[565], [ ], [ ], None], #Maranda Lola's House Inside
    270 : [[566], [ ], [ ], None], #Kohlingen Rachel's House Inside
    271 : [[567, 568, 569, 570, 571, 572, 573, 1216], [ ], [ ], None], #Jidoor Outside
    272 : [[574], [ ], [ ], None], #Jidoor Auction House
    273 : [[575], [ ], [ ], None], #Jidoor Item Shop
    274 : [[576], [ ], [ ], None], #Jidoor Relic
    275 : [[577], [ ], [ ], None], #Jidoor Armor
    276 : [[578], [ ], [ ], None], #Jidoor Weapon
    277 : [[1217], [ ], [ ], None], #Jidoor Chocobo Stable
    278 : [[579], [ ], [ ], None], #Jidoor Inn
    279 : [[580, 581], [ ], [ ], None], #Owzer's Behind Painting Room
    280 : [[582, 583, 585], [ ], [ ], None], #Owzer's Basement 1st Room
    281 : [[584], [ ], [ ], None], #Owzer's Basement Single Chest Room
    282 : [[586, 587], [ ], [ ], None], #Owzer's Basement Switching Door Room
    283 : [[588], [ ], [ ], None], #Owzer's Basement Behind Switching Door Room
    284 : [[589], [ ], [ ], None], #Owzer's Basement Save Point Room

    286 : [[591], [ ], [ ], None], #Owzer's Basement Chadarnook's Room
    287 : [[592, 593], [ ], [ ], None], #Owzer's House
    288 : [[1218, 1219, 1220, 1221, 1222, 1223], [ ], [ ], None], #Esper World Outside
    289 : [[594], [ ], [ ], None], #Esper World Gate
    290 : [[595], [ ], [ ], None], #Esper World Northwest House
    291 : [[596], [ ], [ ], None], #Esper World Far East House
    292 : [[597], [ ], [ ], None], #Esper World South Right House
    293 : [[598], [ ], [ ], None], #Esper World East House
    294 : [[599], [ ], [ ], None], #Esper World South Left House
    295 : [[600, 601, 602, 604, 608], [ ], [ ], None], #Zozo 1F Outside
    296 : [[603], [ ], [ ], None], #Zozo 2F Clock Room Balcony Outside
    297 : [[605], [ ], [ ], None], #Zozo 2F Cafe Balcony Outside
    298 : [[606, 607, 618], [ ], [ ], None], #Zozo Cafe Upstairs Outside
    299 : [[609, 610], [ ], [ ], None], #Zozo Relic 1st Section Outside
    300 : [[611, 612, 616], [ ], [ ], None], #Zozo Relic 2nd Section Outside
    301 : [[613, 617], [ ], [ ], None], #Zozo Relic 3rd Section Outside
    302 : [[614, 615, 619], [ ], [ ], None], #Zozo Relic 4th Section Outside
    303 : [[620, 621, 622], [ ], [ ], None], #Zozo Cafe
    304 : [[623, 624], [ ], [ ], None], #Zozo Relic 1st Room Inside
    305 : [[625, 626], [ ], [ ], None], #Zozo Relic 2nd Room Inside
    306 : [[627, 628], [ ], [ ], None], #Zozo West Tower Inside
    307 : [[629], [ ], [ ], None], #Zozo Armor
    308 : [[630], [ ], [ ], None], #Zozo Weapon
    309 : [[631], [ ], [ ], None], #Zozo Clock Puzzle Room West
    310 : [[632], [ ], [ ], None], #Zozo Clock Puzzle Room East
    311 : [[633], [ ], [ ], None], #Zozo Cafe Chest Room
    312 : [[634], [ ], [ ], None], #Zozo Tower 6F Chest Room
    313 : [[635, 636], [ ], [ ], None], #Zozo Tower Stairwell Room
    314 : [[637], [ ], [ ], None], #Zozo Tower 12F Chest Room
    315 : [[1225], [ ], [ ], None], #Zozo Tower Ramuh's Room
    316 : [[642, 643], [ ], [ ], None], #Opera House Balcony WoR and WoB Disruption
    317 : [[646, 647], [ ], [ ], None], #Opera House Catwalk Stairwell
    318 : [[648], [ ], [ ], None], #Opera House Switch Room
    319 : [[649, 650], [ ], [ ], None], #Opera House Balcony WoB
    320 : [[657], [ ], [ ], None], #Opera House Catwalks
    321 : [[659], [ ], [ ], None], #Opera House Lobby
    322 : [[662], [ ], [ ], None], #Opera House Dressing Room
    323 : [[1226], [ ], [ ], None], #Vector After Train Ride
    324 : [[1229], [ ], [ ], None], #Vector Outside
    325 : [[670], [ ], [ ], None], #Imperial Castle Entrance

    327 : [[671, 672, 673], [ ], [ ], None], #Imperial Castle Roof





    333 : [[674, 676, 678, 679, 680, 682, 684, 1230], [ ], [ ], None], #Imperial Castle Main Room
    334 : [[675], [ ], [ ], None], #Imperial Castle 2 Chest Room
    335 : [[677], [ ], [ ], None], #Imperial Castle Jail Cell
    336 : [[681, 688], [ ], [ ], None], #Imperial Castle 2F Bedroom Hallway
    337 : [[683, 693], [ ], [ ], None], #Imperial Castle Left Side Roof Stairwell
    338 : [[685, 694], [ ], [ ], None], #Imperial Castle Right Side Roof Stairwell

    340 : [[689, 690], [ ], [ ], None], #Imperial Castle Bedroom
    341 : [[691], [ ], [ ], None], #Imperial Castle Bedroom Bathroom
    342 : [[692], [ ], [ ], None], #Imperial Castle Toilet
    343 : [[1231], [ ], [ ], None], #Imperial Castle Top Room

    345 : [[695, 696], [ ], [ ], None], #Imperial Castle Barracks Room

    347 : [[702], [ ], [ ], None], #Magitek Factory Upper Room Platform From Lower Room
    348 : [[703], [ ], [ ], None], #Magitek Factory Upper Room
    349 : [[704], [ ], [ ], None], #Magitek Factory Lower Room

    351 : [[705, 706], [ ], [ ], None], #Magitek Factory Garbage Room

    353 : [[709, 710], [ ], [ ], None], #Magitek Factory Stairwell
    354 : [[711], [ ], [ ], None], #Magitek Factory Save Point Room
    355 : [[712, 713], [ ], [ ], None], #Magitek Factory Tube Hallway
    356 : [[714, 715], [ ], [ ], None], #Magitek Factory Number 024 Room
    357 : [[716], [ ], [ ], None], #Magitek Factory Esper Tube Room
    358 : [[717], [ ], [ ], None], #Zone Eater Entry Room
    359 : [[718, 719, 721], [ ], [ ], None], #Zone Eater Bridge Guards Room
    360 : [[720], [ ], [ ], None], #Zone Eater Pit
    361 : [[723], [ ], [ ], None], #Zone Eater Short Tunnel
    362 : [[724], [ ], [ ], None], #Zone Eater Gogo Room
    363 : [[725], [ ], [ ], None], #Zone Eater Save Point Room
    364 : [[727, 728], [ ], [ ], None], #Zone Eater Bridge Switch Room

    366 : [[729, 730, 731], [ ], [ ], None], #Umaro Cave 1st Room
    367 : [[732, 733], [ ], [ ], None], #Umaro Cave Bridge Room
    368 : [[734], [ ], [ ], None], #Umaro Cave Switch Room
    369 : [[735, 736, 737, 738], [ ], [ ], None], #Umaro Cave 2nd Room

    371 : [[739, 740, 741, 742], [ ], [ ], None], #Maranda Outside
    372 : [[743], [ ], [ ], None], #Doma 3F Outside
    373 : [[744], [ ], [ ], None], #Doma 1F Outside
    374 : [[745, 746], [ ], [ ], None], #Doma 2F Outside

    376 : [[750], [ ], [ ], None], #Maranda Inn
    377 : [[751], [ ], [ ], None], #Maranda Weapon Shop
    378 : [[752], [ ], [ ], None], #Maranda Armor Shop











    390 : [[1241, 1242], [ ], [ ], None], #Darill's Tomb Outside
    391 : [[771, 772], [ ], [ ], None], #Darill's Tomb Entry Room
    392 : [[773, 774, 776, 778, 780, 783], [ ], [ ], None], #Darill's Tomb Main Upstairs Room
    393 : [[775], [ ], [ ], None], #Darill's Tomb Left Side Tombstone Room
    394 : [[777, 786], [ ], [ ], None], #Darill's Tomb Right Side Tombstone Room
    395 : [[779, 785], [ ], [ ], None], #Darill's Tomb B2 Left Side Bottom Room

    397 : [[784], [ ], [ ], None], #Darill's Tomb B2 Right Side Bottom Room
    398 : [[787], [ ], [ ], None], #Darill's Tomb Right Side Secret Room
    399 : [[788], [ ], [ ], None], #Darill's Tomb B2 Graveyard
    400 : [[789], [ ], [ ], None], #Darill's Tomb Dullahan Room
    401 : [[790, 791], [ ], [ ], None], #Darills' Tomb B3
    402 : [[792], [ ], [ ], None], #Darills' Tomb B3 Water Level Switch Room
    403 : [[793, 794], [ ], [ ], None], #Darills' Tomb B2 Water Level Switch Room Left Side

    405 : [[797, 798], [ ], [ ], None], #Darill's Tomb MIAB Hallway


    408 : [[1243], [ ], [ ], None], #Tzen Outside WoR
    409 : [[1244], [ ], [ ], None], #Tzen Outside WoB





    415 : [[814, 815], [ ], [ ], None], #Tzen Collapsing House Downstairs
































    448 : [[865, 866], [ ], [ ], None], #Doma Dream Train Switch Puzzle Room Left Section
    449 : [[867], [ ], [ ], None], #Doma Dream Train Switch Puzzle Room
    450 : [[868, 869, 870, 871], [ ], [ ], None], #Doma Dream Train 1st Car
    451 : [[1245, 1246, 1247], [ ], [ ], None], #Albrook Outside WoB
    452 : [[1249, 1250, 1251], [ ], [ ], None], #Albrook Outside WoR






























    483 : [[922, 923, 924, 925, 926, 927, 928], [ ], [ ], None], #Thamasa After Kefka Outside WoB

    485 : [[1260, 1261], [ ], [ ], None], #Thamasa Outside WoR
    486 : [[950, 951], [ ], [ ], None], #Thamasa Arsenal
    487 : [[952], [ ], [ ], None], #Thamasa Inn
    488 : [[953], [ ], [ ], None], #Thamasa Item Shop
    489 : [[954], [ ], [ ], None], #Thamasa Elder's House
    490 : [[955, 956], [ ], [ ], None], #Strago's House First Floor
    491 : [[957], [ ], [ ], None], #Strago's House Second Floor
    492 : [[958], [ ], [ ], None], #Thamasa Relic
    493 : [[959], [ ], [ ], None], #Burning House Entry Room
    494 : [[960, 961, 962], [ ], [ ], None], #Burning House Second Room
    495 : [[963, 964], [ ], [ ], None], #Burning House Third Room
    496 : [[965, 966, 968], [ ], [ ], None], #Burning House Fourth Room
    497 : [[967, 970, 972], [ ], [ ], None], #Burning House Fifth Room
    498 : [[969], [ ], [ ], None], #Burning House 1st Chest Room
    499 : [[971], [ ], [ ], None], #Burning House 2nd Chest Room
    500 : [[973, 974], [ ], [ ], None], #Burning House Sixth Room
    501 : [[975], [ ], [ ], None], #Burning House Final Room

    503 : [[978, 979, 985], [ ], [ ], None], #Veldt Cave First Room
    504 : [[980], [ ], [ ], None], #Veldt Cave Second Room Dead End
    505 : [[981, 986], [ ], [ ], None], #Veldt Cave Bandit Room / Second Room
    506 : [[982, 983], [ ], [ ], None], #Veldt Cave Third Room
    507 : [[984, 987], [ ], [ ], None], #Veldt Cave Bandit Room / Second Room Lower Floor
    508 : [[988], [ ], [ ], None], #Veldt Cave Fourth Room Left Side
    509 : [[989], [ ], [ ], None], #Veldt Cave Fourth Room Right Side
    510 : [[990, 992], [ ], [ ], None], #Veldt Cave Fifth Room
    511 : [[991], [ ], [ ], None], #Veldt Cave Final Room










    522 : [[1010, 1011, 1012], [ ], [ ], None], #Fanatic's Tower 2nd Floor Outside
    523 : [[1013, 1014, 1015], [ ], [ ], None], #Fanatic's Tower 3rd Floor Outside
    524 : [[1016, 1017, 1018], [ ], [ ], None], #Fanatic's Tower 4th Floor Outside
    525 : [[1019, 1262], [ ], [ ], None], #Fanatic's Tower Bottom
    526 : [[1021, 1022, 1023], [ ], [ ], None], #Fanatic's Tower 1st Floor Outside
    527 : [[1024, 1025], [ ], [ ], None], #Fanatic's Tower Top
    528 : [[1026], [ ], [ ], None], #Fanatic's Tower 1st Floor Treasure Room
    529 : [[1027], [ ], [ ], None], #Fanatic's Tower Top Room
    530 : [[1028], [ ], [ ], None], #Fanatic's Tower 2nd Floor Treasure Room
    531 : [[1029], [ ], [ ], None], #Fanatic's Tower 3rd Floor Treasure Room
    532 : [[1030], [ ], [ ], None], #Fanatic's Tower 4th Floor Treasure Room
    533 : [[1031], [ ], [ ], None], #Fanatic's Tower 1st Floor Secret Room
    534 : [[1032, 1033], [ ], [ ], None], #Esper Mountain 3 Statues Room
    535 : [[1034, 1035, 1036], [ ], [ ], None], #Esper Mountain Outside Bridge Room
    536 : [[1037], [ ], [ ], None], #Esper Mountain Outside East Treasure Room
    537 : [[1038, 1039, 1040, 1041], [ ], [ ], None], #Esper Mountain Outside Path to Final Room
    538 : [[1042, 1043], [ ], [ ], None], #Esper Mountain Outside Statue Path
    539 : [[1044], [ ], [ ], None], #Esper Mountain Outside West Treasure Room
    540 : [[1045], [ ], [ ], None], #Esper Mountain Outside Northwest Treasure Room
    541 : [[1046, 1047, 1048, 1049], [ ], [ ], None], #Esper Mountain Inside First Room
    542 : [[1050, 1051], [ ], [ ], None], #Esper Mountain Inside Second Room South Section
    543 : [[1052], [ ], [ ], None], #Esper Mountain Falling Pit Room
    544 : [[1053, 1054], [ ], [ ], None], #Esper Mountain Inside Second Room West Section
    545 : [[1055], [ ], [ ], None], #Esper Mountain Inside Second Room East Section
    546 : [[1056], [ ], [ ], None], #Esper Mountain Inside Second Room North Section
    547 : [[1057], [ ], [ ], None], #Esper Mountain Inside Second Room Dead End
    548 : [[1058], [ ], [ ], None], #Imperial Base
    549 : [[1061, 1062], [ ], [ ], None], #Imperial Base House
    550 : [[1063], [ ], [ ], None], #Imperial Base House Basement
    551 : [[1064, 1065], [ ], [ ], None], #Cave to Sealed Gate Entry Room
    552 : [[1066, 1067], [ ], [ ], None], #Cave to Sealed Gate B1
    553 : [[1069, 1264], [ ], [ ], None], #Cave to Sealed Gate Last Room
    554 : [[1070], [ ], [ ], None], #Cave to Sealed Gate Main Room Last Section
    555 : [[1071, 1072], [ ], [ ], None], #Cave to Sealed Gate Main Room First Section
    556 : [[1073], [ ], [ ], None], #Cave to Sealed Gate Main Room Middle Section
    557 : [[1074], [ ], [ ], None], #Cave to Sealed Gate 4 Chest Room
    558 : [[1075, 1076, 1077], [ ], [ ], None], #Cave to Sealed Gate Lava Switch Room
    559 : [[1078], [ ], [ ], None], #Cave to Sealed Gate Save Point Room
    560 : [[1079], [ ], [ ], None], #Sealed Gate
    561 : [[1080, 1265, 1266, 1267, 1268, 1269, 1270], [ ], [ ], None], #Solitary Island House Outside
    562 : [[1081], [ ], [ ], None], #Solitary Island House Inside
    563 : [[1271], [ ], [ ], None], #Solitary Island Beach


    566 : [[1083, 1085, 1087], [ ], [ ], None], #Ancient Cave First Room
    567 : [[1084, 1086, 1088, 1274], [ ], [ ], None], #Ancient Cave Second Room
    568 : [[1089, 1275], [ ], [ ], None], #Ancient Cave Third Room
    569 : [[1090, 1091], [ ], [ ], None], #Ancient Cave Save Point Room
    570 : [[1092, 1093], [ ], [ ], None], #Ancient Castle West Side South Room
    571 : [[1094], [ ], [ ], None], #Ancient Castle East Side Single Chest Room
    572 : [[1095], [ ], [ ], None], #Ancient Castle West Side North Room
    573 : [[1096], [ ], [ ], None], #Ancient Castle East Side 2 Chest Room
    574 : [[1098, 1099, 1100, 1278], [ ], [ ], None], #Ancient Castle Throne Room
    575 : [[1276, 1277], [ ], [ ], None], #Ancient Castle Entry Room
    576 : [[1101, 1102, 1103, 1104, 1279], [ ], [ ], None], #Ancient Castle Outside
    577 : [[1105, 1106], [ ], [ ], None], #Ancient Castle Eastern Basement
    578 : [[1107], [ ], [ ], None], #Ancient Castle Dragon Room










    589 : [[1125, 1126, 1280], [ ], [ ], None], #Coliseum Main Room
    590 : [[1127], [ ], [ ], None], #Coliseum Left Room
    591 : [[1128], [ ], [ ], None], #Coliseum Inn


##    '38a' : [ [145, 146], [ ], [3009], None], #Narshe Northern Mines 2nd/3rd Floor Outside WoR incl. exit from Umaro's cave
##    '42a' : [ [1150], [2010], [], None], # Narshe Peak WoR incl. entrance to Umaro's cave
##    '355a' : [ [], [2028], [3027], None],  # Magitek Factory Minecart Room
##    '369a' : [ [735], [2007], [ ], None], #Umaro Cave 2nd Room - west
##    '369b' : [ [736, 738], [2006, 2008], [ ], None], #Umaro Cave 2nd Room - middle
##    '369c' : [ [737], [2005], [ ], None], #Umaro Cave 2nd Room - east
    #'504a' : [ [41, 43], [], [], 0],  # WOB Imperial Base / Cave to Sealed Gate connector


}

# Lists of exits that must be connected
forced_connections = {
    2011 : [3011],   # Esper Mountain Inside 2nd Room: North-to-South bridge jump West
    2012 : [3012],   #      North-to-South bridge jump Mid
    2013 : [3013],   #      North-to-South bridge jump East

    2023 : [3023],   # Magitek factory elevator in Room 1

    2029 : [3029],   # Cave to the Sealed Gate, grand staircase
    2030 : [3030],   # Cave to the Sealed Gate, switch bridges
    1079 : [1264]   # Cave to the Sealed Gate, actual Sealed Gate (must be connected to enable shortcut exit)
}

# Add forced connections for virtual doors (-dra)
#if 'root' in room_data.keys():
#    for i in range(8000, 8000+len(room_data['root'][0])):
#        forced_connections[i] = [i+1000]

# List of one-ways that must have the same destination
shared_oneways = {
    2005: [2006],  # Umaro's cave room 2: east trapdoor (shared exit)
    2006: [2005],  # Umaro's cave room 2: east trapdoor (shared exit)
    2007: [2008],  # Umaro's cave room 2: west trapdoor (shared exit)
    2008: [2007],  # Umaro's cave room 2: west trapdoor (shared exit)

    2017: [2018],   # Owzer's Mansion switching doors (same destination)
    2018: [2017],    # Owzer's Mansion switching doors (same destination)

}

# Lists of doors that have a shared destination. key_doorID : [doorIDs that share destination]
shared_exits = {
    #1034 : [1035],  # Esper Mountain outside bridge, left door
    #1038 : [1039],  # Esper Mountain Outside Path to Final Room East Door
    #1040 : [1041],  # Esper Mountain Outside Path to Final Room West Door

    1229 : [1226],  # Post-minecart Vector long exit to MTek.  Same destination as normal Vector exit to MTek.

    0: [1, 2, 3],   # Dragon's Eye Chocobo Stable WoB
    6: [7, 8, 9],   # South Figaro Top Tile WoB
    16: [17],   # Nikeah Left Tile WoB
    18: [19],   # Doma Left Tile WoB
    21: [22],   # Phantom Forest South Entrance Left Tile
    24: [25],   # Kohlingen Left Tile WoB
    28: [29, 30],   # Jidoor Top Tile WoB
    31: [32],   # Maranda Top Tile WoB
    33: [34],   # Tzen Left Tile WoB
    35: [36],   # Albrook Left Tile WoB
    37: [38, 39],   # Zozo Left Tile WoB
    45: [46, 47],   # Mobliz Chocobo Stable WoR
    49: [50],   # Albrook Left Tile WoR
    54: [55],   # Nikeah Left Tile WoR
    59: [60],   # Kohlingen Left Tile WoR
    63: [64],   # Maranda Left Tile WoR
    65: [66],   # Nikeah Left Tile WoR
    70: [71, 72],   # Zozo Top Left Tile WoR
    73: [74],   # Jidoor Left Tile WoR
    76: [77],   # Doma Left Tile WoR
    1162: [1163, 1164],   # South Figaro West to World Map WoR
    1167: [1168],   # South Figaro West to World Map WoB
    364: [365],   # Mt. Kolts 1F Outside West Door Left Tile
    387: [388],   # Mt. Kolts Back Side Middle Door Left Tile
    1186: [457],   # Duncan's House Outside WoR
    484: [485],   # Doma Dream Train 2nd Car West Top Tile
    486: [487],   # Doma Dream Train 2nd Car East Top Tile
    489: [490],   # Phantom Train Inside Dining Room West Bottom Tile
    491: [492],   # Phantom Train Inside Dining Room East Bottom Tile
    493: [494],   # Phantom Train Inside Front Cars Far Right Car West Top Tile
    496: [498],   # Phantom Train Inside Caboose West Top Tile
    497: [499],   # Phantom Train Inside Caboose East Top Tile
    1190: [1191],   # Mobliz South to World Map WoB
    1192: [1193],   # Mobliz East to World Map WoR
    531: [532],   # Mt Zozo Outside Bridge West Door Left Tile
    1205: [1206, 1207],   # Coliseum Guy's House South to World Map
    1209: [1210],   # Kohlingen South to World Map WoB
    1211: [1212],   # Kohlingen South to World Map WoR
    1213: [1214, 1215],   # Jidoor South to World Map
    1238: [1239],   # Maranda South to World Map
    860: [861],   # Doma Dream Cliffs Outside Final Room Top Tile
    865: [866],   # Doma Dream Train Switch Puzzle Room West Door Top Tile
    868: [869],   # Doma Dream Train 1st Train Car West Door Top Tile
    870: [871],   # Doma Dream Train 1st Train Car East Door Top Tile
    1245: [1246, 1247],   # Albrook West to World Map WoB
    1249: [1250, 1251],   # Albrook West to World Map WoR
    1253: [1254, 1255],   # Thamasa After Kefka North to World Map WoB
    1256: [1257, 1258],   # Thamasa North to World Map WoB
    1260: [1261],   # Thamasa West to World Map WoR
    960: [961],   # Burning House Second Room South Door Left Tile
    1034: [1035],   # Esper Mountain Outside Bridge Room West Door Left Tile
    1038: [1039],   # Esper Mountain Outside Path to Final Room East Door Left Tile
    1040: [1041],   # Esper Mountain Outside Path to Final Room West Door Left Tile
    1059: [1060],   # Imperial Base West to World Map Top Tile
    1075 : [1076],   # Cave to Sealed Gate Lava Switch Room North
    1266: [1267, 1268, 1269, 1270],   # Cid's House East to World Map

}

# List of doors that CANNOT be connected to each other.  Only rare instances.
invalid_connections = {
    702 : [703],  # Magitek factory room 1: entrance & platform door
    703 : [702]
}

# List of rooms that should have a forced update to Parent Map variable when entering.
# force_update_parent_map[roomID] = [x, y, mapID]
force_update_parent_map = {
    '285a' : [1, 34, 157]  # Entering WoR Jidoor from Owzer's Basement
}
