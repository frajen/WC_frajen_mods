from data.map_exit import ShortMapExit, LongMapExit
from data.map_exit_extra import exit_data_patch

from data.map_event import MapEvent
from data.rooms import room_data, force_update_parent_map

from instruction import field

from memory.space import Allocate, Bank, Write

class MapExits():
    SHORT_EXIT_COUNT = 0x469
    LONG_EXIT_COUNT = 0x98

    SHORT_DATA_START_ADDR = 0x1fbf02
    LONG_DATA_START_ADDR = 0x2df882

    def __init__(self, rom):
        self.rom = rom
        self.short_exits = []
        self.long_exits = []
        self.exit_original_data = {}
        self.exit_type = {}

        self.read()

    def read(self):
        global_counter = 0
        for exit_index in range(self.SHORT_EXIT_COUNT):
            exit_data_start = self.SHORT_DATA_START_ADDR + exit_index * ShortMapExit.DATA_SIZE
            exit_data = self.rom.get_bytes(exit_data_start, ShortMapExit.DATA_SIZE)

            new_exit = ShortMapExit()
            new_exit.from_data(exit_data)
            # added for exit rando mod
            new_exit.index = global_counter

            # fix Doma Dream Interior exit being off 1 tile
            if new_exit.index == 441:
                new_exit.x = 17
                
            global_counter = global_counter + 1
            # added for exit rando mod
            self.short_exits.append(new_exit)
            self.exit_type[new_exit.index] = 'short'

            # Archive original data for randomizing
            self.exit_original_data[new_exit.index] = [new_exit.dest_x, new_exit.dest_y, new_exit.dest_map,
                                                              new_exit.refreshparentmap, new_exit.enterlowZlevel,
                                                              new_exit.displaylocationname, new_exit.facing,
                                                              new_exit.unknown]

        for exit_index in range(self.LONG_EXIT_COUNT):
            exit_data_start = self.LONG_DATA_START_ADDR + exit_index * LongMapExit.DATA_SIZE
            exit_data = self.rom.get_bytes(exit_data_start, LongMapExit.DATA_SIZE)

            new_exit = LongMapExit()
            new_exit.from_data(exit_data)
            # added for exit rando mod
            new_exit.index = global_counter
            global_counter = global_counter + 1
            # added for exit rando mod
            self.long_exits.append(new_exit)
            self.exit_type[new_exit.index] = 'long'

            # Archive original data for randomizing
            self.exit_original_data[new_exit.index] = [new_exit.dest_x, new_exit.dest_y, new_exit.dest_map,
                                                       new_exit.refreshparentmap, new_exit.enterlowZlevel,
                                                       new_exit.displaylocationname, new_exit.facing,
                                                       new_exit.unknown]

        # For door mapping to work, all exits must be explicit (i.e. patch out "return to parent map").
        for e in exit_data_patch.keys():
            # Update the "original data"
            self.exit_original_data[e] = exit_data_patch[e](self.exit_original_data[e])
            # Copy the "original data" to the exit itself
            self.copy_exit_info(self._get_exit_from_ID(e), e)

    def write(self):
        for exit_index, exit in enumerate(self.short_exits):
            exit_data = exit.to_data()
            exit_data_start = self.SHORT_DATA_START_ADDR + exit_index * ShortMapExit.DATA_SIZE
            self.rom.set_bytes(exit_data_start, exit_data)

        for exit_index, exit in enumerate(self.long_exits):
            exit_data = exit.to_data()
            exit_data_start = self.LONG_DATA_START_ADDR + exit_index * LongMapExit.DATA_SIZE
            self.rom.set_bytes(exit_data_start, exit_data)

    def mod(self):
        pass

    def _get_exit_from_ID(self, exitID):
        if self.exit_type[exitID] == 'short':
            exit = self.short_exits[exitID]  # Exit = short exit
        else:
            exit = self.long_exits[exitID - self.SHORT_EXIT_COUNT]  # Exit = long exit
        return exit

    def copy_exit_info(self, mod_exit, pair_ID):
        # Copy information to mod_exit from another exit with exitID = pair_ID.
        # Original door data is stored in self.exit_original_data[exitID] as:
        #   [dest_x, dest_y, dest_map, refreshparentmap, enterlowZlevel, displaylocationname, facing, unknown]
        pair_info = self.exit_original_data[pair_ID]
        mod_exit.dest_x = pair_info[0]
        mod_exit.dest_y = pair_info[1]
        mod_exit.dest_map = pair_info[2]
        # mod_exit.refreshparentmap = pair_info[3]  # do not want to copy refresh parent map!  Messes up warp stones.
        mod_exit.enterlowZlevel = pair_info[4]
        mod_exit.displaylocationname = pair_info[5]
        mod_exit.facing = pair_info[6]
        mod_exit.unknown = pair_info[7]
        return

    def print_short_exit_range(self, start, count):
        for offset in range(count):
            self.short_exits[start + offset].print()

    def print_long_exit_range(self, start, count):
        for offset in range(count):
            self.long_exits[start + offset].print()

    def get_short_exit(self, search_start, search_end, x, y):
        for exit in self.short_exits[search_start:search_end + 1]:
            if exit.x == x and exit.y == y:
                return exit
        raise IndexError(f"get_short_exit: could not find short exit at {x} {y}")

    def get_long_exit(self, search_start, search_end, x, y):
        for exit in self.long_exits[search_start:search_end + 1]:
            if exit.x == x and exit.y == y:
                return exit
        raise IndexError(f"get_long_exit: could not find long exit at {x} {y}")

    def delete_short_exit(self, search_start, x, y):
        for exit in self.short_exits[search_start:]:
            if exit.x == x and exit.y == y:
                self.short_exits.remove(exit)
                self.SHORT_EXIT_COUNT -= 1
                return

    def print(self):
        for short_exit in self.short_exits:
            short_exit.print()

        for long_exit in self.long_exits:
            long_exit.print()
