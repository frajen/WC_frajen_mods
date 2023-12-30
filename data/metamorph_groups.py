from data.metamorph_group import MetamorphGroup
from data.structures import DataArray
from data.item_names import name_id
import args

class MetamorphGroups:
    DATA_START = 0x047f40
    DATA_END = 0x047fa7

    def __init__(self, rom):
        self.rom = rom
        self.data = DataArray(self.rom, self.DATA_START, self.DATA_END, MetamorphGroup.DATA_SIZE)

        self.groups = []
        for index in range(len(self.data)):
            group = MetamorphGroup(index, self.data[index])
            self.groups.append(group)

    def remove_fenix_downs(self):
        self.groups[1].items[1] = name_id["Potion"] # replace with potion

    def remove_exp_eggs(self):
        self.groups[18].items[3] = name_id["Rename Card"] # replace with rename card

    ### remove ultimate items from metamorphs
    def remove_ultimate_items(self):
        from data.items import ULTS_ID as ultimate_ids
        for index, group in enumerate(self.groups):
            for items in group.items:
                if items in ultimate_ids:
                    items = name_id["Potion"]
    ### remove ultimate items from metamorphs

    def mod(self):
        if args.permadeath:
            self.remove_fenix_downs()

        if args.no_exp_eggs:
            self.remove_exp_eggs()

        # remove ultimate items from metamorphs
        if args.ultimate_items:
            self.remove_ultimate_items()


    def write(self):
        for index, group in enumerate(self.groups):
            self.data[index] = group.data()

        self.data.write()
