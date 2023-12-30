from memory.space import Reserve
import instruction.asm as asm
import args

### allows characters to hold any item in the game, completely overriding any Equippable flags
### characters will still only be able to equip 1 weapon item type at a time (without Genji Glove)
### equipping certain items and using the Fight command will cause possible soft locking results
class HoldAnything:
    def __init__(self):
        if args.hold_anything:
            self.mod()

    def mod(self):
        ### branch to $9B91
        space = Reserve(0x39b8b, 0x39b8d, "hold anything 1")
        space.write(
            asm.BRA(0x04),
        )
        
        ### remove BEQ $9BA3
        space = Reserve(0x39b99, 0x39b99, "hold anything 2", asm.NOP())
        space.write(asm.NOP())
        space = Reserve(0x39b9a, 0x39b9a, "hold anything 3", asm.NOP())
        space.write(asm.NOP())

##Original code block, from Novalia Spirit $C3 Compendium 
##https://www.ff6hacking.com/wiki/lib/exe/fetch.php?media=ff3:ff3us:doc:game:ff6_bank_c3.zip
##Get Weapon or Shield's equippable chars
##
##C3/9B72:	A600    	LDX $00
##C3/9B74:	9B      	TXY 
##C3/9B75:	7B      	TDC 
##C3/9B76:	B96918  	LDA $1869,Y 	(Load inventory item Y)
##C3/9B79:	C9FF    	CMP #$FF		(Is it the "empty" item?)
##C3/9B7B:	F026    	BEQ $9BA3		(If so, branch -> do the next item)
##C3/9B7D:	202183  	JSR $8321		(Otherwise, do this function (multiplies by 30))
##C3/9B80:	AE3421  	LDX $2134		(Load X with the result of index * 30)
##C3/9B83:	BF0050D8	LDA $D85000,X	(Load item type X)
##C3/9B87:	2907    	AND #$07		(Zero out the upper nibble)
##C3/9B89:	C901    	CMP #$01		(Is it a weapon [item type 1]?)
##C3/9B8B:	F004    	BEQ $9B91		(If so, branch -> check equippable chars)
##C3/9B8D:	C903    	CMP #$03		(Otherwise, is it a shield [item type 3]?)
##C3/9B8F:	D012    	BNE $9BA3		(If not, branch -> do the next item)
##C3/9B91:	C220    	REP #$20      	(Ok, we have a weapon or shield, so set 16 bit memory/accum.)
##C3/9B93:	BF0150D8	LDA $D85001,X	(Load equippable chars for item X)
##C3/9B97:	24E7    	BIT $E7		
##C3/9B99:	F008    	BEQ $9BA3
##C3/9B9B:	E220    	SEP #$20      	(8 bit memory/accum.)
