from memory.space import Bank, Reserve, Allocate, Write, Read
import instruction.asm as asm
import args

class XMagicMenu:
    def __init__(self):
        self.mod()

    def mod(self):
        space = Allocate(Bank.C3, 14, "x-magic user use magic menu")
        xmagic_user_use_menu_magic = space
        space.write(
            asm.CMP(0xC34D78, asm.LNG_X),
            asm.BEQ(0x07),
            asm.CPX(0x0001, asm.IMM16),
            asm.BNE(0x02), 
            asm.CMP(0x17, asm.IMM8),
            asm.RTL(),
        )
        #space.printr()
        
        xmagic_addr = xmagic_user_use_menu_magic.start_address
        space = Reserve(0x34d56, 0x34d5a, "magic menu check")
        space.write(
            asm.JSL(xmagic_addr),
        )

##        space.write(
##            [0xDF, 0x78, 0x4D, 0xC3,  # CMP $C34D78,X
##            0xF0, 0x07,  # BEQ
##            0xE0, 0x01, 0x00,  # CPX #$0001
##            0xD0, 0x02,  # BNE
##            0xC9, 0x17,  # CMP #$17
##            0x6B]  # RTL
##        )
        #space.write([0xDF, 0x78, 0x4D, 0xC3, 0x6B])
        #space.write(0x6B)


##    # Let x-magic user use magic menu.
##    enable_xmagic_menu_sub = Substitution()
##    enable_xmagic_menu_sub.bytestring = bytes([0xDF, 0x78, 0x4D, 0xC3,  # CMP $C34D78,X
##                                               0xF0, 0x07,  # BEQ
##                                               0xE0, 0x01, 0x00,  # CPX #$0001
##                                               0xD0, 0x02,  # BNE
##                                               0xC9, 0x17,  # CMP #$17
##                                               0x6b  # RTL
##                                               ])
##    enable_xmagic_menu_sub.set_location(0x3F091)
##    enable_xmagic_menu_sub.write(fout)
##
##    enable_xmagic_menu_sub.bytestring = bytes([0x22, 0x91, 0xF0, 0xC3])
##    # 0x22 - JSL, LNG format mode opcode
##    # 0x91 - 
##    # 0xF0 - 
##    # 0xC3 - 0xC3F091
##
##    # original 0x34d56: C3/4D56:	DF784DC3	CMP $C34D78,X
##    enable_xmagic_menu_sub.set_location(0x34d56)
##    enable_xmagic_menu_sub.write(fout)
