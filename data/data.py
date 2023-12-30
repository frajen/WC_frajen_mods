import data.dialogs as dialogs
import data.spells as spells
import data.characters as characters
import data.items as items
import data.metamorph_groups as metamorph_groups
import data.maps as maps
import data.enemies as enemies
import data.swdtechs as swdtechs
import data.blitzes as blitzes
import data.lores as lores
import data.rages as rages
import data.dances as dances
import data.steal as steal
import data.sketches as sketches
import data.controls as controls
import data.magiteks as magiteks
import data.espers as espers
import data.shops as shops
import data.coliseum as coliseum
import data.title_graphics as title_graphics

class Data:
    def __init__(self, rom, args):
        self.dialogs = dialogs

        self.spells = spells.Spells(rom, args)
        self.spells.mod()

        self.characters = characters.Characters(rom, args, self.spells)
        self.characters.mod()

        self.items = items.Items(rom, args, self.dialogs, self.characters)
        self.items.mod()

        self.metamorph_groups = metamorph_groups.MetamorphGroups(rom)
        self.metamorph_groups.mod()

        self.maps = maps.Maps(rom, args, self.items)
        self.maps.mod(self.characters)

        ### Mod to more easily make item randomization available for monsters
        self.enemies = enemies.Enemies(rom, args)
        #self.enemies = enemies.Enemies(rom, args, self.items)
        self.enemies.mod(self.maps)

        ### location based command tiering
        if not args.location_tiering:
            self.swdtechs = swdtechs.SwdTechs(rom, args, self.characters)
            self.swdtechs.mod()

            self.blitzes = blitzes.Blitzes(rom, args, self.characters)
            self.blitzes.mod()
            
            self.lores = lores.Lores(rom, args, self.characters)
            self.lores.mod(self.dialogs)
        ### location based command tiering

        ### Rages and Dances need to be run for Menus
        self.rages = rages.Rages(rom, args, self.enemies)
        self.rages.mod()
            
        self.dances = dances.Dances(rom, args, self.characters)
        self.dances.mod()

        self.steal = steal.Steal(rom, args)
        self.steal.mod()

        self.sketches = sketches.Sketches(rom, args, self.enemies, self.rages)
        self.sketches.mod()

        self.controls = controls.Controls(rom, args, self.enemies, self.rages)
        self.controls.mod()

        self.magiteks = magiteks.Magiteks(rom, args)
        self.magiteks.mod()

        self.espers = espers.Espers(rom, args, self.spells, self.characters)
        self.espers.mod(self.dialogs)

        self.shops = shops.Shops(rom, args, self.items)
        self.shops.mod()

        self.coliseum = coliseum.Coliseum(rom, args, self.enemies, self.items)
        self.coliseum.mod()

        self.title_graphics = title_graphics.TitleGraphics(rom, args)
        self.title_graphics.mod()

##    ### Location tiering
##    def determine_location_tiering(self, events):
##        print_debug = True
##        pathway_with_chars_list = []
##        pathway_list = []
##        character_depth = {}
##        
##        for x in range(14):
##        #for char_index in range(self.CHARACTER_COUNT):
##            path = self.characters.get_character_path(x)
##            pathway_with_chars = ""
##            pathway = ""
##            
##            char_depth = 1
##            ### get the path leading to the character's location
##            for req_char_index in path:
##                character_location = events.pathingdict[self.characters.DEFAULT_NAME[req_char_index]]
##                character_name = self.characters.DEFAULT_NAME[req_char_index]
##                ### check for Narshe Battle in the sequence (since it defaults to an inherent depth of 0, we need to increment it by 1)
##                if character_location == "Narshe Battle":
##                    char_depth += 1                
##                pathway += character_location + " -> "
##                pathway_with_chars += (character_name + " / " + character_location + " -> ")
##                char_depth += 1
##
##            ### get the character's location
##            character_location = events.pathingdict[self.characters.DEFAULT_NAME[x]]
##            character_name = self.characters.DEFAULT_NAME[x]
##            ### check for Narshe Battle as it defaults to an inherent depth of 0
##            if character_location == "Narshe Battle":
##                char_depth += 1                    
##            character_depth[character_name] = char_depth
##            pathway += character_location
##            pathway_with_chars += (character_name + " / " + character_location)
##
##            if print_debug:
##                print(pathway_with_chars)
##            pathway_with_chars_list.append(pathway_with_chars)
##            pathway_list.append(pathway)
##
##        if print_debug:
##            print(character_depth)
##
##        event_depth = {}
##        max_depth = 0
##        ### for each event in gatingdict, apply a depth value using character_depth
##        for event_name, char_gate in events.gatingdict.items():
##            if char_gate == "None":
##                event_depth[event_name] = 1
##            else:
##                event_depth[event_name] = character_depth[char_gate]
##
##            if event_depth[event_name] > max_depth:
##                max_depth = event_depth[event_name]
##
##        for event_name, depth in event_depth.items():
##            if event_name == "Kefka's Tower":
##                event_depth[event_name] = max_depth+1
##            if print_debug:
##                print(str(event_name) + " : " + str(depth))
##
##        return event_depth

    def modify_chests_using_location_tier(self, event_depth):
        self.maps.chests.chest_location_tier(event_depth)        

    # bring in the results of events
    #def write(self):
    def write(self, events, rom, args):

        ### forced commands onto starting characters
        if args.force_start_commands:
            #print(events.pathingdict)
            self.characters.commands.mod_starting_slot_commands(events.pathingdict)

        ### location tiering
        if args.location_tiering:
            self.characters.mod_tiered_init_levels(events.character_depth)
            self.characters.commands.mod_tiered_commands(events.character_depth)
            self.modify_chests_using_location_tier(events.event_depth)

        self.dialogs.write()

        ### Experimental - re-run these if location tiering
        if args.location_tiering:
            self.swdtechs = swdtechs.SwdTechs(rom, args, self.characters)
            self.swdtechs.mod()

            self.blitzes = blitzes.Blitzes(rom, args, self.characters)
            self.blitzes.mod()
            
            self.lores = lores.Lores(rom, args, self.characters)
            self.lores.mod(self.dialogs)
        ### re-run these if location tiering            

        self.characters.write()
        self.items.write()
        self.metamorph_groups.write()
        self.maps.write()
        self.enemies.write()
        self.spells.write()
        self.swdtechs.write()
        self.blitzes.write()
        self.lores.write()
        self.rages.write()
        self.dances.write()
        self.steal.write()
        self.sketches.write()
        self.controls.write()
        self.magiteks.write()
        self.espers.write()

        # Experimental: call this again if you want all mods from spells.py to take effect
        # self.spells.write()
        # example: step mine power change is overwritten by self.lores.write()
        
        self.shops.write()
        self.coliseum.write()
        self.title_graphics.write()
