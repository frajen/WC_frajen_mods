from memory.space import Bank, START_ADDRESS_SNES, Reserve, Allocate, Write
import instruction.asm as asm

def equipable_umaro(character_count):
    space = Reserve(0x31e6f, 0x31e6f, "Compare character id for equipment menu")
    space.write(character_count)

    space = Reserve(0x39ef4, 0x39ef7, "Reequip Umaro if genji glove/gauntlet/merit award equipped/removed", asm.NOP())

def set_starting_level(start_level):
    space = Reserve(0x09fc6, 0x09fc6, "Starting level")
    space.write(start_level.to_bytes(1, 'little'))

def update_morph_character(characters):
    from constants.commands import id_name

    # NOTE: this assumes only 1 character has morph
    for character in characters:
        for command in character.commands:
            if id_name[command] == "Morph":
                space = Reserve(0x25e33, 0x25e33, "character who charges up morph gauge by gaining magic points")
                space.write(character.id)
                return

def show_original_names():
    import data.text as text
    from data.characters import Characters

    space = Allocate(Bank.C3, 195, "characters show original names")
    original_names_table = space.next_address
    for index in range(Characters.CHARACTER_COUNT):
        name = Characters.DEFAULT_NAME[index]

        values = text.get_bytes(name, text.TEXT3)
        values.extend([0xFF] * (Characters.NAME_SIZE - len(values))) # pad ending with ' '
        space.write(values)

    draw_original_name = space.next_address
    space.write(
        asm.JSR(0x3519, asm.ABS),   # y = address of character data in sram (+0x1600)
        asm.LDA(0x0000, asm.ABS_Y), # a = character index
        asm.CMP(Characters.CHARACTER_COUNT, asm.IMM8), # is it not a normal character (ex: moogles)?
        asm.BGE("RETURN"),
        asm.STA(0x4202, asm.ABS),
        asm.LDA(Characters.NAME_SIZE, asm.IMM8),
        asm.STA(0x4203, asm.ABS),
        asm.NOP(),                  # multiply...
        asm.NOP(),
        asm.NOP(),
        asm.LDX(0x4216, asm.ABS),   # x = name length * character index
        asm.LDY(0x0006, asm.IMM16), # y = length of string to draw

        "LOOP_START",
        asm.LDA(original_names_table, asm.LNG_X),
        asm.STA(0x2180, asm.ABS),   # store character in name string to draw
        asm.INX(),                  # increment string character index
        asm.DEY(),                  # decrement name length counter
        asm.BNE("LOOP_START"),      # branch if length counter not zero
        asm.STZ(0x2180, asm.ABS),   # store null
        asm.JMP(0x7fd9, asm.ABS),   # call draw string
        "RETURN",
        asm.RTS(),
    )

    # draw original names under the 4 character names in party menu and above the character name in party select menu
    original_code_size = 5
    original_code_starts = [0x3331e, 0x3336a, 0x333b6, 0x33402, 0x3798d]
    positions = [0x3959, 0x3ad9, 0x3c59, 0x3dd9, 0x3a5b]
    for index, original_code_start in enumerate(original_code_starts):
        original_code_end = original_code_start + original_code_size

        menu_draw_name = space.next_address
        space.copy_from(original_code_start, original_code_end) # draw character name
        space.write(
            asm.LDY(positions[index], asm.IMM16),
            asm.JSR(draw_original_name, asm.ABS),
            asm.RTS(),
        )

        # replace draw character name with call to draw name and original name
        original_space = Reserve(original_code_start, original_code_end, "characters draw original name", asm.NOP())
        original_space.write(
            asm.JSR(menu_draw_name, asm.ABS),
        )


### Mod for dynamically changing character start level
#
# Data: Level factor adjustment from average
# C0/A228:    00          (add 0)
# C0/A229:    02          (add 2)
# C0/A22A:    05          (add 5)
# C0/A22B:    FD          (subtract 3)

def mod_level_factor_adjustment(mod0=0x0, mod1=0x02, mod2=0x05, mod3=0xFE):
    space = Reserve(0x0a228, 0x0a228, "add 0")
    space.write(mod0)

    space = Reserve(0x0a229, 0x0a229, "add 2")
    space.write(mod1)

    space = Reserve(0x0a22a, 0x0a22a, "add 5")
    space.write(mod2)

    space = Reserve(0x0a22b, 0x0a22b, "subtract 3")
    space.write(mod3)

# negative levels? See c0 recruit_character. C0/9F45 prevented negative levels at one point but
# not sure where it is now
# C0/9F45:	9029    	BCC $9F70      (if it's less, don't change it, HP, MP, or stats)
