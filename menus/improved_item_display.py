from memory.space import Bank, Reserve, Allocate, Write, Read
import instruction.asm as asm
import args

class ImprovedItemDisplay:
    def __init__(self):
        self.mod()

    def mod(self):
        # adr -> moved from F0 to F2
        # adr+ -> moved from F0 to F2 for ragedance stuff
        
        #display_sub.set_location(0x38706)
        #display_sub.bytestring = bytes([0x22, 0x03, 0x00, 0xF0])
        # adjust C3/8706 to JSL (0x22) jump to F0 (F00003)
        
        #display_sub.set_location(0x389E6)
        #display_sub.bytestring = bytes([0x22, 0x2C, 0x00, 0xF0])
        # adjust C3/89E6 to JSL jump to F0 (F0002C)

##        common_sub.set_location(0x300000)
##        common_sub.bytestring = bytes([
##            0xF2, 0x1B, # SBC $1B
##            0xF0, 0xDA, # BEQ
        # this might be commented wrong. F00003 goes right to 0xDA which
        # is PHX

#Original:
#Fork: Draw defensive properties
#C3/8703:	AE3421  	LDX $2134      ; Item index
#C3/8706:	BF0050D8	LDA $D85000,X  ; Properties        
        space = Reserve(0x38706, 0x38709, "jump to new common menu")
        space.write(
            asm.JSL(0xf20003),
        )
#Original:
#5E: Sustain shifted gear data menu
#C3/89E6:	A509    	LDA $09        ; No-autofire keys
#C3/89E8:	8980    	BIT #$80       ; Pushing B?
        space = Reserve(0x389e6, 0x389e9, "jump to new common menu 2")
        space.write(
            asm.JSL(0xf2002c),
        )

##        space = Reserve(0x325000, 0x32500a, "load and")
##        space.write(
##            asm.LDA(0xd85012, asm.LNG_X),
##            #asm.AND(0xff, asm.IMM16),
##            asm.JSL(0xf200be)
##        )
##        space.printr()
##        calc_addr = space.start_address

#[0x30413f - 0x3041ba] "BC common menu" : takes up 7C
#note that in the BC version it begins with:
    #0xF2, 0x1B, # SBC $1B
    #0xF0, 0xDA, # BEQ
#it seems like these were not needed for WC purposes, since:
    #display_sub.set_location(0x38706)
    #display_sub.bytestring = bytes([0x22, 0x03, 0x00, 0xF0])        
#is a JSL to F0/0003

        #F00003 in BC
        space = Reserve(0x320003, 0x32007f, "BC common menu")
        space.write(
        #src = [
            ### Independent section
            asm.PHX(), # push X to stack
            asm.PHY(), #0x5A, # PHX <- commented wrong, should be PHY / push Y to stack
            asm.TDC(), # terminator
            asm.PHD(), # push D to stack
            asm.PEA(0x1500), # 1500 to stack
            asm.PLD(), # 1500 to register D
            asm.REP(0x20), # 16-bit A
            asm.LDA(0x2134, asm.ABS), # Load item index
            #HDMA Tables: $808F-$80E8 Saved Main/Sub Screen Designation HDMA Table (+212C)
            #https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:ram:field_ram
            asm.STA(0x7e80e8, asm.LNG), # store accum info
            asm.STA(0x08, asm.DIR), # button press? / https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:ram:menu_ram
            asm.SEP(0x20), # 8-bit A
            asm.LDA(0x00, asm.IMM8), 
            asm.STA(0x7e80ea, asm.LNG), # store accum info
            asm.STA(0x0a, asm.DIR),
            asm.JSL(0xF20080),   # adr
            asm.PLD(), # pull stack
            asm.PLY(), # pull stack
            asm.PLX(), # pull stack
            asm.LDA(0xd85000, asm.LNG_X), #get item properties
            asm.RTL(), #return
            ### End independent section
            
            # new jump point from C3/89E6 (F0002C)
            asm.PHX(), #push to stack
            asm.PHY(),
            asm.TDC(),
            asm.PHD(),
            asm.PEA(0x1500),
            asm.PLD(),
            asm.REP(0x20),
            asm.LDA(0x7e80e8, asm.LNG),
            asm.STA(0x08, asm.DIR),
            asm.SEP(0x20),
            asm.LDA(0x7e80ea, asm.LNG),
            asm.STA(0x0a, asm.DIR),
            asm.JSL(0xF20080),   # adr

            
            asm.TAX(), # transfer A to X
            asm.LDA(0x000b, asm.ABS),
            asm.BIT(0x08, asm.IMM8),

            #asm.BEQ(0xF0005F),   # this needs to be changed
            asm.BEQ("F0005F"),
            asm.LDA(0x7e80ea, asm.LNG),
            asm.BPL(0x0009),
            asm.INC(),
            asm.STA(0x7e80ea, asm.LNG),
            asm.JSL(0xF21932),  # adr+ / jump to BC rage menu section

            "F0005F",
            asm.LDA(0x000b, asm.ABS),
            asm.BIT(0x04, asm.IMM8),
            #asm.BEQ(0xF00078),  # this needs to be changed
            asm.BEQ("F00078"),
            asm.CPX(0x0004, asm.IMM16),
            asm.BCC(0x000d),
            asm.LDA(0x7e80ea, asm.LNG),
            asm.DEC(),
            asm.STA(0x7e80ea, asm.LNG),
            asm.JSL(0xF21932),  # adr+ / jump to BC rage menu section

            "F00078",
            asm.PLD(),
            asm.PLY(),
            asm.PLX(),
            asm.LDA(0x09, asm.DIR),
            asm.BIT(0x80, asm.IMM8),
            asm.RTL(),
        #]
        )
        #space = Write(Bank.F0, src, "BC common menu")
        space.printr()


#[0x3041bb - 0x30486d] "BC improved item display" : takes up 6B4
        #F00080 in BC
        space = Reserve(0x320080, 0x320734, "BC improved item display 1")
        #src = [
        space.write(
            "F00080",
            asm.STZ(0x0b, asm.DIR),
            asm.LDA(0x0a, asm.DIR),
            asm.STA(0x0c, asm.DIR),
            asm.STZ(0x0d, asm.DIR),
            asm.LDX(0x08, asm.DIR),
            asm.STX(0x0e, asm.DIR),
            asm.LDX(0x0019, asm.IMM16),
            asm.LDA(0x00, asm.IMM8),
            "BPL Loop",
            asm.STA(0x7e80ef, asm.LNG_X), # store accum info
            asm.STA(0x7e812f, asm.LNG_X),
            asm.STA(0x7e816f, asm.LNG_X),
            asm.STA(0x7e81af, asm.LNG_X),
            asm.DEX(), #decrement X
            asm.BPL(0x00ed),
            asm.LDX(0x0e, asm.DIR),
            # this pulls the proc bit for weapon which in BC
            # in BC this been moved from D85013, bit 04
            # but in vanilla it should be at D85012, bit 40
            #asm.LDA(0xd85013, asm.LNG_X),
            #asm.BIT(0x04, asm.IMM8),

            asm.LDA(0xd85012, asm.LNG_X),
            asm.BIT(0x40, asm.IMM8),
            #asm.BEQ(0xF000C8),  # this needs to be changed
            asm.BEQ(0x1a),  # go to No_proc if bit is not set
            asm.INC(0x0c, asm.DIR),
            asm.LDA(0x0c, asm.DIR),
            #asm.BMI(0xF000C8),  # this needs to be changed
            asm.BMI("No_proc"),
            asm.CMP(0x04, asm.IMM8),            
            #asm.BCS(0xF000C8),   # this needs to be changed
            asm.BCS("No_proc"),

            # this pulls the proc'd spell from D85012
            # we need to just pull the bits up to 3F, get rid of the 2 NOPs after
            asm.LDA(0xd85012, asm.LNG_X),
            asm.AND(0x3f, asm.IMM8),
            #asm.NOP(),
            #asm.NOP(),
            asm.STA(0x11, asm.DIR),
            asm.LDA(0x0c, asm.DIR),
            asm.STA(0x10, asm.DIR),
            asm.JSL(0xF206C1),
            "No_proc",  #F000C8
            asm.LDX(0x08, asm.DIR),
            asm.TXY(),
            asm.INY(),
            asm.STY(0x08, asm.DIR),
            asm.LDA(0xd85005, asm.LNG_X), #get item field effects
            asm.SEC(),
            asm.ROR(),
            asm.STA(0x0d, asm.DIR),
            "F000D6",
            asm.INC(0x0b, asm.DIR),
            asm.BCC(0x0021),
            asm.INC(0x0c, asm.DIR),
            asm.BMI("F00F0B"),   # this needs to be changed
            asm.BEQ("F00F0B"),   # this needs to be changed
            asm.LDA(0x0c, asm.DIR),
            asm.CMP(0x04, asm.IMM8),
            asm.BCS("F00F0B"),   # this needs to be changed
            asm.LDA(0x0b, asm.DIR),
            "F000E8",
            asm.DEC(),
            asm.STA(0x11, asm.DIR),
            asm.LDA(0x0c, asm.DIR),
            asm.STA(0x10, asm.DIR),
            asm.JSL(0xF205E8),   # adr
            asm.LDA(0x00, asm.IMM8),
            asm.ADC(0x0c, asm.DIR),
            asm.STA(0x0c, asm.DIR),
            asm.BRA("F00F0B"),   # this needs to be changed
            "F00F0B",
            asm.LSR(0x0d, asm.DIR),
            asm.BNE("F000D6"),
            asm.LDA(0x0b, asm.DIR),
            asm.CMP(0x48, asm.IMM8),
            asm.BEQ("F0010B"),
            asm.CMP(0x50, asm.IMM8),
            asm.BNE("No_proc"),
            asm.BRA("F0011C"),
            "F0010B",
            asm.REP(0x20),
            asm.LDA(0x08, asm.DIR),
            asm.CLC(),
            asm.ADC(0x000b, asm.IMM16),
            asm.STA(0x08, asm.DIR),
            asm.LDA(0x0000, asm.IMM16),
            asm.SEP(0x20),
            asm.BRA("No_proc"),
            "F0011C",
            asm.LDA(0x0c, asm.DIR),
            asm.CMP(0x04, asm.IMM8),
            asm.BCS("F00155"),
            asm.LDX(0x08, asm.DIR),
            asm.LDA(0xd85006, asm.LNG_X),
            asm.LSR(),
            asm.LSR(),
            asm.LSR(),
            asm.LSR(),
            asm.BEQ("F00155"),
            asm.DEC(),
            asm.ASL(),
            asm.TAX(),
            asm.INC(0x0c, asm.DIR),
            asm.LDA(0x0c, asm.DIR),
            asm.REP(0x20),
            asm.AND(0x00ff, asm.IMM16),
            asm.XBA(),
            asm.LSR(),
            asm.LSR(),
            asm.ADC(0x80ef, asm.IMM16),
            asm.STA(0x23, asm.DIR),
            asm.LDA(0xF20502, asm.LNG_X), # adr
            asm.STA(0x20, asm.DIR),
            asm.LDA(0x0000, asm.IMM16),
            asm.SEP(0x20),
            #asm.LDA(0xf0, asm.IMM8),
            asm.LDA(0xf2, asm.IMM8),  #adr
            asm.STA(0x22, asm.DIR),
            asm.JSL(0xF2188A), #adr
            "F00155",
            asm.LDA(0x0c, asm.DIR),
            asm.SEC(),
            asm.SBC(0x0a, asm.DIR),
            asm.BEQ("F00169"),
            asm.CMP(0x04, asm.IMM8),
            asm.BCS("F00173"),
            asm.CMP(0x01, asm.IMM8),
            asm.BEQ("F0016E"),
            asm.LDX(0x05c8, asm.IMM16),
            asm.BRA("F00176"),
            "F00169",
            asm.LDX(0x05b6, asm.IMM16),
            asm.BRA("F00176"),
            "F0016E",
            asm.LDX(0x05c0, asm.IMM16),
            asm.BRA("F00176"),
            "F00173",
            asm.LDX(0x05d1, asm.IMM16),
            "F00176",
            asm.STX(0x1c, asm.DIR),
            #asm.LDA(0xf0, asm.IMM8),
            # bank F2
            asm.LDA(0xf2, asm.IMM8), #adr
            asm.STA(0x1e, asm.DIR),
            asm.LDX(0x80ef, asm.IMM16),
            asm.STX(0x1f, asm.DIR),
            asm.JSL(0xF218BC),  #adr
            asm.LDX(0x0e, asm.DIR),
            asm.LDA(0xd85013, asm.LNG_X),
            asm.AND(0x20, asm.IMM8),
            asm.BEQ("F001A1"),
            asm.LDX(0x05df, asm.IMM16),
            asm.STX(0x20, asm.DIR),
            #asm.LDA(0xf0, asm.IMM8),
            # bank F2
            asm.LDA(0xf2, asm.IMM8), #adr
            asm.STA(0x22, asm.DIR),
            asm.LDX(0x83af, asm.IMM16),
            asm.STX(0x23, asm.DIR),
            asm.JSL(0xF2188A),  #adr
            "F001A1",
            asm.LDA(0x0c, asm.DIR),
            asm.RTL(),

            #F001A4
            "TextPointerTable",
            # Text Pointer Table
            # fieldeffect
            0x4A, 0x02, 0x53, 0x02, 0x49, 0x02, 0x49, 0x02,
            #0x49, 0x02, 0x5B, 0x02, 0x49, 0x02, 0x49, 0x02,
            0x49, 0x02, 0x5B, 0x02, 0x49, 0x02, 0x62, 0x02,            
            
            # status protect 1
            "StatusProtect1",
            0x6D, 0x02, 0x75, 0x02, 0x7F, 0x02, 0x89, 0x02,
            0x94, 0x02, 0x9D, 0x02, 0xA4, 0x02, 0xAF, 0x02,

            # statusprotect2
            "StatusProtect2",
            0xBB, 0x02, 0xC8, 0x02, 0xD6, 0x02, 0xDF, 0x02,
            0xE7, 0x02, 0xF2, 0x02, 0xFC, 0x02, 0x07, 0x03,

            # statusacquire3
            "StatusProtect3",
            0x10, 0x03, 0x1B, 0x03, 0x26, 0x03, 0x30, 0x03,
            0x3B, 0x03, 0x45, 0x03, 0x50, 0x03, 0x5A, 0x03,

            # statboost1
            "StatBoost1",
            0x67, 0x03, 0x74, 0x03, 0x81, 0x03, 0x89, 0x03,
            0x91, 0x03, 0x99, 0x03, 0xA1, 0x03, 0xA9, 0x03,

            # special1
            "Special1",
            0xB1, 0x03, 0xBC, 0x03, 0x48, 0x02, 0x47, 0x02,
            0x46, 0x02, 0x45, 0x02, 0x44, 0x02, 0xC6, 0x03,

            # statboost2
            "StatBoost2",
            0xD1, 0x03, 0xDE, 0x03, 0xDF, 0x03, 0xED, 0x03,
            0xF9, 0x03, 0x07, 0x04, 0x13, 0x04, 0x1D, 0x04,

            # special2
            "Special2",
            0x28, 0x04, 0x32, 0x04, 0x3E, 0x04, 0x4B, 0x04,
            0x54, 0x04, 0x5F, 0x04, 0x6E, 0x04, 0x62, 0x02,

            # special3
            "Special3",
            0x74, 0x04, 0x81, 0x04, 0x8D, 0x04, 0x9B, 0x04,
            0xA7, 0x04, 0x49, 0x02, 0x49, 0x02, 0xB1, 0x04,

            # statusacquire2
            "StatusAcquire2",
            0xBF, 0x04, 0xC9, 0x04, 0xD4, 0x04, 0xDA, 0x04,
            0xE2, 0x04, 0xEA, 0x04, 0xF4, 0x04, 0xFC, 0x04,            

            0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            #F0024A
            # using text3.py style
            0xB5, 0xC0, 0xB6, 0xFF, 0x9E, 0xA7, 0x9C, 0xC5, 0x00, # 1/2 enc.
            #F00253
            0x8D, 0xA8, 0xFF, 0x9E, 0xA7, 0x9C, 0xC5, 0x00, # No enc.
            #F0025B
            0x92, 0xA9, 0xAB, 0xA2, 0xA7, 0xAD, 0x00, # Sprint
            #F00262
            # tintinabar was modified in BC so the Tintinabar effect does not link to this correctly
            0x92, 0xAD, 0x9E, 0xA9, 0xFF, 0xAB, 0x9E, 0xA0, 0x9E, 0xA7, 0x00, # Step regen
            0x8D, 0xA8, 0xFF, 0x9D, 0x9A, 0xAB, 0xA4, 0x00, # No dark
            0x8D, 0xA8, 0xFF, 0xB3, 0xA8, 0xA6, 0x9B, 0xA2, 0x9E, 0x00, # No zombie
            0x8D, 0xA8, 0xFF, 0xA9, 0xA8, 0xA2, 0xAC, 0xA8, 0xA7, 0x00, # No poison
            0x8D, 0xA8, 0xFF, 0xA6, 0x9A, 0xA0, 0xA2, 0xAD, 0x9E, 0xA4, 0x00, # No magitek
            0x8D, 0xA8, 0xFF, 0x9C, 0xA5, 0x9E, 0x9A, 0xAB, 0x00, # No clear
            0x8D, 0xA8, 0xFF, 0xA2, 0xA6, 0xA9, 0x00, # No imp
            0x8D, 0xA8, 0xFF, 0xA9, 0x9E, 0xAD, 0xAB, 0xA2, 0x9F, 0xB2, 0x00, # No petrify
            0x83, 0x9E, 0x9A, 0xAD, 0xA1, 0xFF, 0xA9, 0xAB, 0xA8, 0xAD, 0xC5, 0x00, # Death prot.
            0x8D, 0xA8, 0xFF, 0x9C, 0xA8, 0xA7, 0x9D, 0x9E, 0xA6, 0xA7, 0x9E, 0x9D, 0x00, # No condemned
            0x8E, 0xA7, 0xFF, 0xA7, 0x9E, 0x9A, 0xAB, 0xFF, 0x9D, 0x9E, 0x9A, 0xAD, 0xA1, 0x00, # On near death
            0x8D, 0xA8, 0xFF, 0xA2, 0xA6, 0x9A, 0xA0, 0x9E, 0x00, # No image
            0x8D, 0xA8, 0xFF, 0xA6, 0xAE, 0xAD, 0x9E, 0x00, # No mute
            0x8D, 0xA8, 0xFF, 0x9B, 0x9E, 0xAB, 0xAC, 0x9E, 0xAB, 0xA4, 0x00, # No berserk
            0x8D, 0xA8, 0xFF, 0xA6, 0xAE, 0x9D, 0x9D, 0xA5, 0x9E, 0x00, # No muddle
            0x8D, 0xA8, 0xFF, 0xAC, 0x9E, 0xA2, 0xB3, 0xAE, 0xAB, 0x9E, 0x00, # No seizure
            0x8D, 0xA8, 0xFF, 0xAC, 0xA5, 0x9E, 0x9E, 0xA9, 0x00, # No sleep
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0x9F, 0xA5, 0xA8, 0x9A, 0xAD, 0x00, # Auto float
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0xAB, 0x9E, 0xA0, 0x9E, 0xA7, 0x00, # Auto regen
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0xAC, 0xA5, 0xA8, 0xB0, 0x00, # Auto slow
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0xA1, 0x9A, 0xAC, 0xAD, 0x9E, 0x00, # Auto haste
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0xAC, 0xAD, 0xA8, 0xA9, 0x00, # Auto stop
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0xAC, 0xA1, 0x9E, 0xA5, 0xA5, 0x00, # Auto shell
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0xAC, 0x9A, 0x9F, 0x9E, 0x00, # Auto safe
            0x80, 0xAE, 0xAD, 0xA8, 0xFF, 0xAB, 0x9E, 0x9F, 0xA5, 0x9E, 0x9C, 0xAD, 0x00, # Auto reflect
            0x81, 0x9A, 0xAD, 0xC5, 0x8F, 0xB0, 0xAB, 0xFF, 0xCA, 0xB5, 0xC0, 0xB8, 0x00, # Bat.Pwr +1/4
            0x8C, 0x9A, 0xA0, 0xC5, 0x8F, 0xB0, 0xAB, 0xFF, 0xCA, 0xB5, 0xC0, 0xB8, 0x00, # Mag.Pwr +1/4
            0x87, 0x8F, 0xFF, 0xCA, 0xB5, 0xC0, 0xB8, 0x00, # HP +1/4
            0x87, 0x8F, 0xFF, 0xCA, 0xB5, 0xC0, 0xB6, 0x00, # HP +1/2
            0x87, 0x8F, 0xFF, 0xCA, 0xB5, 0xC0, 0xBC, 0x00, # HP +1/8
            0x8C, 0x8F, 0xFF, 0xCA, 0xB5, 0xC0, 0xB8, 0x00, # MP +1/4
            0x8C, 0x8F, 0xFF, 0xCA, 0xB5, 0xC0, 0xB6, 0x00, # MP +1/2
            0x8C, 0x8F, 0xFF, 0xCA, 0xB5, 0xC0, 0xBC, 0x00, # MP +1/8
            0x88, 0xA7, 0xA2, 0xAD, 0xA2, 0x9A, 0xAD, 0xA2, 0xAF, 0x9E, 0x00, # Initiative
            0x95, 0xA2, 0xA0, 0xA2, 0xA5, 0x9A, 0xA7, 0x9C, 0x9E, 0x00, # Vigilance
            0x92, 0xAE, 0xA9, 0x9E, 0xAB, 0xFF, 0x89, 0xAE, 0xA6, 0xA9, 0x00, # Super Jump
            0x81, 0x9E, 0xAD, 0xAD, 0x9E, 0xAB, 0xFF, 0xAC, 0xAD, 0x9E, 0x9A, 0xA5, 0x00, # Better Steal
            0x00,
            0x81, 0x9E, 0xAD, 0xAD, 0x9E, 0xAB, 0xFF, 0xAC, 0xA4, 0x9E, 0xAD, 0x9C, 0xA1, 0x00, # Better sketch
            0x81, 0x9E, 0xAD, 0xAD, 0x9E, 0xAB, 0xFF, 0x9C, 0xAD, 0xAB, 0xA5, 0x00, # Better ctrl
            0xB5, 0xB4, 0xB4, 0xCD, 0xFF, 0xA1, 0xA2, 0xAD, 0xFF, 0xAB, 0x9A, 0xAD, 0x9E, 0x00, # 100% hit rate
            0xB5, 0xC0, 0xB6, 0xFF, 0x8C, 0x8F, 0xFF, 0x9C, 0xA8, 0xAC, 0xAD, 0x00, # 1/2 MP cost
            0xB5, 0xFF, 0x8C, 0x8F, 0xFF, 0x9C, 0xA8, 0xAC, 0xAD, 0x00, # 1 MP cost
            0x95, 0xA2, 0xA0, 0xA8, 0xAB, 0xFF, 0xCA, 0xB9, 0xB4, 0xCD, 0x00, # Vigor + 50%
            0xD5, 0xFF, 0x97, 0xC4, 0x85, 0xA2, 0xA0, 0xA1, 0xAD, 0x00, # -> X-Fight
            0x82, 0x9A, 0xA7, 0xFF, 0x9C, 0xA8, 0xAE, 0xA7, 0xAD, 0x9E, 0xAB, 0x00, # Can counter
            0x91, 0x9A, 0xA7, 0x9D, 0xA8, 0xA6, 0xFF, 0x9E, 0xAF, 0x9A, 0x9D, 0x9E, 0x00, # Random evade
            0x86, 0x9A, 0xAE, 0xA7, 0xAD, 0xA5, 0x9E, 0xAD, 0x00, # Gauntlet
            0x83, 0xAE, 0x9A, 0xA5, 0xFF, 0xB0, 0xA2, 0x9E, 0xA5, 0x9D, 0x00, # Dual wield
            0x84, 0xAA, 0xAE, 0xA2, 0xA9, 0xFF, 0x9A, 0xA7, 0xB2, 0xAD, 0xA1, 0xA2, 0xA7, 0xA0, 0x00, # Equip anything
            0x82, 0xA8, 0xAF, 0x9E, 0xAB, 0x00, # Cover
            0x8B, 0xA8, 0xB0, 0xFF, 0x87, 0x8F, 0xFF, 0x92, 0xA1, 0x9E, 0xA5, 0xA5, 0x00, # Low hp shell
            0x8B, 0xA8, 0xB0, 0xFF, 0x87, 0x8F, 0xFF, 0x92, 0x9A, 0x9F, 0x9E, 0x00, # Low HP safe
            0x8B, 0xA8, 0xB0, 0xFF, 0x87, 0x8F, 0xFF, 0x91, 0x9F, 0xA5, 0x9E, 0x9C, 0xAD, 0x00, # Low HP rflect
            0x83, 0xA8, 0xAE, 0x9B, 0xA5, 0x9E, 0xFF, 0x9E, 0xB1, 0xA9, 0xC5, 0x00, # Double exp.
            0x83, 0xA8, 0xAE, 0x9B, 0xA5, 0x9E, 0xFF, 0x86, 0x8F, 0x00, # Double GP
            0x91, 0x9E, 0xAF, 0x9E, 0xAB, 0xAC, 0x9E, 0xFF, 0x9C, 0xAE, 0xAB, 0x9E, 0xAC, 0x00, # Reverse cures
            0x82, 0xA8, 0xA7, 0x9D, 0x9E, 0xA6, 0xA7, 0x9E, 0x9D, 0x00, # Condemned
            0x8D, 0x9E, 0x9A, 0xAB, 0xFF, 0x9D, 0x9E, 0x9A, 0xAD, 0xA1, 0x00, # Near death
            0x88, 0xA6, 0x9A, 0xA0, 0x9E, 0x00, # Image
            0x92, 0xA2, 0xA5, 0x9E, 0xA7, 0x9C, 0x9E, 0x00, # Silence
            0x81, 0x9E, 0xAB, 0xAC, 0x9E, 0xAB, 0xA4, 0x00, # Berserk
            0x82, 0xA8, 0xA7, 0x9F, 0xAE, 0xAC, 0xA2, 0xA8, 0xA7, 0x00, #Confusion
            0x92, 0x9E, 0xA2, 0xB3, 0xAE, 0xAB, 0x9E, 0x00, # Seizure
            0x92, 0xA5, 0x9E, 0x9E, 0xA9, 0x00, # Sleep
            'F00502',
            0x20, 0x05,
            0x2A, 0x05, 0x2F, 0x05, 0x36, 0x05, 0x40, 0x05, 0x49, 0x05,
            0x52, 0x05, 0x5F, 0x05, 0x6C, 0x05, 0x71, 0x05, 0x79, 0x05, 0x85, 0x05,
            0x92, 0x05, 0x9D, 0x05, 0xA9, 0x05,
            0x82, 0x9A, 0xA7, 0xFF, 0xAC, 0xAD, 0x9E, 0x9A, 0xA5, 0x00, # Can steal
            0x80, 0xAD, 0xA6, 0x9A, 0x00, # Atma
            0x97, 0xFF, 0xA4, 0xA2, 0xA5, 0xA5, 0x00, # X-kill
            0x8C, 0x9A, 0xA7, 0xFF, 0x9E, 0x9A, 0xAD, 0x9E, 0xAB, 0x00, # Man eater
            0x83, 0xAB, 0x9A, 0xA2, 0xA7, 0xFF, 0x87, 0x8F, 0x00, # Drain HP
            0x83, 0xAB, 0x9A, 0xA2, 0xA7, 0xFF, 0x8C, 0x8F, 0x00, # Drain MP
            0x94, 0xAC, 0x9E, 0xAC, 0xFF, 0xAC, 0xA8, 0xA6, 0x9E, 0xFF, 0x8C, 0x8F, 0x00, # Uses some MP
            0x91, 0x9A, 0xA7, 0x9D, 0xA8, 0xA6, 0xFF, 0xAD, 0xA1, 0xAB, 0xA8, 0xB0, 0x00, # Random throw
            0x83, 0xA2, 0x9C, 0x9E, 0x00, # Dice
            0x95, 0x9A, 0xA5, 0xA2, 0x9A, 0xA7, 0xAD, 0x00, # Valiant
            0x96, 0xA2, 0xA7, 0x9D, 0xFF, 0x9A, 0xAD, 0xAD, 0x9A, 0x9C, 0xA4, 0x00, # Wind attack
            0x87, 0x9E, 0x9A, 0xA5, 0xAC, 0xFF, 0xAD, 0x9A, 0xAB, 0xA0, 0x9E, 0xAD, 0x00, # Heals target
            0x92, 0xA5, 0xA2, 0x9C, 0x9E, 0xFF, 0xA4, 0xA2, 0xA5, 0xA5, 0x00, # Slice kill
            0x85, 0xAB, 0x9A, 0xA0, 0xA2, 0xA5, 0x9E, 0xFF, 0xB0, 0xA9, 0xA7, 0x00, # Fragile wpn
            0x94, 0xAC, 0x9E, 0xAC, 0xFF, 0xA6, 0xA8, 0xAB, 0x9E, 0xFF, 0x8C, 0x8F, 0x00, # Uses more MP
            0x8D, 0xA8, 0xFF, 0x9E, 0x9F, 0x9F, 0x9E, 0x9C, 0xAD, 0x00, # No effect
            0x84, 0x9F, 0x9F, 0x9E, 0x9C, 0xAD, 0xC1, 0x00, # Effect:
            0x84, 0x9F, 0x9F, 0x9E, 0x9C, 0xAD, 0xAC, 0xC1, 0x00, # Effects:
            0x8C, 0xA8, 0xAB, 0x9E, 0xFF, 0x9E, 0x9F, 0x9F, 0x9E, 0x9C, 0xAD, 0xAC, 0xC1, 0x00, # More effects:
            0x81, 0x9A, 0x9C, 0xA4, 0xFF, 0xAB, 0xA8, 0xB0, 0x00, # Back row

            #F005E8
            asm.REP(0x30),
            asm.LDA(0x11, asm.DIR),
            asm.AND(0x00ff, asm.IMM16),
            asm.ASL(),
            asm.TAX(),
            asm.LDA(0xF201A4, asm.LNG_X),  #adr "TextPointerTable"
            asm.TAX(),
            asm.CPX(0x0249, asm.IMM16),
            asm.BCC("F00637"),
            asm.BNE("F00619"),
            asm.LDA(0x10, asm.DIR),
            asm.AND(0x00ff, asm.IMM16),
            asm.XBA(),
            asm.LSR(),
            asm.LSR(),
            asm.ADC(0x80ef, asm.IMM16),
            asm.STA(0x13, asm.DIR),
            asm.LDA(0x0000, asm.IMM16),
            asm.SEP(0x20),
            asm.LDA(0x11, asm.DIR),
            asm.STA(0x12, asm.DIR),
            asm.JSL(0xF206F6),   #adr
            asm.BRA("F00635"),
            "F00619",
            asm.LDA(0x10, asm.DIR),
            asm.AND(0x00ff, asm.IMM16),
            asm.XBA(),
            asm.LSR(),
            asm.LSR(),
            asm.ADC(0x80ef, asm.IMM16),
            asm.STA(0x23, asm.DIR),
            asm.LDA(0x0000, asm.IMM16),
            asm.SEP(0x20),
            #asm.LDA(0xf0, asm.IMM8),
            asm.LDA(0xf2, asm.IMM8),  #adr
            asm.STA(0x22, asm.DIR),
            asm.STX(0x20, asm.DIR),
            asm.JSL(0xF2188A),   #adr

            "F00635",  #WriteEffect_Return
            asm.CLC(),
            asm.RTL(),

            "F00637",
            asm.REP(0x20),
            asm.SEC(),
            asm.TXA(),
            asm.SBC(0x0244, asm.IMM16),
            asm.TAX(),
            asm.PHX(),
            asm.LDA(0x10, asm.DIR),
            asm.AND(0x00ff, asm.IMM16),
            asm.XBA(),
            asm.LSR(),
            asm.LSR(),
            asm.ADC(0x80f3, asm.IMM16),
            asm.STA(0x3b, asm.DIR),
            asm.PHX(),
            asm.TAX(),
            asm.LDA(0x6cd5, asm.IMM16),
            asm.STA(0x7dfffc, asm.LNG_X),
            asm.PLX(),
            asm.LDA(0xc36198, asm.LNG_X),
            asm.AND(0x00ff, asm.IMM16),
            asm.STA(0x12, asm.DIR),
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),
            asm.ADC(0xcea0, asm.IMM16),
            asm.SEC(),
            asm.SBC(0x12, asm.DIR),
            asm.STA(0x38, asm.DIR),
            asm.LDA(0x00d8, asm.IMM16),
            asm.SEP(0x20),
            asm.STA(0x3a, asm.DIR),
            asm.LDA(0x07, asm.IMM8),
            asm.STA(0x3d, asm.DIR),
            asm.JSL(0xF218A3),   # adr
            asm.LDA(0x10, asm.DIR),
            asm.CMP(0x04, asm.IMM8),
            asm.BCS("F00635"),
            asm.INC(0x10, asm.DIR),
            asm.REP(0x20),
            asm.PLX(),
            asm.LDA(0x10, asm.DIR),
            asm.AND(0x00ff, asm.IMM16),
            asm.XBA(),
            asm.LSR(),
            asm.LSR(),
            asm.ADC(0x80f3, asm.IMM16),
            asm.STA(0x3b, asm.DIR),
            asm.PHX(),
            asm.TAX(),
            asm.LDA(0x2cd5, asm.IMM16),
            asm.STA(0x7dfffc, asm.LNG_X),
            asm.PLX(),
            asm.LDA(0xc3619d, asm.LNG_X),
            asm.AND(0x00ff, asm.IMM16),
            asm.STA(0x12, asm.DIR),
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),
            asm.ADC(0xcea0, asm.IMM16),
            asm.SEC(),
            asm.SBC(0x12, asm.DIR),
            asm.STA(0x38, asm.DIR),
            asm.LDA(0x00d8, asm.IMM16),
            asm.SEP(0x20),
            asm.STA(0x3a, asm.DIR),
            asm.LDA(0x07, asm.IMM8),
            asm.STA(0x3d, asm.DIR),
            asm.JSL(0xF218A3),   #adr
            asm.SEC(),
            asm.RTL(),
            # F006C1 / F206C1
            "F006C1",
            asm.LDA(0x10, asm.DIR),
            asm.BEQ("F006F5"),
            asm.BMI("F006F5"),
            asm.CMP(0x04, asm.IMM8),
            asm.BCS("F006F5"),
            asm.LDA(0x11, asm.DIR),
            asm.STA(0x38, asm.DIR),
            asm.JSL(0xF21821),    #adr
            asm.STA(0x17, asm.DIR),
            asm.STX(0x12, asm.DIR),
            asm.LDA(0xe6, asm.IMM8),
            asm.STA(0x14, asm.DIR),
            asm.LDA(0x10, asm.DIR),
            asm.REP(0x20),
            asm.AND(0x00ff, asm.IMM16),
            asm.XBA(),
            asm.LSR(),
            asm.LSR(),
            asm.ADC(0x80ef, asm.IMM16),
            asm.STA(0x15, asm.DIR),
            asm.LDA(0x0028, asm.IMM16),
            asm.SEP(0x20),
            asm.STA(0x18, asm.DIR),
            asm.JSL(0xF218EE),   #adr
            "F006F5",
            asm.RTL(),

            "F006F6", #WriteHex
            asm.LDA(0x12, asm.DIR),
            asm.AND(0xf0, asm.IMM8),
            asm.LSR(),
            asm.LSR(),
            asm.LSR(),
            asm.LSR(),
            asm.TAX(),
            asm.LDA(0xF20725, asm.LNG_X), #adr
            asm.LDX(0x13, asm.DIR),
            asm.STA(0x7e0000, asm.LNG_X),
            asm.LDA(0x20, asm.IMM8),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.LDA(0x12, asm.DIR),
            asm.AND(0x0f, asm.IMM8),
            asm.TAX(),
            asm.LDA(0xf20725, asm.LNG_X), #adr
            asm.LDX(0x13, asm.DIR),
            asm.STA(0x7e0002, asm.LNG_X),
            asm.LDA(0x20, asm.IMM8),
            asm.STA(0x7e0003, asm.LNG_X),
            asm.RTL(),
            # $F00725 table for hex digits
            "F00725",
            0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB,
            0xBC, 0xBD, 0x9A, 0x9B, 0x9C, 0x9D, 0x9E, 0x9F,
        )   
        #]            
        #space = Write(Bank.F0, src, "BC improved item display")
        space.printr()


#[0x30486e - 0x30497a] "BC common menu pt2" : takes up 110
        space = Reserve(0x321821, 0x321931, "BC common menu pt 2")
        #src = [
        space.write(
##            common_sub.set_location(0x301821)
##            common_sub.bytestring = bytes([
##                # Get_attack_name:
            #F01821
            # jumped to from F0/06CF, 1875, 1C3D
            "Get_attack_name",
            asm.LDA(0x38, asm.DIR),
            asm.STZ(0x39, asm.DIR),
            asm.CMP(0x36, asm.IMM8),
            asm.BCC("Get_spell_attack_name"),
            asm.CMP(0x51, asm.IMM8),
            asm.BCC("Get_esper_attack_name"),
            asm.CMP(0x55, asm.IMM8),
            asm.BCC("to_get_other_attack_name"),
            asm.CMP(0x5d, asm.IMM8),
            asm.BCC("to_get_swdtech_attack_name"),
            "to_get_other_attack_name",
            asm.JMP(0x1c4e, asm.ABS),
            "to_get_swdtech_attack_name",
            asm.JMP(0x1c67, asm.ABS),
            asm.ADC(0xf7b9, asm.IMM16),
            asm.TAX(),
            asm.LDA(0x000a, asm.IMM16),
            asm.SEP(0x20),
            asm.RTL(),
            "Get_esper_attack_name",
            asm.SEC(),
            asm.SBC(0x36, asm.IMM8),
            asm.REP(0x20),
            asm.AND(0x00ff, asm.IMM16),
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),
            asm.ADC(0xf6e1, asm.IMM16),
            asm.TAX(),
            asm.LDA(0x0008, asm.IMM16),
            asm.SEP(0x20),
            asm.RTL(),
            "Get_spell_attack_name",
            asm.REP(0x20),
            asm.AND(0x00ff, asm.IMM16),
            asm.STA(0x38, asm.DIR),
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),
            asm.ADC(0xf567, asm.IMM16),
            asm.SEC(),
            asm.SBC(0x38, asm.DIR),
            asm.TAX(),
            asm.LDA(0x0007, asm.IMM16),
            asm.SEP(0x20),
            asm.RTL(),

            #F01871
            #"write_attack_name",
            'F01871',
            asm.JMP(0x1c35, asm.ABS),
            asm.NOP(),
            asm.JSL(0xF21821),  #adr this needs change to beginning of this src
            asm.STX(0x38, asm.DIR),
            asm.STA(0x3d, asm.DIR),
            asm.LDA(0xe6, asm.IMM8),
            asm.STA(0x3a, asm.DIR),
            asm.LDX(0x36, asm.DIR),
            asm.STX(0x3b, asm.DIR),
            asm.JSL(0xF218A3),  #adr JSR #$F018A3 Gui__WriteTextLength
            asm.RTL(),
            # F0188A
            "WriteText",
            asm.LDX(0x23, asm.DIR),
            asm.LDY(0x0000, asm.IMM16),

            #0xB7, 0x20, # LDA [$20], Y
            #0xF0, 0x0F, # BEQ
            #asm.LDA(0x0FF020, asm.DIR_24_Y),  #??????????
            asm.LDA(0x20, asm.DIR_24_Y),
            asm.BEQ(0x0f),
            
            asm.STA(0x7e0000, asm.LNG_X),
            asm.LDA(0x20, asm.IMM8),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.INX(),
            asm.INX(),
            asm.INY(),
            asm.BRA(0xed),
            asm.RTL(),
            # $F018A3 Gui__WriteTextLength:
            "Gui__WriteTextLength",
            asm.JMP(0x1c00, asm.ABS),
            # 22 NOP's
            asm.NOP(),asm.NOP(),asm.NOP(),asm.NOP(),
            asm.NOP(),asm.NOP(),asm.NOP(),asm.NOP(),
            asm.NOP(),asm.NOP(),asm.NOP(),asm.NOP(),
            asm.NOP(),asm.NOP(),asm.NOP(),asm.NOP(),
            asm.NOP(),asm.NOP(),asm.NOP(),asm.NOP(),
            asm.NOP(),asm.NOP(),

            # F018BC
            'F018BC',
            asm.LDX(0x1f, asm.DIR),
            asm.LDY(0x0000, asm.IMM16),
            # Loop:
            #0xB7, 0x1C, # LDA [$1C], Y
            #0xF0, 0x0F, # BEQ $18d4
            asm.LDA(0x1c, asm.DIR_24_Y),
            asm.BEQ(0x0f),  #jump to F018D5
            asm.STA(0x7e0000, asm.LNG_X),
            asm.LDA(0x30, asm.IMM8),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.INX(),
            asm.INX(),
            asm.INY(),
            asm.BRA(0xed),
            asm.RTL(),

            # F018D5
            asm.LDX(0x27, asm.DIR),
            asm.LDY(0x0000, asm.IMM16),
            #0xB7, 0x24, # LDA [$24], Y
            #0xF0, 0x0F, # BEQ
            asm.LDA(0x24, asm.DIR_24_Y),
            asm.BEQ(0x0f),
            asm.STA(0x7e0000, asm.LNG_X),
            asm.LDA(0x29, asm.DIR),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.INX(),
            asm.INX(),
            asm.INY(),
            asm.BRA(0xed),
            asm.RTL(),

            # $F018EE WriteTextGreen?
            'F018EE',
            asm.LDX(0x15, asm.DIR),
            asm.LDY(0x0000, asm.IMM16),
            #0xB7, 0x12, # LDA [$12], Y
            #Loop
            asm.LDA(0x12, asm.DIR_24_Y),
            asm.STA(0x7e0000, asm.LNG_X),
            asm.LDA(0x18, asm.DIR),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.INX(),
            asm.INX(),
            asm.INY(),
            asm.DEC(0x17, asm.DIR),
            asm.BNE(0xed),
            asm.RTL(),

            # F01907
            asm.CLC(),
            asm.LDX(0x1e, asm.DIR),
            asm.LDY(0x1c, asm.DIR),
            asm.STY(0x4204, asm.ABS),
            asm.LDA(0x0a, asm.IMM8),
            asm.STA(0x4206, asm.ABS),
            asm.LDA(0x20, asm.DIR),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.DEX(),
            asm.DEX(),
            asm.LDA(0xb4, asm.IMM8),
            asm.ADC(0x4216, asm.ABS),
            asm.STA(0x7e0002, asm.LNG_X),
            asm.LDY(0x4214, asm.ABS),
            asm.BNE(0xe2),
            asm.RTL(),

            # F0192B
            asm.LDA(0x20, asm.IMM8),
            asm.STA(0x002140, asm.LNG),
            asm.RTL(),
        )
        #]        
        #space = Write(Bank.F0, src, "BC common menu pt2")
        space.printr()        

#[0x30497b - 0x3049fe] "BC common menu pt3" : takes up 85
##        common_sub.set_location(0x301C00)
##        common_sub.bytestring = bytes([
##            #Print_attack_name:
        space = Reserve(0x321c00, 0x321c85, "BC common menu pt3")
        #src = [
        space.write(
            "Print_attack_name",
            asm.LDA(0x0a, asm.IMM8),
            asm.STA(0x3f, asm.DIR),
            asm.LDX(0x3b, asm.DIR),
            asm.LDY(0x0000, asm.IMM16),
            asm.LDA(0x38, asm.DIR_24_Y),
            # Loop:
            asm.STA(0x7e0000, asm.LNG_X),
            asm.LDA(0x20, asm.IMM8),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.INX(),
            asm.INX(),
            asm.INY(),
            asm.DEC(0x3f, asm.DIR),
            asm.DEC(0x3d, asm.DIR),
            asm.BNE(0xeb),   #BNE Loop      ????
            asm.LDA(0x3f, asm.DIR),
            asm.BEQ(0x12),
            # Loop2:
            asm.LDA(0xff, asm.IMM8),
            asm.STA(0x7e0000, asm.LNG_X),
            asm.LDA(0x20, asm.IMM8),
            asm.STA(0x7e0001, asm.LNG_X),
            asm.INX(),
            asm.INX(),
            asm.DEC(0x3f, asm.DIR),
            asm.BNE(0xee),
            asm.RTL(),

            # $F01C35 write_attack_name:
            #"write_attack_name",
            'F01C35',
            asm.LDA(0xe6, asm.IMM8),
            asm.STA(0x3a, asm.DIR),
            asm.LDA(0x35, asm.DIR),
            asm.STA(0x38, asm.DIR),
            asm.JSL(0xF21821),   #adr update: JSR Get_attack_name
            asm.STX(0x38, asm.DIR),
            asm.STA(0x3d, asm.DIR),
            asm.LDX(0x36, asm.DIR),
            asm.STX(0x3b, asm.DIR),
            asm.JSL(0xF218A3),   #adr update: JSR #$F018A3 Gui__WriteTextLength
            asm.RTL(),
            

            # $F01C4E Get other attack name
            asm.SEC(),
            asm.SBC(0x51, asm.IMM8),
            asm.REP(0x20),
            asm.AND(0x00ff, asm.IMM16),
            asm.STA(0x38, asm.DIR),
            asm.ASL(),
            asm.ASL(),
            asm.ADC(0x38, asm.DIR),
            asm.ASL(),
            asm.ADC(0xf7b9, asm.IMM16),
            asm.TAX(),
            asm.LDA(0x000a, asm.IMM16),
            asm.SEP(0x20),
            asm.RTL(),

            # $F01C67 Get_swdtech_name
            asm.LDA(0xcf, asm.IMM8),
            asm.STA(0x3a, asm.DIR),
            asm.LDA(0x35, asm.DIR),
            asm.SEC(),
            asm.SBC(0x55, asm.IMM8),
            asm.REP(0x20),
            asm.AND(0x00ff, asm.IMM16),
            asm.ASL(),
            asm.STA(0x38, asm.DIR),
            asm.ASL(),
            asm.ADC(0x38, asm.DIR),
            asm.ASL(),
            asm.ADC(0x3c40, asm.IMM16),
            asm.TAX(),
            asm.LDA(0x000a, asm.IMM16),
            asm.SEP(0x20),
            asm.RTL(),
        )
        #]
        #space = Write(Bank.F0, src, "BC common menu pt3")
        space.printr() 

### these are referenced from above (search for "adr+")
### the consequences of removing this, i don't know yet
        
        if 0 == 1:
    ##def _rage_dance_common(fout):
    ##    rage_dance_sub = Substitution()
    ##    rage_dance_sub.set_location(0x301932)
    ##    rage_dance_sub.bytestring = bytes([
            space = Reserve(0x321932, 0x321ae4, "BC ragemenu stuff")
            #src = [
            
            space.write(
                # jumped to from F0/005B, 0074
                0xA9, 0x21, # LDA #$21
                0x8F, 0x40, 0x21, 0x00, # STA $002140
                0x6B, # RTL
                0x08, # PHP
                0xC2, 0x30, # REP #$30
                0x48, #PHA
                0xDA, #PHX
                0x5A, #PHY
                0x0B, #PHD
                0xA9, 0x00, 0x15, # LDA #$1500
                0x5B, # TCD
                0xA9, 0x00, 0x00, # LDA #$0000
                0xE2, 0x20, # SEP #$20
                0x22, 0x2B, 0x1B, 0xF2, # JSR #$F01B2B   arg
                0xC2, 0x30, # REP #$30
                0x2B,   # PLD
                0x7A,   # PLY
                0xFA,   # PLX
                0x68,   # PLA
                0x28,   # PLP
                0xA5, 0x09, # LDA $09   ; No-autofire keys
                0x89, 0x80, # BIT #$80  ; Pushing B?
                0x5C, 0xB4, 0x28, 0xC3, # JMP #$C328B4 (sustain dance menu)
                0x08, # PHP
                0xC2, 0x30, # REP $30
                0x48, #PHA
                0xDA, #PHX
                0x5A, #PHY
                0x0B, #PHD
                0xA9, 0x00, 0x15, # LDA #$1500
                0x5B, #TCD
                0xA9, 0x00, 0x00, # LDA #$0000
                0xE2, 0x20, # SEP #$20
                0x22, 0xA2, 0x19, 0xF2, # JSR #$F119A2   arg
                0xC2, 0x30, # REP #$30
                0x2B,   # PLD
                0x7A,   # PLY
                0xFA,   # PLX
                0x68,   # PLA
                0x28,   # PLP
                0xA9, 0x1C, # LDA #$1C  ; C3/22AA
                0x85, 0x26, # STA $26   ; Next: Sustain menu
                0x5C, 0xF4, 0x21, 0xC3, #JMP #$C321F4 (initialize dance menu)
                0x08,# PHP
                0xC2, 0x30, # REP #$30
                0x48,   #PHA
                0xDA,   #PHX
                0x5A,   #PHY
                0x0B,   #PHD
                0xA9, 0x00, 0x15,   # LDA #$1500
                0x5B,   #TCD
                0xA9, 0x00, 0x00,   # LDA #$0000
                0xE2, 0x20, # SEP #$20
                0x22, 0x81, 0x1A, 0xF2, # JSR #$F11A81    arg
                0xC2, 0x30, # REP #$30
                0x2B,   # PLD
                0x7A,   # PLY
                0xFA,   # PLX
                0x68,   # PLA
                0x28,   # PLP
                0xA9, 0x0A, #LDA #$0A       ; C3/1FF4
                0x85, 0x26, #STA $26        ; Next: Skills menu
                0x5C, 0xB2, 0x29, 0xC3, # JMP #$C329B2 (return to skills menu)
                0x64, 0x10, # STZ $10
                0x64, 0x11, # STZ $11
                0xA6, 0x10, # LDX $10
                0xA9, 0x00, # LDA #$00
                0x9D, 0x00, 0x01,   #STA $0100,X
                0x18, # CLC
                0xE8, # INX
                0x86, 0x10, # STX $10
                0xE0, 0x08, 0x00,   # CPX #$0008
                0x90, 0xF0, # BCC
                0x6B,   #RTL
                0x64, 0x27, # STZ $27
                0x64, 0x28, # STZ $28
                0xA0, 0x10, 0x00,   # LDY #$0010
                0x84, 0x29, # STY $29
                0x64, 0x2D, # STZ $29
                0x64, 0x2E, # STZ $2E
                0x64, 0x2B, # STZ $2B
                0x64, 0x2C, # STZ $2C
                0xA6, 0x27, # LDX $27
                0xBF, 0x1B, 0x42, 0x7E, # LDA #$7E421B
                0x85, 0x2F, # STA $2F
                0xA4, 0x29, #LDY $29
                0xA5, 0x2F, #LDA $2F
                0x99, 0x00, 0x01, #STA $0100,Y
                0xA9, 0x00, #$00
                0x9F, 0x1B, 0x42, 0x7E, # STA $7E421B,X
                0x18, # CLC
                0xC8, # INY
                0x84, 0x29, # STY $29
                0x18, # CLC
                0xE8, # INX
                0x86, 0x27, #STX $27
                0x18, # CLC
                0xA4, 0x2B, # LDY $2B
                0xC8, # INY
                0x84, 0x2B, # STY $2B
                0xA6, 0x2B, # LDX $2B
                0xE0, 0x2A, 0x00, # CPX #$002A
                0x90, 0xD6, # BCC
                0x18, #CLC
                0xA5, 0x27, # LDA $27
                0x69, 0x80, # ADC #$80
                0x85, 0x30, # STA $30
                0xA5, 0x28, # LDA $28
                0x69, 0x00, # ADC #$00
                0x85, 0x31, # STA $31
                0x38, # SEC
                0xA5, 0x30, # LDA $30
                0xE9, 0x28, # SBC #$28
                0x85, 0x32, # STA $32
                0xA5, 0x31, # LDA $31
                0xE9, 0x00, # SBC #$00
                0x85, 0x33, # STA $33
                0xA4, 0x32, # LDY $32
                0x84, 0x27, # STY $27
                0x18, #CLC
                0xA4, 0x2D, # LDY $2D
                0xC8, #INY
                0x84, 0x2D, # STY $2D
                0xA6, 0x2D, # LDX $2D
                0xE0, 0x04, 0x00, # CPX #$0004
                0x90, 0xA7, # BCC
                0x6B,   # RTL
                0x64, 0x27, # STZ $27
                0x64, 0x28, # STZ $28
                0xA0, 0x10, 0x00, # LDY #$0010
                0x84, 0x29, # STY $29
                0x64, 0x2D, # STZ $2D
                0x64, 0x2E, # STZ $2E
                0x64, 0x2B, # STZ $2B
                0x64, 0x2C, # STZ $2C
                0xA6, 0x29, # LDX $29
                0xBD, 0x00, 0x01,   # LDA $0100,X
                0x85, 0x2F, # STA $2F
                0xA6, 0x27, # LDX $27
                0xA5, 0x2F, # LDA $2F
                0x9F, 0x1B, 0x42, 0x7E, # STA $7E421B
                0x18, # CLC
                0xA4, 0x29, # LDY $29
                0xC8, # INY
                0x84, 0x29, # STY $29
                0x18, # CLC
                0xE8, # INX
                0x86, 0x27, # STX $27
                0x18, # CLC
                0xA4, 0x2B, # LDY $2B
                0xC8, # INY
                0x84, 0x2B, # STY $2B
                0xA6, 0x2B, # LDX $2B
                0xE0, 0x2A, 0x00, # CPX #$002A
                0x90, 0xDA, # BCC
                0x18, # CLC
                0xA5, 0x27, # LDA $27
                0x69, 0x80, # ADC #$80
                0x85, 0x30, # STA $30
                0xA5, 0x28, # LDA $28
                0x69, 0x00, # ADC #$00
                0x85, 0x31, # STA $31
                0x38, # SEC
                0xA5, 0x30, # LDA $30
                0xE9, 0x28, # SBC #$28
                0x85, 0x32, # STA $32
                0xA5, 0x31, # LDA $31
                0xE9, 0x00, # SBC #$00
                0x85, 0x33, # STA $33
                0xA4, 0x32, # LDY $32
                0x84, 0x27, # STY $27
                0x18, # CLC
                0xA4, 0x2D,
                0xC8, #INY
                0x84, 0x2D,
                0xA6, 0x2D, # LDX $2D
                0xE0, 0x04, 0x00, # CPX #$0004
                0x90, 0xAB, # BCC
                0x6B, # RTL
                0xA9, 0x08, # LDA #$08
                0x8D, 0x13, 0x00,   # STA $0013
                0x6B, #RTL
                #$F01A87:
                0xAD, 0x4B, 0x00, # LDA $004B   ; get dance index
                0x0A, # ASL ; multiply dance index by 2
                0xAA, #TAX
                0xAD, 0x4C, 0x1D, # ADC $1D4C   ; get known dances
                0x3F, 0x67, 0x9C, 0xC3, # AND $C39C67,X ; A &= 2^X
                0xF0, 0x05, # BEQ unknown_dance
                0x8A, # TXA
                0x0A, # ASL
                0xAA, # TAX     ; X = dance index * 4
                0x80, 0x03, # BRA get_dance_moves
                #unknown_dance:
                0xA2, 0xD0, 0xD0, # LDX #$D0D0		; points to $CFFFBE
                0xBF, 0x80, 0xFE, 0xCF, # LDA $CFFE80,X    ; get id of dance move
                0x85, 0x35, # STA $35
                0xA0, 0x9B, 0x42, # LDY #$429B
                0x84, 0x36, # STY $36
                0xDA, # PHX
                0x22, 0x71, 0x18, 0xF2, # JSL $F11871   ; draw move name    arg
                0xFA, # PLX
                0xE8, # INX
                0xBF, 0x80, 0xFE, 0xCF, # LDA $CFFE80,X    ; get id of dance move
                0x85, 0x35, # STA $35
                0xA0, 0xB1, 0x42, # LDY #$42B1
                0x84, 0x36, # STY $36
                0xDA, # PHX
                0x22, 0x71, 0x18, 0xF2,  # JSL $F11871   ; draw move name    arg
                0xFA, # PLX
                0xE8, # INX
                0xBF, 0x80, 0xFE, 0xCF, # LDA $CFFE80,X    ; get id of dance move
                0x85, 0x35, # STA $35
                0xA0, 0x1B, 0x43, # LDY #$431B
                0x84, 0x36, # STY $36
                0xDA, # PHX
                0x22, 0x71, 0x18, 0xF2,  # JSL $F11871   ; draw move name     arg
                0xFA, # PLX
                0xE8, # INX
                0xBF, 0x80, 0xFE, 0xCF, # LDA $CFFE80,X    ; get id of dance move
                0x85, 0x35, # STA $35
                0xA0, 0x31, 0x43, # LDY #$4331
                0x84, 0x36, # STY $36
                0xDA, # PHX
                0x22, 0x71, 0x18, 0xF2,  # JSL $F11871   ; draw move name     arg
                0xFA, # PLX
                0x6B # RTL
            )
            #]
            #space = Write(Bank.F1, src, "BC ragedance stuff")
            space.printr()


            space = Reserve(0x321b2b, 0x321bf1, "more BC ragedance stuff")
            #src = [
            space.write(
        #rage_dance_sub.set_location(0x301B2B)
        #rage_dance_sub.bytestring = bytes([
                0xAD, 0x00, 0x01, # LDA $0100
                0x85, 0x12, # STA $12
                0xA5, 0x12, # LDA $12
                0xC9, 0x04, # CMP $04
                0xD0, 0x05, # BNE
                0xA9, 0x80, # LDA #$80
                0x8D, 0x09, 0x00, # STA $0009
                0xAD, 0x00, 0x01, # LDA $0100
                0x85, 0x13, # STA $13
                0xA5, 0x13, # LDA $13
                0xC9, 0x03, # CMP #$03
                0xD0, 0x1B, # BNE
                0xA9, 0x00, # LDA $00
                0x8D, 0x15, 0x00, # STA $0015
                0xA9, 0x38, # LDA #$38
                0x8D, 0x17, 0x00, # STA $0017
                0xAD, 0x00, 0x01, # LDA $0001
                0x85, 0x14, # STA $14
                0x18, # CLC
                0xA5, 0x14, # LDA $14
                0x69, 0x01, # ADC #$01
                0x85, 0x15, # STA $15
                0xA5, 0x15, # LDA $15
                0x8D, 0x00, 0x01, # STA $0100
                0xAD, 0x00, 0x01, # LDA $0100
                0x85, 0x16, # LDA $16
                0xA5, 0x16, # STA $16
                0xC9, 0x02, # CMP #$02
                0xD0, 0x2F, # BNE
                0xAD, 0x09, 0x00, # LDA
                0x85, 0x17, # STA
                0xA5, 0x17, # LDA
                0xC9, 0x80, # CMP
                0x90, 0x1A, # BCC
                0xAD, 0x00, 0x01, # LDA
                0x85, 0x18, # STA
                0x18, # CLC
                0xA5, 0x18, # LDA $18
                0x69, 0x01,
                0x85, 0x19,
                0xA5, 0x19,
                0x8D, 0x00, 0x01,
                0xA9, 0x00,
                0x8D, 0x09, 0x00,
                0x22, 0x1E, 0x1A, 0xF0, # JSL
                0xA9, 0x04,
                0x8D, 0x15, 0x00,
                0xA9, 0x40,
                0x8D, 0x17, 0x00, # STA $0017
                0xAD, 0x00, 0x01,
                0x85, 0x1A,
                0xA5, 0x1A,
                0xC9, 0x01,
                0xD0, 0x15,
                0x22, 0xB7, 0x19, 0xF0,
                0xAD, 0x00, 0x01,
                0x85, 0x1B,
                0x18, # CLC
                0xA5, 0x1B,
                0x69, 0x01,
                0x85, 0x1C,
                0xA5, 0x1C,
                0x8D, 0x00, 0x01,
                0xAD, 0x00, 0x01,
                0x85, 0x1D,
                0xA9, 0x00,
                0xC5, 0x1D, # CMP $1D
                0xB0, 0x0F, # BCS
                0xAD, 0x00, 0x01,
                0x85, 0x1E,
                0xA5, 0x1E,
                0xC9, 0x03, # CMP #$03
                0xB0, 0x04, # BCS
                0x22, 0x87, 0x1A, 0xF0,
                0xAD, 0x00, 0x01,
                0x85, 0x1F,
                0xA5, 0x1F,
                0xC9, 0x00, # CMP #$09
                0xD0, 0x11, # BNE
                0xAD, 0x00, 0x01,
                0x85, 0x20,
                0x18, # CLC
                0xA5, 0x20,
                0x69, 0x01, # ADC #$01
                0x85, 0x21,
                0xA5, 0x21,
                0x8D, 0x00, 0x01,
                0x6B # RTL
            )
            #]
            #space = Write(Bank.F1, src, "more BC ragedance")
            space.printr()
        #rage_dance_sub.write(fout)

            space = Reserve(0x32cf50, 0x32cf53, "FFs")
            space.write(
                0xff,
                0xff,
                0xff,
                0xff,
            )
        #rage_dance_sub.set_location(0x10CF50)
        #rage_dance_sub.bytestring = bytes([0xFF] * 4)
        #rage_dance_sub.write(fout)
