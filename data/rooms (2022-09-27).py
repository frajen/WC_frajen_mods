#rooms - series of doors
room_data = {
    2 : [81], #Blackjack Outside
    3 : [82, 83], #Blackjack Gambling Room
    4 : [84, 85, 87], #Blackjack Party Room
    5 : [86], #Blackjack Shop Room
    6 : [88, 89], #Blackjack Engine Room
    7 : [90], #Blackjack Parlor Room
    8 : [91], #Falcon Outside
    9 : [92, 93, 95], #Falcon Main Room
    10 : [94], #Falcon Small Room
    11 : [96], #Falcon Engine Room
    12 : [1129], #Chocobo Stable Exterior WoB
    13 : [1131], #Chocobo Stable Interior
    14 : [1132], #Chocobo Stable Exterior WoR

    16 : [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 108, 112, 1135, 1136], #Narshe Outside WoB
    17 : [107, 111], #Narshe Outside Behind Arvis to Mines WoB
    18 : [109, 110], #Narshe South Caves Secret Passage Outside WoB
    19 : [113, 114], #Narshe Northern Mines 2nd/3rd Floor Outside WoB
    20 : [115, 1139], #Narshe Northern Mines 3rd Floor Outside WoB
    21 : [1137, 1138], #Narshe Northern Mines 1st Floor Outside WoB
    22 : [1140, 1141], #Snow Battlefield WoB
    23 : [1142], #Narshe Peak WoB
    24 : [116, 117], #Narshe Weapon Shop
    25 : [118], #Narshe Weapon Shop Back Room
    26 : [119, 120], #Narshe Armor Shop
    27 : [121], #Narshe Item Shop
    28 : [122], #Narshe Relic Shop
    29 : [123], #Narshe Inn
    30 : [124, 125], #Narshe Arvis House
    31 : [126], #Narshe Elder House
    32 : [127], #Narshe Cursed Shld House
    33 : [128], #Narshe Treasure Room
    34 : [129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 140, 144, 1143, 1144], #Narshe Outside WoR
    35 : [139, 143], #Narshe Outside Behind Arvis to Mines WoR
    36 : [141, 142], #Narshe South Caves Secret Passage Outside WoR
    37 : [145, 146], #Narshe Northern Mines 2nd/3rd Floor Outside WoR
    38 : [147, 1147], #Narshe Northern Mines 3rd Floor Outside WoR
    39 : [1145, 1146], #Narshe Northern Mines 1st Floor Outside WoR
    40 : [1148, 1149], #Snow Battlefield WoR
    41 : [1150], #Narshe Peak WoR
    42 : [148, 149], #Narshe Northern Mines 1F Side/East Room WoR
    43 : [150, 151], #Narshe Northern Mines 2F Inside WoR
    44 : [152, 153], #Narshe Northern Mines 3F Inside WoR
    45 : [154, 155], #Narshe South Caves Secret Passage 1F WoR
    46 : [156, 157, 1151], #Narshe Northern Mines Main Hallway WoR
    47 : [158], #Narshe Northern Mines Tritoch Room WoR
    48 : [159, 160], #Narshe 3-Party Cave WoR
    49 : [161, 162, 163, 164], #Narshe South Caves WoR
    50 : [165, 166], #Narshe Checkpoint Room WoR
    51 : [167, 168], #Narshe South Caves Secret Passage 3F WoR

    53 : [169, 170], #Narshe Northern Mines Side Room 1F WoB
    54 : [171, 172], #Narshe Northern Mines Side Room 2F WoB
    55 : [173, 174], #Narshe Northern Mines Inside 3F WoB
    56 : [175, 176], #Narshe South Caves Secret Passage 1F WoB


    59 : [178, 179, 1155], #Narshe Northern Mines Main Hallway WoB
    60 : [180], #Narshe Northern Mines Tritoch Room WoB
    61 : [181, 182], #Narshe Moogle Cave WoR
    62 : [183, 184], #Narshe South Caves Secret Passage 3F WoB
    63 : [185, 186], #Narshe Checkpoint Room WoB
    64 : [187, 188, 189, 190], #Narshe South Caves WoB
    65 : [191, 192], #Narshe 3-Party Cave WoB
    66 : [193, 194], #Narshe Moogle Cave WoB
    67 : [195], #Cave to South Figaro Siegfried Tunnel
    68 : [197], #Figaro Castle Entrance
    69 : [198, 199, 201, 204], #Figaro Castle Outside Courtyard
    70 : [200], #Figaro Castle Center Tower Outside
    71 : [202, 205, 207, 208], #Figaro Castle Desert Outside
    72 : [203], #Figaro Castle West Tower Outside
    73 : [206], #Figaro Castle East Tower Outside
    74 : [209, 210], #Figaro Castle King's Bedroom
    75 : [1160], #Figaro Castle Throne Room
    76 : [211, 212, 213, 214], #Figaro Castle Foyer
    77 : [215, 216, 217, 218, 219, 220], #Figaro Castle Main Hallway
    78 : [221, 222, 223], #Figaro Castle Behind Throne Room
    79 : [224, 225], #Figaro Castle East Bedroom
    80 : [226, 227], #Figaro Castle Inn
    81 : [228], #Figaro Castle West Shop
    82 : [229], #Figaro Castle East Shop
    83 : [230, 231], #Figaro Castle Below Inn
    84 : [232, 233], #Figaro Castle Below Library
    85 : [234, 235], #Figaro Castle Library
    86 : [236, 238], #Figaro Castle Switch Room
    87 : [237], #Figaro Castle Prison
    88 : [239, 240], #Figaro Castle B1 Hallway East
    89 : [241, 242], #Figaro Castle B1 Hallway West
    90 : [243, 244], #Figaro Castle B2 Hallway
    91 : [245, 247], #Figaro Castle B2 East Hallway
    92 : [246, 248], #Figaro Castle B2 West Hallway
    93 : [249, 250, 251], #Figaro Castle B2 4 Chest Room
    94 : [252, 253], #Figaro Castle Engine Room
    95 : [254], #Figaro Castle Treasure Room Behind Engine Room
    96 : [255], #Figaro Castle B1 Single Chest Room
    97 : [256, 257], #Cave to South Figaro Small Hallway WoR
    98 : [258, 259, 260], #Cave to South Figaro Big Room WoR
    99 : [261, 262], #Cave to South Figaro South Entrance WoR
    100 : [263, 264], #Cave to South Figaro Small Hallway WoB
    101 : [265, 266, 267], #Cave to South Figaro Big Room WoB
    102 : [268], #Cave to South Figaro South Entrance WoB
    103 : [270], #Cave to South Figaro Single Chest Room WoB
    104 : [271], #Cave to South Figaro Turtle Room WoB
    105 : [1161], #Cave to South Figaro Outside WoB
    106 : [283, 286, 287, 288, 289, 290, 291, 292, 293, 294, 1165, 1166], #South Figaro Outside WoR
    107 : [284, 285], #South Figaro Rich Man's House Side Outside WoR
    108 : [295, 299, 300, 301, 302, 303, 304, 305, 306, 1170, 1171], #South Figaro Outside WoB
    109 : [296, 297], #South Figaro Rich Man's House Side Outside WoB
    110 : [298], #South Figaro East Side

    112 : [307, 308], #South Figaro Relics
    113 : [309, 310], #South Figaro Inn
    114 : [311, 312], #South Figaro Armory
    115 : [313, 314, 316], #South Figaro Pub
    116 : [315], #South Figaro Pub Basement
    117 : [1172], #South Figaro Chocobo Stable
    118 : [317, 318, 319], #South Figaro Rich Man's House 1F
    119 : [320, 321, 324], #South Figaro Rich Man's House 2F Hallway
    120 : [322, 325], #South Figaro Rich Man's Master Bedroom
    121 : [323], #South Figaro Rich Man's House Kids' Room
    122 : [326, 327], #South Figaro Rich Man's House Bedroom Secret Stairwell
    123 : [328, 329, 331, 332, 333], #South Figaro Rich Man's House B1
    124 : [330], #South Figaro Celes Cell
    125 : [334, 335], #South Figaro Clock Room
    126 : [336], #South Figaro Duncan's House Basement
    127 : [337], #South Figaro Item Shop
    128 : [338], #South Figaro Rich Man's House Secret Back Door Room
    129 : [346], #South Figaro Cider House Secret Room
    130 : [339, 344], #South Figaro Cider House Upstairs
    131 : [340, 343, 348], #South Figaro Cider House Downstairs
    132 : [341, 342], #South Figaro Behind Duncan's House
    133 : [345, 347], #South Figaro Duncan's House Upstairs
    134 : [349, 350, 351], #South Figaro Escape Tunnel
    135 : [352], #South Figaro Rich Man's House Save Point Room
    136 : [353], #South Figaro B2 3 Chest Room
    137 : [354], #South Figaro B2 2 Chest Room
    138 : [355], #Cave to South Figaro Single Chest Room WoR
    139 : [356], #Cave to South Figaro Turtle Room WoR
    140 : [357], #Cave to South Figaro Turtle Door WoR
    141 : [1173], #South Figaro Docks
    142 : [358, 359], #Cave to South Figaro Behind Turtle
    143 : [361], #Sabin's House Outside
    144 : [362], #Sabin's House Inside
    145 : [363, 1175], #Mt. Kolts South Entrance
    146 : [364, 365, 366], #Mt. Kolts 1F Outside
    147 : [367], #Mt Kolts Outside Chest 1 Room
    148 : [368, 1176], #Mt Kolts Outside Cliff West
    149 : [369], #Mt Kolts Outside Chest 2 Room
    150 : [370, 371], #Mt. Kolts Outside Bridge
    151 : [372, 373], #Mt. Kolts Vargas Spiral
    152 : [374, 375], #Mt. Kolts First Inside Room
    153 : [376, 377, 378, 385], #Mt. Kolts 4-Way Split Room
    154 : [379, 380], #Mt. Kolts 2F Inside Room
    155 : [381, 382], #Mt. Kolts Inside Bridges Room
    156 : [383, 384], #Mt. Kolts After Vargas Room
    157 : [386], #Mt Kolts Inside Chest Room
    158 : [1177, 1178], #Mt. Kolts North Exit
    159 : [387, 388, 389, 1179], #Mt. Kolts Back Side
    160 : [390, 391], #Mt. Kolts Save Point Room
    161 : [392, 393, 394, 395], #Narshe School Main Room
    162 : [396], #Narshe School Left Room
    163 : [397], #Narshe School Middle Room
    164 : [398], #Narshe School Right Room
    165 : [1180, 1181], #Returners Hideout Outside
    166 : [399, 400, 401, 402, 403], #Returners Hideout Main Room
    167 : [404], #Returners Hideout Back Room
    168 : [405, 406], #Returners Hideout Banon's Room
    169 : [407], #Returner's Hideout Bedroom
    170 : [408], #Returner's Hideout Inn
    171 : [409, 410], #Returner's Hideout Secret Passage
    172 : [1182], #Lete River Jumpoff
    173 : [411], #Crazy Old Man's House Outside WoB
    174 : [412], #Crazy Old Man's House Inside

    176 : [417, 432], #Doma 3F Inside
    177 : [418, 419, 422, 424, 425, 428, 430, 431, 433], #Doma Main Room
    178 : [420], #Doma 2F Treasure Room
    179 : [421], #Doma Right Side Bedroom
    180 : [423], #Doma Throne Room
    181 : [426], #Doma Left Side Bedroom
    182 : [427, 429], #Doma Inner Room
    183 : [434], #Doma Cyan's Room
    184 : [435], #Doma Dream 3F Outside
    185 : [436], #Doma Dream 1F Outside
    186 : [437, 438], #Doma Dream 2F Outside
    187 : [439, 453], #Doma Dream 3F Inside
    188 : [440, 441, 443, 444, 445, 446, 449, 451, 452, 454], #Doma Dream Main Room
    189 : [442], #Doma Dream Treasure Room
    190 : [447], #Doma Dream Side Bedroom
    191 : [448, 450], #Doma Dream Inner Room
    192 : [455], #Doma Dream Cyan's Room
    193 : [456], #Doma Dream Throne Room
    194 : [458], #Duncan's House Outside
    195 : [459], #Duncan's House
    196 : [460], #Crazy Old Man's House WoR




    201 : [469], #Phantom Train Station
    202 : [470, 471, 472, 473], #Phantom Train Outside 4th Section

    204 : [474, 475, 476], #Phantom Train Outside 1st Section



    208 : [477, 483], #Doma Dream Train Outside 3rd Section
    209 : [478, 479, 480, 481], #Doma Dream Train Outside 2nd Section
    210 : [482], #Doma Dream Train Outside 1st Section
    211 : [484, 485, 486, 487], #Doma Dream Train 2nd Car

    213 : [488], #Phantom Train Caboose Inner Room

    215 : [489, 490, 491, 492], #Phantom Train Dining Room
    216 : [493, 494], #Phantom Train Seating Car with Switch Left Side



    220 : [496, 497, 498, 499, 500, 501], #Phantom Train Caboose
    221 : [502], #Phantom Train Final Save Point Room



    225 : [503], #Mobliz Kids' Hideaway
    226 : [504, 505], #Baren Falls Inside
    227 : [1189], #Baren Falls Cliff
    228 : [506, 507, 508, 512, 1190, 1191], #Mobliz Outside WoB
    229 : [1192, 1193], #Mobliz Outside WoR

    231 : [516], #Mobliz Inn
    232 : [517, 518], #Mobliz Arsenal

    234 : [519], #Mobliz Mail Room Upstairs
    235 : [520], #Mobliz Item Shop
    236 : [521], #Mobliz Mail Room Basement WoB


    239 : [1196, 1197], #Baren Falls Outside
    240 : [523, 524], #Crescent Mountain
    241 : [1198], #Serpent Trench Cliff
    242 : [525, 526, 1199, 1200, 1201, 1202], #Nikeah Outside WoB
    243 : [527], #Nikeah Inn
    244 : [528], #Nikeah Pub
    245 : [1203], #Nikeah Chocobo Stable
    246 : [529], #Serpent Trench Cave 2nd Part 1st Room
    247 : [530], #Serpent Trench Cave 2nd Part 2nd Room


    250 : [531, 532, 533], #Mt Zozo Outside Bridge
    251 : [534], #Mt Zozo Outside Single Chest Room
    252 : [535, 536], #Mt Zozo Outside Cliff to Cyan's Cave
    253 : [537, 538, 539], #Mt Zozo Inside First Room
    254 : [540, 541], #Mt Zozo Inside Dragon Room
    255 : [542, 543], #Mt Zozo Cyan's Cave
    256 : [1204], #Mt Zozo Cyan's Cliff
    257 : [544, 1205, 1206, 1207], #Coliseum Guy's House Outside
    258 : [545], #Coliseum Guy's House Inside
    259 : [1208], #Nikeah Docks
    260 : [546, 547, 548, 549, 550, 551, 1209, 1210], #Kohlingen Outside WoB
    261 : [552, 553, 554, 555, 556, 557, 1211, 1212], #Kohlingen Outside WoR
    262 : [558], #Kohlingen Inn Inside
    263 : [559, 560], #Kohlingen General Store Inside
    264 : [561, 563], #Kohlingen Chemist's House Upstairs
    265 : [562], #Kohlingen Chemist's House Downstairs
    266 : [564], #Kohlingen Chemist's House Back Room
    267 : [565], #Maranda Lola's House Inside
    268 : [566], #Kohlingen Rachel's House Inside
    269 : [567, 568, 569, 570, 571, 572, 573, 1213, 1214, 1215, 1216], #Jidoor Outside
    270 : [574], #Jidoor Auction House
    271 : [575], #Jidoor Item Shop
    272 : [576], #Jidoor Relic
    273 : [577], #Jidoor Armor
    274 : [578], #Jidoor Weapon
    275 : [1217], #Jidoor Chocobo Stable
    276 : [579], #Jidoor Inn
    277 : [580, 581], #Owzer's Behind Painting Room
    278 : [582, 583, 585], #Owzer's Basement 1st Room
    279 : [584], #Owzer's Basement Single Chest Room
    280 : [586, 587], #Owzer's Basement Switching Door Room
    281 : [588], #Owzer's Basement Behind Switching Door Room
    282 : [589], #Owzer's Basement Save Point Room

    284 : [591], #Owzer's Basement Chadarnook's Room
    285 : [592, 593], #Owzer's House
    286 : [1218, 1219, 1220, 1221, 1222, 1223], #Esper World Outside
    287 : [594], #Esper World Gate
    288 : [595], #Esper World Northwest House
    289 : [596], #Esper World Far East House
    290 : [597], #Esper World South Right House
    291 : [598], #Esper World East House
    292 : [599], #Esper World South Left House
    293 : [600, 601, 602, 604, 608, 1224], #Zozo 1F Outside
    294 : [603], #Zozo 2F Clock Room Balcony Outside
    295 : [605], #Zozo 2F Cafe Balcony Outside
    296 : [606, 607, 618], #Zozo Cafe Upstairs Outside
    297 : [609, 610], #Zozo Relic 1st Section Outside
    298 : [611, 612, 616], #Zozo Relic 2nd Section Outside
    299 : [613, 617], #Zozo Relic 3rd Section Outside
    300 : [614, 615, 619], #Zozo Relic 4th Section Outside
    301 : [620, 621, 622], #Zozo Cafe
    302 : [623, 624], #Zozo Relic 1st Room Inside
    303 : [625, 626], #Zozo Relic 2nd Room Inside
    304 : [627, 628], #Zozo West Tower Inside
    305 : [629], #Zozo Armor
    306 : [630], #Zozo Weapon
    307 : [631], #Zozo Clock Puzzle Room West
    308 : [632], #Zozo Clock Puzzle Room East
    309 : [633], #Zozo Cafe Chest Room
    310 : [634], #Zozo Tower 6F Chest Room
    311 : [635, 636], #Zozo Tower Stairwell Room
    312 : [637], #Zozo Tower 12F Chest Room
    313 : [1225], #Zozo Tower Ramuh's Room
    314 : [642, 643], #Opera House Balcony WoR and WoB Disruption
    315 : [646, 647], #Opera House Catwalk Stairwell
    316 : [648], #Opera House Switch Room
    317 : [649, 650], #Opera House Balcony WoB
    318 : [657], #Opera House Catwalks
    319 : [658, 659], #Opera House Lobby
    320 : [662], #Opera House Dressing Room
    321 : [1226], #Vector After Train Ride
    322 : [1229], #Vector Outside
    323 : [670], #Imperial Castle Entrance

    325 : [671, 672, 673], #Imperial Castle Roof





    331 : [674, 676, 678, 679, 680, 682, 684, 1230], #Imperial Castle Main Room
    332 : [675], #Imperial Castle 2 Chest Room
    333 : [677], #Imperial Castle Jail Cell
    334 : [681, 688], #Imperial Castle 2F Bedroom Hallway
    335 : [683, 693], #Imperial Castle Left Side Roof Stairwell
    336 : [685, 694], #Imperial Castle Right Side Roof Stairwell

    338 : [689, 690], #Imperial Castle Bedroom
    339 : [691], #Imperial Castle Bedroom Bathroom
    340 : [692], #Imperial Castle Toilet
    341 : [1231], #Imperial Castle Top Room
    342 : [1233], #Imperial Castle Banquet Room
    343 : [695, 696], #Imperial Castle Barracks Room

    345 : [702], #Magitek Factory Upper Room Platform From Lower Room
    346 : [703], #Magitek Factory Upper Room
    347 : [704], #Magitek Factory Lower Room

    349 : [705, 706], #Magitek Factory Garbage Room

    351 : [709, 710], #Magitek Factory Stairwell
    352 : [711], #Magitek Factory Save Point Room
    353 : [712, 713], #Magitek Factory Tube Hallway
    354 : [714, 715], #Magitek Factory Number 024 Room
    355 : [716], #Magitek Factory Esper Tube Room
    356 : [717], #Zone Eater Entry Room
    357 : [718, 719, 721], #Zone Eater Bridge Guards Room
    358 : [720], #Zone Eater Pit
    359 : [723], #Zone Eater Short Tunnel
    360 : [724], #Zone Eater Gogo Room
    361 : [725], #Zone Eater Save Point Room
    362 : [727, 728], #Zone Eater Bridge Switch Room

    364 : [729, 730, 731], #Umaro Cave 1st Room
    365 : [732, 733], #Umaro Cave Bridge Room
    366 : [734], #Umaro Cave Switch Room
    367 : [735, 736, 737, 738], #Umaro Cave 2nd Room

    369 : [739, 740, 741, 742], #Maranda Outside
    370 : [743], #Doma 3F Outside
    371 : [744, 1240], #Doma 1F Outside
    372 : [745, 746], #Doma 2F Outside

    374 : [750], #Maranda Inn
    375 : [751], #Maranda Weapon Shop
    376 : [752], #Maranda Armor Shop
    377 : [1241], #Darill's Tomb Outside
    378 : [771, 772], #Darill's Tomb Entry Room
    379 : [773, 774, 776, 778, 780, 783], #Darill's Tomb Main Upstairs Room
    380 : [775], #Darill's Tomb Left Side Tombstone Room
    381 : [777, 786], #Darill's Tomb Right Side Tombstone Room
    382 : [779, 785], #Darill's Tomb B2 Left Side Bottom Room
    383 : [781, 782], #Darill's Tomb B2 Turtle Hallway
    384 : [784], #Darill's Tomb B2 Right Side Bottom Room
    385 : [787], #Darill's Tomb Right Side Secret Room
    386 : [788], #Darill's Tomb B2 Graveyard
    387 : [789], #Darill's Tomb Dullahan Room
    388 : [790, 791], #Darills' Tomb B3
    389 : [792], #Darills' Tomb B3 Water Level Switch Room
    390 : [793, 794], #Darills' Tomb B2 Water Level Switch Room Left Side


    393 : [797, 798], #Darill's Tomb MIAB Hallway







    401 : [814, 815], #Tzen Collapsing House Downstairs
































    434 : [865, 866], #Doma Dream Train Switch Puzzle Room Left Section
    435 : [867], #Doma Dream Train Switch Puzzle Room
    436 : [868, 869, 870, 871], #Doma Dream Train 1st Car










    447 : [922, 923, 924, 925, 926, 927, 928], #Thamasa After Kefka Outside WoB


    450 : [950, 951], #Thamasa Arsenal
    451 : [952], #Thamasa Inn
    452 : [953], #Thamasa Item Shop
    453 : [954], #Thamasa Elder's House
    454 : [955, 956], #Strago's House First Floor
    455 : [957], #Strago's House Second Floor
    456 : [958], #Thamasa Relic
    457 : [959], #Burning House Entry Room
    458 : [960, 961, 962], #Burning House Second Room
    459 : [963, 964], #Burning House Third Room
    460 : [965, 966, 968], #Burning House Fourth Room
    461 : [967, 970, 972], #Burning House Fifth Room
    462 : [969], #Burning House 1st Chest Room
    463 : [971], #Burning House 2nd Chest Room
    464 : [973, 974], #Burning House Sixth Room
    465 : [975], #Burning House Final Room

    467 : [979, 985], #Veldt Cave First Room
    468 : [980], #Veldt Cave Second Room Dead End
    469 : [981, 986], #Veldt Cave Bandit Room / Second Room
    470 : [982, 983], #Veldt Cave Third Room
    471 : [984, 987], #Veldt Cave Bandit Room / Second Room Lower Floor
    472 : [988], #Veldt Cave Fourth Room Left Side
    473 : [989], #Veldt Cave Fourth Room Right Side
    474 : [990, 992], #Veldt Cave Fifth Room
    475 : [991], #Veldt Cave Final Room
    476 : [1010, 1011, 1012], #Fanatic's Tower 2nd Floor Outside
    477 : [1013, 1014, 1015], #Fanatic's Tower 3rd Floor Outside
    478 : [1016, 1017, 1018], #Fanatic's Tower 4th Floor Outside
    479 : [1019], #Fanatic's Tower Bottom
    480 : [1020, 1021, 1022, 1023], #Fanatic's Tower 1st Floor Outside
    481 : [1024, 1025], #Fanatic's Tower Top
    482 : [1026], #Fanatic's Tower 1st Floor Treasure Room
    483 : [1027], #Fanatic's Tower Top Room
    484 : [1028], #Fanatic's Tower 2nd Floor Treasure Room
    485 : [1029], #Fanatic's Tower 3rd Floor Treasure Room
    486 : [1030], #Fanatic's Tower 4th Floor Treasure Room
    487 : [1031], #Fanatic's Tower 1st Floor Secret Room
    488 : [1032, 1033], #Esper Mountain 3 Statues Room
    489 : [1034, 1035, 1036], #Esper Mountain Outside Bridge Room
    490 : [1037], #Esper Mountain Outside East Treasure Room
    491 : [1038, 1039, 1040, 1041], #Esper Mountain Outside Path to Final Room
    492 : [1042, 1043], #Esper Mountain Outside Statue Path
    493 : [1044], #Esper Mountain Outside West Treasure Room
    494 : [1045], #Esper Mountain Outside Northwest Treasure Room
    495 : [1046, 1047, 1048, 1049], #Esper Mountain Inside First Room
    496 : [1050, 1051], #Esper Mountain Inside Second Room South Section
    497 : [1052], #Esper Mountain Falling Pit Room
    498 : [1053, 1054], #Esper Mountain Inside Second Room West Section
    499 : [1055], #Esper Mountain Inside Second Room East Section
    500 : [1056], #Esper Mountain Inside Second Room North Section
    501 : [1057], #Esper Mountain Inside Second Room Dead End
    502 : [1058], #Imperial Base
    503 : [1061, 1062], #Imperial Base House
    504 : [1063], #Imperial Base House Basement
    505 : [1065], #Cave to Sealed Gate Entry Room
    506 : [1066, 1067], #Cave to Sealed Gate B1
    507 : [1069, 1264], #Cave to Sealed Gate Last Room
    508 : [1070], #Cave to Sealed Gate Main Room Last Section
    509 : [1071, 1072], #Cave to Sealed Gate Main Room First Section
    510 : [1073], #Cave to Sealed Gate Main Room Middle Section
    511 : [1074], #Cave to Sealed Gate 4 Chest Room
    512 : [1075, 1076, 1077], #Cave to Sealed Gate Lava Switch Room
    513 : [1078], #Cave to Sealed Gate Save Point Room
    514 : [1079], #Sealed Gate
    515 : [1080, 1265, 1266, 1267, 1268, 1269, 1270], #Solitary Island House Outside
    516 : [1081], #Solitary Island House Inside
    517 : [1271], #Solitary Island Beach


    520 : [1083, 1085, 1087], #Ancient Cave First Room
    521 : [1084, 1086, 1088, 1274], #Ancient Cave Second Room
    522 : [1089, 1275], #Ancient Cave Third Room
    523 : [1090, 1091], #Ancient Cave Save Point Room
    524 : [1092, 1093], #Ancient Castle West Side South Room
    525 : [1094], #Ancient Castle East Side Single Chest Room
    526 : [1095], #Ancient Castle West Side North Room
    527 : [1096], #Ancient Castle East Side 2 Chest Room
    528 : [1098, 1099, 1100, 1278], #Ancient Castle Throne Room
    529 : [1276, 1277], #Ancient Castle Entry Room
    530 : [1101, 1102, 1103, 1104, 1279], #Ancient Castle Outside
    531 : [1105, 1106], #Ancient Castle Eastern Basement
    532 : [1107], #Ancient Castle Dragon Room
    533 : [1125, 1126, 1280], #Coliseum Main Room
    534 : [1127], #Coliseum Left Room


}
