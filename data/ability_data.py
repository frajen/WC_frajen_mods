class AbilityData:
    DATA_SIZE = 14

    def __init__(self, id, data):
        self.id = id

        self.targets        = data[0]
        self.elements       = data[1]
        self.flags1         = data[2]
        self.flags2         = data[3]
        self.flags3         = data[4]
        self.mp             = data[5]
        self.power          = data[6]
        self.flags4         = data[7]
        self.accuracy       = data[8]
        self.effect         = data[9]
        self.status1        = data[10]
        self.status2        = data[11]
        self.status3        = data[12]
        self.status4        = data[13]

    def ability_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0]     = self.targets
        data[1]     = self.elements
        data[2]     = self.flags1
        data[3]     = self.flags2
        data[4]     = self.flags3
        data[5]     = self.mp
        data[6]     = self.power
        data[7]     = self.flags4
        data[8]     = self.accuracy
        data[9]     = self.effect
        data[10]    = self.status1
        data[11]    = self.status2
        data[12]    = self.status3
        data[13]    = self.status4

        return data


#Offset	Description"
#$00	Targeting"
    #$01	Allows movable cursor for single target"
    #$02	Disable switch of targets between groups"
    #$04	Select all targets (both groups)"
    #$08	Select one group"
    #$10	Auto-accept default selection"
    #$20	Multiple selection possible"
    #$40	Enemy selected by default"
    #$80	Random selection"
#$01	Elemental Properties"
    #$01	Fire"
    #$02	Ice"
    #$04	Lightning"
    #$08	Poison"
    #$10	Wind"
    #$20	Pearl/Holy"
    #$40	Earth"
    #$80	Water"
#$02	Spell flags 1"
    #$01	physical damage"
    #$02	miss if protected against death"
    #$04	target only dead allies"
    #$08	inverse damage for undead"
    #$10	randomize target"
    #$20	ignore defense"
    #$40	don't split damage on multiple targets"
    #$80	abort if used against allies"
#$03	Special flags 2"
    #$01	Can use spell on menu (field)"
    #$02	Ignore reflect"
    #$04	Learn as lore if cast"
    #$08	Allow runic"
    #$10	???"
    #$20	Change target if actual target is dead"
    #$40	Kill user after spell is cast"
    #$80	Use MP damage"
#$04	Special flags 3"
    #$01	Heal target"
    #$02	Drain from target to caster"
    #$04	Lift status"
    #$08	Toggle status"
    #$10	Use stamina in evasion formula"
    #$20	Can't dodge"
    #$40	Hits if target level is multiple of spell hit rate"
    #$80	Use fractal damage (spell power should be between 1 and 16)"
    #$05	MP Cost"
    #$06	Spell power"
#$07	Special flags 4"
    #$01	Miss if target is protected against status"
    #$02	Show text if spell hits (monster only)"
    #$04	???"
    #$08	???"
    #$10	???"
    #$20	???"
    #$40	???"
    #$80	???"
#$08	Hit rate of spell"
#$09	Special effect"
#$0A	Status 1"
#$0B	Status 2"
#$0C	Status 3"
#$0D	Status 4"
