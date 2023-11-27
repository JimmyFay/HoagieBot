import discord
import random
import os
import pytube
import openpyxl
import math
from discord.ext import commands
from pytube import YouTube
from pytube import Search
from openpyxl import load_workbook
from sNSPlayer import player, gun, buddie
import pickle

#Discord authorization
intents = discord.Intents.all()
#intents.message_content = True
#intents.members = True
bot = commands.Bot(command_prefix='~', intents=intents)
applicationID= "INSERT DISCORD APP ID HERE"
publickey= "INSERT BOT PUBLIC KEY HERE"
token="PRIVATE BOT TOKEN"
allowed_mentions = discord.AllowedMentions(everyone = True)

#A few different arrays for random choice calls for some random interractions, censored for professionalism.
ick=["CENSORED"]
gunshot=['*PEW*','*BANG*','*KAPEW*','*BAM*']
shotself=["CENSORED"]
badsleep=["CENSORED"]
oksleep=["CENSORED"]
goodsleep=["CENSORED"]
crapmats=["yellow root","purple root","green root","blue root","orange root","red root","black root","rock"]
okmats=["carbon","mysterious toadstool","murkweed","spikeweed","rootweed","fury bloom","worm","fat worm","horn beetle","turtle","feathers","rabbit"]
raremats=["yellow lizard","purple lizard","green lizard","blue lizard","orange lizard","red lizard","grey lizard","special flower","deathweed"]
enemies=[]

#important vars
#Here is where I had stored the paths to different folders and assets, as well as users' discord ids. These have been removed for privacy.
#Any references to "myID" refers to the discord id of the dm, so certain commands will exclude that id from displaying since the dm has no stats

#For use in later implementation of furthering the audio playback possibilities.
queue=[]

#For the roll method later on, simulates a d20
rolls=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

#Arrays of various "game states" most are read from binary files and changed locally then just overwriting the whole file on a change to save binary parsing. 
chars=[]
guns=[]
lores=[]
drinkys=[]
beastys=[]
archives=[]
potionys=[]
buddys=[]
debuffss=[]

#Basic open and write functions for each binary file
with open('characters.bin','rb') as f: #load chars
    while True:
        try: 
            chars.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break
with open('guns.bin','rb') as f: #load guns
    while True:
        try: 
            guns.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break
with open('lore.bin','rb') as f: #load lore
    while True:
        try: 
            lores.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break
with open('drinks.bin','rb') as f: #load drinks
    while True:
        try: 
            drinkys.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break
with open('beasts.bin','rb') as f: #load beasts
    while True:
        try: 
            beastys.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break
with open('archive.bin','rb') as f: #load archive
    while True:
        try: 
            archives.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break
with open('potions.bin','rb') as f: #load potions
    while True:
        try: 
            potionys.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break        
with open('buds.bin','rb') as f:
    while True:
        try:
            buddys.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break    
with open('debuffs.bin','rb') as f:
    while True:
        try:
            debuffss.append(pickle.load(f))
        except (EOFError,pickle.UnpicklingError):
            break 

def writeChars():
    global chars
    f=open("characters.bin","wb")
    for x in chars:
        pickle.dump(x,f)
    f.close()
def writeGuns():
    global guns
    f=open("guns.bin","wb")
    for x in guns:
        pickle.dump(x,f)
    f.close()
def writeLore():
    global lores
    f=open("lore.bin","wb")
    for x in lores:
        pickle.dump(x,f)
    f.close()
def writeDrinks():
    global drinkys
    f=open("drinks.bin","wb")
    for x in drinkys:
        pickle.dump(x,f)
    f.close()
def writeBeasts():
    global beastys
    f=open("beasts.bin","wb")
    for x in beastys:
        pickle.dump(x,f)
    f.close()
def writeArchive():
    global archives
    f=open("archive.bin","wb")
    for x in archives:
        pickle.dump(x,f)
    f.close()
def writePotions():
    global potionys
    f=open("potions.bin","wb")
    for x in potionys:
        pickle.dump(x,f)
    f.close()
def writeBuds():
    global buddys
    f=open("buds.bin","wb")
    for x in buddys:
        pickle.dump(x,f)
    f.close()
def writeDebuffs():
    global debuffss
    f=open("debuffs.bin","wb")
    for x in debuffss:
        pickle.dump(x,f)
    f.close()

#These provide an easy way to index character objects
def findChar(id):
    for x in chars:
        #print("id is: "+str(id)+", x id is:"+str(x.id))
        if str(x.id)==str(id):
           # print(chars.index(x))
            return chars.index(x)
def findGun(id):
    y=-1
    for x in guns:
        if str(x.id)==str(id):
            y=guns.index(x)
            break
    return y

#inititializes a character object into the system, this I do manually to avoid confusion on the player side of things
def initChar(char,id,name,race,age,alignment,level,proficiency,specials,armorType,
             weaponMain,weaponMDMG,weaponOff,weaponODMG,statEffects,spd,strenth,
             acc,intellect,cha,maxHP,atk,arm,hp,gold,bac,sleep,foraging,luck,luckDur):
    chars[char].id=id
    chars[char].name=name
    chars[char].race=race
    chars[char].age=age
    chars[char].alignment=alignment
    chars[char].level=level
    chars[char].proficiency=proficiency
    chars[char].specials=specials
    chars[char].armorType=armorType
    chars[char].weaponMain=weaponMain
    chars[char].weaponMDMG=weaponMDMG
    chars[char].weaponOff=weaponOff
    chars[char].weaponODMG=weaponODMG
    chars[char].statEffects=statEffects
    chars[char].spd=spd
    chars[char].strenth=strenth
    chars[char].acc=acc
    chars[char].intellect=intellect
    chars[char].cha=cha
    chars[char].maxHP=maxHP
    chars[char].atk=atk
    chars[char].arm=arm
    chars[char].hp=hp
    chars[char].gold=gold
    chars[char].bac=bac
    chars[char].sleep=sleep
    chars[char].foraging=foraging
    chars[char].luck=luck
    chars[char].luckDur=luckDur
    f=open("characters.bin","wb")
    writeChars()
    f.close()
#similar to the reasoning of initChar this method is meant for quick updates to player stats while the bot is down, the changes will save the next time the bot is ran
def editChar(id,info):
    for x in chars:
        if x.id==id:
            print("found char")
            #change to whatever needs to be edited
            writeChars()
            break

#events 
@bot.event 
async def on_ready():
    print('logged in as {0.user}'.format(bot))

#basic commands
@bot.command(hidden=True)
async def author(ctx):
    await ctx.send(ctx.author)
@bot.command(hidden=True)
async def id(ctx):
    await ctx.send(ctx.author.id)
@bot.command(hidden=True)
async def summon(ctx):
    await ctx.send(content = "@everyone", allowed_mentions = allowed_mentions)
@bot.command(hidden=True)
async def online(ctx):
    for user in ctx.guild.members:
        print(user.id)
        print(user.name)
        print(user.status)
        print('\n')

#game commands
@bot.command(brief='Supply the sided dice you wish to roll') #generates a random 1-n
async def d(ctx,x:int):
    await ctx.send(str(random.randint(1,x)))
@bot.command(brief='Rolls a D20') #generates a random 1-20 n times, also taking into account the players luck stat, making it harder to get good or bad rolls
async def roll(ctx,*args):
    msg=''
    ind=findChar(ctx.author.id)
    if ind <0:
        ind=0
    luck=chars[ind].luck
    dVal=chars[ind].luckDur
    x=1
    if len(args)>0:
        if args[0].isnumeric():
            x=args[0]
    for a in range(int(x)):
        if not str(ctx.channel)=="jamies-rolls": #a special exception where rolls "don't count" in a specific channel
            if not (luck==0): #check if worth updating luck
                if (dVal==0): #end duration
                    luck=0
                    chars[ind].luck=0
                else: #more duration
                    chars[ind].luckDur=dVal-1
            writeChars()
        weight=[1*(math.exp(-luck)),1+(-luck/4),1+(-luck/4),1+(-luck/4),1+(-luck/4),1+(-luck/4),1+(-luck/4),1+(-luck/4),1+(-luck/4),1+(-luck/4),
                1+(luck/4),1+(luck/4),1+(luck/4),1+(luck/4),1+(luck/4),1+(luck/4),1+(luck/4),1+(luck/4),1+(luck/4),1*(math.exp(luck))] #this formula was half made from a chatgpt question but didn't actually work so I fixed it to get a distribution I liked
        total=sum(weight)
        weighted=[w/total for w in weight]
        msg=msg+str(random.choices(rolls,weights=weighted,k=1)[0])+'\n'
    await ctx.send(msg)
@bot.command()  #shows the players current luck, or modifies it based on arguments given
async def luck(ctx,*args):
    ind=findChar(ctx.author.id)
    if len(args)>0:
        if args[0]=='+':
            chars[ind].luck=chars[ind].luck+1
        if args[0]=='-':
            chars[ind].luck=chars[ind].luck-1
        chars[ind].luckDur=5
        writeChars()
    await ctx.send("Feelin lucky? Luck: "+str(chars[ind].luck))
@bot.command(brief='Makes your new character in my system.')
async def newChar(ctx,*,name:str): 
    chars.append(player(ctx.author.id,name))
    writeChars()
    for x in chars:
        print(x)
    await ctx.send(name+': Was added!')   
@bot.command(brief='Shows all current characters.')
async def allChars(ctx):
    for x in chars:
        msg=msg+x.name+'\n'
    await ctx.send(msg)
@bot.command(hidden=True) #A admin command to see the inspect of any player character
async def peek(ctx,id:str):
    ind=findChar(id)
    msg=chars[ind].fullInspect()
    await ctx.send(msg)
@bot.command(brief='Shows your full character sheet.')
async def inspectFull(ctx):
    ind=findChar(ctx.author.id)
    msg=chars[ind].fullInspect()
    await ctx.send(msg)
@bot.command(brief='Shows a quick snapshot of your stats.')
async def inspect(ctx):
    ind=findChar(ctx.author.id)
    msg=chars[ind].inspect()
    await ctx.send(msg)
@bot.command(brief='Adds an item to your inventory.') #A fairly complicated and still mildly buggy way to track inventory, sensitive to typos but includes automatic stacking of items
async def add(ctx,*,string:str):
    all=string.split(',')
    for x in all:
        item=x.lower().strip()
        item2=item
        l=item.split(' ')
        if l[-1].isnumeric():
            #print("last of l is "+l[-1])
            item2=item.replace(l[-1],'')
            item2=item2.rstrip()
            q=l[-1]
            #print("Item2 is: "+item2+".")
        else:
            q=1
        ind=findChar(ctx.author.id)
        found=False
        for x in chars[ind].inventory:
            if x[0]==item2:
                #print("stacking item")
                x[1]=int(x[1])+int(q)
                found=True
                break
        if not found:
            #print("adding item")
            chars[ind].inventory.append([item2,q])
        writeChars()
        if any(word in item for word in ick):
            await ctx.send("Gross... added: "+item+" to inventory.")
        else:
            await ctx.send("Added: "+item+" to inventory.")
@bot.command(brief='Removes item from inventory.') #same process as add
async def remove(ctx,*,string:str):
    all=string.split(',')
    for x in all:
        item=x.lower().strip()
        item2=item
        l=item.split(" ")
        if l[-1].isnumeric():
            a=l[-1]
            item2=item.replace(l[-1],'')
            item2=item2.rstrip()
        else:
            a=1
        ind=findChar(ctx.author.id)
        found=False
        for x in chars[ind].inventory:
            if x[0]==item2: #found item
                found=True
                if x[1]==1:
                    chars[ind].inventory.remove(x)
                else:
                    x[1]=int(x[1])-int(a)
                    if x[1]<1:
                        chars[ind].inventory.remove(x)
                writeChars()
                break
        if not found:
            await ctx.send("Couldn't find that item...")
        else:
            await ctx.send("Removed: "+str(item))
@bot.command(brief='...') #this is mildly useless but a fun way to have player interraction
async def levelUp(ctx):
    ind=findChar(ctx.author.id)
    chars[ind].level=chars[ind].level+1
    writeChars()
    if (ctx.guild.voice_client!=None and ctx.message.author.voice):
        voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
        if not voice.is_playing():
            file=fXpath.rstrip()+'levelup.wav'
            voice.play(discord.FFmpegPCMAudio(file)) 
    await ctx.send("Levelled up!")
@bot.command(brief='Takes a specified amount of damage.') #takes damage to player counting armor
async def take(ctx,dmg:int):
    ind=findChar(ctx.author.id)
    dmg=dmg-chars[ind].arm
    if dmg>0:
        chars[ind].hp=chars[ind].hp-dmg
    else:
        dmg=1
        chars[ind].hp=chars[ind].hp-dmg
    writeChars()
    print(ctx.author.id)
    if (ctx.guild.voice_client!=None): #each player has a unique "hurt" sound, we use minecraft mob noises for fun
        voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
        if not voice.is_playing():
            match ctx.author.id:
                #CENSORED for user privacy
                case _:
                    file=''
            voice.play(discord.FFmpegPCMAudio(file)) 
    await ctx.send("Took "+str(dmg)+" dmg!")
@bot.command(brief='For gold transactions.') #currency
async def gold(ctx,*args): 
    ind=findChar(ctx.author.id)
    if len(args)<1:#no arg
        await ctx.send("Current purse is: "+str(chars[ind].gold))
        if (ctx.guild.voice_client!=None):
            voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
            if not voice.is_playing():
                file=fXpath.rstrip()+'goldCheck.wav'
                voice.play(discord.FFmpegPCMAudio(file)) 
    else:
        chars[ind].gold=chars[ind].gold+int(args[0])
        writeChars()
        if (ctx.guild.voice_client!=None):
            voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
            if not voice.is_playing():
                if int(args[0])<0:
                    file=fXpath.rstrip()+'goldPay.wav'
                else:
                    file=fXpath.rstrip()+'goldGain.wav'
                voice.play(discord.FFmpegPCMAudio(file)) 
        await ctx.send("Current purse is: "+str(chars[ind].gold))
@bot.command(brief='All specials atk.') #a few character object entry retrievals
async def specials(ctx):
    ind=findChar(ctx.author.id)
    await ctx.send("Specials: "+str(chars[ind].specials))
@bot.command()
async def inventory(ctx):
    ind=findChar(ctx.author.id)
    await ctx.send("Inventory: \n"+chars[ind].strInv())
@bot.command(brief="Displays current hp of all active members.")
async def hp(ctx):
    msg=''
    for user in ctx.guild.members:
        if (str(user.id)!=myID and user.id!=CENSORED):
            for x in chars:
                if x.id==str(user.id):
                    msg=msg+x.name+": "+str(x.hp)+'\n'
                    break
    await ctx.send(msg)
@bot.command(brief="Displays atk of all active members.")
async def atk(ctx):
    msg=''
    for user in ctx.guild.members:
        if (str(user.id)!=myID and user.id!=1066440248336338976):
            for x in chars:
                if x.id==str(user.id):
                    msg=msg+x.name+": "+str(x.atk)+'\n'
                    break
    await ctx.send(msg)
@bot.command(brief="Displays speed of all active members.")
async def spd(ctx):
    msg=''
    for user in ctx.guild.members:
        if (str(user.id)!=myID and user.id!=1066440248336338976):
            for x in chars:
                if x.id==str(user.id):
                    msg=msg+x.name+": "+str(x.spd)+'\n'
                    break
    await ctx.send(msg)
@bot.command(brief="Displays intellect of all active members.")
async def intellect(ctx):
    msg=''
    for user in ctx.guild.members:
        if (str(user.id)!=myID and user.id!=1066440248336338976):
            for x in chars:
                if x.id==str(user.id):
                    msg=msg+x.name+": "+str(x.intellect)+'\n'
                    break
    await ctx.send(msg)
@bot.command(brief="Displays accuracy of all active members.")
async def acc(ctx):
    msg=''
    for user in ctx.guild.members:
        if (str(user.id)!=myID and user.id!=1066440248336338976):
            for x in chars:
                if x.id==str(user.id):
                    msg=msg+x.name+": "+str(x.acc)+'\n'
                    break
    await ctx.send(msg)
@bot.command(brief="Displays charisma of all active members.")
async def cha(ctx):
    msg=''
    for user in ctx.guild.members:
        if (str(user.id)!=myID and user.id!=1066440248336338976):
            for x in chars:
                if x.id==str(user.id):
                    msg=msg+x.name+": "+str(x.cha)+'\n'
                    break
    await ctx.send(msg)
@bot.command(brief="Displays max HP of all active members.")
async def maxHP(ctx):
    msg=''
    for user in ctx.guild.members:
        if (str(user.id)!=myID and user.id!=1066440248336338976):
            for x in chars:
                if x.id==str(user.id):
                    msg=msg+x.name+": "+str(x.maxHP)+'\n'
                    break
    await ctx.send(msg)
@bot.command(brief="Your character takes a drink") #just a fun hidden drunkenness stat
async def drink(ctx,*args):
    z=0
    if len(args)>0:
        z=args[0]
    else:
        z=1
    ind=findChar(ctx.author.id)
    chars[ind].bac=chars[ind].bac+(float(z)*.01)
    writeChars()
    await ctx.send("Bottoms up!")
@bot.command()
async def sober(ctx):
    ind=findChar(ctx.author.id)
    if chars[ind].bac>.05:
        chars[ind].bac=chars[ind].bac-.05
    else:
        chars[ind].bac=0.0
    #wb.save("SnS.xlsx")
    writeChars
    await ctx.send("*Whew... need some water.*")
@bot.command()
async def BAC(ctx):
    ind=findChar(ctx.author.id)
    await ctx.send("Current BAC is: "+str(chars[ind].bac))
@bot.command() #gives the players descriptions of how they slept, dreams etc, has a hidden stat where worse and worse sleep will continue to stack
async def sleep(ctx):
    z=random.randrange(1,21)
    ind=findChar(ctx.author.id)
    z=z+chars[ind].sleep
    if z<6:
        await ctx.send("You slept terribly last night... "+random.choice(badsleep))
        chars[ind].sleep=chars[ind].sleep-.5
        #wb.save("SnS.xlsx")
        writeChars()
    elif z<16:
        await ctx.send("You got some OK sleep last night... "+random.choice(oksleep))
    else:
        chars[ind].sleep=chars[ind].sleep+.5
        if chars[ind].hp+5>chars[ind].maxHP:
            chars[ind].hp=chars[ind].maxHP
            writeChars()
        else:
            chars[ind].hp=chars[ind].hp+5
            writeChars()
        await ctx.send("You slept Great last night and recovered some HP... "+random.choice(goodsleep)+'\n New HP is now '+str(chars[ind].hp))
@bot.command()
async def heal(ctx, z:int):
    ind=findChar(ctx.author.id)
    if chars[ind].hp+z>chars[ind].maxHP:
        chars[ind].hp=chars[ind].maxHP
        writeChars()
    else:
        chars[ind].hp=chars[ind].hp+z
        writeChars()
    if (ctx.guild.voice_client!=None):
        file=fXpath.rstrip()+'healthUp.wav'
        print(file)
        voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
        if not voice.is_playing():
                    voice.play(discord.FFmpegPCMAudio(file))
    await ctx.send("You've recovered "+str(z)+" health! Now at "+str(chars[ind].hp)+" HP.")
@bot.command() #for item gathering for potions nobody uses :_)
async def forage(ctx):
    z=random.randrange(1,11)
    msg="You found: "
    ind=findChar(ctx.author.id)
    y=chars[ind].foraging
    while z>0:
        i=y+random.randrange(1,21)
        if i>19:
            msg=msg+random.choice(raremats)+', '
        elif i>14:
            msg=msg+random.choice(okmats)+', '
        else:
            msg=msg+random.choice(crapmats)+', '
        z=z-1
    msg=msg+"\nAdd what you'd like to keep to inventory and discard the rest."
    await ctx.send(msg)
@bot.command(hidden=True) #a way to edit a character on the fly, I dont like using this as its too user error prone
async def edit(ctx,*,comm:str):
    l=comm.split("$")
    id=l[0]
    entry=l[1]
    data=l[2]
    append=""
    if len(l)==4:
        append=l[3]
    print(id,entry,data,append)
    ind=findChar(id)
    if append=="+":
        match entry:
            case 'specials': 
                chars[ind].specials=chars[ind].specials+"\n"+str(data)
            case 'statEffects':
                chars[ind].statEffects=chars[ind].statEffects+str(data)
    else:
        match entry:
            case 'specials': 
                chars[ind].specials=data
            case 'weaponMain':
                chars[ind].weaponMain=data
            case 'weaponMDMG':
                chars[ind].weaponMDMG=int(data)
            case 'weaponOff':
                chars[ind].weaponOff=data
            case 'weaponODMG':
                chars[ind].weaponODMG=int(data)
            case 'spd':
                chars[ind].spd=int(data)
            case 'strenth':
                chars[ind].strenth=int(data)
            case 'acc':
                chars[ind].acc=int(data)
            case 'intellect':
                chars[ind].intellect=int(data)
            case 'cha':
                chars[ind].cha=int(data)
            case 'maxHP':
                chars[ind].maxHP=int(data)
            case 'atk':
                chars[ind].atk=int(data)
            case 'arm':
                chars[ind].arm=int(data)
            case 'cock':
                chars[ind].cock=data
            case 'foraging':
                chars[ind].foraging=int(data)
    writeChars()
    await ctx.send("Edited!")
@bot.command() #Im 99 percent sure I never use this, but I'm scared to take it out
async def constructor(ctx): 
    await ctx.send("id,name,race,age,alignment,level,proficiency,specials,armorType,weaponMain,weaponMDMG,weaponOff,weaponODMG,statEffects,spd,strenth,acc,intellect,cha,maxHP,atk,arm,hp,gold,bac,sleep,foraging,luck,luckDur")
@bot.command() #A few commands for making digital enemies, this usually results in more time than is worth it being spent typing, faster to use a collaborative drawing document
async def addEnemy(ctx,name:str,hp:int):
    global enemies
    enemies.append([name,hp])
    await ctx.send("Added enemy.")
@bot.command()
async def allEnemies(ctx):
    global enemies
    msg=''
    for x in enemies:
        msg=msg+x[0]+': '+str(x[1])+'\n'
    if msg=='':
        await ctx.send("You have no enemies...")
    else:
        await ctx.send(msg)
@bot.command()
async def enemyTake(ctx,name:str,hp:int):
    global enemies
    for x in enemies:
        if x[0].lower()==name.lower():
            x[1]=x[1]-hp
            if x[1]<1:
                enemies.remove(x)
                await ctx.send(name+" has been killed.")
            else:
                await ctx.send(name+" took "+str(hp)+" dmg. "+str(x[1])+" hp remaining.")
            break
@bot.command() #Implemented this as way to track damage over time since i notoriously forget about it
async def debuff(ctx,*args):
    #PlayerID,Type,Amount,Duration
    if str(ctx.author.id)!=myID:
        print(ctx.author.id)
        print(myID)
        id=ctx.author.id
        type=args[0]
        dmg=args[1]
        dur=args[2]
        debuffss.append([id,args[0],int(args[1]),int(args[2])])
    else:
        id=args[0]
        type=args[1]
        dmg=args[2]
        dur=args[3]
        debuffss.append([args[0],args[1],int(args[2]),int(args[3])])
    await ctx.send(type+" (-"+str(dmg)+")"+" debuff added for "+str(dur)+" turns.")
    writeDebuffs()
@bot.command()
async def round(ctx):
    for x in debuffss:
        ind=findChar(x[0])
        chars[ind].hp=chars[ind].hp-int(x[2])
        x[3]=int(x[3])-1
        if int(x[3])==0:
            debuffss.remove(x)        
        await ctx.send(chars[ind].name+" took "+str(x[2])+" "+x[1]+" damage.")
        writeDebuffs()
@bot.command()
async def cleanse(ctx):
    for x in debuffss:
        if str(x[0])==str(ctx.author.id):
            debuffss.remove(x)
    await ctx.send("All debuffs removed.")
    writeDebuffs()
@bot.command()
async def debuffs(ctx):
    msg=''
    for x in debuffss:
        if str(x[0])==str(ctx.author.id):
            msg=msg+x[1]+" (-"+x[2]+") for "+x[3]+" turns.\n"
    if msg=='':
        await ctx.send("No debuffs.")
    else:
        await ctx.send(msg)
#lore commands
@bot.command() #these two link to a third party website we use
async def skillTree(ctx):
    await ctx.send("Private Link")
@bot.command()
async def battlemap(ctx):
    await ctx.send("Private Link")
#LORE
@bot.command(brief='Shows all the lore categories you can read from.')
async def categories(ctx,*args):
    await ctx.send("You can use ~lore, ~drinks, ~beasts, ~archives, or ~potions. \nIf no entry is specified, a random entry will be supplied.")
@bot.command(brief='Shows lore about a topic.')
async def lore(ctx,*args):
    item=''
    for x in args:
        item=item+x+' '
    item=(item.rstrip()).lower()
    found=False
    msg=''
    if item=='':
        x=random.randint(0,len(lores)-1)
        msg=lores[x][0]+": "+lores[x][1]
        if len(lores[x])==3:
            msg=msg+"\n"+lores[x][2]
        await ctx.send(msg) 
    else:
        for x in lores:
            if x[0].lower()==item:
                found=True
                msg=x[0]+": "+x[1] 
                if len(x)==3:
                    msg=msg+"\n"+x[2]
                break
        if found:   
            await ctx.send(msg)
        else:
            await ctx.send("Couldn't find \""+item+"\". Maybe try a different collection?")
@bot.command(brief='Shows the title of all lore entries')
async def allLore(ctx):   
    msg='All Lore entries:\n'
    for x in lores:
        msg=msg+x[0]+", "
    await ctx.send(msg)
@bot.command(brief='Displays specified map, or the continental map by default')
async def map(ctx,*args):
    if len(args)<1:
        await ctx.send('private file')
    else:
        name=''
        for x in args:
                name=name+x+' '
        name=(name.rstrip()).lower()
        found=False
        msg=''
        for x in lores:
            if x[0].lower()==name:
                found=True
                if len(x)==3:
                    msg=x[2]
                else:
                    msg="Map not available yet..."
                break
        if found:
            await ctx.send(msg)
        else:
            await ctx.send("Couldn't find that area...")
#DRINKS
@bot.command(brief='Shows all known drinks.')
async def allDrinks(ctx):
    msg='All Drink entries:\n'
    for x in drinkys:
        if x[1]=='??':
            msg=msg+"**"+x[0]+"**, "
        else:
            msg=msg+x[0]+", "
    await ctx.send(msg)
@bot.command(brief='Shows a specified drink entry, or a random one by default')
async def drinks(ctx,*args):
    item=''
    for x in args:
        item=item+x+' '
    item=(item.rstrip()).lower()
    found=False
    msg=''
    if item=='':
        x=random.randint(0,len(drinkys)-1)
        msg=drinkys[x][0]+": "+drinkys[x][1]
        await ctx.send(msg)
    else:
        for x in drinkys:
            if x[0].lower()==item:
                found=True
                msg=x[0]+": "+x[1] 
                if len(x)==3:
                    msg=msg+"\n"+x[2]
                break
        if found:   
            await ctx.send(msg)
        else:
            await ctx.send("Couldn't find \""+item+"\". Maybe try a different collection?")
#BEASTS
@bot.command(brief='Shows all known beasts.')
async def allBeasts(ctx):
    msg='All Beast entries:\n'
    for x in beastys:
        msg=msg+x[0]+", "
    await ctx.send(msg)
@bot.command(brief='Shows a specified beastiary entry, or a random one by default')
async def beasts(ctx,*args):
    item=''
    for x in args:
        item=item+x+' '
    item=(item.rstrip()).lower()
    found=False
    msg=''
    if item=='':
        x=random.randint(0,len(beastys)-1)
        msg=beastys[x][0]+": "+beastys[x][1]
        if len(beastys[x])==3:
            msg=msg+"\n"+beastys[x][2]
        await ctx.send(msg)
    else:
        for x in beastys:
            if x[0].lower()==item:
                found=True
                msg=x[0]+": "+x[1] 
                if len(x)==3:
                    msg=msg+"\n"+x[2]
                break
        if found:   
            await ctx.send(msg)
        else:
            await ctx.send("Couldn't find \""+item+"\". Maybe try a different collection?")
#ARCHIVES
@bot.command(brief="Lists lore authors.") #all these lore commands work in the same way, its just a more and more complicated way of specifying which to grab
async def authors(ctx):
    await ctx.send("All Authors:\nFerdinand Trenchwerth\nParzival B Jarvin\nAaron Mackenroy\nTerminal AXUM4\nFenwick Carlisle")
@bot.command(brief='Shows all Archive entries.')
async def allArchives(ctx):
    msg='All Archive entries:\n'
    for x in archives:
        msg=msg+x[0]+": "+str(len(x)-1)+" entries. "
    await ctx.send(msg)
@bot.command(brief='To access lore entry collectibles, you can include a specific entry to look at or just a collection in general.')
async def archive(ctx, *args):
    if len(args)<1: #no args
        x=random.randint(0,len(archives)-1)
        y=random.randint(1,len(archives[x])-1)
        msg=archives[x][0]+": "+archives[x][y]
        await ctx.send(msg)   
    else: #args
        name=''
        found=False
        msg=''
        for x in args:
            name=name+x+' '
        name=name.lower().rstrip()
        l=name.split(' ')
        if l[-1].isnumeric(): #specified an entry
            ind=l[-1]
            name=name.replace(l[-1],'')
            name=name.rstrip()   
            for x in archives:
                if x[0].lower()==name and len(x[0])>=int(ind):
                    found=True
                    msg=x[0]+": Entry "+ind+":\n"+x[int(ind)]
                    break
            if found:
                await ctx.send(msg)
            else:
                await ctx.send("Couldn't find that entry, please try again")
        else: #random entry 
            for x in archives:
                if x[0].lower()==name:
                    ind=random.randint(1,len(x)-1)
                    found=True
                    msg=x[0]+": Entry "+str(ind)+":\n"+x[ind]
                    break
            if found:
                await ctx.send(msg)
            else:
                await ctx.send("Couldn't find that entry, please try again")   
#POTIONS
@bot.command(brief='Shows all known Potions.')
async def allPotions(ctx):
    msg='All Potion entries:\n'
    for x in potionys:
        msg=msg+x[0]+", "
    await ctx.send(msg)
@bot.command()
async def potions(ctx,* args):
    item=''
    for x in args:
        item=item+x+' '
    item=(item.rstrip()).lower()
    found=False
    msg=''
    if item=='':
        x=random.randint(0,len(potionys)-1)
        msg=potionys[x][0]+": "+potionys[x][1]
        await ctx.send(msg)
    else:
        for x in potionys:
            if x[0].lower()==item:
                found=True
                msg=x[0]+": "+x[1] 
                if len(x)==3:
                    msg=msg+"\n"+x[2]
                break
        if found:   
            await ctx.send(msg)
        else:
            await ctx.send("Couldn't find \""+item+"\". Maybe try a different collection?")
#Buddies
@bot.command() #a system for npc companions
async def allBuddies(ctx):
    msg='All buddies:\n'
    for x in buddys:
        msg=msg+x.toString()+"\n\n "
    await ctx.send(msg)
@bot.command()
async def killBuddy(ctx,*,name:str):
    for x in buddys:
        if x.name.lower()==name.lower():
            buddys.remove(x)
            writeBuds()
    await ctx.send(name+" died...")
@bot.command()
async def hpBuddy(ctx,hp:int,*,name:str):
    for x in buddys:
        if x.name.lower()==name.lower():
            y=x.hp+hp
            if y>x.max:
                x.hp=x.max
                y=x.hp
            elif y<1:
                y=0
                await killBuddy(ctx,name=name)
            else:
                x.hp=x.hp+hp
                y=x.hp
                writeBuds()
    await ctx.send(name+" HP: "+str(y)) 
@bot.command()
async def buddy(ctx,*,name:str):
    a=True
    for x in buddys:
        if x.name.lower()==name.lower():
            a=False
            await ctx.send(x.toString())
    if a:
        await ctx.send("Couldn't find buddy")
@bot.command()
async def newBuddy(ctx,*,input:str):
    l=input.split(';')
    buddys.append(buddie(l[0],l[1],l[2],l[3],l[4]))
    writeBuds()
    await ctx.send("Added new buddy!")
#gun commands
@bot.command()
async def shoot(ctx,*args):
    msg=''
    ind=findGun(ctx.author.id)
    if ind>-1:
        x=1
        if len(args)>0:
            if args[0].isnumeric():
                x=args[0]
        for a in range(int(x)):
            msg=''
            if guns[ind].loaded<1:
                if (ctx.guild.voice_client!=None):
                    voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
                    if not voice.is_playing():
                        file=fXpath.rstrip()+'gunEmpty.wav'
                        voice.play(discord.FFmpegPCMAudio(file)) 
                msg=msg+"*Click*\n"
                #await ctx.send("*Click*")
            else:
                if (ctx.guild.voice_client!=None): #and ctx.message.author.voice to limit only ppl in vc make the sounds
                    voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
                    if not voice.is_playing():
                        file=fXpath.rstrip()+'gunShoot.wav'
                        voice.play(discord.FFmpegPCMAudio(file)) 
                msg=msg+random.choice(gunshot)
                #await ctx.send(random.choice(gunshot)) 
                guns[ind].loaded=guns[ind].loaded-1 
                writeGuns()
            await ctx.send(msg)
    else:
        await ctx.send("You don't have a gun...")
@bot.command(hidden=True)
async def peekGun(ctx,id:str): #for dm
    ind=findGun(id) 
    if ind>-1:
        await ctx.send("You look at your gun...\n"+guns[ind].ammo+", nice.\n*Opens chamber* Hmm, "+str(guns[ind].loaded)+" shots left.")
    else:
        await ctx.send("You don't have a gun to inspect...")
@bot.command()
async def inspectGun(ctx): #for player
    ind=findGun(ctx.author.id)
    if ind>-1:
        await ctx.send("You look at your gun...\n"+guns[ind].ammo+", nice.\n*Opens chamber* Hmm, "+str(guns[ind].loaded)+" shots left.")
    else:
        await ctx.send("You don't have a gun to inspect...")
@bot.command()
async def reload(ctx):
    ind=findGun(ctx.author.id)
    if ind>-1:
        need=guns[ind].max-guns[ind].loaded
        if need<1:
            await ctx.send("Chamber full.")
        else:
            if guns[ind].total<1:
                await ctx.send("You have no bullets.")
            else:
                if (ctx.guild.voice_client!=None and ctx.message.author.voice):
                    voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
                    if not voice.is_playing():
                        file=fXpath.rstrip()+'gunReload.wav'
                        voice.play(discord.FFmpegPCMAudio(file)) 
                if guns[ind].total<need: #not enough bullets to reload w
                    guns[ind].loaded=guns[ind].loaded+guns[ind].total
                    await ctx.send("Could only reload "+str(guns[ind].total)+" bullets.")
                    guns[ind].total=0
                    writeGuns()
                else:
                    guns[ind].total=guns[ind].total-need
                    guns[ind].loaded=guns[ind].max
                    writeGuns()
                    await ctx.send("Reloaded.")
@bot.command(hidden=True)
async def peekBullets(ctx,id:str):
    ind=findGun(id)
    if ind>-1:
        await ctx.send("Hmm, "+str(guns[ind].total)+" bullets left.")
    else:
        await ctx.send("You don't have a gun to inspect...")
@bot.command()
async def inspectBullets(ctx):
    ind=findGun(ctx.author.id)
    if ind>-1:
        await ctx.send("Hmm, "+str(guns[ind].total)+" bullets left.")
    else:
        await ctx.send("You don't have a gun to inspect...")
@bot.command()
async def addBullets(ctx,num:int):
    ind=findGun(ctx.author.id)
    if ind>-1:
        guns[ind].total=guns[ind].total+num
        writeGuns()
        await ctx.send("Added "+str(num)+ " bullets.")
    else:
        await ctx.send("You don't have a gun just add these to inventory...")
@bot.command()
async def changeAmmo(ctx,*,tpye:str):
    ind=findGun(ctx.author.id)
    msg=guns[ind].ammo+" "+str(guns[ind].total)
    if ind>-1:
        guns[ind].ammo=tpye
        guns[ind].total=0
        guns[ind].loaded=0
        writeGuns()
        await add(ctx,string=msg)
        writeChars()
        await ctx.send("Switched ammo to "+tpye+ ".")
    else:
        await ctx.send("You don't have a gun...")
@bot.command()
async def dropClip(ctx):
    ind=findGun(ctx.author.id)
    if ind>-1:
        guns[ind].total=guns[ind].total+guns[ind].loaded
        guns[ind].loaded=0
        writeGuns()
        await ctx.send("Clip emptied...")
    else:
        await ctx.send("You don't have a gun...")
#vc commands
@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
    else:
            channel = ctx.message.author.voice.channel
    await channel.connect()
@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
@bot.command(brief='Plays SnS 2: Main Theme.')
async def play(ctx,*,song:str):
    x=1
    song=song.lower()
    l=song.split(' ')
    if l[-1].isnumeric(): #included a loop amount
        song=song.replace(l[-1],'')
        song=song.rstrip()
        x=int(l[-1])

    if (ctx.guild.voice_client==None): 
        await ctx.send("Not in a VC")
    else:
        if (ctx.author.voice.channel!=ctx.guild.voice_client.channel):
                await ctx.send("Not in your VC")
        else:
            file=mpath.rstrip()+song+'.wav'
            await ctx.send("Playing "+song+"...")
            voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
            if not voice.is_playing():
                voice.play(discord.FFmpegPCMAudio(file),after=lambda e: loop(ctx,x))

    def loop(ctx,x):
        if x>0:
            voice.play(discord.FFmpegPCMAudio(file),after=lambda e: loop(ctx,x))              
            x=x-1
@bot.command()
async def pause(ctx):
    voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused.")
@bot.command()
async def resume(ctx):
  voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
    await ctx.send("Resuming.")
@bot.command()
async def stop(ctx):
  voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)
  voice.stop()
# custom help commands
@bot.command()
async def gunTips(ctx):
    await ctx.send("Gun Help:\n~shoot -Will shoot a single bullet.\n~reload -Will reload your current gun.\n~inspectGun -Will show you what kind of, and how many, bullets that are currently loaded.\n~inspectBullets -Shows how many of the current ammo type you have.\n~addBullets x -Will add x amount of bullets.\n~changeAmmo x -Will change current ammo type to x bullets. Meanwhile adding leftover bullets to your inventory.\n~dropClip -Will unload the current chamber, this is helpful for switching between special ammo types on the go.")
@bot.command(hidden=True)
async def tips(ctx):
    await ctx.send("~roll -Rolls a d20.\n~newChar *name* -Makes a new character linked to just you with a name.\n~allChars -Lists all characters currently in game.\n~inspect -Shows a quick snapshot of your stats and inventory.\n~inspectFull -Shows your entire character sheet.\n~add *item* -Adds an item to your inventory.\n~levelUp -Auto levels up your character.\n~take *damage* -Take character damage.")
bot.run(token)
