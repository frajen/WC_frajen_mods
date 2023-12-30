### this mod allows the player to hold down the Y button
### while in a shop's Buy menu to see extra details
### about the item: 8 primary stat mods (Vigor, Speed, MagPwr, Stamina, Evade, MBlock, Def, MDef)
### as well as the item's description and BatPwr (if relevant)

from memory.space import Bank, Reserve, Allocate, Write, Read
import instruction.asm as asm
import args

class BuyItemDetails:
    def __init__(self):
        self.mod()

    def mod(self):

##C3/8DCB:	AF84 92A99E9E9D00              ; Speed
##C3/8DD3:	2F86 819AADC58FB0AB00          ; Bat.Pwr
##C3/8DDD:	AF86 839E9F9EA7AC9E00          ; Defense
##C3/8DE7:	AF87 8C9AA0C5839E9F00          ; Mag.Def
##C3/8DF1:	8D7B B9B4CDFF83A6A000          ; 50% Dmg
##C3/8DFB:	A97B 809BACA8AB9BFF878F00      ; Absorb HP
##C3/8E07:	8D7C 8DA8FF849F9F9E9CAD00      ; No Effect
##C3/8E13:	A97C 969E9AA4FFA9AD00          ; Weak pt
##C3/8E1D:	8D7B 80ADAD9A9CA400            ; Attack
##C3/8E26:	2F82 92B09D939E9CA100          ; SwdTech
##C3/8E30:	AF82 91AEA7A29C00              ; Runic
##C3/8E38:	2F83 B6C4A19AA79D00            ; 2-hand

# number of references
# "gear_stats_evasion_attack_elements" c3/fc8c section is only jumped to once
# and because it ends in JMP you can 
# "check_text_color" c3/fc9b section is jumped to 3 times
# "load_item_index" c3/fca6 section is jumped to 3 times
# "process_text" c3/fcae jumped to 3 times

### New sections
# Help - 
# Vigor - 22
# Speed - 30
# Stamina - 38
# Magic - 48
# Def - 56
# MDef - 66
# Evade - 75
# MBlock - 83
# Power - 93
# Unknown - 103
# PowerDash - 109
# DefDash - 115
# MDefDash - 121

        #####DW section
        ### 2022-12-19: Bank C3 is so tight that separating this entire DW block out
        ### into individual components still doesn't increase the available amount of C3 space

        #HelpText is used at C3/B989
        # this text shows up at the top right of each shop's Buy menu ("Hold Y for details.")
        src = [
            "HelpText", #  dw $791F : db "Hold",$FE,"Y",$FE,"for",$FE,"details.",$00 ; TODO: Why FE?
            0x1f, 0x79,
            0x87, 0xa8, 0xa5, 0x9d, 0xfe, 0x98, 0xfe, 0x9f, 0xa8, 0xab, 0xfe, 0x9d, 0x9e, 0xad, 0x9a, 0xa2, 0xa5, 0xac, 0xc5, 0x00,
        ]
        space = Write(Bank.C3, src, "shop y HelpText")
        helptext = space.start_address
        space.printr()

        ###Vigor to PowerText is only used in the DrawDetailsLabels section
        src = [
            "VigorText", #  dw $820D : db "Vigor",$00
            0x0d, 0x82,
            0x95, 0xa2, 0xa0, 0xa8, 0xab, 0x00,
        ]
        space = Write(Bank.C3, src, "shop y VigorText")
        vigortext = space.start_address
        space.printr()

        src = [
        "SpeedText", #  dw $830D : db "Speed",$00
            0x0d, 0x83,
            0x92, 0xa9, 0x9e, 0x9e, 0x9d, 0x00,
        ]
        space = Write(Bank.C3, src, "shop y SpeedText")
        speedtext = space.start_address
        space.printr()

        src = [
            "StaminaText",  # dw $838D : db "Stamina",$00
            0x8d, 0x83,
            0x92, 0xad, 0x9a, 0xa6, 0xa2, 0xa7, 0x9a, 0x00, 
        ]
        space = Write(Bank.C3, src, "shop y StaminaText")
        staminatext = space.start_address
        space.printr()

        src = [
            "MagicText",  # dw $828D : db "Magic",$00
            0x8d, 0x82,
            0x8c, 0x9a, 0xa0, 0xa2, 0x9c, 0x00, 
        ]
        space = Write(Bank.C3, src, "shop y MagicText")
        magictext = space.start_address
        space.printr()

        src = [
            "DefText",  # dw $822B : db "Defense",$00
            0x2b, 0x82,
            0x83, 0x9e, 0x9f, 0x9e, 0xa7, 0xac, 0x9e, 0x00, 
        ]
        space = Write(Bank.C3, src, "shop y DefText")
        deftext = space.start_address
        space.printr()

        src = [
            "MDefText",  # dw $832B : db "M.Def.",$00
            0x2b, 0x83,
            0x8c, 0xc5, 0x83, 0x9e, 0x9f, 0xc5, 0x00, 
        ]
        space = Write(Bank.C3, src, "shop y MDefText")
        mdeftext = space.start_address
        space.printr()

        src = [
            "EvadeText", # dw $82AB : db "Evade",$00
            0xab, 0x82,
            0x84, 0xaf, 0x9a, 0x9d, 0x9e, 0x00, 
        ]
        space = Write(Bank.C3, src, "shop y EvadeText")
        evadetext = space.start_address
        space.printr()

        src = [
            "MEvadeText",  # dw $83AB : db "M.Evade",$00
            0xab, 0x83,
            0x8c, 0xc5, 0x84, 0xaf, 0x9a, 0x9d, 0x9e, 0x00, 
        ]
        space = Write(Bank.C3, src, "shop y MEvadeText")
        mevadetext = space.start_address
        space.printr()

        src = [
            "PowerText",  # dw $812B : db "Attack",$00,$00 ; TODO Remove extra $00 here
            0x2b, 0x81,
            0x80, 0xad, 0xad, 0x9a, 0x9c, 0xa4, 0x00, 0x00,        ]
        space = Write(Bank.C3, src, "shop y PowerText")
        powertext = space.start_address
        space.printr()

### these are used for items with no values for the stat in question
        src = [
            ### used after "hide_bpow"
            "UnknownTxt",  #dw $813F : db "???",$00
            0x3f, 0x81,
            0xbf, 0xbf, 0xbf, 0x00,
        ]
        space = Write(Bank.C3, src, "shop y UnknownTxt")
        unknowntxt = space.start_address
        space.printr()

        src = [
            ### used after BNE "skip_all_dashes" and above "is_weapon"
            "PowerDash",  # dw $813F : db "---",$00
            0x3f, 0x81,
            0xc4, 0xc4, 0xc4, 0x00,
        ]
        space = Write(Bank.C3, src, "shop y PowerDash")
        powerdash = space.start_address
        space.printr()

        src = [
            ### used after BNE "skip_all_dashes" and above BNE "not_weapon"
            "DefDash",#dw $823F : db "---",$00
            0x3f, 0x82,
            0xc4, 0xc4, 0xc4, 0x00,
        ]
        space = Write(Bank.C3, src, "shop y DefDash")
        defdash = space.start_address
        space.printr()

        src = [
            ### used after BNE "skip_all_dashes" and above BNE "not_weapon"
            "MDefDash", #dw $833F : db "---",$00
            0x3f, 0x83,
            0xc4, 0xc4, 0xc4, 0x00, 
        ]
        space = Write(Bank.C3, src, "shop y MDefDash")
        mdefdash = space.start_address
        space.printr()

        # Window layout data, used in clear_screen_bg2
        src = [
            "GearWindow",  # dw $718B : db $1C,$06
            0x8b, 0x71, 0x1c, 0x06, 
            "GearActors",  # dw $750B : db $1C,$06
            0x0b, 0x75, 0x1c, 0x06, 
            "GearNameBox", # dw $708B : db $1C,$02
            0x8b, 0x70, 0x1c, 0x02, 
            "GearDesc",  # dw $738B : db $1C,$04
            0x8b, 0x73, 0x1c, 0x04,
        ]
        space = Write(Bank.C3, src, "window layout data")
        window_layout_data = space.start_address
        space.printr()
        
        # gear_desc2
        src = [
            # originally C3/FEFD, jumped to from C3/FEEF
            "gear_desc2",
            asm.LDX(0x7849, asm.IMM16), #Base: 7E/7849
            asm.STX(0xeb, asm.DIR), #Set map ptr LBs
            asm.LDA(0x7e, asm.IMM8), #Bank: 7E
            asm.STA(0xed, asm.DIR), #Set ptr HB
            asm.LDY(0x0cbc, asm.IMM16), #Ends at 30,19
            asm.STY(0xe7, asm.DIR), #Set row's limit
            asm.LDY(0x0c84, asm.IMM16), #Starts at 3,19
            asm.LDX(0x3500, asm.IMM16), #Tile 256, pal 5
            asm.STX(0xe0, asm.DIR), #Priority enabled
            asm.JSR(0xa783, asm.ABS), #Do line 1, row 1
            asm.LDY(0x0cfc, asm.IMM16), #Ends at 30,20
            asm.STY(0xe7, asm.DIR), #Set row's limit
            asm.LDY(0x0cc4, asm.IMM16), #Starts at 3,20
            asm.LDX(0x3501, asm.IMM16), #Tile 257, pal 5
            asm.STX(0xe0, asm.DIR), #Priority enabled
            asm.JSR(0xa783, asm.ABS), #Do line 1, row 2
            asm.LDY(0x0d3c, asm.IMM16), #Ends at 30,21
            asm.STY(0xe7, asm.DIR), #Set row's limit
            asm.LDY(0x0d04, asm.IMM16), #Starts at 3,21
            asm.LDX(0x3538, asm.IMM16), #Tile 312, pal 5
            asm.STX(0xe0, asm.DIR), #Priority enabled
            asm.JSR(0xa783, asm.ABS), #Do line 2, row 1
            asm.LDY(0x0d7c, asm.IMM16), #Ends at 30,22
            asm.STY(0xe7, asm.DIR), #Set row's limit
            asm.LDY(0x0d44, asm.IMM16), #Starts at 3,22
            asm.LDX(0x3539, asm.IMM16), #Tile 313, pal 5
            asm.STX(0xe0, asm.DIR), #Priority enabled
            asm.JMP(0xa783, asm.ABS), #Do line 2, row 2            # C3/A783 eventually leads to RTS
        ]
        # called in gear description pt 1, below
        space = Write(Bank.C3, src, "gear description pt 2")
        gear_desc_pt_2 = space.start_address
        space.printr()

        src = [
            # originally C3/FEE9, jumped to from C3/FD16
            "gear_desc",
            asm.LDA(0x02, asm.DIR),
            asm.CMP(0x4b, asm.DIR),
            asm.BNE("gear_desc_end"),
            #asm.JSR(0xfefd, asm.ABS), #jump to gear_desc2
            asm.JSR(gear_desc_pt_2, asm.ABS),
            asm.JSR(0xb4e6, asm.ABS), #Set description to be displayed and to ignore joypad
            asm.JSR(0xb4ef, asm.ABS), #Load item description for Buy menu
            "gear_desc_end",
            asm.LDA(0x4b, asm.DIR),
            asm.STA(0x02, asm.DIR),
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "gear description pt 1")
        gear_desc_pt_1 = space.start_address
        space.printr()

###whenever the console (or the emulator) does a 24-bit multiplication,
###you can read the result of that multiplication from RAM bytes $2136, $2135, and $2134 (high to low).
###So something was multiplied and the subroutine is using the first eight bits as the result.
### 2134 is using the first 8 bits to reference the item index in this example
### given the explanation in https://ersanio.gitbook.io/assembly-for-the-snes/mathemathics-and-logic/math
### 2134 in the following uses are references to an item index, which is stored from something like a section C3/8321
### (e.g. it's very common in bank C3 to see JSR $8321 followed up with LDX $2134)

        src = [
            # originally C3/FEC9, jumped to from C3/FE5F
            "all_dashes",
            asm.LDX(0x2134, asm.ABS), #Load item index
            asm.LDA(0xd85000, asm.LNG_X), #Load item properties
            asm.AND(0x07, asm.IMM8),  #Get item type
            asm.CMP(0x06, asm.IMM8),  #item?
            asm.BNE("skip_all_dashes"),  #if not an item type, skip dashing out Power/Def/MDef
            #PowerDash
            asm.LDY(powerdash, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),  #Load text string into tilemap
            #DefDash
            asm.LDY(defdash, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),  #Load text string into tilemap
            #MDefDash
            asm.LDY(mdefdash, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),  #Load text string into tilemap
            "skip_all_dashes",
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "display all dashes")
        all_dashes = space.start_address
        space.printr()

        src = [
            # this section can be independently separated, is linked to once above 3fc8c
            "gear_stats_evasion_attack_elements",
            asm.JSR(0x87eb, asm.ABS),  #jump to Draw Evade and MBlock modifiers for gear data menu
            asm.JSR(0xc2f7, asm.ABS),  #jump to Set text color to blue
            asm.LDY(0x8e1d, asm.IMM16),  #Positioned text for gear data menu
            asm.JSR(0x02f9, asm.ABS),  #Load text string into tilemap
            asm.JMP(0x88a0, asm.ABS),  #Build and draw list of attack or halved elements
        ]
        space = Write(Bank.C3, src, "draw evasions atk and elements")
        draw_evasions_atk_elements = space.start_address
        space.printr()

        src = [
            "check_text_color",
            asm.BEQ("grey_text_color"),
            "user_text_color",
            asm.LDA(0x20, asm.IMM8),  # loads palette 0
            asm.BRA("store_tcolor"),
            "grey_text_color",
            asm.LDA(0x24, asm.IMM8),  # loads grey text
            "store_tcolor",
            asm.STA(0x29, asm.DIR),
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "check and store text color")
        check_text_color = space.start_address
        space.printr()

        src = [
            asm.LDX(0x2134, asm.ABS),  #Load item index
            asm.LDA(0xD85013, asm.LNG_X),  #get item flags (https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:fmt:items)
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "load item's weapon flags")
        load_weapon_flags = space.start_address
        space.printr()

        src = [
            "process_text",
            asm.STY(0xe7, asm.DIR),
            asm.JSR(0x8795, asm.ABS),
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "process text")
        process_text = space.start_address
        space.printr()

        # C3 text file lookup phrase:
        #Fork : Draw offensive properties
        space = Reserve(0x38746, 0x38795, "Fork: Draw offensive properties", 0xFF)
        space.write(
            asm.JSR(0x879c, asm.ABS),   # jump to C3/879C, draw weapon's Bat.Pwr in gear data menu
            asm.JSR(draw_evasions_atk_elements, asm.ABS),

            asm.JSR(load_weapon_flags, asm.ABS),
            asm.AND(0x80, asm.IMM8),   # Get Runic bit

            asm.JSR(check_text_color, asm.ABS),
            asm.LDY(0x8e30, asm.IMM16),

            asm.JSR(process_text, asm.ABS),

            asm.JSR(load_weapon_flags, asm.ABS),
            asm.AND(0x40, asm.IMM8),   # Get allows two-hands bit

            asm.JSR(check_text_color, asm.ABS),
            asm.LDY(0x8e38, asm.IMM16),

            asm.JSR(process_text, asm.ABS),

            asm.JSR(load_weapon_flags, asm.ABS),
            asm.AND(0x02, asm.IMM8),    # Get SwdTech bit

            asm.JSR(check_text_color, asm.ABS),
            asm.LDY(0x8e26, asm.IMM16),

            asm.JSR(process_text, asm.ABS),
            asm.RTS(),
        )
        space.printr()

        src = [
            # only jumped to once, from c3/fcf8
            "check_stats",
            asm.PHA(),
            asm.PHX(),
            asm.PHY(),
            asm.PHP(),
            asm.JSR(0xc2f2, asm.ABS),  #C3/C2F2: Set text color to player's color. Sets palette to white
            asm.JSR(0xbfc2, asm.ABS),  #C3/BFC2: Get item by cursor in Buy menu.
            asm.JSR(0x8321, asm.ABS),  #C3/8321: Compute item data index
            asm.LDX(0x2134, asm.ABS),  #Load item index
            asm.TDC(),  # Terminator

            #positioned text buffer? https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:ram:menu_ram
            #or? $9E00-$9EFF VWF Widths https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:ram:field_ram
            asm.STA(0x7e9e8d, asm.LNG),  #store accum into. Mod B3(?)
            asm.STA(0x7e9e8e, asm.LNG),  #store accum into. Mod B4(?)
            asm.REP(0x20),  #16-bit A
            asm.LDA(0x8223, asm.IMM16), # Tilemap ptr(?)
            
            asm.STA(0x7e9e89, asm.LNG),  #store accum into. Set position 
            asm.SEP(0x20),  #8-bit A
            asm.TDC(),   # Clear A
            asm.LDA(0xd85010, asm.LNG_X),  #load item's vigor/speed
            asm.PHA(),
            asm.AND(0x0f, asm.IMM8),   # get the vigor value
            asm.ASL(),  # Double it
            asm.JSR(0x8836, asm.ABS),  # Draw a non-evasion stat modifier for gear data menu
            asm.REP(0x20),  #16-bit A
            asm.LDA(0x8323, asm.IMM16),  # Tilemap ptr(?)
            asm.STA(0x7e9e89, asm.LNG),  #store accum into 
            asm.SEP(0x20),
            asm.TDC(),
            asm.PLA(),
            asm.AND(0xf0, asm.IMM8),  # get the speed value
            asm.LSR(),  #Put in b3-b6
            asm.LSR(),  #Put in b2-b5
            asm.LSR(),  #Put in b1-b4
            asm.JSR(0x8836, asm.ABS),  # Draw a non-evasion stat modifier for gear data menu
            asm.REP(0x20),
            asm.LDA(0x83a3, asm.IMM16), #Using more Tilemap ptr(?)
            asm.STA(0x7e9e89, asm.LNG), #Set position
            asm.SEP(0x20),  #8-bit A
            asm.LDX(0x2134, asm.ABS),  #Item index
            asm.TDC(),
            asm.LDA(0xd85011, asm.LNG_X),  #load item's stamina/magpwr
            asm.PHA(),
            asm.AND(0x0f, asm.IMM8),   # get the stamina value
            asm.ASL(),  #Double it
            asm.JSR(0x8836, asm.ABS),  # Draw a non-evasion stat modifier for gear data menu
            asm.REP(0x20),  #16-bit A
            asm.LDA(0x82a3, asm.IMM16), #Using more Tilemap ptr(?)
            asm.STA(0x7e9e89, asm.LNG), #Set position
            asm.SEP(0x20),  #8-bit A
            asm.TDC(),
            asm.PLA(),
            asm.AND(0xf0, asm.IMM8),  # get the magpwr value
            asm.LSR(),  #Put in b3-b6
            asm.LSR(),  #Put in b2-b5
            asm.LSR(),  #Put in b1-b4
            asm.JSR(0x8836, asm.ABS),  # Draw a non-evasion stat modifier for gear data menu
            # draw defensive properties
            asm.LDX(0x2134, asm.ABS),  #Item index
            asm.LDA(0xd85000, asm.LNG_X),  #get item properties
            asm.AND(0x07, asm.IMM8),  #get item type
            asm.BEQ("not_weapon"),  #branch if tool
            asm.CMP(0x01, asm.IMM8),  #weapon?
            asm.BEQ("is_weapon"),  #branch if weapon
            asm.CMP(0x06, asm.IMM8),  #item?
            asm.BEQ("not_weapon"),  #branch if item
            # item is neither a weapon nor item
            asm.LDA(0xd85014, asm.LNG_X),  # get weapon's phys def
            asm.JSR(0x04e0, asm.ABS),  #Convert 8-bit number into text, blank leading zeroes
            asm.LDX(0x823f, asm.IMM16),  # see DW below for DefDash ("---")
            asm.JSR(0x04c0, asm.ABS),  #Draw 3 digits (8-bit number)
            asm.LDX(0x2134, asm.ABS),  #Load item index
            asm.LDA(0xd85015, asm.LNG_X),  # get weapon's mdef
            asm.JSR(0x04e0, asm.ABS),  #Convert 8-bit number into text, blank leading zeroes
            asm.LDX(0x833f, asm.IMM16),  # see DW below for MDefDash ("---")
            asm.JSR(0x04c0, asm.ABS),  #Draw 3 digits (8-bit number)
            #asm.LDY(0xffb3, asm.IMM16), #PowerDash, see DW below for PowerDash
            asm.LDY(powerdash, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS), #Load text string into tilemap

            "is_weapon",
            asm.TDC(),  #direct register into 16-bit accum
            asm.LDX(0x2134, asm.ABS),  #Load item index
            asm.LDA(0xd85000, asm.LNG_X),  #get item properties
            asm.AND(0x07, asm.IMM8),  #get item type
            asm.CMP(0x01, asm.IMM8),  #weapon?
            asm.BNE("not_weapon"),  #branch if item
            asm.LDA(0x20, asm.IMM8),  #Palette 0
            asm.STA(0x29, asm.DIR),  #Color: User's
            asm.CMP(0x51, asm.IMM8), #Dice?
            asm.BEQ("hide_bpow"), #Hide BatPwr if Dice
            asm.LDX(0x2134, asm.ABS), #Load item index
            asm.LDA(0xd85014, asm.LNG_X), #get bat pwr
            asm.JSR(0x04e0, asm.ABS),  #Convert 8-bit number into text, blank leading zeroes
            asm.LDX(0x813f, asm.IMM16), #UnknownTxt, see DW below "???"
            
            asm.JSR(0x04c0, asm.ABS),  #Draw 3 digits (8-bit number)
            #asm.LDY(0xffb9, asm.IMM16), #LDY DefDash
            asm.LDY(defdash, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS), #Load text string into tilemap
            #asm.LDY(0xffbf, asm.IMM16), #LDY MDefDash
            asm.LDY(mdefdash, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS), #Load text string into tilemap
            asm.BRA("not_weapon"),  #get the other properties sahred with non-weapons
            "hide_bpow",
            #asm.LDY(0xffad, asm.IMM16), #UnknownTxt
            asm.LDY(unknowntxt, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS), #Load text string into tilemap
            "not_weapon",
            #asm.JSR(0xfec9, asm.ABS), #all_dashes, C3/FEC9
            asm.JSR(all_dashes, asm.ABS),
            asm.REP(0x20),
            asm.LDA(0x82bf, asm.IMM16),  #Using more Tilemap ptr(?)
            asm.STA(0x7e9e89, asm.LNG),  #Pointer to Positioned Text in BG1 Data 
            asm.SEP(0x20),
            asm.LDX(0x2134, asm.ABS),  #Load item index
            asm.TDC(),
            asm.LDA(0xd8501a, asm.LNG_X),  #get evade/mblock
            asm.PHA(),
            asm.AND(0x0f, asm.IMM8),  #get evade
            asm.ASL(),  #x2
            asm.ASL(),  #x4
            asm.JSR(0x881a, asm.ABS),  #ending section of Draw Evade and MBlock modifiers for gear data menu
            asm.REP(0x20),
            asm.LDA(0x83bf, asm.IMM16), #Using more Tilemap ptr(?)
            asm.STA(0x7e9e89, asm.LNG),  #Pointer to Positioned Text in BG1 Data 
            asm.SEP(0x20),
            asm.LDX(0x2134, asm.ABS),  #Load item index
            asm.TDC(),
            asm.PLA(),
            asm.AND(0xf0, asm.IMM8),  #get mblock
            asm.LSR(),
            asm.LSR(),
            asm.TAX(),
            asm.LDA(0xc38854, asm.LNG_X),  #sign
            asm.STA(0x7e9e8b, asm.LNG), #add to string
            asm.LDA(0xc38855, asm.LNG_X), #tens digit
            asm.STA(0x7e9e8c, asm.LNG), #add to string
            asm.LDA(0xc38856, asm.LNG_X), #ones digit
            asm.STA(0x7e9e8d, asm.LNG), #add to string
            asm.JSR(0x8847, asm.ABS),  #2nd half of Draw a non-evasion stat modifier for gear data menu
            # name and cleanup
            asm.REP(0x20),
            asm.LDA(0x810d, asm.IMM16), #Using more Tilemap ptr(?)
            asm.STA(0x7e9e89, asm.LNG), #Set pointer
            asm.SEP(0x20),
            asm.JSR(0xbfc2, asm.ABS),  #C3/BFC2: Get item by cursor in Buy menu.
            asm.JSR(0xc068, asm.ABS),  #Load item's name
            asm.JSR(0x7fd9, asm.ABS),  #Draw memorized string
            asm.PLP(),
            asm.PLY(),
            asm.PLX(),
            asm.PLA(),
            asm.JSR(0xbc92, asm.ABS),  #Get quantity owned of item in Buy menu
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "check item stats")
        check_item_stats = space.start_address
        space.printr()

        src = [
            # jumped to from C3/B8C4
            "clear_screen_bg2",  #C3/FCB4
            asm.JSR(0x6a28, asm.ABS), # Clear BG2 tilemap A
            asm.JSR(0x6a2d, asm.ABS), # Clear BG2 tilemap B
            asm.JSR(0x6a32, asm.ABS), # Clear BG2 tilemap C
            asm.JSR(0x6a37, asm.ABS), # Clear BG2 tilemap D (unused)
            #LDY GearWindow
            asm.LDY(window_layout_data, asm.IMM16),
            asm.JSR(0x0341, asm.ABS), #Prepare to and draw a menu window
            #LDY GearActors
            asm.LDY(window_layout_data+4, asm.IMM16),
            asm.JSR(0x0341, asm.ABS), #Prepare to and draw a menu window
            #LDY GearNameBox
            asm.LDY(window_layout_data+8, asm.IMM16),
            asm.JSR(0x0341, asm.ABS), #Prepare to and draw a menu window
            #LDY GearDesc
            asm.LDY(window_layout_data+12, asm.IMM16),
            asm.JSR(0x0341, asm.ABS), #Prepare to and draw a menu window

            # jumped to from C3/B95A
            "clear_screen_bg3",  #C3/FCD8
            asm.JSR(0x6a3c, asm.ABS), # Clear BG3 tilemap A
            asm.JSR(0x6a41, asm.ABS), # Clear BG3 tilemap B
            asm.JSR(0x6a46, asm.ABS), # Clear BG3 tilemap C
            asm.JSR(0x6a4b, asm.ABS), # Clear BG3 tilemap D
            asm.RTS(),

            #"draw_title_dupe",
            #asm.JSR(0x02ff, asm.ABS), # Draw title. Not needed?
            #removing this saves 3 bytes which will then offset
            #later jumps to handle_shop_stats
            #asm.NOP(),
            #asm.NOP(),
            #asm.NOP(),

            # jumped to from c3/b4bd
            "handle_shop_stats", #c3fce8
            "handle_buy_item_list",
            asm.LDA(0x10, asm.IMM8),
            asm.TSB(0x45, asm.DIR),
            asm.JSR(0x0f39, asm.ABS),  #Set to upload BG3 tilemap A (version 1)
            asm.JSR(0x1368, asm.ABS),  #Trigger NMI, allow cursor sound to repeat
            asm.JSR(0x0f4d, asm.ABS),  #Set to upload BG3 tilemap B (version 1)
            asm.JSR(0xb8a6, asm.ABS),  #Handle D-Pad for Buy menu
            #"check_stats"
            asm.JSR(check_item_stats, asm.ABS),
            asm.JSR(0xbc84, asm.ABS),  #Load and draw quantity owned of item in Buy menu
            asm.JSR(0xbca8, asm.ABS),  #Count and draw quantity worn of item in Buy menu
            # C3/BCA8 eventually leads to RTS

            # Handle hold Y
            "shop_handle_y",
            asm.LDA(0x0d, asm.DIR),
            asm.BIT(0x40, asm.IMM8), #Holding Y?
            asm.BEQ("shop_handle_b"), #branch to "Fork: Handle B" if not
            asm.REP(0x20), #16-bit A
            asm.LDA(0x0100, asm.IMM16), #BG2 scroll position
            asm.STA(0x3b, asm.DIR),  #BG2 Y position
            asm.STA(0x3d, asm.DIR),  #BG3 X position
            asm.SEP(0x20), #8-bit A
            asm.LDA(0x04, asm.IMM8), # bit 2
            asm.TRB(0x45, asm.DIR), # set bit in menu flags
            #jump to "gear_desc"
            asm.JSR(gear_desc_pt_1, asm.ABS),
            asm.RTS(),
            # Fork: Handle B
            "shop_handle_b",
            asm.STZ(0x3c, asm.DIR),
            asm.STZ(0x3e, asm.DIR),
            asm.LDA(0x04, asm.IMM8),
            asm.TSB(0x45, asm.DIR),
            asm.LDA(0x09, asm.DIR), #No-autofire keys
            asm.BIT(0x80, asm.IMM8), #pushing B?
            asm.BEQ("shop_handle_a"), #branch to A
            asm.JSR(0x0ea9, asm.ABS), #Sound: Cursor
            asm.JMP(0xb760, asm.ABS), #Exit submenu
            # Fork: Handle A
            "shop_handle_a",
            asm.LDA(0x08, asm.DIR), #No-autofire keys
            asm.BIT(0x80, asm.IMM8), #Pushing (A)
            asm.BEQ("shop_exit"), #branch to exit
            asm.JSR(0xb82f, asm.ABS),  #Sub: Define buy quantity limit
            asm.JSR(0xb7e6, asm.ABS),  #Invoke buy order menu if justified
            "shop_exit",
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "handle shop menus")
        handle_shop_menus = space.start_address
        clear_screen_bg3 = space.start_address + 0x24

        #handle_shop_stats = space.start_address + 0x34
        #save 3 bytes by not including draw_title_dupe
        handle_shop_stats = space.start_address + 0x31
        space.printr()

        # 26: Handle buy item list
        # replaces Fork: Handle B and Fork: Handle A as well
        space = Reserve(0x3b4bd, 0x3b4e5, "NMI draw name", 0xFF)
        space.write(
            #handle_shop_stats
            asm.JSR(handle_shop_stats, asm.ABS),
            asm.RTS(),
            "check_nmi",
            asm.JSR(0x1368, asm.ABS),  #Trigger NMI, allow cursor sound to repeat
            asm.JSR(0x7fd9, asm.ABS),  #Draw memorized string
            asm.RTS(),
        )
        space.printr()

        #Draw main shop menu and submenu windows, set to update description
#C3/B8C4:	20286A  	JSR $6A28      ; Clear BG2 map A
#C3/B8C7:	202D6A  	JSR $6A2D      ; Clear BG2 map B
#C3/B8CA:	20326A  	JSR $6A32      ; Clear BG2 map C
        #jump to C3/FCB4 instead. Code starts up again at C3/B8CD
        space = Reserve(0x3b8c4, 0x3b8cc, "jump clear screen bg2")
        space.write(
            asm.JSR(handle_shop_menus, asm.ABS),
            asm.NOP(),
            asm.NOP(),
            asm.NOP(),
            asm.NOP(),
            asm.NOP(),
            asm.NOP(),
        )
        space.printr()

#Draw shop title and party's gold, clear rest of BG3
        space = Reserve(0x3b95a, 0x3b97c, "jump clear screen bg3")
        space.write(
            asm.JSR(clear_screen_bg3, asm.ABS),
            asm.JSR(0xbfd3, asm.ABS), #Draw shop title and define shop index
            asm.LDY(0xc338, asm.IMM16),  #Text pointer
            asm.JSR(0x02f9, asm.ABS),  #Load text string into tilemap, draw GP
            asm.JSR(0xc2f2, asm.ABS), #Set text color to player's color
            asm.LDY(0x1860, asm.ABS), #Gold LBs
            asm.STY(0xf1, asm.DIR), #Memorize it
            asm.LDA(0x1862, asm.ABS), #Gold HB
            asm.STA(0xf3, asm.DIR), #Memorize it 
            asm.JSR(0x0582, asm.ABS), #Convert 24-bit number into text, blank leading zeroes
            asm.LDX(0x7a33, asm.IMM16), #Text position
            asm.JSR(0x04ac, asm.ABS), #Draw 7 digits
            asm.RTS(),
        )
        space.printr()

#C3/B989:	A085C3  	LDY #$C385     ; Text pointer
        space = Reserve(0x3b989, 0x3b98c, "ldy helptext")
        space.write(
            #HelpText
            asm.LDY(helptext, asm.IMM16),
        )
        space.printr()

        #skip drawing "Power" info on buy order menu
#Draw item specs for buy order menu, reset buy quantity
#C3/BABA:	20ECBA  	JSR $BAEC      ; Draw power info        
        space = Reserve(0x3baba, 0x3babc, "skip power info draw")
        space.write(
            asm.NOP(),
            asm.NOP(),
            asm.NOP(),
        )
        space.printr()

#C3/BAC9:	20D97F  	JSR $7FD9      ; Draw name
        space = Reserve(0x3bac9, 0x3bacb, "jsr check nmi")
        space.write(
            asm.JSR(0xb4c1, asm.ABS),
        )
        space.printr()

        #BG3 text shifting table for shop
        # originally is 2F 0400 -> becomes 2F 0600
        space = Reserve(0x3c037, 0x3c039, "modify BG3 text shifting table")
        space.write(
            0x2f,
            0x06,
            0x00,
        )
        space.printr()

        src = [
            #jumped to from C3/FD3B
            "DrawDetailsLabels",
            asm.JSR(0x1368, asm.ABS),
            asm.JSR(0xc2f7, asm.ABS),
            # VigorText
            asm.LDY(vigortext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # SpeedText
            asm.LDY(speedtext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # StaminaText
            asm.LDY(staminatext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # MagicText
            asm.LDY(magictext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # DefText
            asm.LDY(deftext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # MDefText
            asm.LDY(mdeftext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # EvadeText
            asm.LDY(evadetext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # MEvadeText
            asm.LDY(mevadetext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            # PowerText
            asm.LDY(powertext, asm.IMM16),
            asm.JSR(0x02f9, asm.ABS),
            asm.JSR(0xbfc2, asm.ABS),
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "draw details labels")
        draw_details_labels = space.start_address
        space.printr()

#Draw "Owned:" and "Equipped:" for Buy menu
        space = Reserve(0x3c2e1, 0x3c2e3, "jump Draw Details Labels")
        space.write(
            #asm.JSR(0xfd3b, asm.ABS),  #DrawDetailsLabels
            asm.JSR(draw_details_labels, asm.ABS),
        )
        space.printr()
