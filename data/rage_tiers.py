### Used as part of a tiering system for initial Rages
### Tiers pulled from https://docs.google.com/spreadsheets/d/1EjxzHbzouz7YHHlHvh0d1cofkCugURNgAGXIUnBhjuc/edit#gid=686849456
rage_tiers = [
    [24,37,51],
    [37,142,85],
    [51,7,254],
    [212,111,86,249],
    [142,245,250],
    [85,137,74,188,89,177,180,198,83,155,174,179,185,39,5,36,105,106,189,114,128,49,143,11,108,201,239,104,213,3],
    [76,176,10,109,220,221,127,132,117,149,81,32,224,160,61,147,154,187,71,97,126,100,103,210,16],
    [7,43,129,216,236,170,156,181,191,62,200],
    [254,101,211,30,31,58,228,6,50,53,165,183,13,166,9,102,195,38,226,99,112,133,241,252,15,197,34,88,18,223,0,23,25,26,46,57,92,94,113,115,121,123,150,244,248,178,70,79,8,90,107,47,141,208,2,229,247,234,134,82,96,163,125,199,240,93,124,148,232],
    [55,22,27,122,206,17,40,60,84,153,116,130,171,56,14,196,203,87,161,253,120,192,167,1,182,207,69,6,65,110,169,205,12,45,215,6,118,52,72,146,164,218,4,80,21,48,217,139,6,20,44,138,173,186,19,41,54,73,144,225,235,238,151,131,172,242,251,194,35,95,42,136,230,193,140,233,59,75,152,184,68,33,91,158,66,67,157,159,227,63,145,246,64,204,202,77,222,78,219,237,209,98,168],
]
weights = [0.005, 0.005, 0.015, 0.03, 0.085, 0.09, 0.1, 0.12, 0.25, 0.3]

# Stray Cat | S+ | 24
# Doom Drgn | S+ | 37
# Nightshade | S+ | 51
# Prussian | S | 212
# Luridan | S | 142
# Magic Urn | S | 85
# Cactrot | A+ | 76
# Retainer | A+ | 7
# Io | A+ | 254
# Siegfried | A | 55
# PowerDemon | A | 111
# Mover | A | 86
# Didalos | A | 249
# Barb-e | B+ | 190
# Gold Bear | B+ | 245
# Woolly | B+ | 250
# Sprinter | B | 135
# Harpiai | B | 137
# Brainpan | B | 74
# Phase | B | 188
# Aspik | B | 89
# Parasite | B | 177
# Anemone | B | 180
# Ceritops | B | 198
# HadesGigas | B | 83
# Land Worm | B | 155
# Gigantos | B | 174
# Coelecite | B | 179
# Latimeria | B | 185
# Tyranosaur | B | 39
# Orog | B | 5
# White Drgn | B | 36
# Warlock | B | 105
# Madam | B | 106
# Outsider | B | 189
# Peepers | B | 114
# Vectaur | B | 128
# Gilomantis | B | 49
# Toe Cutter | B | 143
# Brawler | B | 11
# Iron Fist | B | 108
# Poppers | B | 201
# 1st Class | B | 239
# Ogor | B | 104
# Black Drgn | B | 213
# Ninja | B | 3
# Wild Cat | C | 119
# Spek Tor | C | 176
# Rain Man | C | 10
# Goblin | C | 109
# Karkass | C | 220
# Punisher | C | 221
# SrBehemoth | C | 127
# Brontaur | C | 132
# Rhinox | C | 117
# Sky Cap | C | 149
# Boxed Set | C | 81
# Behemoth | C | 32
# GtBehemoth | C | 224
# Chaser | C | 160
# ChickenLip | C | 61
# Uroburos | C | 147
# Cluck | C | 154
# Allo Ver | C | 187
# Flan | C | 71
# Mad Oscar | C | 97
# Rhyos | C | 126
# Marshal | C | 100
# Covert | C | 103
# Mantodea | C | 210
# Osteosaur | C | 16
# Baskervor | C- | 29
# Harpy | C- | 43
# Wyvern | C- | 129
# Wirey Drgn | C- | 216
# Aquila | C- | 236
# Grenade | C- | 170
# Test Rider | C- | 156
# Hipocampus | C- | 181
# Parasoul | C- | 191
# Hoover | C- | 62
# Opinicus | C- | 200
# Fidor | D | 28
# Trooper | D | 101
# Bogy | D | 211
# Suriander | D | 30
# Chimera | D | 31
# Anguiform | D | 58
# Vectagoyle | D | 228
# Mag Roader | D | 6
# Trilium | D | 50
# Bloompire | D | 53
# Eland | D | 165
# Evil Oscar | D | 183
# Dark Force | D | 13
# Enuo | D | 166
# Dahling | D | 9
# General | D | 102
# Nohrabbit | D | 195
# Brachosaur | D | 38
# Chaos Drgn | D | 226
# Bleary | D | 99
# Displayer | D | 112
# Allosaurus | D | 133
# Necromancr | D | 241
# Sky Base | D | 252
# Over-Mind | D | 15
# Scrapper | D | 197
# Pterodon | D | 34
# Buffalax | D | 88
# Rhodox | D | 18
# Gabbldegak | D | 223
# Guard | D | 0
# Leafer | D | 23
# Lobo | D | 25
# Doberman | D | 26
# Hornet | D | 46
# Exocite | D | 57
# Sand Ray | D | 92
# Actaneon | D | 94
# Vector Pup | D | 113
# Sewer Rat | D | 115
# Bounty Man | D | 121
# Ralph | D | 123
# Cephaler | D | 150
# Wild Rat | D | 244
# Red Wolf | D | 248
# EarthGuard | D | 178
# Vaporite | D | 70
# Bomb | D | 79
# Hazer | D | 8
# Ghost | D | 90
# Joker | D | 107
# CrassHoppr | D | 47
# WeedFeeder | D | 141
# Insecare | D | 208
# Templar | D | 2
# Lich | D | 229
# Trixter | D | 247
# Fortis | D | 234
# Cirpius | D | 134
# SlamDancer | D | 82
# Dark Side | D | 96
# Intangir | D | 163
# Wart Puck | D | 125
# Commando | D | 199
# Tap Dancer | D | 240
# Areneid | D | 93
# Chitonid | D | 124
# Primordite | D | 148
# Bug | D | 232
# Adamanchyt | F | 214
# Steroidite | F | 22
# Vomammoth | F | 27
# Tusker | F | 122
# Nastidon | F | 206
# Commander | F | 17
# Dark Wind | F | 40
# Lizard | F | 60
# Pug | F | 84
# Geckorex | F | 153
# Slatter | F | 116
# Zombone | F | 130
# Critic | F | 171
# Nautiloid | F | 56
# Whisper | F | 14
# Wizard | F | 196
# Garm | F | 203
# Figaliz | F | 87
# Scullion | F | 161
# IronHitman | F | 253
# Red Fang | F | 120
# Pm Stalker | F | 192
# Deep Eye | F | 167
# Soldier | F | 1
# Spectre | F | 182
# Rinn | F | 207
# Lethal Wpn | F | 69
# Mag Roader | F | 6
# Pipsqueak | F | 65
# Apparite | F | 110
# NeckHunter | F | 169
# Kiwok | F | 205
# Apokryphos | F | 12
# Trapper | F | 45
# Dante | F | 215
# Mag Roader | F | 6
# Rhobite | F | 118
# TumbleWeed | F | 52
# Ing | F | 72
# Crusher | F | 146
# Misfit | F | 164
# Psychot | F | 218
# Samurai | F | 4
# Still Life | F | 80
# Rhinotaur | F | 21
# Delta Bug | F | 48
# Dueller | F | 217
# Drop | F | 139
# Mag Roader | F | 6
# Ursus | F | 20
# HermitCrab | F | 44
# GloomShell | F | 138
# SoulDancer | F | 173
# StillGoing | F | 186
# Were-Rat | F | 19
# Beakor | F | 41
# Trilobiter | F | 54
# Humpty | F | 73
# Over Grunk | F | 144
# Scorpion | F | 225
# Abolisher | F | 235
# Mandrake | F | 238
# Maliga | F | 151
# Dragon | F | 131
# Pan Dora | F | 172
# Borras | F | 242
# Veteran | F | 251
# Sp Forces | F | 194
# FossilFang | F | 35
# Sand Horse | F | 95
# Vulture | F | 42
# Gobbler | F | 136
# Osprey | F | 230
# Hemophyte | F | 193
# Mind Candy | F | 140
# Sea Flower | F | 233
# Reach Frog | F | 59
# Cruller | F | 75
# Gigan Toad | F | 152
# Slurm | F | 184
# Telstar | F | 68
# Mesosaur | F | 33
# Crawler | F | 91
# Tomb Thumb | F | 158
# M-TekArmor | F | 66
# Sky Armor | F | 67
# PlutoArmor | F | 157
# HeavyArmor | F | 159
# Spit Fire | F | 227
# Rider | F | 63
# Exoray | F | 145
# Innoc | F | 246
# Chupon | F | 64
# Vindr | F | 204
# Lunaris | F | 202
# Repo Man | F | 77
# Balloon | F | 222
# Harvester | F | 78
# Muus | F | 219
# Junk | F | 237
# Vermin | F | 209
# Crawly | F | 98
# GreaseMonk | F | 168
# Poplium | F | 162
