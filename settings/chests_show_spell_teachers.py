from memory.space import Reserve, Write, Space, Bank
import instruction.asm as asm
import args

### modifies chest open dialog to show the spells that items teach
### this shouldn't affect item dialog in battle, objectives, or check rewards
### requires changing dialog line 2950 as follows:
### self.set_text(2950, "<line><     >Received “<item>”!<line><     >Teaches: <skill> x<GP><end>")
### <GP> is a reference to 0x19, which translates to the spell learn rate for items
class ChestsShowSpellTeachers:
    def __init__(self):
        if args.item_teacher is not None:
            self.mod()

    def mod(self):
##Lenophis 2022-10-12
##org $C0DD00
##; an empty block of free space
##; coming in, $1A holds the item we are getting from the chest. we need to look at its data to see if it teaches a spell
##treasure_lookup:
##LDA $1A  ; load item
##STA $4202  ; store it for multiplication
##LDA #$1E
##STA $4203  ; *30
##NOP
##NOP
##NOP
##LDX $4216  ; load product
##LDA $D85003,X  ; spell's learn rate. we check this first to see if it's 0. if it is, skip.
##BEQ treasure_exit_no_spell
##STA $22  ; put the learn rate into our number-decoding variable for later
##STZ $23  ; zero out the upper two bytes of the variable just in case for anti-taint purposes
##STZ $24
##LDA $D85004,X  ; spell learned by item
##STA $0584  ; store it in our dialogue decoder variable
##JSR $02E5  ; prep the number for the dialogue
##LDX #$000C  ; hijack the "Learned <spell>!" event and repurpose it for our new treasure message
##RTS
##
##treasure_exit_no_spell:
##LDX #$0008
##RTS
##
        
        src = [
            "TREASURE_LOOKUP",
            asm.LDA(0x1a, asm.DIR),
            asm.STA(0x4202, asm.ABS),
            asm.LDA(0x1e, asm.IMM8),
            asm.STA(0x4203, asm.ABS),
            asm.NOP(),
            asm.NOP(),
            asm.NOP(),
            asm.LDX(0x4216, asm.ABS),
            asm.LDA(0xD85003, asm.LNG_X),
            asm.BEQ("TREASURE_EXIT_NO_SPELL"),
            asm.STA(0x22, asm.DIR),
            asm.STZ(0x23, asm.DIR),
            asm.STZ(0x24, asm.DIR),
            asm.LDA(0xD85004, asm.LNG_X),
            asm.STA(0x0584, asm.ABS),
            asm.JSR(0x02E5, asm.ABS),
            asm.LDX(0x000C, asm.IMM16),
            asm.RTS(),
            "TREASURE_EXIT_NO_SPELL",
            asm.LDX(0x0008, asm.IMM16),
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "c0 chest modifier for spells")
        modded_chest_addr = space.start_address
        #space.printr()

##org $C04C8E
##; we are hooking our dialogue index to determine if we need the original or our new one
##JSR treasure_lookup

        space = Reserve(0x4c8e, 0x4c90, "jsr treasure lookup")
        space.write(
            asm.JSR(modded_chest_addr, asm.ABS)
        )
        #space.printr()

##org $C08419
##; now we have to change our dialogue decoding to account for proper spell name length. they weren't changed from vanilla FF6 japanese
##LDA #$07  ; 6 letters plus the icon
##

        space = Reserve(0x8419, 0x841a, "change dialog per spell length")
        space.write(
            asm.LDA(0x07, asm.IMM8),
        )
        #space.printr()

##org $C0843A
##CPY #$0006  ; have we done 6 letters yet? the first letter, the icon is already skipped and accounted for here

        space = Reserve(0x843a, 0x843c, "check for 6 letters (max spell name length)")
        space.write(
            asm.CPY(0x6, asm.IMM16),
        )
        #space.printr()
