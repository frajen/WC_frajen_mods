from memory.space import Bank, Allocate
# added choose_tiered_reward
from event.event_reward import CHARACTER_ESPER_ONLY_REWARDS, RewardType, choose_reward, weighted_reward_choice, choose_tiered_reward
import instruction.field as field

class Events():
    def __init__(self, rom, args, data):
        self.rom = rom
        self.args = args

        self.dialogs = data.dialogs
        self.characters = data.characters
        self.items = data.items
        self.maps = data.maps
        self.enemies = data.enemies
        self.espers = data.espers
        self.shops = data.shops

        ### Add this to get logic for location/chest rank tiering and post-events mods
        self.pathing = ""   #used for display but not in logic
        self.pathingdict = {}
        self.gatingdict = {}
        self.event_depth = {}
        self.character_depth = {}
       
        events = self.mod()

        self.validate(events)

    def mod(self):
        # generate list of events from files
        import os, importlib, inspect
        from event.event import Event
        events = []
        name_event = {}
        for event_file in sorted(os.listdir(os.path.dirname(__file__))):
            if event_file[-3:] != '.py' or event_file == 'events.py' or event_file == 'event.py':
                continue

            module_name = event_file[:-3]
            event_module = importlib.import_module('event.' + module_name)

            for event_name, event_class in inspect.getmembers(event_module, inspect.isclass):
                if event_name.lower() != module_name.replace('_', '').lower():
                    continue
                event = event_class(name_event, self.rom, self.args, self.dialogs, self.characters, self.items, self.maps, self.enemies, self.espers, self.shops)
                events.append(event)
                name_event[event.name()] = event

        ### gather gating dictionary, do this in a separate function probably
        ### take out for other CG testings
        if 1 == 1:
            for eventname, event in name_event.items():
                if event.character_gate() != None:
                    self.gatingdict[eventname] = self.characters.get_default_name(event.character_gate())
                else:
                    self.gatingdict[eventname] = "None"
        #print(self.gatingdict)


        # select event rewards        
        if self.args.character_gating:
            # Mod for location tiering
            if self.args.location_tiering:
                self.character_gating_with_location_tiering_mod(events, name_event)
            else:
                self.character_gating_mod(events, name_event)
        else:
            self.open_world_mod(events)

        # initialize event bits, mod events, log rewards
        log_strings = []
        space = Allocate(Bank.CC, 400, "event/npc bit initialization", field.NOP())
        for event in events:
            event.init_event_bits(space)
            event.mod()

            if self.args.spoiler_log and (event.rewards_log or event.changes_log):
                log_strings.append(event.log_string())

            ### if open world+location tiering is on
            if self.args.location_tiering and not self.args.character_gating:
                ### add this to get check path for location/chest rank tiering            
                tempstr = event.log_string()
                checkname = event.name()
                #search the rest of the line to see if a character exists

                ### generate gating dict
                if event.character_gate() != None:
                    self.gatingdict[checkname] = self.characters.get_default_name(event.character_gate())
                else:
                    self.gatingdict[checkname] = "None"

                for x in range(14):
                    #look for each character
                    if tempstr.find(self.characters.get_name(x)) > 0:
                        #combine the checkname and the character
                        self.pathing = self.pathing + "\n" + checkname + ": " + self.characters.get_name(x) + "/ " + self.characters.get_default_name(x)
                        self.pathingdict[self.characters.get_default_name(x)] = checkname
                ### end of loop through each character
            ### end of check if open world+location tiering is on
        ###end of loop through events

        ### if open world+location tiering is on
        if self.args.location_tiering and not self.args.character_gating:
            self.event_depth = self.determine_location_tiering(print_debug=True)

        # generate pathing depth, needed for several mods that depend on
        # knowing charater pathing
        if 1 == 1:
            for event in events:
                for reward in event.rewards:
                    if reward.type == RewardType.CHARACTER:
                        self.pathing = self.pathing + "\n" + event.name() + ": " + self.characters.get_name(reward.id) + "/ " + self.characters.get_default_name(reward.id)
                        self.pathingdict[self.characters.get_default_name(reward.id)] = event.name()
            self.event_depth = self.determine_location_tiering(print_debug=False)


        space.write(field.Return())

        if self.args.spoiler_log:
            from log import section
            section("Events", log_strings, [])

        return events

    def init_reward_slots(self, events):
        import random
        reward_slots = []
        for event in events:
            event.init_rewards()
            for reward in event.rewards:
                if reward.id is None:
                    reward_slots.append(reward)

        random.shuffle(reward_slots)
        return reward_slots

    def choose_single_possible_type_rewards(self, reward_slots):
        for slot in reward_slots:
            if slot.single_possible_type():
                slot.id, slot.type = choose_reward(slot.possible_types, self.characters, self.espers, self.items)

    def choose_char_esper_possible_rewards(self, reward_slots):
        for slot in reward_slots:
            if slot.possible_types == (RewardType.CHARACTER | RewardType.ESPER):
                slot.id, slot.type = choose_reward(slot.possible_types, self.characters, self.espers, self.items)

    def choose_item_possible_rewards(self, reward_slots):
        for slot in reward_slots:
            slot.id, slot.type = choose_reward(slot.possible_types, self.characters, self.espers, self.items)

    def character_gating_mod(self, events, name_event):
        import random
        reward_slots = self.init_reward_slots(events)

        # for every event with only one reward type possible, assign random rewards
        # note: this includes start, which can get up to 4 characters
        self.choose_single_possible_type_rewards(reward_slots)

        # find characters that were assigned to start
        characters_available = [reward.id for reward in name_event["Start"].rewards]

        # find all the rewards that can be a character
        character_slots = []
        for event in events:
            for reward in event.rewards:
                if reward.possible_types & RewardType.CHARACTER:
                    character_slots.append(reward)

        iteration = 0
        slot_iterations = {} # keep track of how many iterations each slot has been available
        while self.characters.get_available_count():

            # build list of which slots are available and how many iterations those slots have already had
            unlocked_slots = []
            unlocked_slot_iterations = []
            for slot in character_slots:
                slot_empty = slot.id is None
                gate_char_available = (slot.event.character_gate() in characters_available or slot.event.character_gate() is None)
                enough_chars_available = len(characters_available) >= slot.event.characters_required()
                if slot_empty and gate_char_available and enough_chars_available:
                    if slot in slot_iterations:
                        slot_iterations[slot] += 1
                    else:
                        slot_iterations[slot] = 0
                    unlocked_slots.append(slot)
                    unlocked_slot_iterations.append(slot_iterations[slot])

            # pick slot for the next character weighted by number of iterations each slot has been available
            slot_index = weighted_reward_choice(unlocked_slot_iterations, iteration)
            slot = unlocked_slots[slot_index]
            slot.id = self.characters.get_random_available()
            slot.type = RewardType.CHARACTER
            characters_available.append(slot.id)
            self.characters.set_character_path(slot.id, slot.event.character_gate())
            iteration += 1

        # get all reward slots still available
        reward_slots = [reward for event in events for reward in event.rewards if reward.id is None]
        random.shuffle(reward_slots) # shuffle to prevent picking them in alphabetical order

        # for every event with only char/esper rewards possible, assign random rewards
        self.choose_char_esper_possible_rewards(reward_slots)

        reward_slots = [slot for slot in reward_slots if slot.id is None]

        # assign rest of rewards where item is possible
        self.choose_item_possible_rewards(reward_slots)
        return

    def open_world_mod(self, events):
        import random
        reward_slots = self.init_reward_slots(events)

        # first choose all the rewards that only have a single type possible
        # this way we don't run out of that reward type before getting to the event
        self.choose_single_possible_type_rewards(reward_slots)

        reward_slots = [slot for slot in reward_slots if not slot.single_possible_type()]

        # next choose all the rewards where only character/esper types possible
        # this way we don't run out of characters/espers before getting to these events
        self.choose_char_esper_possible_rewards(reward_slots)

        reward_slots = [slot for slot in reward_slots if slot.id is None]

        # choose the rest of the rewards, items given to events after all characters/events assigned
        self.choose_item_possible_rewards(reward_slots)


    ### Mod to incorporate location tiering when character gating is on
    def choose_tiered_esper_possible_rewards(self, reward_slots):
        for slot in reward_slots:
            if slot.possible_types == (RewardType.CHARACTER | RewardType.ESPER):
                slot.id, slot.type = choose_tiered_reward(slot.possible_types, self.characters, self.espers, self.items, self.event_depth, slot.event)

    def choose_tiered_item_possible_rewards(self, reward_slots):
        for slot in reward_slots:
            slot.id, slot.type = choose_tiered_reward(slot.possible_types, self.characters, self.espers, self.items, self.event_depth, slot.event)

    def character_gating_with_location_tiering_mod(self, events, name_event):
        import random
        reward_slots = self.init_reward_slots(events)

        # for every event with only one reward type possible, assign random rewards
        # note: this includes start, which can get up to 4 characters
        # ^ this actually happens at "reward_slots = self.init_reward_slots(events)"

        # this assigns every item only reward
        # need to stop that from happening if we are going to use location tiering

        # turns out we don't actually need this to run
        #self.choose_single_possible_type_rewards(reward_slots, name_event)

        # find characters that were assigned to start
        characters_available = [reward.id for reward in name_event["Start"].rewards]

        # find all the rewards that can be a character
        character_slots = []
        for event in events:
            for reward in event.rewards:
                if reward.possible_types & RewardType.CHARACTER:
                    character_slots.append(reward)

        iteration = 0
        slot_iterations = {} # keep track of how many iterations each slot has been available
        while self.characters.get_available_count():

            # build list of which slots are available and how many iterations those slots have already had
            unlocked_slots = []
            unlocked_slot_iterations = []
            for slot in character_slots:
                slot_empty = slot.id is None
                gate_char_available = (slot.event.character_gate() in characters_available or slot.event.character_gate() is None)
                enough_chars_available = len(characters_available) >= slot.event.characters_required()
                if slot_empty and gate_char_available and enough_chars_available:
                    if slot in slot_iterations:
                        slot_iterations[slot] += 1
                    else:
                        slot_iterations[slot] = 0
                    unlocked_slots.append(slot)
                    unlocked_slot_iterations.append(slot_iterations[slot])

            # pick slot for the next character weighted by number of iterations each slot has been available
            slot_index = weighted_reward_choice(unlocked_slot_iterations, iteration)
            slot = unlocked_slots[slot_index]
            slot.id = self.characters.get_random_available()
            slot.type = RewardType.CHARACTER
            characters_available.append(slot.id)
            self.characters.set_character_path(slot.id, slot.event.character_gate())
            iteration += 1


        ### this is the earliest point that pathingdict and event_depth can be determined
        for event in events:
            for reward in event.rewards:
                if reward.type == RewardType.CHARACTER:
                    self.pathing = self.pathing + "\n" + event.name() + ": " + self.characters.get_name(reward.id) + "/ " + self.characters.get_default_name(reward.id)
                    self.pathingdict[self.characters.get_default_name(reward.id)] = event.name()
                    #print(str(event.name()) + " " + self.characters.get_default_name(reward.id))
        self.event_depth = self.determine_location_tiering()

        ### get all reward slots still available
        reward_slots = [reward for event in events for reward in event.rewards if reward.id is None]
        random.shuffle(reward_slots) # shuffle to prevent picking them in alphabetical order

        # self.print_event_rewards(events)   #verify which reward slots are left
        
        ### for every event with only char/esper rewards possible, assign random rewards
        #self.choose_char_esper_possible_rewards(reward_slots)

        ### since we already have all the characters figured out
        ### choose_tiered_esper_possible_rewards only assigns Espers to C/E slots
        self.choose_tiered_esper_possible_rewards(reward_slots)

        #self.print_event_rewards(events)   #verify which reward slots are left
        
        reward_slots = [slot for slot in reward_slots if slot.id is None]

        ### assign rest of rewards where item is possible
        #self.choose_item_possible_rewards(reward_slots)
        ### this assigns all remaining Esper/Item rewards

        self.choose_tiered_item_possible_rewards(reward_slots)
        
        return

    def print_event_rewards(self, events):
        for event in events:
            for reward in event.rewards:
                print(event.name() + " | " + str(reward.id) + " | " + str(reward.type))
    ### End of: Mod to incorporate location tiering when character gating is on

    ### Mod for location tiering
    ### not sure how to handle Floating Continent, as the final sequence
    ### could be considered another level of depth a la Narshe Battle
    def determine_location_tiering(self, print_debug=True):
        #print_debug = True
        #print(self.gatingdict)
        #print(self.pathing)
        #print(self.pathinglist)
        #print(self.pathingdict)
        pathway_with_chars_list = []
        pathway_list = []
        character_depth = {}
        
        for x in range(14):
        #for char_index in range(self.CHARACTER_COUNT):
            path = self.characters.get_character_path(x)
            pathway_with_chars = ""
            pathway = ""
            
            char_depth = 1
            ### get the path leading to the character's location
            for req_char_index in path:
                #character_location = events.pathingdict[self.characters.DEFAULT_NAME[req_char_index]]
                character_location = self.pathingdict[self.characters.DEFAULT_NAME[req_char_index]]
                character_name = self.characters.DEFAULT_NAME[req_char_index]
                ### check for Narshe Battle in the sequence (since it defaults to an inherent depth of 0, we need to increment it by 1)
                if character_location == "Narshe Battle":
                    char_depth += 1                
                pathway += character_location + " -> "
                pathway_with_chars += (character_name + " / " + character_location + " -> ")
                char_depth += 1

            ### get the character's location
            character_location = self.pathingdict[self.characters.DEFAULT_NAME[x]]
            character_name = self.characters.DEFAULT_NAME[x]
            ### check for Narshe Battle as it defaults to an inherent depth of 0
            if character_location == "Narshe Battle":
                char_depth += 1                    
            character_depth[character_name] = char_depth
            pathway += character_location
            pathway_with_chars += (character_name + " / " + character_location)

            if print_debug:
                print(pathway_with_chars)
            pathway_with_chars_list.append(pathway_with_chars)
            pathway_list.append(pathway)

        if print_debug:
            print(character_depth)
        self.character_depth = character_depth
        
        event_depth = {}
        max_depth = 0
        ### for each event in gatingdict, apply a depth value using character_depth
        for event_name, char_gate in self.gatingdict.items():
            if char_gate == "None":
                event_depth[event_name] = 1
            else:
                event_depth[event_name] = character_depth[char_gate]

            if event_depth[event_name] > max_depth:
                max_depth = event_depth[event_name]

        ### KT gets one more level of depth. don't have to necessarily do this since
        ### KT access is gated by 3 characters
        for event_name, depth in event_depth.items():
            if event_name == "Kefka's Tower":
                event_depth[event_name] = max_depth+1
            if print_debug:
                print(str(event_name) + " : " + str(depth))

        return event_depth
    ### End of: Mod for location tiering


    def validate(self, events):
        char_esper_checks = []
        for event in events:
            char_esper_checks += [r for r in event.rewards if r.possible_types == (RewardType.CHARACTER | RewardType.ESPER)]

        assert len(char_esper_checks) == CHARACTER_ESPER_ONLY_REWARDS, "Number of char/esper only checks changed - Check usages of CHARACTER_ESPER_ONLY_REWARDS and ensure no breaking changes"
