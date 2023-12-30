from data.enemy import Enemy
from data.structures import DataArray

from data.enemy_formations import EnemyFormations
from data.enemy_packs import EnemyPacks
from data.enemy_zones import EnemyZones
from data.enemy_scripts import EnemyScripts
import data.bosses as bosses

### added for removing items from enemies
from data.item_names import name_id
import data.items as items
### added for removing items from enemies

class Enemies():
    DATA_START = 0xf0000
    DATA_END = 0xf2fff
    DATA_SIZE = 32

    NAMES_START = 0xfc050
    NAMES_END = 0xfd0cf
    NAME_SIZE = 10

    ITEMS_START = 0xf3000
    ITEMS_END = 0xf35ff
    ITEMS_SIZE = 4

    SPECIAL_NAMES_START = 0xfd0d0
    SPECIAL_NAMES_END = 0xfdfdf
    SPECIAL_NAMES_SIZE = 10

    DRAGON_COUNT = 8

    SRBEHEMOTH2_ID = 127
    INVINCIBLE_GUARDIAN_ID = 273

    #def __init__(self, rom, args, items):
    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.enemy_data = DataArray(self.rom, self.DATA_START, self.DATA_END, self.DATA_SIZE)
        self.enemy_name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.enemy_item_data = DataArray(self.rom, self.ITEMS_START, self.ITEMS_END, self.ITEMS_SIZE)
        self.enemy_special_name_data = DataArray(self.rom, self.SPECIAL_NAMES_START, self.SPECIAL_NAMES_END, self.SPECIAL_NAMES_SIZE)

        self.enemies = []
        self.bosses = []
        for enemy_index in range(len(self.enemy_data)):
            enemy = Enemy(enemy_index, self.enemy_data[enemy_index], self.enemy_name_data[enemy_index], self.enemy_item_data[enemy_index], self.enemy_special_name_data[enemy_index])
            self.enemies.append(enemy)

            if enemy_index in bosses.enemy_name and enemy_index not in bosses.removed_enemy_name:
                self.bosses.append(enemy)

        self.formations = EnemyFormations(self.rom, self.args, self)
        self.packs = EnemyPacks(self.rom, self.args, self.formations)
        self.zones = EnemyZones(self.rom, self.args)
        self.scripts = EnemyScripts(self.rom, self.args, self)

        if self.args.doom_gaze_no_escape:
            # if doom gaze cannot escape, do not allow the party to escape from doom gaze
            # this prevents escaping from doom gaze in a shuffled/random place and getting a free check
            doom_gaze_id = self.get_enemy("Doom Gaze")
            self.enemies[doom_gaze_id].no_run = 1


        ### Mod to randomize enemy drops/steals
        self.items = items #(use later)

        # build drop/steal lists
        # use a list if the desire is to randomize items with duplicates
        # use set() and remove 255's for unique items if desired
        self.rare_drops = []
        self.common_drops = []
        self.rare_steals = []
        self.common_steals = []
        for enemy in self.enemies:
            if enemy.name != "":
            #if enemy.drop_rare != 255:
                self.rare_drops.append(enemy.drop_rare)
            #if enemy.drop_common != 255:
                self.common_drops.append(enemy.drop_common)
            #if enemy.steal_rare != 255:
                self.rare_steals.append(enemy.steal_rare)
            #if enemy.steal_common != 255:
                self.common_steals.append(enemy.steal_common)
            # debug: print enemy steal/drop tables
##            print(enemy.steal_rare)
##            print(enemy.steal_common)
##            print(enemy.drop_rare)
##            print(enemy.drop_common)

        # drop/steal lists are now ready
        # debug: print full lists
##        print(self.rare_drops)
##        print(self.common_drops)
##        print(self.rare_steals)
##        print(self.common_steals)


    def __len__(self):
        return len(self.enemies)

    def get_random(self):
        import random
        random_enemy = random.choice(self.enemies[:255])
        return random_enemy.id

    def get_enemy(self, name):
        if name in bosses.name_enemy:
            return bosses.name_enemy[name]
        for enemy in self.enemies:
            if enemy.name == name:
                return enemy.id

    def get_name(self, enemy_id):
        if enemy_id in bosses.enemy_name:
            return bosses.enemy_name[enemy_id]
        return self.enemies[enemy_id].name

    def set_rare_steal(self, enemy_id, item_id):
        self.enemies[enemy_id].steal_rare = item_id

    def set_common_steal(self, enemy_id, item_id):
        self.enemies[enemy_id].steal_common = item_id

    def set_rare_drop(self, enemy_id, item_id):
        self.enemies[enemy_id].drop_rare = item_id

    def set_common_drop(self, enemy_id, item_id):
        self.enemies[enemy_id].drop_common = item_id

    ### Mods for drop and steal randomization ###

    # shuffle enemy drops within other enemies
##    def shuffle_drops(self, mix_rarity=True):
##        from data.item_names import id_name
##        total_common_drops = len(self.common_drops)
##        total_rare_drops = len(self.rare_drops)
##        import random
##        #random_percent = self.args.shop_inventory_shuffle_random_percent / 100.0
##        random_percent = 20 / 100.0
##        if mix_rarity:
##            num_total_drops = total_common_drops + total_rare_drops
##            total_drops = self.common_drops.append(self.rare_drops)
##            num_random_items = int(num_total_drops * random_percent)
##            sorted_random_indices = sorted(random.sample(range(num_total_drops), num_random_items), reverse = False)
##
##            print(num_total_drops)
##            #print(random_drops)
##            print(sorted_random_indices)
##            input("X")
##            x = 0
##            for enemy in self.enemies:
##                if enemy.name != "":
##                    if x in sorted_random_indices:
##                        print(x)
##                        new_item = self.items.get_random()
##                        if x % 2 == 0:
##                            print("rare set: " + str(id_name[new_item]) + " on " + str(enemy.name))
##                            self.set_rare_drop(enemy.id, new_item)
##                        else:
##                            print("common set: " + str(id_name[new_item]) + " on " + str(enemy.name))
##                            self.set_common_drop(enemy.id, new_item)
##
##                    #check it again
##                    x = x + 1
##                    if x in sorted_random_indices:
##                        print(x)
##                        new_item = self.items.get_random()
##                        if x % 2 == 0:
##                            print("rare set: " + str(id_name[new_item]) + " on " + str(enemy.name))
##                            self.set_rare_drop(enemy.id, new_item)
##                        else:
##                            print("common set: " + str(id_name[new_item]) + " on " + str(enemy.name))
##                            self.set_common_drop(enemy.id, new_item)
##                    x = x + 1


    # fully randomize drop tables with no regard to enemy or vanilla item
    def randomize_drops(self):
        import random
        for enemy in self.enemies:
            replacement = random.choice(self.items)
            self.set_common_drop(enemy.id, replacement)
            replacement = random.choice(self.items)
            self.set_rare_drop(enemy.id, replacement)

    # fully randomize steal tables with no regard to enemy or vanilla item
    def randomize_steals(self):
        import random
        for enemy in self.enemies:
            replacement = random.choice(self.items)
            self.set_common_steal(enemy.id, replacement)
            replacement = random.choice(self.items)
            self.set_rare_steal(enemy.id, replacement)

    # Options:
    # 1. Re-create BC's ranking system
    # 2. Use WC's shuffle+rand system
    # 3. Use WC's random tiered system
    # 1. Ranking system follows:
    # randomize steals/drops if enemy had an item in those slots in vanilla
    def randomize_steals_drops_ranked(self, chance_to_randomize=50, item_variance=8):
        from data.item_names import id_name
        from data.item_ranks import ranked_items     # pull in ranked item dictionary
        import random
        
        # turn items into a list so we can access indices directly
        itemindex = list(ranked_items.keys())  
        def get_new_index(enemy_item_id):
            # get the current item's index and generate a new index based on variance setting
            variant = random.randint(1, item_variance)
            # 50/50 chance to have a lower/higher ranking
            if random.randint(1, 2) == 1:
                variant = variant * -1
            base_index = itemindex.index(enemy_item_id)
            new_index = base_index + variant
            # make sure the item index isn't out of bounds
            if new_index < 0:
                new_index = 0 + random.randint(0, item_variance-1)
            elif new_index > 254:
                new_index = 254 - random.randint(0, item_variance-1)
            return itemindex[new_index]

        # loop through all enemies. if they had vanilla steals/drops, possibly randomize the item
        for enemy in self.enemies:
            if enemy.steal_common != 255 and random.randint(1,100) <= chance_to_randomize:
                original = enemy.steal_common
                replacement = get_new_index(enemy.steal_common)
                self.set_common_steal(enemy.id, replacement)
                # debug:
##                input("common steal " + str(id_name[original]) + " replaced with: " + str(id_name[replacement]))
            if enemy.steal_rare != 255 and random.randint(1,100) <= chance_to_randomize:
                original = enemy.steal_rare
                replacement = get_new_index(enemy.steal_rare)
                self.set_rare_steal(enemy.id, replacement)
                # debug:
##                input("rare steal " + str(id_name[original]) + " replaced with: " + str(id_name[replacement]))
            if enemy.drop_common != 255 and random.randint(1,100) <= chance_to_randomize:
                original = enemy.drop_common
                replacement = get_new_index(enemy.drop_common)
                self.set_common_drop(enemy.id, replacement)
                # debug:
##                input("common drop " + str(id_name[original]) + " replaced with: " + str(id_name[replacement]))
            if enemy.drop_rare != 255 and random.randint(1,100) <= chance_to_randomize:
                original = enemy.drop_rare
                replacement = get_new_index(enemy.drop_rare)
                self.set_rare_drop(enemy.id, replacement)
                # debug:
##                input("rare drop " + str(id_name[original]) + " replaced with: " + str(id_name[replacement]))

            # provide a chance for a preveiously empty steal/drop slot
            # to actually have an item. todo: allow this to be user set
            empty_rand_chance = 5
            # randomly pick an item from the first 73 items for common steals/drops
            # randomly pick an item from the first 145 items for common steals/drops
            # todo: match the randomized item to monster difficulty
            if enemy.steal_common == 255 and random.randint(1,100) <= empty_rand_chance:
                self.set_common_steal(enemy.id, itemindex[random.randint(0, 72)])
            if enemy.steal_rare == 255 and random.randint(1,100) <= empty_rand_chance:
                self.set_rare_steal(enemy.id, itemindex[random.randint(0, 144)])
            if enemy.drop_common == 255 and random.randint(1,100) <= empty_rand_chance:
                self.set_common_drop(enemy.id, itemindex[random.randint(0, 72)])
            if enemy.drop_rare == 255 and random.randint(1,100) <= empty_rand_chance:
                self.set_rare_drop(enemy.id, itemindex[random.randint(0, 144)])

    #def remove_from_drops_steals(self, item="Illumina", replacements=["Tonic", "Potion", "Tincture", "Antidote", "Echo Screen", "Eyedrop", "Green Cherry",
                                 #"Revivify", "Soft", "Ether", "Sleeping Bag", "Tent", "Remedy", "Dried Meat"]):
    def remove_from_drops_steals(self, target_item, possible_replacements):
        
        import random
        from data.item_names import id_name
        possible_replacements = [name_id[item_name] for item_name in possible_replacements]
        item = name_id[target_item]

        # if using random replacements, use this to ensure exclusions
        exclusionlist = set()
        from constants.items import good_items
        for item in good_items:
            exclusionlist.add(name_id[item])
        for item in self.items.GOOD:
            exclusionlist.add(item)
            
        for enemy in self.enemies:
            if enemy.steal_common == item:
                #replacement = random.choice(replacements)
                replacement = self.items.get_random(exclude=list(exclusionlist))                
                self.set_common_steal(enemy.id, replacement)
                # debug
##                input("common steal " + str(id_name[item]) + " replaced with: "
##                      + str(id_name[replacement]))
            if enemy.steal_rare == item:
                #replacement = random.choice(replacements)
                replacement = self.items.get_random(exclude=list(exclusionlist))                
                self.set_rare_steal(enemy.id, replacement)
                # debug
##                input("rare steal " + str(id_name[item]) + " replaced with: "
##                      + str(id_name[replacement]))
            if enemy.drop_common == item:
                #replacement = random.choice(replacements)
                replacement = self.items.get_random(exclude=list(exclusionlist))                
                self.set_common_drop(enemy.id, replacement)
                # debug
##                input("common drop " + str(id_name[item]) + " replaced with: "
##                    + str(id_name[replacement]))
            if enemy.drop_rare == item:
                #replacement = random.choice(replacements)
                replacement = self.items.get_random(exclude=list(exclusionlist))                
                self.set_rare_drop(enemy.id, replacement)
                # debug
##                input("rare drop " + str(id_name[item]) + " replaced with: "
##                    + str(id_name[replacement]))

    # remove ultimate items from monster steals/drops
    def remove_ultimate_items(self):
        from data.items import ULTS_ID as ultimate_ids
        for enemy in self.enemies:
            if enemy.steal_common in ultimate_ids:
                while(enemy.steal_common in ultimate_ids):
                    self.set_common_steal(enemy.id, name_id["Potion"])
                #print("Common steal replaced for: " + str(enemy.id))
            if enemy.steal_rare in ultimate_ids:
                while(enemy.steal_rare in ultimate_ids):
                    self.set_rare_steal(enemy.id, name_id["Potion"])
                #print("Rare steal replaced for: " + str(enemy.id))
            if enemy.drop_common in ultimate_ids:
                while(enemy.drop_common in ultimate_ids):
                    self.set_common_drop(enemy.id, name_id["Potion"])
                #print("Common drop replaced for: " + str(enemy.id))
            if enemy.drop_rare in ultimate_ids:
                while(enemy.drop_rare in ultimate_ids):
                    self.set_rare_drop(enemy.id, name_id["Potion"])
                #print("Rare drop replaced for: " + str(enemy.id))
    # remove ultimate items from monster steals/drops

    ### End of section: Mods for drop and steal randomization ###


    def remove_fenix_downs(self):
        import random
        from data.item_names import name_id

        fenix_down = name_id["Fenix Down"]
        possible_replacements = ["Tonic", "Potion", "Tincture", "Antidote", "Echo Screen", "Eyedrop", "Green Cherry",
                                 "Revivify", "Soft", "Ether", "Sleeping Bag", "Tent", "Remedy", "Dried Meat"]
        possible_replacements = [name_id[item_name] for item_name in possible_replacements]

        for enemy in self.enemies:
            if enemy.steal_common == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_common_steal(enemy.id, replacement)

            if enemy.steal_rare == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_rare_steal(enemy.id, replacement)

            if enemy.drop_common == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_common_drop(enemy.id, replacement)

            if enemy.drop_rare == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_rare_drop(enemy.id, replacement)

    def apply_scaling(self):
        # lower vargas and whelk's hp
        vargas_id = self.get_enemy("Vargas")
        self.enemies[vargas_id].hp = self.enemies[vargas_id].hp // 2

        ultros3_id = self.get_enemy("Ultros 3")
        self.enemies[ultros3_id].hp = self.enemies[ultros3_id].hp // 2

        # increase hp of some early bosses (especially ones which are normally not fought with a full party)
        hp4x = ["Leader", "Marshal"]
        hp3x = ["Rizopas", "Piranha", "TunnelArmr"]
        hp2x = ["Ipooh", "GhostTrain", "Kefka (Narshe)", "Dadaluma", "Ifrit", "Shiva", "Number 024",
                "Number 128", "Left Blade", "Right Blade", "Left Crane", "Right Crane", "Nerapa"]

        if not self.args.boss_normalize_distort_stats:
            # double opera ultros' hp only if not already normalized
            # each form (location) has different hp pools so it is already challenging enough after the normalize
            hp2x.append("Ultros 2")

        for boss_id, boss_name in bosses.enemy_name.items():
            enemy = self.enemies[boss_id]
            if boss_name in hp4x:
                enemy.hp *= 4
            elif boss_name in hp3x:
                enemy.hp *= 3
            elif boss_name in hp2x:
                enemy.hp *= 2

    ### Mods for enemy challenges
    # Enemy speed boost mod
    def speed_boost(self):
        import random
        for enemy in self.enemies:
            # speed over 235 causes problems
            new_speed = random.randint(170, 230)
            enemy.speed = new_speed
    # speed boost mod

    # make "easy" bosses harder
    def easyboss_buff(self):
        for boss_id, boss_name in bosses.enemy_name.items():
            enemy = self.enemies[boss_id]
            if boss_name == "Leader":
                enemy.hp = enemy.hp * 2   #total is 8x HP
                enemy.regen = 1
                enemy.runic = 1
            if boss_name == "Rizopas":
                enemy.hp = enemy.hp * 2   #total is 6x HP
                enemy.image = 1
                enemy.shell = 1
            if boss_name == "TunnelArmr":
                enemy.hp = enemy.hp * 2   #total is 6x HP
                enemy.haste = 1
                enemy.shell = 1
                enemy.safe = 1
            if boss_name == "Ipooh":
                enemy.hp = enemy.hp * 2   #total is 4x HP
            if boss_name == "Left Blade":
                enemy.hp = enemy.hp * 2   #total is 4x HP
            if boss_name == "RightBlade":
                enemy.hp = enemy.hp * 2   #total is 4x HP
            if boss_name == "Kefka (Narshe)":
                enemy.hp = enemy.hp * 2   #total is 4x HP
                enemy.haste = 1
                enemy.reflect = 1
            if boss_name == "Dadaluma":
                enemy.hp = enemy.hp * 2   #total is 2x HP
                enemy.regen = 1
                enemy.shell = 1                
            if boss_name == "Number 128":
                enemy.hp = enemy.hp * 2   #total is 2x HP    
            if boss_name == "GhostTrain":
                enemy.hp = enemy.hp * 2   #total is 2x HP
            if boss_name == "Air Force":
                enemy.hp = enemy.hp * 2   #total is 2x HP
            if boss_name == "Nerapa":
                enemy.hp = enemy.hp * 2   #total is 2x HP
            if boss_name == "Vargas":
                enemy.hp = enemy.hp * 2   #total is 1x HP (vanilla)

    ### End of section: Mods for enemy challenges            

    def boss_experience(self):
        from data.bosses_custom_exp import custom_exp
        for enemy_id, exp in custom_exp.items():
            self.enemies[enemy_id].exp = exp * self.enemies[enemy_id].level

        ### modify boss XP
        if self.args.boss_experience_mod:
            boss_xp_mod = self.args.boss_experience_percent / 100
        else:  #probably redundant since boss_experience_percent defaults to 100
            boss_xp_mod = 1
        for enemy_id, exp in custom_exp.items():
            self.enemies[enemy_id].exp = int(exp * boss_xp_mod) * self.enemies[enemy_id].level
        ### modify boss XP

    def boss_normalize_distort_stats(self):
        import random

        def stat_min_max(stat_value, min_possible, max_possible):
            distortion_percent = 0.25
            stat_distortion_amount = int(stat_value * distortion_percent)

            # if distortion_percent can potentially set value outside allowed range
            # then set the distortion to the max amount allowable
            if stat_value - stat_distortion_amount < min_possible:
                stat_distortion_amount = stat_value
            elif stat_value + stat_distortion_amount > max_possible:
                stat_distortion_amount = max_possible - stat_value

            stat_min = stat_value - stat_distortion_amount
            stat_max = stat_value + stat_distortion_amount

            return stat_min, stat_max

        stats = ["speed", "vigor", "accuracy", "evasion", "magic_evasion", "defense", "magic_defense", "magic"]
        min_stat_max = [70, 24, 100, 0, 0, 150, 160, 16] # minimum values for maximum random values

        for enemy in self.bosses:
            for stat_index, stat in enumerate(stats):
                stat_value = getattr(enemy, stat)
                stat_min, stat_max = stat_min_max(stat_value, 0, 2**8 - 1)

                if stat_max < min_stat_max[stat_index]:
                    # max rand value is lower than the minimum for this stat, increase it to the minimum
                    stat_max = min_stat_max[stat_index]

                setattr(enemy, stat, random.randint(stat_min, stat_max))

        stats = ["hp", "mp"]
        for enemy in self.bosses:
            hp_min, hp_max = stat_min_max(enemy.hp, 0, 2**16 - 1)
            mp_min, mp_max = stat_min_max(enemy.mp, 0, 2**16 - 1)

            # minimum hp/mp max values based on mean (hp / level) and mean (mp / level) of bosses
            # cap the max at triple the original hp/mp
            min_hp_max = min(enemy.level * 500, enemy.hp * 3)
            min_mp_max = min(enemy.level * 150, enemy.mp * 3)

            if hp_max < min_hp_max:
                hp_max = min_hp_max
            if mp_max < min_mp_max:
                mp_max = min_mp_max

            enemy.hp = random.randint(hp_min, hp_max)
            enemy.mp = random.randint(mp_min, mp_max)

    def skip_shuffling_zone(self, maps, zone):
        if zone.MAP and zone.id >= maps.MAP_COUNT:
            return True # do not shuffle map zones that do not correspond to a map

        if zone.MAP and not maps.properties[zone.id].enable_random_encounters:
            return True # do not shuffle map zones with disabled random encounters

        return False

    def skip_shuffling_pack(self, pack, encounter_rate):
        from data.enemy_zone import EnemyZone

        if pack == 0 and encounter_rate == EnemyZone.NORMAL_ENCOUNTER_RATE:
            # 0 is used as a placeholder (leafer x1 and leafer x2, dark wind)
            # luckily the real ones outside narshe have lower encounter rates to differentiate them
            # except for the forest, does this cause problems?
            return True

        if pack == EnemyPacks.VELDT:
            return True

        if pack == EnemyPacks.ZONE_EATER:
            return True

        return False

    def skip_shuffling_formation(self, formation):
        if formation == EnemyFormations.PRESENTER:
            return True

        return False

    def shuffle_encounters(self, maps):
        import collections
        # find all packs that are randomly encountered in zones
        packs = collections.OrderedDict()
        for zone in self.zones.zones:
            if self.skip_shuffling_zone(maps, zone):
                continue

            for x in range(zone.PACK_COUNT):
                if self.skip_shuffling_pack(zone.packs[x], zone.encounter_rates[x]):
                    continue

                packs[self.packs.packs[zone.packs[x]]] = None

        # find all formations that are randomly encountered in packs
        formations = []
        for pack in packs:
            for y in range(pack.FORMATION_COUNT):
                if self.skip_shuffling_formation(pack.formations[y]):
                    continue

                if pack.extra_formations[y]:
                    # pack has extra formations (i.e. each formation is randomized with the subsequent 3 formations)
                    # unfortunately, this means there are more formations than packs to put them in, so some formations are lost
                    for x in range(4):
                        formations.append(pack.formations[y] + x)
                else:
                    formations.append(pack.formations[y])

        # shuffle the randomly encounterable formations
        import random
        random.shuffle(formations)

        for pack in packs:
            for y in range(pack.FORMATION_COUNT):
                if self.skip_shuffling_formation(pack.formations[y]):
                    continue

                pack.formations[y] = formations.pop()

        # NOTE: any remaining formations (due to extra_formations) are lost

    def chupon_encounters(self, maps):
        # find all packs that are randomly encountered in zones
        packs = []
        for zone in self.zones.zones:
            if self.skip_shuffling_zone(maps, zone):
                continue

            for x in range(zone.PACK_COUNT):
                if self.skip_shuffling_pack(zone.packs[x], zone.encounter_rates[x]):
                    continue

                packs.append(zone.packs[x])

        self.packs.chupon_packs(packs)
        
    def randomize_encounters(self, maps):
        # find all packs that are randomly encountered in zones
        packs = []
        boss_percent = self.args.random_encounters_random / 100.0
        for zone in self.zones.zones:
            if self.skip_shuffling_zone(maps, zone):
                continue

            for x in range(zone.PACK_COUNT):
                if self.skip_shuffling_pack(zone.packs[x], zone.encounter_rates[x]):
                    continue

                packs.append(zone.packs[x])

        print("randomize packs")
        self.packs.randomize_packs(packs, boss_percent)

    def set_escapable(self):
        import random

        escapable_percent = self.args.encounters_escapable_random / 100.0
        for enemy in self.enemies:
            if enemy.id in bosses.enemy_name or enemy.id == self.SRBEHEMOTH2_ID or enemy.id == self.INVINCIBLE_GUARDIAN_ID:
                continue

            enemy.no_run = random.random() >= escapable_percent

    def no_undead_bosses(self):
        boss_ids = list(bosses.enemy_name.keys())
        boss_ids.append(self.SRBEHEMOTH2_ID)

        for boss_id in boss_ids:
            self.enemies[boss_id].undead = False

    def scan_all(self):
        for enemy in self.enemies:
            enemy.no_scan = 0

    def mod(self, maps):
        # shuffle drops
        if (self.args.random_ranked_drops_steals_chance > 0 and
            self.args.random_ranked_drops_steals_variation > 0):
            self.randomize_steals_drops_ranked(self.args.random_ranked_drops_steals_chance,
                                               self.args.random_ranked_drops_steals_variation)
        # prevent ultimate items from randomly appearing in monster steals/drops
        if self.args.ultimate_items:
            self.remove_ultimate_items()
            
        if self.args.boss_normalize_distort_stats:
            self.boss_normalize_distort_stats()

        if self.args.permadeath:
            self.remove_fenix_downs()

        self.apply_scaling()

        # challenge mods
        if self.args.fast_enemies:
            self.speed_boost()
        if self.args.easy_boss_buff:
            self.easyboss_buff()
        # challenge mods

        if self.args.boss_experience:
            self.boss_experience()

        if not self.args.encounters_escapable_original:
            self.set_escapable()

        if self.args.boss_no_undead:
            self.no_undead_bosses()

        if self.args.random_encounters_shuffle:
            self.shuffle_encounters(maps)
        elif self.args.random_encounters_chupon:
            self.chupon_encounters(maps)
        elif not self.args.random_encounters_original:
            self.randomize_encounters(maps)

        self.formations.mod()
        self.packs.mod()
        self.zones.mod()
        self.scripts.mod()

        if self.args.scan_all:
            self.scan_all()

##        if self.args.debug:
##            for enemy in self.enemies:
##                enemy.debug_mod()

    def get_event_boss(self, original_boss_name):
        return self.packs.get_event_boss_replacement(original_boss_name)

    def print(self):
        for enemy in self.enemies:
            enemy.print()

    def write(self):
        for enemy_index in range(len(self.enemies)):
            self.enemy_data[enemy_index] = self.enemies[enemy_index].data()
            self.enemy_name_data[enemy_index] = self.enemies[enemy_index].name_data()
            self.enemy_item_data[enemy_index] = self.enemies[enemy_index].item_data()
            self.enemy_special_name_data[enemy_index] = self.enemies[enemy_index].special_name_data()

        self.enemy_data.write()
        self.enemy_name_data.write()
        self.enemy_item_data.write()
        self.enemy_special_name_data.write()

        self.formations.write()
        self.packs.write()
        self.zones.write()
        self.scripts.write()
