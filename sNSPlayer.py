class player:
    id=None
    name=None
    race=None
    age=None
    alignment=None
    level=None
    proficiency=None
    specials=None
    armorType=None
    weaponMain=None
    weaponMDMG=None
    weaponOff=None
    weaponODMG=None
    statEffects=None
    spd=None
    strenth=None
    acc=None
    intellect=None
    cha=None
    maxHP=None
    atk=None
    arm=None
    hp=None
    gold=None
    inventory=None
    bac=None
    sleep=None
    foraging=None
    luck=None
    luckDur=None

    def __init__(self,id,name):
        self.id=id
        self.name=name
        self.race=''
        self.age=0
        self.alignment=''
        self.level=1
        self.proficiency=''
        self.specials=''
        self.armorType=''
        self.weaponMain=''
        self.weaponMDMG=0
        self.weaponOff=''
        self.weaponODMG=0
        self.statEffects=''
        self.spd=0
        self.strenth=0
        self.acc=0
        self.intellect=0
        self.cha=0
        self.maxHP=0
        self.atk=0
        self.arm=0
        self.hp=0
        self.gold=0
        self.inventory=[]
        self.bac=0.0
        self.sleep=0.0
        self.foraging=0
        self.luck=0
        self.luckDur=0

    def fullInspect(self):
        return "**--Info--\nName:** "+self.name+"\n**Race:** "+self.race+"\n**Age:** "+str(self.age)+"\n**Alignment:** "+self.alignment+"\n**Level:** "+str(self.level)+"\n**Class/Proffeciency: **"+self.proficiency+"\n**Specials: **"+self.specials+"\n**--Equip--\nArmor Type:** "+self.armorType+"\n**Weapon (Mainhand): **"+self.weaponMain+"\n**Weapon Damage (Main): **"+str(self.weaponMDMG)+"\n**Weapon (Off-hand): **"+self.weaponOff+"\n**Weapon Damage (Off): **"+str(self.weaponODMG)+"\n**--Stats--\nStatus Effects: **"+self.statEffects+"\n**Speed: **"+str(self.spd)+"\n**Strength: **"+str(self.strenth)+"\n**Accuracy: **"+str(self.acc)+"\n**Intellect: **"+str(self.intellect)+"\n**Charisma: **"+str(self.cha)+"\n**Max HP: **"+str(self.maxHP)+"\n**ATK: **"+str(self.atk)+"\n**ARM: **"+str(self.arm)+"\n**HP: **"+str(self.hp)+"\n**Gold: **"+str(self.gold)+"\n**Inventory: **"+self.strInv()  
    def inspect(self):
        return "**Name: **"+self.name+"\n**Level: **"+str(self.level)+"\n**Specials: **"+self.specials+"\n**Status Effects: **"+self.statEffects+"\n**Speed: **"+str(self.spd)+"\n**Strength: **"+str(self.strenth)+"\n**Accuracy: **"+str(self.acc)+"\n**Intellect: **"+str(self.intellect)+"\n**Charisma: **"+str(self.cha)+"\n**Max HP: **"+str(self.maxHP)+"\n**ATK: **"+str(self.atk)+"\n**ARM: **"+str(self.arm)+"\n**HP: **"+str(self.hp)+"\n**Gold: **"+str(self.gold)+"\n**Inventory: **"+self.strInv() 
    def strInv(self):
        msg=''
        for x in self.inventory:
            if x[1]==1:
                msg=msg+x[0]+", "
            else:
                msg=msg+x[0]+" ("+str(x[1])+"), "
        return msg

class gun:
    id=None
    loaded=None
    total=None
    max=None
    ammo=None

    def __init__(self,id,loaded,total,max,ammo):
        self.id=id
        self.loaded=loaded
        self.total=total
        self.max=max
        self.ammo=ammo

class buddie:
    name=None
    ability=None
    friendLevel=None
    hp=None
    max=None

    def __init__(self,name,ability,friendLevel,hp,max):
        self.name=name
        self.ability=ability
        self.friendLevel=friendLevel
        self.hp=hp
        self.max=max
    
    def toString(self):
        return "**Name:** "+self.name+", **Ability:** "+self.ability+",** Friend Level: **"+str(self.friendLevel)+", **HP:** "+str(self.hp)+",** Max HP:** "+str(self.max)

