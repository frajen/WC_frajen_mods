from memory.space import *
from event import *

def main():
    import args
    import log

    from memory.memory import Memory
    memory = Memory()

    from data.data import Data
    data = Data(memory.rom, args)

    from event.events import Events
    events = Events(memory.rom, args, data)

    from menus.menus import Menus
    menus = Menus(data.characters, data.dances, data.rages, data.enemies)

    from battle import Battle
    battle = Battle()

    from settings import Settings
    settings = Settings()

    from bug_fixes import BugFixes
    bug_fixes = BugFixes()

    #data.write()
    data.write(events, memory.rom, args)
    memory.write()
    
    #print(Space.heaps)
    #Space.bank_space_available()
##    space = Read(0x0B9AC9, 0x0B9AD6)
##    #space = Read(0x000000, 0x001000)
##    hex_array = [hex(x)[2:] for x in space]
##    print(hex_array)
##    print(len(hex_array))
##    printer = Allocate(Bank.FF, len(space), "none")
##    printer.write(space)
##    printer.printr()

if __name__ == '__main__':
    main()
