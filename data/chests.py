from data.chest import Chest
import data.chests_asm as chests_asm
from data.structures import DataArrays
import random

class Chests():
    PTRS_START = 0x2d82f4
    PTRS_END = 0x2d8633
    DATA_START = 0x2d8634
    DATA_END = 0x2d8e5a
    DATA_SIZE = 5

    def __init__(self, rom, args, items):
        self.rom = rom
        self.args = args
        self.items = items

        self.chest_data = DataArrays(self.rom, self.PTRS_START, self.PTRS_END, self.rom.SHORT_PTR_SIZE, self.DATA_START, self.DATA_END, self.DATA_SIZE)

        self.all_chests = []
        self.map_chests = []
        for map_index in range(len(self.chest_data)):
            map_chests = []
            for map_chest_index in range(len(self.chest_data[map_index])):
                chest = Chest(len(self.all_chests), self.chest_data[map_index][map_chest_index])
                self.all_chests.append(chest)
                map_chests.append(chest)
            self.map_chests.append(map_chests)

        self.next_id = 287           # next id to use for new chests
        self.next_opened_bit = 0x103 # next opened bit flag to use for new chests

        # some chests are duplicated on multiple maps (mt kolts, doma, albrook, kefka's tower)
        # list of tuples (<first chest id>, <duplicate chest id>)
        self.duplicates = [(68, 70), (69, 71)] + \
                          [(95, 97), (91, 98), (92, 99), (93, 100), (94, 101), (95, 102), (96, 103)] + \
                          [(202, 203)] + \
                          [(174, 284), (175, 285)]

        # list of all available chests (for shuffling and modifying)
        # exclude lone wolf chest, unreachabe, duplicate chests so they are not modified
        lone_wolf_chest_id = 2
        gem_box_chest_id = 231
        self.unreachable_ids = [0, 32, 33, 34, 141, 142, 143, 144, 145]
        self.chests = [chest for chest in self.all_chests if chest.id not in self.unreachable_ids and \
                                                             chest.id not in [dup[1] for dup in self.duplicates] and \
                                                             chest.id != lone_wolf_chest_id and \
                                                             chest.id != gem_box_chest_id]

        from data.chest_item_tiers import tiers, tier_s_distribution
        self.item_tiers = tiers

        # remove excluded items from tiers
        excluded_items = self.items.get_excluded()
        for idx, tier in enumerate(self.item_tiers):
            tier = [(item) for item in tier if item not in excluded_items]
            self.item_tiers[idx] = tier

        # for S-tier, remaining item weights raised proportionally to their original weight
        #   e.g. if original weights were [0.10, 0.50, 0.40] and 0.50 removed, the remaining ones become [0.20, 0.80]
        self.item_tier_s_distribution = [(item_weight[0], item_weight[1]) for item_weight in tier_s_distribution
                                         if item_weight[0] not in excluded_items]


        # pull in data for sorted chest item tiers
        from data.sorted_chest_item_tiers import sorted_tiers
        self.sorted_item_tiers = sorted_tiers

    def chest_count(self, map_id):
        return len(self.map_chests[map_id])

    def set_item(self, map_id, x, y, item_id):
        for chest in self.map_chests[map_id]:
            if chest.x == x and chest.y == y:
                chest.type = Chest.ITEM
                chest.contents = item_id
                return
        raise IndexError(f"set_item: could not find chest at ({x}, {y}) on map {hex(map_id):<5}")

    def shuffle(self, types):
        import copy
        chests_shuffle = [copy.deepcopy(chest) for chest in self.chests if chest.type in types]

        random.shuffle(chests_shuffle)

        shuffle_index = 0
        for chest in self.chests:
            if chest.type in types:
                shuffled_chest = chests_shuffle[shuffle_index]
                shuffle_index += 1

                chest.type = shuffled_chest.type
                chest.contents = shuffled_chest.contents

    def shuffle_random(self):
        randomizable_types = [Chest.EMPTY, Chest.ITEM, Chest.GOLD]

        # first shuffle the chests to mix up empty/item/gold positions
        self.shuffle(randomizable_types)
        if self.args.chest_contents_shuffle_random_percent == 0:
            return

        possible_chests = [chest for chest in self.chests if chest.type in randomizable_types]
        random_percent = self.args.chest_contents_shuffle_random_percent / 100.0
        num_random_chests = int(len(possible_chests) * random_percent)
        random_chests = random.sample(possible_chests, num_random_chests)
        for chest in random_chests:
            if chest.type == Chest.GOLD:
                chest.randomize_gold()
            elif chest.type == Chest.ITEM:
                chest.contents = self.items.get_random()

    def random_tiered(self):
        def get_item(tiers, tier_s_distribution):
            from data.chest_item_tiers import weights
            from utils.weighted_random import weighted_random

            random_tier = weighted_random(weights)
            if random_tier < len(weights) - 1: # not s tier, use equal distribution
                random_tier_index = random.randrange(len(tiers[random_tier]))
                return tiers[random_tier][random_tier_index]

            weights = [entry[1] for entry in tier_s_distribution]
            random_s_index = weighted_random(weights)
            return tier_s_distribution[random_s_index][0]

        # first shuffle the chests to mix up empty/item/gold positions
        self.shuffle([Chest.EMPTY, Chest.ITEM, Chest.GOLD])

        for chest in self.chests:
            if chest.type == Chest.GOLD:
                chest.contents = int(random.triangular(1, Chest.MAX_GOLD_VALUE + 1, 1))
                if chest.contents == Chest.MAX_GOLD_VALUE + 1:
                    # triangular max is inclusive, very small chance need to round max down
                    chest.contents = Chest.MAX_GOLD_VALUE
            elif chest.type == Chest.ITEM:
                chest.contents = get_item(self.item_tiers, self.item_tier_s_distribution)

    def random_scaled(self):
        import math
        from utils.weighted_random import weighted_random

        # shuffle the chests to mix up empty/item/gold positions
        self.shuffle([Chest.EMPTY, Chest.ITEM, Chest.GOLD])

        item_chests = [chest for chest in self.chests if chest.type == Chest.ITEM]
        gold_chests = [chest for chest in self.chests if chest.type == Chest.GOLD]

        # tier weights, start_weights are the odds for chest 0, end_weights are for chest (len(item_chests) - 1)
        start_weights = [
            25, 15, 3, 1, 0,
            10, 40, 5, 1, 0,
        ]
        end_weights = [
            10, 12, 6, 3, 1,
            0, 0, 40, 25, 3,
        ]

        # most chests are often not opened, a quadratic transition allows values close to end_weights to be used
        # for late game chests and achieves the main desired effect of lowering the odds of high tier items early
        # start with horizontal parabola: x = a * (y - k)^2 + h
        # at chest_index = 0, weight = start_weight
        #   vertex = (h, k) = (0, start_weight), axis = k = start_weight, x = a * (y - start_weight)^2
        # at chest_index = x = len(item_chests) - 1, weight = y = end_weight
        #   a = rate = (len(item_chests) - 1) / (end_weight - start_weight)^2
        # weight = +-sqrt(chest_index / rate) + start_weight
        rates = [0] * len(start_weights)
        for index in range(len(start_weights)):
            rates[index] = (len(item_chests) - 1) / ((end_weights[index] - start_weights[index]) ** 2)

        item_bits = []
        self.item_contents = []
        for chest_index, chest in enumerate(item_chests):
            weights = [None] * len(rates)
            for tier_index in range(len(weights)):
                weights[tier_index] = math.sqrt(chest_index / rates[tier_index])
                if start_weights[tier_index] > end_weights[tier_index]:
                    weights[tier_index] = -weights[tier_index]
                weights[tier_index] += start_weights[tier_index]

            random_tier_index = weighted_random(weights)
            if random_tier_index < len(self.item_tiers) - 1: # not s tier, use equal distribution
                random_element_index = random.randrange(len(self.item_tiers[random_tier_index]))
                self.item_contents.append(self.item_tiers[random_tier_index][random_element_index])
            else:
                weights = [entry[1] for entry in self.item_tier_s_distribution]
                random_s_index = weighted_random(weights)
                self.item_contents.append(self.item_tier_s_distribution[random_s_index][0])
            item_bits.append(chest.bit.to_bytes(2, "little"))

        chests_asm.scale_items(item_bits, self.item_contents)

        gold_bits = []
        self.gold_contents = []
        for chest_index, chest in enumerate(gold_chests):
            max_value = int((Chest.MAX_GOLD_VALUE / len(gold_chests)) * (chest_index + 1))
            self.gold_contents.append(random.randint(1, max_value))
            gold_bits.append(chest.bit.to_bytes(2, "little"))

        chests_asm.scale_gold(gold_bits, self.gold_contents)

    def clear_contents(self):
        for chest in self.chests:
            if chest.type == Chest.ITEM or chest.type == Chest.GOLD:
                chest.type = Chest.EMPTY
                chest.contents = 0


    ### Mod to add in random % GP chests
    def shuffle_random_gold(self):
        #252 randomizable chests, 7 GP chests by default
        randomizable_types = [Chest.EMPTY, Chest.ITEM, Chest.GOLD]
        # guarantee 0 GP before doing randomization
        # by placing random items in every empty chest
        for chest in self.chests:
            if chest.type == Chest.GOLD:
                chest.type = chest.ITEM
                chest.contents = self.items.get_random(exclude=self.items.get_excluded())

        if self.args.gold_chest_shuffle_percent == 0:
            return

        import random
        possible_chests = [chest for chest in self.chests if ((chest.type in randomizable_types))]        
        random_percent = (self.args.gold_chest_shuffle_percent) / 100.0
        num_gold_chests = int(len(possible_chests) * random_percent)

        # debug:
##        print(num_gold_chests)
##        print("^ number of gold chests added ^")

        #gets the specific chests that will be randomized
        random_chests = random.sample(possible_chests, num_gold_chests)

        for chest in random_chests:
            chest.type = Chest.GOLD
            chest.randomize_gold()
    ### Mod to add in random % GP chests

    ### Mod to add in random % empty chests
    def shuffle_random_empties(self):
        #252 randomizable chests, 9 empties by default
        randomizable_types = [Chest.EMPTY, Chest.ITEM, Chest.GOLD]
        # guarantee 0 empties before doing randomization
        # by placing random items in every empty chest
        for chest in self.chests:
            if chest.type == Chest.EMPTY:
                chest.type = chest.ITEM
                chest.contents = self.items.get_random(exclude=self.items.get_excluded())

        if self.args.empty_chest_shuffle_percent == 0:
            return

        import random
        possible_chests = [chest for chest in self.chests if ((chest.type in randomizable_types))]
        random_percent = (self.args.empty_chest_shuffle_percent) / 100.0
        num_empty_chests = int(len(possible_chests) * random_percent)

        # debug:
##        print(num_empty_chests)
##        print("^ number of empty chests added ^")

        #gets the specific chests that will be randomized
        random_chests = random.sample(possible_chests, num_empty_chests)  

        for chest in random_chests:
            chest.type = Chest.EMPTY
            chest.contents = 0
    ### Mod to add in random % empty chests


    # modify exclusion lists for chests
    def remove_excluded_items(self):
        exclude = self.items.get_excluded()

        ### exclude more items from chests
        reward_tier_items = []
        if self.args.no_good_chests:
            reward_tier_items.append("ValiantKnife")
            reward_tier_items.append("Illumina")
            reward_tier_items.append("Ragnarok")
            reward_tier_items.append("Pearl Lance")
            reward_tier_items.append("Aura Lance")
            reward_tier_items.append("Magus Rod")
            reward_tier_items.append("Fixed Dice")
            reward_tier_items.append("Flame Shld")
            reward_tier_items.append("Ice Shld")
            reward_tier_items.append("Thunder Shld")
            reward_tier_items.append("Force Shld")
            reward_tier_items.append("Minerva")
            reward_tier_items.append("Exp. Egg")
            reward_tier_items.append("Genji Glove")
            reward_tier_items.append("Offering")      

            if self.args.stronger_atma_weapon:
                reward_tier_items.append("Atma Weapon")

        # loop through all items in reward_tier_items and add them to excluded list
        from constants.items import id_name, name_id
        for item_name in reward_tier_items:
            exclude.append(name_id[item_name])
        ### exclude more items from chests

        for chest in self.all_chests:
            if chest.type == Chest.ITEM and chest.contents in exclude:
                # replace chest content with a random, non-excluded item 
                # instead of just making it empty
                if self.args.replace_with_items:
                    chest.contents = self.items.get_random(exclude=exclude)
                else:
                    chest.type = Chest.EMPTY
                    chest.contents = 0

    def fix_shared_bits(self):
        # some chests on different maps share the same opened bits but have different contents
        # give them unique bits so both can be opened and contents aren't lost
        from data.area_chests import area_chests

        shared_chests = list(area_chests["Narshe Mines WOB"])
        shared_chests += list(area_chests["South Figaro Cave WOB"])
        shared_chests += list(area_chests["South Figaro Outside WOB"])

        for chest_id in shared_chests:
            self.all_chests[chest_id].bit = self.next_opened_bit
            self.next_opened_bit += 1

    def copy_thamasa_chests(self):
        # the unreachable thamasa map before leo's death has chests that are later lost
        # copy those chests to the wob/wor thamasa maps to make them available

        def copy_chest(self, src_map_id, src_chest_id, dst_map_id):
            import copy
            new_chest = copy.deepcopy(self.map_chests[src_map_id][src_chest_id])

            self.all_chests[self.next_id].x = new_chest.x
            self.all_chests[self.next_id].y = new_chest.y
            self.all_chests[self.next_id].bit = new_chest.bit
            self.all_chests[self.next_id].type = new_chest.type
            self.all_chests[self.next_id].contents = new_chest.contents
            self.next_id += 1

            # delete last chest to free space for new chest
            del self.chest_data[-1][-1]
            del self.map_chests[-1][-1]

            self.chest_data[dst_map_id].append(new_chest.data())
            self.map_chests[dst_map_id].append(new_chest)

        unreachable_thamasa_id = 0x157
        thamasa_wob_id = 0x154
        thamasa_wor_id = 0x158

        for chest_index in range(len(self.map_chests[unreachable_thamasa_id])):
            copy_chest(self, unreachable_thamasa_id, chest_index, thamasa_wob_id)
            copy_chest(self, unreachable_thamasa_id, chest_index, thamasa_wor_id)

    def update_duplicates(self):
        # for chests on multiple maps, only one of them should have been modified (the one with the lower id)
        # copy the first one to the duplicates so they all have the same contents/type/bits
        # they will give the same item and if one is opened the other(s) are no longer available
        for first_duplicate in self.duplicates:
            first_chest = self.all_chests[first_duplicate[0]]
            duplicate_chest = self.all_chests[first_duplicate[1]]

            duplicate_chest.bit = first_chest.bit
            duplicate_chest.type = first_chest.type
            duplicate_chest.contents = first_chest.contents

    ### debugging: print chest contents
    def print_chest_contents(self):
        randomizable_types = [Chest.EMPTY, Chest.ITEM, Chest.GOLD]
        from constants.items import id_name, name_id
        for chest in self.chests:
            if chest.type in randomizable_types:
                if chest.type == Chest.ITEM:
                    print(str(id_name[chest.contents]))
                elif chest.type == Chest.GOLD:
                    print(f"{chest.contents * 100} GP")
                elif chest.type == Chest.MONSTER:
                    # TODO how to get enemy name?
                    contents.append("MIAB")
                elif chest.type == Chest.EMPTY:
                    print("EMPTY")
    ### debugging: print chest contents


    def mod(self):
        self.fix_shared_bits()

        if self.args.chest_contents_shuffle_random:
            self.shuffle_random()
            self.remove_excluded_items()
        elif self.args.chest_contents_random_tiered:
            self.random_tiered()
        elif self.args.chest_contents_random_scaled:
            self.random_scaled()
        elif self.args.chest_contents_empty:
            self.clear_contents()
        else:
            self.remove_excluded_items()

        # % empty/GP chest mods
        if self.args.empty_chest_shuffle and self.args.gold_chest_shuffle:
            self.shuffle_random_types()
        elif self.args.empty_chest_shuffle or self.args.gold_chest_shuffle:
            if self.args.empty_chest_shuffle:
                self.shuffle_random_empties()
            if self.args.gold_chest_shuffle:
                self.shuffle_random_gold()


        if self.args.chest_monsters_shuffle:
            self.shuffle([Chest.MONSTER])

        self.copy_thamasa_chests()

        # update duplicates last after other chest mods finished
        self.update_duplicates()

        # print chest contents after mods
        if 0 == 1:
            print_chest_contents()


    def write(self):
        if self.args.spoiler_log:
            self.log()

        for map_index in range(len(self.chest_data)):
            for map_chest_index in range(len(self.chest_data[map_index])):
                self.chest_data[map_index][map_chest_index] = self.map_chests[map_index][map_chest_index].data()

        self.chest_data.write()

    def log(self):
        from log import SECTION_WIDTH, section, format_option
        from data.area_chests import area_chests
        from data.item_names import id_name
        from data.item import Item
        from textwrap import wrap

        lcolumn = []
        if self.args.chest_contents_random_scaled:
            lcolumn.append("Items:")
            items_per_line = 5

            lines = [self.item_contents[index : index + items_per_line] for index in range(0, len(self.item_contents), items_per_line)]
            for line_index, line_items in enumerate(lines):
                line = f"{line_index * items_per_line:>3}: "
                for item_index, item_id in enumerate(line_items):
                    line += f"{id_name[item_id]:<{Item.NAME_LENGTH}}"
                lcolumn.append(line)

            lcolumn.append("")
            lcolumn.append("GP: " + ", ".join([f"{gold * 100}" for gold in self.gold_contents]))
        else:
            for area_name, chest_ids in area_chests.items():
                lcolumn.append(area_name)

                contents = []
                for chest_id in chest_ids:
                    chest = self.all_chests[chest_id]
                    if chest.type == Chest.ITEM:
                        contents.append(id_name[chest.contents])
                    elif chest.type == Chest.GOLD:
                        contents.append(f"{chest.contents * 100} GP")
                    elif chest.type == Chest.MONSTER:
                        # TODO how to get enemy name?
                        contents.append("MIAB")
                    elif chest.type == Chest.EMPTY:
                        contents.append("Empty")

                lines = wrap(", ".join(contents), width = SECTION_WIDTH, \
                             initial_indent = "    ", subsequent_indent = "    ")
                for line in lines:
                    lcolumn.append(line)
                lcolumn.append("")
            lcolumn.pop()

        section("Chests", lcolumn, [])

    def print(self):
        for map_index in range(len(self.map_chests)):
            print(f"map {hex(map_index):<5} chests:")
            for map_chest_index in range(len(self.map_chests[map_index])):
                self.map_chests[map_index][map_chest_index].print()


##    ### location tiering tier
    def chest_location_tier(self, event_depth):
        from data.area_chests import area_chests
        ### create area_chest to event area linkage
        area_chests_to_event_area = {
            "Narshe School" : "Start", 
            "Narshe Outside WOB (Unreachable)" : "Commented Out", 
            "Narshe Inside WOB" : "Start", 
            "Narshe Mines WOB" : "Start", 
            "Narshe Mines WOR" : "Start", 
            "Figaro Castle" : "Figaro Castle WOB", 
            "Figaro Castle Basement" : "Figaro Castle WOR", 
            "South Figaro Cave WOB" : "South Figaro Cave", 
            "South Figaro Cave WOB (Unreachable)" : "Commented Out", 
            "South Figaro Cave WOR" : "Figaro Castle WOR", 
            "South Figaro Outside WOB" : "Start", 
            "South Figaro Outside WOR" : "Start", 
            "South Figaro Inside/Basement" : "Start", 
            "Duncan's House WOB" : "Start", 
            "Mt. Kolts" : "Mt. Kolts", 
            "Returner's Hideout" : "Start", 
            "Imperial Camp" : "Imperial Camp", 
            "Doma" : "Doma WOB", 
            "Cyan's Dream Doma (Duplicates)" : "Commented Out", 
            "Cyan's Dream Phantom Train" : "Doma WOR", 
            "Phantom Train" : "Phantom Train", 
            "Mobliz Inside" : "Start", 
            "Mobliz Bookshelf Room WOR" : "Mobliz WOR", 
            "Mobliz Outside WOR" : "Mobliz WOR", 
            "Serpent Trench" : "Serpent Trench", 
            "Nikeah" : "Start", 
            "Kohlingen" : "Start", 
            "Coliseum Owner's House WOB" : "Start", 
            "Zozo" : "Zozo", 
            "Mt. Zozo" : "Mt. Zozo", 
            "Owzer's Mansion" : "Owzer Mansion", 
            "Owzer's Basement" : "Owzer Mansion", 
            "Albrook Outside" : "Start", 
            "Albrook Outside WOR (Duplicate)" : "Commented Out", 
            "Albrook Inside" : "Start", 
            "Albrook Dock" : "Start", 
            "Maranda" : "Maranda", 
            "Tzen Collapsing House" : "Collapsing House", 
            "Imperial Palace (Unreachable)" : "Commented Out", 
            "Magitek Factory" : "Magitek Factory", 
            "Thamasa Outside" : "Start", 
            "Thamasa Strago's House" : "Veldt Cave WOR", 
            "Thamasa Burning House" : "Burning House", 
            "Esper Mountain" : "Esper Mountain", 
            "Imperial Base" : "Sealed Gate", 
            "Cave To Sealed Gate" : "Sealed Gate", 
            "Floating Continent" : "Floating Continent", 
            "Daryl's Tomb" : "Daryl's Tomb", 
            "Veldt Cave WOR" : "Veldt Cave WOR", 
            "Ancient Cave" : "Ancient Castle", 
            "Phoenix Cave" : "Phoenix Cave", 
            "Fanatic's Tower" : "Fanatic's Tower", 
            "Zone Eater" : "Zone Eater", 
            "Umaro's Cave" : "Umaro's Cave", 
            "Kefka's Tower" : "Kefka's Tower", 
            "Kefka's Tower (Duplicate)" : "Commented Out",
            }
        chest_tier_counter = []
        actual_chest_tier_counter = {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
        }
        ### get max depth
        max_depth = 0
        for x, depth in event_depth.items():
            if depth > max_depth:
                max_depth = depth


        def get_tiered_item(tiers, tier_s_distribution, chest_depth, max_depth):
            tier_modifier = chest_depth / max_depth #1/9, 2/9, 3/9, etc.
            # try boosting tier_modifier value
            tier_modifier = tier_modifier + 0.25
            
            from data.sorted_chest_item_tiers import weights
            from utils.weighted_random import weighted_random

            #random_tier = weighted_random(weights)
            temptier = weighted_random(weights)
            # modify the random_tier
            random_tier = min(round(temptier * tier_modifier), 4)
            #print(str(temptier) + " * " + str(tier_modifier) + " | " + str(random_tier))
            if random_tier < len(weights) - 1: # not s tier, use equal distribution
                random_tier_index = random.randrange(len(tiers[random_tier]))
                #print(random_tier_index)
                return tiers[random_tier][random_tier_index], random_tier

            weights = [entry[1] for entry in tier_s_distribution]
            random_s_index = weighted_random(weights)
            #print(random_s_index)
            return tier_s_distribution[random_s_index][0], 4

        # loop thru all chests
        for chest in self.chests:
            # loop thru all area chests
            for area, chestrange in area_chests.items():
                if chest.id in chestrange:
                    # get the associated event
                    event_area = area_chests_to_event_area[area] 
                    chest_depth = event_depth[event_area]  
                    chest_tier_counter.append(chest_depth)  # do this for analysis later
                    #print(str(event_area) + ": " + str(chest_depth))

                    #for chest in self.chests:
                    if chest.type == Chest.GOLD:
                        chest.contents = int(random.triangular(1, Chest.MAX_GOLD_VALUE + 1, 1))
                        if chest.contents == Chest.MAX_GOLD_VALUE + 1:
                            # triangular max is inclusive, very small chance need to round max down
                            chest.contents = Chest.MAX_GOLD_VALUE
                    elif chest.type == Chest.ITEM:
                        chest.contents, tier_result = get_tiered_item(self.sorted_item_tiers, self.item_tier_s_distribution, chest_depth, max_depth)

                        ### do not allow ultimate items to be randomly placed in chests
                        if self.args.ultimate_items:
                            from data.items import ULTS_ID as ultimate_ids
                            while(chest.contents in ultimate_ids):
                                chest.contents, tier_result = get_tiered_item(self.sorted_item_tiers, self.item_tier_s_distribution, chest_depth, max_depth)
                        ### do not allow ultimate items to be randomly placed in chests
                                
                        actual_chest_tier_counter[tier_result] += 1
                #  end of if for chestrange
            # search for chest in next area
        # go to next chest

        # print the depth
        print(actual_chest_tier_counter)
        for x in range(max_depth):
            if x < (max_depth-1):
                print("Character Depth " + str(x+1) + ": " + str(chest_tier_counter.count(x+1)))
            else:
                print("Kefka's Tower " + str(x+1) + ": " + str(chest_tier_counter.count(x+1)))
