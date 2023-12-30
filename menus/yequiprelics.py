from memory.space import Reserve
import instruction.asm as asm
import args

class YEquipRelics:
    def __init__(self):
        self.mod()

    def mod(self):
        ### Change jump table

        # C3/0247:	2196    	; 36: Handle Equip menu options
        space = Reserve(0x30247, 0x30249, "36: Handle Equip menu options")
        space.write(
            0x1e,
            0x96,
        )
        #C3/0287:	CF98    	; 56: Handle manual gear removal
        space = Reserve(0x30287, 0x30289, "56: Handle manual gear removal")
        space.write(
            0xcd,
            0x98,
        )
        #7E: Swap actor in Equip menu, retain Equip mode
        #C3/1BE5:	20011C  	JSR $1C01      ; Draw menu, etc.
        #C3/1BE8:	204F96  	JSR $964F      ; Draw blue "EQUIP"
        space = Reserve(0x31be8, 0x31beb, "Draw blue EQUIP")
        space.write(
            asm.JSR(0x965b, asm.ABS),
        )
#7F: Swap actor in Equip menu, retain Remove mode
#C3/1BF3:	20011C  	JSR $1C01      ; Draw menu, etc.
#C3/1BF6:	205696  	JSR $9656      ; Draw blue "REMOVE"
        space = Reserve(0x31bf6, 0x31bf9, "Draw blue REMOVE")
        space.write(
            asm.JSR(0x9660, asm.ABS),
        )
#Switch to layout with options in Equip or Relic menu
#C3/960C:	205D96  	JSR $965D      ; Erase title
        space = Reserve(0x3960c, 0x3960f, "Erase title")
        space.write(
            asm.JSR(0x9665, asm.ABS),
        )
        #C3/9615 Switch to layout without options in Equip or Relic menu
        #C3/966C Jump table for the above
##        space = Reserve(0x39615, 0x3966c, "Layout switching")
##        space.write(
##            0x0c, 0x96, 0xe6, 0x3a, 0xa9, 0x2c, 0x85, 0x29, 0x60, 0x20,
##            0x0c, 0x96, 0x20, 0x4e, 0x90, 0x20, 0x56, 0x8e, 0xa5, 0x08,
##            0x10, 0x0b, 0x20, 0xb2, 0x0e, 0x7b, 0xa5, 0x4b, 0x0a, 0xaa,
##            0x7c, 0x6c, 0x96, 0xa5, 0x09, 0x10, 0x0d, 0x20, 0xa9, 0x0e,
##            0x20, 0x10, 0x91, 0xa9, 0x04, 0x85, 0x27, 0x64, 0x26, 0x60,
##            0x0a, 0x10, 0x0a, 0x20, 0xb2, 0x0e, 0xa9, 0x58, 0x85, 0x26,
##            0xe6, 0x25, 0x60, 0xa9, 0x35, 0x85, 0xe0, 0x4c, 0x22, 0x20,
##            0xa0, 0x09, 0xa3, 0x80, 0x08, 0xa0, 0x11, 0xa3, 0x80, 0x03,
##            0xa0, 0xea, 0xa2, 0x4c, 0xf9, 0x02, 0x60,
##        )
        
        space = Reserve(0x39614, 0x3966B, "Layout switching")
        space.write(
            asm.JSR(0x960C, asm.ABS),
            asm.INC(0x3A, asm.DIR),
            asm.LDA(0x2C, asm.IMM8),
            asm.STA(0x29, asm.DIR),
            asm.RTS(),
            asm.JSR(0x960C, asm.ABS),
            asm.JSR(0x904E, asm.ABS),
            asm.JSR(0x8E56, asm.ABS),
            asm.LDA(0x08, asm.DIR),
            asm.BPL(0x000b),
            asm.JSR(0x0EB2, asm.ABS),
            asm.TDC(),
            asm.LDA(0x4B, asm.DIR),
            asm.ASL(),
            asm.TAX(),
            asm.JMP(0x966C, asm.ABS_X_16),
            "C3/9636",
            asm.LDA(0x09, asm.DIR),
            asm.BPL(0x000d),
            asm.JSR(0x0EA9, asm.ABS),
            asm.JSR(0x9110, asm.ABS),
            asm.LDA(0x04, asm.IMM8),
            asm.STA(0x27, asm.DIR),
            asm.STZ(0x26, asm.DIR),
            asm.RTS(),
            "C3/9647",
            asm.ASL(),
            asm.BPL(0x000a),
            asm.JSR(0x0EB2, asm.ABS),
            asm.LDA(0x58, asm.IMM8),
            asm.STA(0x26, asm.DIR),
            asm.INC(0x25, asm.DIR),
            asm.RTS(),
            asm.LDA(0x35, asm.IMM8),
            asm.STA(0xE0, asm.DIR),
            asm.JMP(0x2022, asm.ABS),
            asm.LDY(0xA309, asm.IMM16),
            asm.BRA(0x0008),
            asm.LDY(0xA311, asm.IMM16),
            asm.BRA(0x0003),
            asm.LDY(0xA2EA, asm.IMM16),
            asm.JMP(0x02F9, asm.ABS),
            asm.RTS(),
        )
        #space.printr()

##0c 96 JSR $960c ABS
##e6 3a INC 3a DIR
##a9 2c LDA 2c IMM8
##85 29 STA 29 DIR
##60 RTS
##20 0c 96 JSR 960c ABS
##20 4e 90 JSR 904e ABS
##20 56 8e JSR 8e56 ABS
##a5 08 LDA 08 DIR
#C3/9629
##10 0b BPL figure this addr out later : BPL 9636
#c3/962B
##20 b2 0e JSR 0eb2 ABS
##7b TDC
##a5 4b LDA 4b DIR
##0a ASL
##aa TAX
##7c 6c 96 JMP 966c ABS_X_16
##a5 09 LDA 09 DIR
#C3/9638
##10 0d BPL figure this addr out later : BPL 9647
#C3/963a
##20 a9 0e JSR 0ea9 ABS
##20 10 91 JSR 9110 ABS
##a9 04 LDA 04 IMM8
##85 27 STA 27 DIR
##64 26 STZ 26 DIR
##60 RTS
#C3/9647
##0a ASL
#C3/9648
##10 0a BPL figure latr : BPL 9654
#C3/964A
##20 b2 0e JSR 0eb2 ABS
##a9 58 LDA 58 IMM8
##85 26 STA 26 DIR
##e6 25 INC 25 DIR
##60 RTS
##a9 35 LDA 35 IMM8
##85 e0 STA e0 DIR
##4c 22 20 JMP 2022 ABS
##a0 09 a3 LDY a309 IMM16
#C3/965E
##80 08 BRA figure latr : BRA 9668
#C3/9660
##a0 11 a3 LDY a311 IMM16
#C3/9663
##80 03 BRA figure latr : BRA 9667
#C3/9665
##a0 ea a2 LDY a2ea IMM16
##4c f9 02 JMP 02f9 ABS
##60 RTS


###C3/9614:	205D96  	JSR $965D      ; Erase options
###0x0c, 0x96 JSR $960c
##
##            0x0c, 0x96,
##            0xe6, 0x3a,
##            0xa9, 0x2c,
##            0x85, 0x29,
##            0x60,
##            0x20, 0x0c, 0x96,
##            0x20, 0x4e, 0x90,
##            0x20, 0x56, 0x8e,
##            0xa5, 0x08,
##            0x10, 0x0b,
##            0x20, 0xb2, 0x0e,
##            0x7b,
##            0xa5, 0x4b,
##            0x0a,
##            0xaa,
##            0x7c, 0x6c, 0x96,
##            0xa5, 0x09,
##            0x10, 0x0d,
##            0x20, 0xa9, 0x0e,
##            0x20, 0x10, 0x91,
##            0xa9, 0x04,
##            0x85, 0x27,
##            0x64, 0x26,
##            0x60,
##            0x0a,
##            0x10, 0x0a,
##            0x20, 0xb2, 0x0e,
##            0xa9, 0x58,
##            0x85, 0x26,
##            0xe6, 0x25,
##            0x60,
##            0xa9, 0x35,
##            0x85, 0xe0,
##            0x4c, 0x22, 0x20,
##            0xa0, 0x09, 0xa3,
##            0x80, 0x08,
##            0xa0, 0x11, 0xa3,
##            0x80, 0x03,
##            0xa0, 0xea, 0xa2,
##            0x4c, 0xf9, 0x02, 0x60,
##C3/9614
##0c 96 JSR $960c ABS
##e6 3a INC 3a DIR
##a9 2c LDA 2c IMM8
##85 29 STA 29 DIR
##60 RTS
##20 0c 96 JSR 960c ABS
##20 4e 90 JSR 904e ABS
##20 56 8e JSR 8e56 ABS
##a5 08 LDA 08 DIR
#C3/9629
##10 0b BPL figure this addr out later : BPL 9636
#c3/962B
##20 b2 0e JSR 0eb2 ABS
##7b TDC
##a5 4b LDA 4b DIR
##0a ASL
##aa TAX
##7c 6c 96 JMP 966c ABS_X_16
##a5 09 LDA 09 DIR
#C3/9638
##10 0d BPL figure this addr out later : BPL 9647
#C3/963a
##20 a9 0e JSR 0ea9 ABS
##20 10 91 JSR 9110 ABS
##a9 04 LDA 04 IMM8
##85 27 STA 27 DIR
##64 26 STZ 26 DIR
##60 RTS
# 9647
##0a ASL
#C3/9648
##10 0a BPL figure latr : BPL 9654
#C3/964A
##20 b2 0e JSR 0eb2 ABS
##a9 58 LDA 58 IMM8
##85 26 STA 26 DIR
##e6 25 INC 25 DIR
##60 RTS
##a9 35 LDA 35 IMM8
##85 e0 STA e0 DIR
##4c 22 20 JMP 2022 ABS
##a0 09 a3 LDY a309 IMM16
#C3/965E
##80 08 BRA figure latr : BRA 9668
#C3/9660
##a0 11 a3 LDY a311 IMM16
#C3/9663
##80 03 BRA figure latr : BRA 9667
#C3/9665
##a0 ea a2 LDY a2ea IMM16
##4c f9 02 JMP 02f9 ABS
##60 RTS
            
            
#C3/9672:	9F96    	; EMPTY
        space = Reserve(0x39672, 0x39673, "EMPTY")
        space.write(
            0x9a,
        )
        #space.printr()
        #C3/9677:	204F96  	JSR $964F      ; Draw blue "EQUIP"
        space = Reserve(0x39677, 0x3967a, "Draw blue EQUIP")
        space.write(
            asm.JSR(0x965b, asm.ABS),
        )
        #space.printr()
#Handle "RMOVE" selection in Equip menu
#C3/968E:	201496  	JSR $9614      ; Switch windows
#C3/9691:	205696  	JSR $9656      ; Draw blue "REMOVE"
##        space = Reserve(0x39692, 0x396a7, "Handle RMOVE selection in Equip")
##        space.write(
##            0x60, 0x96, 0x20, 0x7a, 0x96, 0xe6, 0x26, 0x60, 0x20, 0xa8,
##            0x96, 0x80, 0xe9, 0xa9, 0x35, 0x85, 0x26, 0x64, 0x27, 0xc6,
##            0x25,
##        )
##        #space.printr()
        space = Reserve(0x39691, 0x396a6, "Handle RMOVE selection in Equip")
        space.write(
            asm.JSR(0x9660, asm.ABS),
            asm.JSR(0x967A, asm.ABS),
            asm.INC(0x26, asm.DIR),
            asm.RTS(),
            asm.JSR(0x96A8, asm.ABS),
            asm.BRA(0x00e9),
            asm.LDA(0x35, asm.IMM8),
            asm.STA(0x26, asm.DIR),
            asm.STZ(0x27, asm.DIR),
            asm.DEC(0x25, asm.DIR),
        )
        #space.printr()
#C3/9691:	205696  	JSR $9656      ; Draw blue "REMOVE"
##            0x60, 0x96,
##            0x20, 0x7a, 0x96,
##            0xe6, 0x26,
##            0x60,
##            0x20, 0xa8, 0x96,
##            0x80, 0xe9,
##            0xa9, 0x35,
##            0x85, 0x26,
##            0x64, 0x27,
##            0xc6, 0x25,
###C3/9691:
##60 96 JSR $9660 ABS
##20 7a 96 JSR 967a ABS
##e6 26 INC 26 DIR
##60 RTS
##20 a8 96 JSR 96a8 ABS
#C3/969d
##80 e9 BRA figure latr : BRA 9788 (?)
#C3/969f
##a9 35 LDA 35 IMM8
##85 26 STA 26 DIR
##64 27 STZ 27 DIR
##c6 25 DEC 25 DIR


        #55: Handle selection of gear slot to fill
        #57: Handle gear browsing
##        space = Reserve(0x3988c, 0x39910, "Handle selection of gear slot to fill")
##        space.write(
##            0x10, 0x21, 0x20, 0xb2, 0x0e, 0xa5, 0x4e, 0x85, 0x5f, 0xa2,
##            0x57, 0x55, 0x86, 0x26, 0x20, 0x59, 0x9b, 0x20, 0x50, 0xa1,
##            0x20, 0xeb, 0x9a, 0x20, 0x33, 0x92, 0x20, 0x15, 0x6a, 0x20,
##            0x68, 0x13, 0x4c, 0xac, 0x9c, 0xa5, 0x09, 0x10, 0x0d, 0x20,
##            0xa9, 0x0e, 0xa9, 0x36, 0x85, 0x26, 0x20, 0x50, 0x8e, 0x4c,
##            0x59, 0x8e, 0x0a, 0x10, 0x03, 0x4C, 0x4A, 0x96, 0xA5, 0x26,
##            0x69, 0x29, 0x4C, 0x56, 0x96, 0x20, 0x72, 0x8E, 0xA5, 0x08,
##            0x10, 0xDB, 0x20, 0xB2, 0x0E, 0x20, 0xF2, 0x93, 0xC2, 0x21,
##            0x98, 0xE2, 0x20, 0x65, 0x4B, 0xA8, 0xB9, 0x1F, 0x00, 0x20,
##            0x5E, 0x9D, 0xA9, 0xFF, 0x99, 0x1F, 0x00, 0x20, 0x1B, 0x91,
##            0x80, 0xBD, 0xA5, 0x09, 0x0A, 0x10, 0x14, 0x20, 0xB2, 0x0E,
##            0x20, 0x5F, 0x1E, 0xB0, 0x0A, 0x20, 0xEB, 0x9E, 0xA5, 0x99,
##            0xD0, 0x03, 0x20, 0x9F, 0x96, 0x64, 0x08, 0x4C, 0xE6, 0x9E,
##            0xEA,
##        )
        space = Reserve(0x3988c, 0x3990e, "Handle selection of gear slot to fill")
        space.write(
            asm.BPL(0x0021),
            asm.JSR(0x0EB2, asm.ABS),
            asm.LDA(0x4E, asm.DIR),
            asm.STA(0x5F, asm.DIR),
            asm.LDX(0x5557, asm.IMM16),
            asm.STX(0x26, asm.DIR),
            asm.JSR(0x9B59, asm.ABS),
            asm.JSR(0xA150, asm.ABS),
            asm.JSR(0x9AEB, asm.ABS),
            asm.JSR(0x9233, asm.ABS),
            asm.JSR(0x6A15, asm.ABS),
            asm.JSR(0x1368, asm.ABS),
            asm.JMP(0x9CAC, asm.ABS),
            asm.LDA(0x09, asm.DIR),
            asm.BPL(0x000D),
            asm.JSR(0x0EA9, asm.ABS),
            asm.LDA(0x36, asm.IMM8),
            asm.STA(0x26, asm.DIR),
            asm.JSR(0x8E50, asm.ABS),
            asm.JMP(0x8E59, asm.ABS),
            asm.ASL(),
            asm.BPL(0x0003),
            asm.JMP(0x964A, asm.ABS),
            asm.LDA(0x26, asm.DIR),
            asm.ADC(0x29, asm.IMM8),
            asm.JMP(0x9656, asm.ABS),
            asm.JSR(0x8E72, asm.ABS),
            asm.LDA(0x08, asm.DIR),
            asm.BPL(0x00DB),
            asm.JSR(0x0EB2, asm.ABS),
            asm.JSR(0x93F2, asm.ABS),
            asm.REP(0x21),
            asm.TYA(),
            asm.SEP(0x20),
            asm.ADC(0x4B, asm.DIR),
            asm.TAY(),
            asm.LDA(0x001F, asm.ABS_Y),
            asm.JSR(0x9D5E, asm.ABS),
            asm.LDA(0xFF, asm.IMM8),
            asm.STA(0x001F, asm.ABS_Y),
            asm.JSR(0x911B, asm.ABS),
            asm.BRA(0x00BD),
            asm.LDA(0x09, asm.DIR),
            asm.ASL(),
            asm.BPL(0x0014),
            asm.JSR(0x0EB2, asm.ABS),
            asm.JSR(0x1E5F, asm.ABS),
            asm.BCS(0x000A),
            asm.JSR(0x9EEB, asm.ABS),
            asm.LDA(0x99, asm.DIR),
            asm.BNE(0x0003),
            asm.JSR(0x969F, asm.ABS),
            asm.STZ(0x08, asm.DIR),
            asm.JMP(0x9EE6, asm.ABS),
            asm.NOP(),
        )
        #space.printr()
##C3/988C:	8980    	BIT #$80       ; Pushing A?
##            0x10, 0x21,
##            0x20, 0xb2, 0x0e,
##            0xa5, 0x4e,
##            0x85, 0x5f,
##            0xa2, 0x57, 0x55,
##            0x86, 0x26,
##            0x20, 0x59, 0x9b,
##            0x20, 0x50, 0xa1,
##            0x20, 0xeb, 0x9a,
##            0x20, 0x33, 0x92,
##            0x20, 0x15, 0x6a,
##            0x20, 0x68, 0x13,
##            0x4c, 0xac, 0x9c,
##            0xa5, 0x09,
##            0x10, 0x0d,
##            0x20, 0xa9, 0x0e,
##            0xa9, 0x36,
##            0x85, 0x26,
##            0x20, 0x50, 0x8e,
##            0x4c, 0x59, 0x8e,
##            0x0a,
##            0x10, 0x03,
##            0x4C, 0x4A, 0x96,
##            0xA5, 0x26,
##            0x69, 0x29,
##            0x4C, 0x56, 0x96,
##            0x20, 0x72, 0x8E,
##            0xA5, 0x08,
##            0x10, 0xDB,
##            0x20, 0xB2, 0x0E,
##            0x20, 0xF2, 0x93,
##            0xC2, 0x21,
##            0x98,
##            0xE2, 0x20,
##            0x65, 0x4B,
##            0xA8,
##            0xB9, 0x1F, 0x00,
##            0x20, 0x5E, 0x9D,
##            0xA9, 0xFF,
##            0x99, 0x1F, 0x00,
##            0x20, 0x1B, 0x91,
##            0x80, 0xBD,
##            0xA5, 0x09,
##            0x0A,
##            0x10, 0x14,
##            0x20, 0xB2, 0x0E,
##            0x20, 0x5F, 0x1E,
##            0xB0, 0x0A,
##            0x20, 0xEB, 0x9E,
##            0xA5, 0x99,
##            0xD0, 0x03,
##            0x20, 0x9F, 0x96,
##            0x64, 0x08, 0x4C, 0xE6, 0x9E,
##            0xEA,
##
##C3/988C:
##10 21 BPL 21 addr? 98a1
##20 b2 0e JSR 0eb2 ABS
##a5 4e LDA 4e DIR
##85 5f STA 5f DIR
##a2 57 55 LDX 5557 IMM16
##86 26 STX 26 DIR
##20 59 9b JSR 9b59 ABS
##20 50 a1 JSR a150 ABS
##20 eb 9a JSR 9aeb ABS
##20 33 92 JSR 9233 ABS
##20 15 6a JSR 6a15 ABS
##20 68 13 JSR 1368 ABS
##4c ac 9c JMP 9cac ABS
##a5 09 LDA 09 DIR
##10 0d BPL 0d addr?
##20 a9 0e JSR 0ea9 ABS
##a9 36 LDA 36 IMM8
##85 26 STA 26 DIR
##20 50 8e JSR 8e50 ABS
##4c 59 8e JMP 8e59 ABS
##0a ASL
##10 03 BPL 03 addr?
##4c 4a 96 JMP 964a ABS
##a5 26 LDA 26 DIR
##69 29 ADC 29 IMM8
##4c 56 96 JMP 9656 ABS
##20 72 8e JSR 8e72 ABS
##a5 08 LDA 08 DIR
##10 db BPL db addr?
##20 b2 0e JSR 0eb2 ABS
##20 f2 93 JSR 93f2 ABS
##c2 21 REP 21
##98 TYA
##e2 20 SEP 20
##65 4b ADC 4b DIR
##a8 TAY
##b9 1f 00 LDA 001f ABS_Y
##20 5e 9d JSR 9d5e ABS
##a9 ff LDA ff IMM8
##99 1f 00 STA 001f ABS_Y
##20 1b 91 JSR 911b ABS
##BRA bd BRA bd addr?
##a5 09 LDA 09 DIR
##a0 ASL
##10 14 BPL 14 addr?
##20 b2 0e JSR 0eb2 ABS
##20 5f 1e JSR 1e5f ABS
##b0 0a BCS 0a addr?
##20 eb 9e JSR 9eeb ABS
##a5 99 LDA 99 DIR
##d0 03 BNE addr?
##20 9f 96 JSR 969f ABS
##64 08 STZ 08 DIR
##4c e6 9e JMP 9ee6 ABS
##ea NOP

#79: Swap actor in Relic menu, retain Equip mode
#C3/9E7D:	20999E  	JSR $9E99      ; Draw menu, etc.
#C3/9E80:	204F96  	JSR $964F      ; Draw blue "EQUIP"
        space = Reserve(0x39e80, 0x39e83, "Draw blue EQUIP")
        space.write(
            asm.JSR(0x965b, asm.ABS)
        )
        #space.printr()

#7A: Swap actor in Relic menu, retain Remove mode
#C3/9E8B:	20999E  	JSR $9E99      ; Draw menu, etc.
#C3/9E8E:	205696  	JSR $9656      ; Draw blue "REMOVE"
        space = Reserve(0x39e8e, 0x39e91, "Draw blue REMOVE")
        space.write(
            asm.JSR(0x9660, asm.ABS)
        )
        #space.printr()
#Fork: Handle L and R, prepare for menu reset
#C3/9EDC:	20E69E  	JSR $9EE6      ; Plan Reequip pos
        space = Reserve(0x39edc, 0x39edf, "Plan Reequip pos")
        space.write(
            asm.JSR(0x98f2, asm.ABS)
        )
        #space.printr()
#Handle Reequip activation
#C3/9F1C:	205D96  	JSR $965D      ; Erase top text
        space = Reserve(0x39f1c, 0x39f1f, "Erase top text")
        space.write(
            asm.JSR(0x9665, asm.ABS)
        )
        #space.printr()
#Handle "EQUIP" selection in Relic menu
#C3/9FDB:	201496  	JSR $9614      ; Switch windows
#C3/9FDE:	204F96  	JSR $964F      ; Draw blue "EQUIP"
        space = Reserve(0x39fde, 0x39fe1, "Draw blue EQUIP")
        space.write(
            asm.JSR(0x965b, asm.ABS)
        )
        #space.printr()
#C3/9FEF:	205696  	JSR $9656      ; Draw blue "REMOVE"
        space = Reserve(0x39fef, 0x39ff2, "Draw blue REMOVE")
        space.write(
            asm.JSR(0x9660, asm.ABS)
        )
#Fork: Handle L and R, prepare for menu reset
#C3/A047:	20E69E  	JSR $9EE6      ; Plan Reequip pos
        space = Reserve(0x3a047, 0x3a04a, "Plan Reequip pos")
        space.write(
            asm.JSR(0x98f2, asm.ABS)
        )
        #space.printr()
#Fork: Handle L and R, prepare for menu reset
#C3/A146:	20E69E  	JSR $9EE6      ; Plan Reequip pos
        space = Reserve(0x3a146, 0x3a149, "Plan Reequip pos")
        space.write(
            asm.JSR(0x98f2, asm.ABS)
        )
        #space.printr()


##    y_equip_relics_sub = Substitution()
##    y_equip_relics_sub.set_location(0x30247)
##    y_equip_relics_sub.bytestring = bytes([0x1e, 0x96])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x30287)
##    y_equip_relics_sub.bytestring = bytes([0xcd, 0x98])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x31be9)
##    y_equip_relics_sub.bytestring = bytes([0x5b, 0x96])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x31bf7)
##    y_equip_relics_sub.bytestring = bytes([0x60, 0x96])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x3960d)
##    y_equip_relics_sub.bytestring = bytes([0x65, 0x96])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39615)
##    y_equip_relics_sub.bytestring = bytes([0x0c, 0x96,
##        0xe6, 0x3a, 0xa9, 0x2c, 0x85, 0x29, 0x60, 0x20, 0x0c, 0x96, 0x20,
##        0x4e, 0x90, 0x20, 0x56, 0x8e, 0xa5, 0x08, 0x10, 0x0b, 0x20, 0xb2,
##        0x0e, 0x7b, 0xa5, 0x4b, 0x0a, 0xaa, 0x7c, 0x6c, 0x96, 0xa5, 0x09,
##        0x10, 0x0d, 0x20, 0xa9, 0x0e, 0x20, 0x10, 0x91, 0xa9, 0x04, 0x85,
##        0x27, 0x64, 0x26, 0x60, 0x0a, 0x10, 0x0a, 0x20, 0xb2, 0x0e, 0xa9,
##        0x58, 0x85, 0x26, 0xe6, 0x25, 0x60, 0xa9, 0x35, 0x85, 0xe0, 0x4c,
##        0x22, 0x20, 0xa0, 0x09, 0xa3, 0x80, 0x08, 0xa0, 0x11, 0xa3, 0x80,
##        0x03, 0xa0, 0xea, 0xa2, 0x4c, 0xf9, 0x02, 0x60])
##        #86 bytes
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39672)
##    y_equip_relics_sub.bytestring = bytes([0x9a])
##    y_equip_relics_sub.write(fout)
##    y_equip_relics_sub.set_location(0x39678)
##    y_equip_relics_sub.bytestring = bytes([0x5b])
##    y_equip_relics_sub.write(fout)
##    y_equip_relics_sub.set_location(0x39692)
##    y_equip_relics_sub.bytestring = bytes([0x60, 0x96, 0x20, 0x7a, 0x96,
##        0xe6, 0x26, 0x60, 0x20, 0xa8, 0x96, 0x80, 0xe9, 0xa9, 0x35, 0x85,
##        0x26, 0x64, 0x27, 0xc6, 0x25])
##        #21 bytes
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x3988c)
##    y_equip_relics_sub.bytestring = bytes([0x10, 0x21, 0x20, 0xb2, 0x0e,
##        0xa5, 0x4e, 0x85, 0x5f, 0xa2, 0x57, 0x55, 0x86, 0x26, 0x20, 0x59,
##        0x9b, 0x20, 0x50, 0xa1, 0x20, 0xeb, 0x9a, 0x20, 0x33, 0x92, 0x20,
##        0x15, 0x6a, 0x20, 0x68, 0x13, 0x4c, 0xac, 0x9c, 0xa5, 0x09, 0x10,
##        0x0d, 0x20, 0xa9, 0x0e, 0xa9, 0x36, 0x85, 0x26, 0x20, 0x50, 0x8e,
##        0x4c, 0x59, 0x8e, 0x0a, 0x10, 0x03, 0x4C, 0x4A, 0x96, 0xA5, 0x26,
##        0x69, 0x29, 0x4C, 0x56, 0x96, 0x20, 0x72, 0x8E, 0xA5, 0x08, 0x10,
##        0xDB, 0x20, 0xB2, 0x0E, 0x20, 0xF2, 0x93, 0xC2, 0x21, 0x98, 0xE2,
##        0x20, 0x65, 0x4B, 0xA8, 0xB9, 0x1F, 0x00, 0x20, 0x5E, 0x9D, 0xA9,
##        0xFF, 0x99, 0x1F, 0x00, 0x20, 0x1B, 0x91, 0x80, 0xBD, 0xA5, 0x09,
##        0x0A, 0x10, 0x14, 0x20, 0xB2, 0x0E, 0x20, 0x5F, 0x1E, 0xB0, 0x0A,
##        0x20, 0xEB, 0x9E, 0xA5, 0x99, 0xD0, 0x03, 0x20, 0x9F, 0x96, 0x64,
##        0x08, 0x4C, 0xE6, 0x9E, 0xEA])
##        #131 bytes
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39e81)
##    y_equip_relics_sub.bytestring = bytes([0x5b])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39e8f)
##    y_equip_relics_sub.bytestring = bytes([0x60])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39edd)
##    y_equip_relics_sub.bytestring = bytes([0xf2, 0x98])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39f1d)
##    y_equip_relics_sub.bytestring = bytes([0x65])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39fdf)
##    y_equip_relics_sub.bytestring = bytes([0x5b])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x39ff0)
##    y_equip_relics_sub.bytestring = bytes([0x60])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x3a048)
##    y_equip_relics_sub.bytestring = bytes([0xf2, 0x98])
##    y_equip_relics_sub.write(fout)
##
##    y_equip_relics_sub.set_location(0x3a147)
##    y_equip_relics_sub.bytestring = bytes([0xf2, 0x98])
##    y_equip_relics_sub.write(fout)
