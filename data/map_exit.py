class ShortMapExit():
    DATA_SIZE = 0x06

    def __init__(self):
        self.x = 0
        self.y = 0

        ### mod for door rando, sync up with longmapexit
        self.size = 0
        self.direction = 0
        self.index = 0
        self.parent_map = 0
        self.parent_room = 0

        self.doorpair = 0   #requires external lookup

        # when swapping with another exit, these are the coords THAT exit should go to
        #self.doorpair_map = 0   #requires external lookup
        self.doorpair_x = 0   #requires external lookup
        self.doorpair_y = 0   #requires external lookup
        self.doorpair_facing = 0   #requires external lookup
        ### mod for door rando, sync up with longmapexit

    def from_data(self, data):
        assert(len(data) == self.DATA_SIZE)

        self.x = data[0]
        self.y = data[1]
        self.dest_map = data[2] | (data[3] & 0x01) << 8

        ### get extra details for door rando mod
        self.refreshparentmap = (data[3] & 0x02) >> 1
        self.enterlowZlevel = (data[3] & 0x04) >> 2
        self.displaylocationname = (data[3] & 0x08) >> 3
        self.facing = (data[3] & 0x30) >> 4  #0 = north, 1 = east, 2 = south, 3 = west
        #self.unknown = data[3] & 0xfe #original
        self.unknown = data[3] & 0xC0
        ### get extra details for door rando mod

        self.dest_x = data[4]
        self.dest_y = data[5]

    def to_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0] = self.x
        data[1] = self.y
        data[2] = self.dest_map & 0xff
        data[3] = ((self.dest_map & 0x100) >> 8) | self.unknown

        ### mod for door rando
        data[3] |= self.refreshparentmap << 1
        data[3] |= self.enterlowZlevel << 2
        data[3] |= self.displaylocationname << 3
        data[3] |= self.facing << 4
        ### mod for door rando
        
        data[4] = self.dest_x
        data[5] = self.dest_y

        return data

    def print(self):
        print("{}, {} -> {}: {}, {} ({})".format(self.x, self.y, hex(self.dest_map), self.dest_x, self.dest_y, hex(self.unknown)))

        # more details for door rando printout
##        print(str(self.x) + " | " + str(self.y) + " | " + str(self.dest_map) + " | " +
##          str(self.dest_x) + " | " + str(self.dest_y) + " | " + str(self.facing) + " | " + 
##          str(self.displaylocationname) + " | " + str(self.refreshparentmap) + " | " +
##          str(self.unknown) + " | " + str(self.size) + " | " + str(self.direction) + " | " +
##          str(self.index))

class LongMapExit():
    DATA_SIZE = 0x07

    def __init__(self):
        self.x = 0
        self.y = 0

        ### mod for exit rando
        # safe_x/y are used for swapping xy coords, 
        # so you don't get sent to out of bounds tiles
        self.safe_x = 0  
        self.safe_y = 0
        self.index = 0

        self.parent_map = 0
        self.doorpair = 0   #requires external lookup
        ### mod for exit rando

    def from_data(self, data):
        assert(len(data) == self.DATA_SIZE)

        self.x = data[0]
        self.y = data[1]
        self.size = data[2] & 0x7f  #tile length
        self.direction = data[2] & 0x80 # horizontal/vertical
        self.dest_map = data[3] | (data[4] & 0x01) << 8

        ### get extra details for door rando mod
        self.refreshparentmap = (data[4] & 0x02) >> 1
        self.enterlowZlevel = (data[4] & 0x04) >> 2
        self.displaylocationname = (data[4] & 0x08) >> 3
        self.facing = (data[4] & 0x30) >> 4  #0 = north, 1 = east, 2 = south, 3 = west
        #self.unknown = data[4] & 0xFE  #original
        self.unknown = data[4] & 0xC0
        ### get extra details for door rando mod

        self.unknown = data[4] & 0xfe
        self.dest_x = data[5]
        self.dest_y = data[6]

    def to_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0] = self.x
        data[1] = self.y
        data[2] = self.size | self.direction
        data[3] = self.dest_map & 0xff
        data[4] = ((self.dest_map & 0x100) >> 8) | self.unknown

        ### mod for door rando
        data[4] = ((self.dest_map & 0x100) >> 8) | self.unknown
        data[4] |= self.refreshparentmap << 1
        data[4] |= self.enterlowZlevel << 2
        data[4] |= self.displaylocationname << 3
        data[4] |= self.facing << 4
        ### mod for door rando
        
        data[5] = self.dest_x
        data[6] = self.dest_y

        return data

    def print(self):
        print("{}, {} {}, {} -> {}: {}, {}".format(self.x, self.y, self.size, self.direction, hex(self.dest_map), self.dest_x, self.dest_y))


        # more details for door rando printout
##        print(str(self.x) + " | " + str(self.y) + " | " + str(self.dest_map) + " | " +
##              str(self.dest_x) + " | " + str(self.dest_y) + " | " + str(self.facing) + " | " + 
##              str(self.displaylocationname) + " | " + str(self.refreshparentmap) + " | " +
##              str(self.unknown) + " | " + str(self.size) + " | " + str(self.direction) + " | " +
##              str(self.index))
