import time
import configparser
import os.path
import configparser
import datetime
import random
from mudserver import MudServer
#Server Settings
universew = 80
universeh = 80
autosaveinterval = 5
resourcebroadcastinterval = 5
#Init color escape codes
blue = '\033[94m'
green = '\033[92m'
yellow = '\033[93m'
red = '\033[91m'
cyan = '\033[96m'
magenta= '\033[95m'
Reset = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
blinkeffect = '\033[5m'
marker = '\033[45m'
print("Dark-Nebula Server Starting...")
#Initialize functions
def sendmappoint(x, y, id):
    x = str(x)
    y = str(y)
    if not x.isdigit():
        x = 0
    if not y.isdigit():
        y = 0
    umx = int(x)
    umy = int(y)
    ox = int(x) - 39
    oy = int(y) - 10
    if ox < 0:
        ox = 0
    if oy < 0:
        oy = 0
    x = int(ox) 
    y = int(oy)
    width = x + 77
    height = y + 20
    if width > universew:
        width = universew
    if height > universeh:
        height = universeh
    mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
    while y < height:
        outputstr = ""
        while x < width:
            if x == umx and y == umy:
                outputstr = outputstr+magenta+"X"
            elif universe[str(x)+"-"+str(y)]["type"] == "planet":
                if universe[str(x)+"-"+str(y)]["owner"] == "none":
                    outputstr = outputstr+cyan+"O"
                else:
                    outputstr = outputstr+green+"O"
            elif universe[str(x)+"-"+str(y)]["type"] == "star":
                if universe[str(x)+"-"+str(y)]["owner"] == "none":
                    outputstr = outputstr+yellow+"*"
                else:
                    outputstr = outputstr+green+"*"
            elif universe[str(x)+"-"+str(y)]["type"] == "blackhole":
                outputstr = outputstr+blue+"-"
            elif universe[str(x)+"-"+str(y)]["type"] == "space":
                outputstr = outputstr+" "
            x += 1
        x = ox
        mud.send_message(id,BOLD+"#"+outputstr+Reset+BOLD+"#"+Reset)
        outputstr = ""
        y += 1
    mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
def get_unowned_planets():
    usedplanets = []
    unusedplanets = []
    x = 0
    y = 0
    while x < universew + 1:
        while y < universeh + 1:
            if universe[str(x)+"-"+str(y)]["type"] == "planet":
                if universe[str(x)+"-"+str(y)]["owner"] == "none":
                    unusedplanets.append(str(x)+"-"+str(y)) 
                else:
                    usedplanets.append(str(x)+"-"+str(y)) 
            y += 1
        y = 0
        x += 1
    return unusedplanets
def get_fleet_ships(id, fleet):
    loadedships = configparser.ConfigParser()
    loadedships.read("Database/Player_Data/"+players[id]["name"]+"/ships.ini")
    fleetships = []
    for ship,vals in loadedships.items():
        if not ship == "DEFAULT":
            if vals["fleet"] == fleet:
                fleetships.append(ship)
    return fleetships
def set_fleet_pos(id, fleet, x, y):
    loadedships = configparser.ConfigParser()
    loadedships.read("Database/Player_Data/"+players[id]["name"]+"/ships.ini")
    loadedfleet = configparser.ConfigParser()
    loadedfleet.read("Database/Player_Data/"+players[id]["name"]+"/fleets.ini")
    for ship,vals in loadedships.items():
        if not ship == "DEFAULT":
            if vals["fleet"] == fleet:
                loadedships[ship]["location"] = str(x)+"-"+str(y)
    loadedfleet[fleet]["location"] = str(x)+"-"+str(y)
    with open("Database/Player_Data/"+players[id]["name"]+"/fleets.ini", 'w') as configfile:
        loadedfleet.write(configfile)
    with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
        loadedships.write(configfile)
def set_ship_pos(id, ship, x, y):
    loadedships = configparser.ConfigParser()
    loadedships.read("Database/Player_Data/"+players[id]["name"]+"/ships.ini")
    loadedships[ship]["location"] = str(x)+"-"+str(y)
    with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
        loadedships.write(configfile)
def fleet_movetotarget(id, fleet, targetx, targety,):
    loadedfleet = configparser.ConfigParser()
    loadedfleet.read("Database/Player_Data/"+players[id]["name"]+"/fleets.ini")
    splitvals = loadedfleet[fleet]["location"].split('-', 1)
    x = int(splitvals[0])
    y = int(splitvals[1])
    newx = x
    newy = y
    if x > targetx:
        newx = x - 1
    elif x < targetx:
        newx = x + 1
    if y > targety:
        newy = y - 1
    elif y < targety:
        newy = y + 1
    if newx == targetx and newy == targety:
        loadedfleet[fleet]["status"] = "stopped"
        targetname = "none"
        if universe.has_option(str(newx)+"-"+str(newy), "name"):
            targetname = universe[str(newx)+"-"+str(newy)]["name"]
        if targetname == "none":
            targetname = str(newx)+"-"+str(newy)
            mud.send_message(pid,green+BOLD+"Fleet "+fleet+" has arrived at "+targetname+Reset)
        else:
            mud.send_message(pid,green+BOLD+"Fleet "+fleet+" has arrived at "+targetname+Reset)
        with open("Database/Player_Data/"+players[id]["name"]+"/fleets.ini", 'w') as configfile:
            loadedfleet.write(configfile)
    set_fleet_pos(id, fleet, newx, newy)
def ship_movetotarget(id, ship, targetx, targety,):
    loadedships = configparser.ConfigParser()
    loadedships.read("Database/Player_Data/"+players[id]["name"]+"/ships.ini")
    splitvals = loadedships[ship]["location"].split('-', 1)
    x = int(splitvals[0])
    y = int(splitvals[1])
    newx = x
    newy = y
    if x > targetx:
        newx = x - 1
    elif x < targetx:
        newx = x + 1
    if y > targety:
        newy = y - 1
    elif y < targety:
        newy = y + 1
    if newx == targetx and newy == targety:
        loadedships[ship]["status"] = "stopped"
        targetname = "none"
        if universe.has_option(str(newx)+"-"+str(newy), "name"):
            targetname = universe[str(newx)+"-"+str(newy)]["name"]
        if targetname == "none":
            targetname = str(newx)+"-"+str(newy)
            mud.send_message(pid,green+BOLD+"Ship "+ship+" has arrived at "+targetname+Reset)
        else:
            mud.send_message(pid,green+BOLD+"Ship "+ship+" has arrived at "+targetname+Reset)
        with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
            loadedships.write(configfile)
    set_ship_pos(id, ship, newx, newy)
#Generate missing directories
if not os.path.exists("Database"):
    os.makedirs("Database")
if not os.path.exists("Database/Player_Data"):
    os.makedirs("Database/Player_Data")

#Find universe file or generate one if not found

if os.path.isfile("Database/universe.ini") == True:
    print(green+"Universe data found and loaded!"+Reset)
    universe = configparser.ConfigParser()
    universe.read("Database/universe.ini")
else:
    print(red+"Universe missing!, Generating universe..."+Reset)
    x = 0
    y = 0
    universe = configparser.ConfigParser()
    universe["data"] = {}
    universe["data"]["spaces"] = "0"
    universe["data"]["planets"] = "0"
    universe["data"]["stars"] = "0"
    universe["data"]["blackholes"] = "0"
    while x < universew + 1:
        print("[ "+str(datetime.datetime.now())+" ] Generating Environment, Sector("+str(x)+")")
        while y < universeh + 1:
            universe[str(x)+"-"+str(y)] = {}
            chance = (random.randint(1,350))
            if chance == 1:
                universe["data"]["blackholes"] = str(int(universe["data"]["blackholes"]) + 1)
                universe[str(x)+"-"+str(y)]["type"] = "blackhole"
                universe[str(x)+"-"+str(y)]["owner"] = "none"
            elif chance <= 5:
                universe["data"]["stars"] = str(int(universe["data"]["stars"]) + 1)
                universe[str(x)+"-"+str(y)]["type"] = "star"
                universe[str(x)+"-"+str(y)]["owner"] = "none"
                universe[str(x)+"-"+str(y)]["name"] = "none"
            elif chance <= 10:
                universe["data"]["planets"] = str(int(universe["data"]["planets"]) + 1)
                universe[str(x)+"-"+str(y)]["type"] = "planet"
                universe[str(x)+"-"+str(y)]["owner"] = "none"
                universe[str(x)+"-"+str(y)]["name"] = "none"
                chance = (random.randint(1,10))
                universe[str(x)+"-"+str(y)]["maxminingdrills"] = str(chance)
                chance = (random.randint(1,10))
                universe[str(x)+"-"+str(y)]["maxfueldrills"] = str(chance)
                universe[str(x)+"-"+str(y)]["miningdrills"] = "0"
                universe[str(x)+"-"+str(y)]["fuelgdrills"] = "0"
            else:
                universe["data"]["spaces"] = str(int(universe["data"]["spaces"]) + 1)
                universe[str(x)+"-"+str(y)]["type"] = "space"
            y += 1
        y = 0
        x += 1
    with open("Database/universe.ini", 'w') as configfile:
        universe.write(configfile)
    print(BOLD+green+"Universe generated!"+Reset)
#Parse player data
if os.path.isfile("Database/Player_Data/PlayerData.ini") == True:
    print("Parsing player data...")
    PlayerData = configparser.ConfigParser()
    PlayerData.read('Database/Player_Data/PlayerData.ini')
else:
    print(red+"No player data found! Generating DB..."+Reset)
    PlayerData = configparser.ConfigParser()
    with open("Database/Player_Data/PlayerData.ini", 'w') as configfile:
        PlayerData.write(configfile)
#Load ships for shop
shopships = configparser.ConfigParser()
shopships.read("ships.ini")
#Inialize main loop vars
players = {}
mud = MudServer()
onlineplayers = 0

now = datetime.datetime.now()
savetime = now + datetime.timedelta(minutes = autosaveinterval)
broadcastresources = now
print("[ "+str(now)+" ]"+green+BOLD+" Server started succesfully on port: 9872!"+Reset)
# main game loop
while True:
    time.sleep(0.2)
    now = datetime.datetime.now()
    if now > savetime:
        print("[ "+str(now)+" ]"+" Autosaving...")
        with open("Database/Player_Data/PlayerData.ini", 'w') as configfile:
            PlayerData.write(configfile)
        with open("Database/universe.ini", 'w') as configfile:
            universe.write(configfile)
        savetime = now + datetime.timedelta(minutes = autosaveinterval)
        print("[ "+str(now)+" ]"+green+" Autosave Complete!"+Reset)
    mud.update()
    # go through any newly connected players
    for id in mud.get_new_players():
        players[id] = { 
            "name": None,
            "authenticated": False,
        }
        mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
        mud.send_message(id,BOLD+"#"+blue+"                  *                         *            .                   "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"   *    /$$    .                /$$               .                          "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"       | $$                    | $$                         *          *     "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"   /$$$$$$$  /$$$$$$   /$$$$$$ | $$   /$$     *    .            .            "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"  /$$__  $$ |____  $$ /$$__  $$| $$  /$$/                                    "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+" | $$  | $$  /$$$$$$$| $$  \__/| $$$$$$/            *                 *      "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+" | $$  | $$ /$$__  $$| $$      | $$_  $$                                     "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+" |  $$$$$$$|  $$$$$$$| $$      | $$ \  $$          .         *               "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"  \_______/ \_______/|__/      |__/  \__/                                *   "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"           *                 *             /$$          *      /$$           "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"                      .                   | $$                | $$           "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+" *    *           *    /$$$$$$$   /$$$$$$ | $$$$$$$  /$$   /$$| $$  /$$$$$$  "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"             .        | $$__  $$ /$$__  $$| $$__  $$| $$  | $$| $$ |____  $$ "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"      *               | $$  \ $$| $$$$$$$$| $$  \ $$| $$  | $$| $$  /$$$$$$$ "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"           *          | $$  | $$| $$_____/| $$  | $$| $$  | $$| $$ /$$__  $$ "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+" *     .          *   | $$  | $$|  $$$$$$$| $$$$$$$/|  $$$$$$/| $$|  $$$$$$$ "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"                      |__/  |__/ \_______/|_______/  \______/ |__/ \_______/ "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#"+blue+"             *            .                            *                .    "+Reset+BOLD+"#"+Reset)
        mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
        mud.send_message(id,"Username:")
        print("[ "+str(datetime.datetime.now().time())+" ]"+cyan+BOLD+" New client connected. ID:"+str(id)+Reset)
    # go through any recently disconnected players    
    for id in mud.get_disconnected_players():
        if id not in players: continue
        # remove the player's entry in the player dictionary
        onlineplayers -= 1
        if players[pid]["name"] is not None and players[pid]["authenticated"]:
            print("[ "+str(datetime.datetime.now().time())+" ] "+red+BOLD+players[id]["name"]+" Disconnected"+Reset)
        for pid,pl in players.items():
            # send each player a message to tell them about the diconnected player
            if players[pid]["name"] is not None and players[pid]["authenticated"]:
                mud.send_message(pid,"%s quit the game" % players[id]["name"])
        del players[pid]
    #resources code
    for pid,pvalue in players.items():
        if players[pid]["name"] is not None and players[pid]["authenticated"]:
            #tick event for fulemines
            if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["fueldrillticktime"], "%Y-%m-%d %H:%M:%S.%f"):
                delay = 15 - int(PlayerData[players[pid]["name"]]["fueldrilllvl"])
                PlayerData[players[pid]["name"]]["fueldrillticktime"] = str(datetime.datetime.strptime(PlayerData[players[pid]["name"]]["fueldrillticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(seconds = delay))
                if not PlayerData[players[pid]["name"]]["fuel"] == PlayerData[players[pid]["name"]]["maxfuel"]:
                    gain = 25 + int(PlayerData[players[pid]["name"]]["fueldrilllvl"])
                    gain = gain * int(PlayerData[players[pid]["name"]]["fueldrillcount"])
                    energycost = int(gain / 2)
                    if energycost < int(PlayerData[players[pid]["name"]]["energy"]):
                        PlayerData[players[pid]["name"]]["fuel"] = str(int(PlayerData[players[pid]["name"]]["fuel"]) + gain)
                        PlayerData[players[pid]["name"]]["energy"] = str(int(PlayerData[players[pid]["name"]]["energy"]) - energycost)
                        if int(PlayerData[players[pid]["name"]]["fuel"]) > int(PlayerData[players[pid]["name"]]["maxfuel"]):
                            PlayerData[players[pid]["name"]]["fuel"] = PlayerData[players[pid]["name"]]["maxfuel"]
                            if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["fueldrillticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours = 1):
                                PlayerData[players[pid]["name"]]["fueldrillticktime"] = str(now)
                    else:
                        mud.send_message(pid,BOLD+red+"Insufficient power for fuel drills."+Reset)
                else:
                    if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["fueldrillticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours = 1):
                        PlayerData[players[pid]["name"]]["fueldrillticktime"] = str(now)

            #tick event for resource mines
            if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["miningdrillticktime"], "%Y-%m-%d %H:%M:%S.%f"):
                delay = 100 / int(PlayerData[players[pid]["name"]]["miningdrilllvl"])
                PlayerData[players[pid]["name"]]["miningdrillticktime"] = str(datetime.datetime.strptime(PlayerData[players[pid]["name"]]["miningdrillticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(seconds = delay))
                if not PlayerData[players[pid]["name"]]["metal"] == PlayerData[players[pid]["name"]]["maxmetal"]:
                    gain = 20 + int(PlayerData[players[pid]["name"]]["miningdrilllvl"])
                    gain = gain * int(PlayerData[players[pid]["name"]]["miningdrillcount"])
                    energycost = int(gain / 2)
                    if energycost < int(PlayerData[players[pid]["name"]]["energy"]):
                        PlayerData[players[pid]["name"]]["metal"] = str(int(PlayerData[players[pid]["name"]]["metal"]) + gain)
                        PlayerData[players[pid]["name"]]["energy"] = str(int(PlayerData[players[pid]["name"]]["energy"]) - energycost)
                        if int(PlayerData[players[pid]["name"]]["metal"]) > int(PlayerData[players[pid]["name"]]["maxmetal"]):
                            PlayerData[players[pid]["name"]]["metal"] = PlayerData[players[pid]["name"]]["maxmetal"]
                            if PlayerData[players[pid]["name"]]["heavymetal"] == PlayerData[players[pid]["name"]]["maxheavymetal"]:
                                if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["miningdrillticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours = 1):
                                    PlayerData[players[pid]["name"]]["miningdrillticktime"] = str(now)
                    else:
                        mud.send_message(pid,BOLD+red+"Insufficient power for mining drills."+Reset)
                if not PlayerData[players[pid]["name"]]["heavymetal"] == PlayerData[players[pid]["name"]]["maxheavymetal"]:
                    gain = 10 + int(PlayerData[players[pid]["name"]]["miningdrilllvl"])
                    gain = gain * int(PlayerData[players[pid]["name"]]["miningdrillcount"])
                    energycost = int(gain / 2)
                    if energycost < int(PlayerData[players[pid]["name"]]["energy"]):
                        PlayerData[players[pid]["name"]]["heavymetal"] = str(int(PlayerData[players[pid]["name"]]["heavymetal"]) + gain)
                        PlayerData[players[pid]["name"]]["energy"] = str(int(PlayerData[players[pid]["name"]]["energy"]) - energycost)
                        if int(PlayerData[players[pid]["name"]]["heavymetal"]) > int(PlayerData[players[pid]["name"]]["maxheavymetal"]):
                            PlayerData[players[pid]["name"]]["heavymetal"] = PlayerData[players[pid]["name"]]["maxheavymetal"]
                            if PlayerData[players[pid]["name"]]["metal"] == PlayerData[players[pid]["name"]]["maxmetal"]:
                                if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["miningdrillticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours = 1):
                                    PlayerData[players[pid]["name"]]["miningdrillticktime"] = str(now)
                    else:
                        mud.send_message(pid,BOLD+red+"Insufficient power for mining drills."+Reset)
                if PlayerData[players[pid]["name"]]["heavymetal"] == PlayerData[players[pid]["name"]]["maxheavymetal"] and PlayerData[players[pid]["name"]]["metal"] == PlayerData[players[pid]["name"]]["maxmetal"]:
                    if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["miningdrillticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours = 1):
                        PlayerData[players[pid]["name"]]["miningdrillticktime"] = str(now)
                   # tick event for reactors
            if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["reactorticktime"], "%Y-%m-%d %H:%M:%S.%f"):
                delay = 10 - int(PlayerData[players[pid]["name"]]["reactorlvl"])
                PlayerData[players[pid]["name"]]["reactorticktime"] = str(datetime.datetime.strptime(PlayerData[players[pid]["name"]]["reactorticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(seconds = delay))
                if not PlayerData[players[pid]["name"]]["energy"] == PlayerData[players[pid]["name"]]["maxenergy"]:
                    gain = 20 + int(PlayerData[players[pid]["name"]]["reactorlvl"])
                    gain = gain * int(PlayerData[players[pid]["name"]]["reactorcount"])
                    fuelcost = int(gain / 2)
                    if fuelcost < int(PlayerData[players[pid]["name"]]["fuel"]):
                        PlayerData[players[pid]["name"]]["energy"] = str(int(PlayerData[players[pid]["name"]]["energy"]) + gain)
                        PlayerData[players[pid]["name"]]["fuel"] = str(int(PlayerData[players[pid]["name"]]["fuel"]) - fuelcost)
                        if int(PlayerData[players[pid]["name"]]["energy"]) > int(PlayerData[players[pid]["name"]]["maxenergy"]):
                            PlayerData[players[pid]["name"]]["energy"] = PlayerData[players[pid]["name"]]["maxenergy"]
                            if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["reactorticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours = 1):
                                PlayerData[players[pid]["name"]]["reactorticktime"] = str(now)
                    else:
                        mud.send_message(pid,BOLD+red+"Insufficient fuel for reactors."+Reset)
                else:
                    if now > datetime.datetime.strptime(PlayerData[players[pid]["name"]]["reactorticktime"], "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(hours = 1):
                        PlayerData[players[pid]["name"]]["reactorticktime"] = str(now)
    if now > broadcastresources:
        for pid,pl in players.items():
            if players[pid]["name"] is not None and players[pid]["authenticated"]:
                broadcastresources = now + datetime.timedelta(seconds = resourcebroadcastinterval)
                energycolor = red
                fuelcolor = red
                metalcolor = red
                hmetalcolor = red
                if int(PlayerData[players[pid]["name"]]["energy"]) > int(PlayerData[players[pid]["name"]]["maxenergy"]) / 1.5:
                    energycolor = green
                elif int(PlayerData[players[pid]["name"]]["energy"]) > int(PlayerData[players[pid]["name"]]["maxenergy"]) / 3:
                    energycolor = yellow
                if int(PlayerData[players[pid]["name"]]["fuel"]) > int(PlayerData[players[pid]["name"]]["maxfuel"]) / 1.5:
                    fuelcolor = green
                elif int(PlayerData[players[pid]["name"]]["fuel"]) > int(PlayerData[players[pid]["name"]]["maxfuel"]) / 3:
                    fuelcolor = yellow
                if int(PlayerData[players[pid]["name"]]["metal"]) > int(PlayerData[players[pid]["name"]]["maxmetal"]) / 1.5:
                    metalcolor = green
                elif int(PlayerData[players[pid]["name"]]["metal"]) > int(PlayerData[players[pid]["name"]]["maxmetal"]) / 3:
                    metalcolor = yellow
                if int(PlayerData[players[pid]["name"]]["heavymetal"]) > int(PlayerData[players[pid]["name"]]["maxheavymetal"]) / 1.5:
                    hmetalcolor = green
                elif int(PlayerData[players[pid]["name"]]["heavymetal"]) > int(PlayerData[players[pid]["name"]]["maxheavymetal"]) / 3:
                    hmetalcolor = yellow
                if energycolor == red or fuelcolor == red or metalcolor == red or hmetalcolor == red:
                    mud.send_message(pid,energycolor+"[ENERGY]:"+PlayerData[players[pid]["name"]]["energy"]+"/"+PlayerData[players[pid]["name"]]["maxenergy"]+fuelcolor+" [FUEL]:"+PlayerData[players[pid]["name"]]["fuel"]+"/"+PlayerData[players[pid]["name"]]["maxfuel"]+metalcolor+" [METAL]:"+PlayerData[players[pid]["name"]]["metal"]+"/"+PlayerData[players[pid]["name"]]["maxmetal"]+hmetalcolor+" [HEAVY-METAL]:"+PlayerData[players[pid]["name"]]["heavymetal"]+"/"+PlayerData[players[pid]["name"]]["maxheavymetal"]+Reset)
                    # go through any new commands sent from players
        for pid,pl in players.items():   
            if players[pid]["name"] is not None and players[pid]["authenticated"]:
                loadedships = configparser.ConfigParser()
                loadedships.read("Database/Player_Data/"+players[pid]["name"]+"/ships.ini")
                loadedfleet = configparser.ConfigParser()
                loadedfleet.read("Database/Player_Data/"+players[pid]["name"]+"/fleets.ini")
                
                for key,vals in loadedfleet.items():
                    if not key == "DEFAULT":
                        movetime = datetime.datetime.strptime(vals["nextmove"], "%Y-%m-%d %H:%M:%S.%f")
                        if now >= movetime:
                            if loadedfleet[key]["status"] == "moving":
                                fleetships = get_fleet_ships(pid, key)
                                if not len(fleetships) < 1:
                                    index = 0
                                    speed = 999999999999999
                                    while index <= len(fleetships) - 1:
                                        if speed > int(loadedships[fleetships[index]]["speed"]):
                                            speed = int(loadedships[fleetships[index]]["speed"])
                                        index += 1
                                    if int(PlayerData[players[pid]["name"]]["fuel"]) >= (int(speed)*(len(fleetships) - 1)) * 2:
                                        PlayerData[players[pid]["name"]]["fuel"] = str(int(PlayerData[players[pid]["name"]]["fuel"]) - int(speed) * 2)
                                        loadedfleet[key]["nextmove"] = str(movetime + datetime.timedelta(seconds = 160 - int(speed)))
                                        with open("Database/Player_Data/"+players[pid]["name"]+"/fleets.ini", 'w') as configfile:
                                            loadedfleet.write(configfile)
                                        fleet_movetotarget(pid, key, int(loadedfleet[key]["targetx"]), int(loadedfleet[key]["targety"])) 
                                    else:
                                        mud.send_message(pid,red+BOLD+"Fleet "+key+" is out of fuel."+Reset)
                                else:
                                    mud.send_message(pid,red+BOLD+"Fleet "+key+" has no ships assigned. Travel canceled."+Reset)
                                    loadedfleet[key]["status"] == "stopped"
                            else:
                                loadedfleet[key]["nextmove"] = str(movetime + datetime.timedelta(hours = 999))
                                with open("Database/Player_Data/"+players[pid]["name"]+"/fleets.ini", 'w') as configfile:
                                    loadedfleet.write(configfile)
                loadedships = configparser.ConfigParser()
                loadedships.read("Database/Player_Data/"+players[pid]["name"]+"/ships.ini")
                for key,vals in loadedships.items():
                    if not key == "DEFAULT":
                        
                        movetime = datetime.datetime.strptime(vals["nextmove"], "%Y-%m-%d %H:%M:%S.%f")
                        if now >= movetime:
                            if loadedships[key]["status"] == "moving":
                                speed = vals["speed"]
                                if int(PlayerData[players[pid]["name"]]["fuel"]) >= int(speed) * 2:
                                    PlayerData[players[pid]["name"]]["fuel"] = str(int(PlayerData[players[pid]["name"]]["fuel"]) - int(speed) * 2)
                                    loadedships[key]["nextmove"] = str(now + datetime.timedelta(seconds = 160 - int(speed)))
                                    with open("Database/Player_Data/"+players[pid]["name"]+"/ships.ini", 'w') as configfile:
                                        loadedships.write(configfile)
                                    ship_movetotarget(pid, key, int(loadedships[key]["targetx"]), int(loadedships[key]["targety"])) 
                                else:
                                    mud.send_message(pid,red+BOLD+"Ship "+key+" is out of fuel."+Reset)
                            else:
                                loadedships[key]["nextmove"] = str(now + datetime.timedelta(hours = 999))
                                with open("Database/Player_Data/"+players[pid]["name"]+"/ships.ini", 'w') as configfile:
                                    loadedships.write(configfile)

    for id,command,params in mud.get_commands():
        if id not in players: continue
        # if the player hasn't given their name yet, use this first command as their name
        if players[id]["name"] is None:
                alreadyloggedin = False
                for pid,pl in players.items():
                    if players[pid]["name"] == command:
                        alreadyloggedin = True
                if not alreadyloggedin:
                    players[id]["name"] = command
                    if not PlayerData.has_section(players[id]["name"]):
                        mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
                        mud.send_message(id,"#      This is your first time logging in! Please type a password to use!     #")
                        mud.send_message(id,"#               You can change this later with setpass <newpass>              #")
                        mud.send_message(id,"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                    mud.send_message(id,"Password:")
                else:
                    mud.send_message(id,red+BOLD+"User already logged in."+Reset)
                    del(players[id])
        elif players[id]["authenticated"] is False:
            #Authenitcate player if not authenticated
            password = command
            if not PlayerData.has_section(players[id]["name"]):
                if not os.path.exists("Database/Player_Data/"+players[id]["name"]):
                    os.makedirs("Database/Player_Data/"+players[id]["name"])
                PlayerData[players[id]["name"]] = {}
                PlayerData[players[id]["name"]]['pass'] = command
                PlayerData[players[id]["name"]]["level"] = "1"
                planetcount = len(get_unowned_planets())
                chance = (random.randint(1,planetcount))
                unusedplanets = get_unowned_planets()
                PlayerData[players[id]["name"]]["homeworld"] = unusedplanets[chance]
                universe[unusedplanets[chance]]["owner"] = players[id]["name"]
                universe[unusedplanets[chance]]["name"] = players[id]["name"]+"'s Homeworld"
                universe[unusedplanets[chance]]["maxminingdrills"] = "3"
                universe[unusedplanets[chance]]["maxfueldrills"] = "3"
                universe[unusedplanets[chance]]["miningdrills"] = "1"
                universe[unusedplanets[chance]]["fuelgdrills"] = "1"
                PlayerData[players[id]["name"]]["currency"] = "200"
                PlayerData[players[id]["name"]]["reactorlvl"] = "1"
                PlayerData[players[id]["name"]]["reactorcount"] = "1"
                PlayerData[players[id]["name"]]["reactorticktime"] = str(now)
                PlayerData[players[id]["name"]]["energylvl"] = "1"
                PlayerData[players[id]["name"]]["energy"] = "200"
                PlayerData[players[id]["name"]]["maxenergy"] = "500"
                PlayerData[players[id]["name"]]["fueldrilllvl"] = "1"
                PlayerData[players[id]["name"]]["fueldrillcount"] = "1"
                PlayerData[players[id]["name"]]["fueldrillticktime"] = str(now)
                PlayerData[players[id]["name"]]["fuellvl"] = "1"
                PlayerData[players[id]["name"]]["fuel"] = "200"
                PlayerData[players[id]["name"]]["maxfuel"] = "500"
                PlayerData[players[id]["name"]]["miningdrilllvl"] = "1"
                PlayerData[players[id]["name"]]["miningdrillcount"] = "1"
                PlayerData[players[id]["name"]]["miningdrillticktime"] = str(now)
                PlayerData[players[id]["name"]]["metallvl"] = "1"
                PlayerData[players[id]["name"]]["metal"] = "50"
                PlayerData[players[id]["name"]]["maxmetal"] = "300"
                PlayerData[players[id]["name"]]["heavymetallvl"] = "1"
                PlayerData[players[id]["name"]]["heavymetal"] = "10"
                PlayerData[players[id]["name"]]["maxheavymetal"] = "150"
                PlayerData[players[id]["name"]]["lastresourcebroadcast"] = "none"
                friends = configparser.ConfigParser()
                with open("Database/Player_Data/"+players[id]["name"]+"/friends.ini", 'w') as configfile:
                    friends.write(configfile)
                loadedships = configparser.ConfigParser()
                with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
                    loadedships.write(configfile)
                loadedfleet = configparser.ConfigParser()
                with open("Database/Player_Data/"+players[id]["name"]+"/fleets.ini", 'w') as configfile:
                    loadedfleet.write(configfile)
                with open('Database/Player_Data/PlayerData.ini', 'w') as configfile:
                    PlayerData.write(configfile)
                with open("Database/universe.ini", 'w') as configfile:
                    universe.write(configfile)
            correctPW = PlayerData[players[id]["name"]]['pass']
            if password == correctPW:
                print("[ "+str(datetime.datetime.now().time())+" ]\033[96m "+players[id]["name"]+" logged in.\033[0m")
                players[id]["authenticated"] = True
                onlineplayers += 1
			    # go through all the players in the game
                for pid,pl in players.items():
                    # send each player a message to tell them about the new player
                    if players[pid]["name"] is not None and players[pid]["authenticated"]:
                        mud.send_message(pid,"%s has logged in." % players[id]["name"])
			    # send the new player a welcome message
                mud.send_message(id,"\u001B[2J")
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
                mud.send_message(id,BOLD+"#"+magenta+"     Welcome to DarkNebula. Type 'help' for a list of commands. Have fun!    "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
                mud.send_message(id,BOLD+"#"+magenta+"                           Current online players:                           "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#"+cyan+"                    To add a friend, type add <username>.                    "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#"+cyan+"                     To view friends, just type friends.                     "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                for sid,vals in players.items():
                    if not  players[sid]["name"] is None and players[sid]["authenticated"]: 
                        name = cyan+players[sid]["name"]+Reset
                        mud.send_message(id, name+" Homeworld name:"+universe[PlayerData[players[sid]["name"]]["homeworld"]]["name"]+" Homeworld coordinates:"+PlayerData[players[sid]["name"]]["homeworld"])
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
            else:
                print("[ "+str(datetime.datetime.now().time())+" ]"+BOLD+red+" Incorrect password entered for "+players[id]["name"]+Reset)
                mud.send_message(id,red+BOLD+"Invalid Password..."+Reset)
                mud.send_message(id,"Password:")
        elif command == "help":
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
            mud.send_message(id,BOLD+"#"+magenta+"   Below is all the commands available to you with your current permisions.  "+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
            mud.send_message(id,BOLD+"#"+cyan+"pm <username> - Send private message.  shout <message> - Global chat command."+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#"+cyan+"changepass <newpass> - Change Password.        players - Show online players."+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#"+cyan+"resources - Shows resources menu.                 clear - Clears the console."+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#"+cyan+"map <x> <y> - Shows map at coords.      ships <args...> - Work in ships menu."+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#"+cyan+"fleets <args...> - Work in fleets menu.  (type just ship/fleets to see more.)"+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
        elif command == "changepass":
            PlayerData[players[id]["name"]]['pass'] = params
            with open('Database/Player_Data/PlayerData.ini', 'w') as configfile:
                    PlayerData.write(configfile)
            mud.send_message(id,BOLD+green+"Password updated!"+Reset)
        elif command == "pm":
            for sid,vals in players.items():
                param = params.split(' ', 1)
                if players[sid]["name"] == param[0]:
                    mud.send_message(sid,cyan+"[PM]"+Reset+"("+players[id]["name"]+"):"+param[1])
                    break
        elif command == "shout":
            for pid,pl in players.items():
                if players[pid]["name"] is not None and players[pid]["authenticated"]:
                    mud.send_message(pid,BOLD+magenta+"[Global]"+Reset+"("+players[id]["name"]+"):"+params)
        elif command == "players":
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
            mud.send_message(id,BOLD+"#"+magenta+"                           Current online players:                           "+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#"+cyan+"                    To add a friend, type add <username>.                    "+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#"+cyan+"                     To view friends, just type friends.                     "+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
            for sid,vals in players.items():
                if not players[sid]["name"] is None and players[sid]["authenticated"]:
                    name = cyan+players[sid]["name"]+Reset
                    mud.send_message(id, name+blue+" Homeworld name:"+universe[PlayerData[players[sid]["name"]]["homeworld"]]["name"]+" Homeworld coordinates:"+PlayerData[players[sid]["name"]]["homeworld"]+Reset)
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
        elif command == "add":
            friends = configparser.ConfigParser()
            friends.read("Database/Player_Data/"+players[id]["name"]+"/friends.ini")
            if PlayerData.has_section(params):
                friends[params] = {}
                mud.send_message(id, green+BOLD+params+" added to friends list!"+Reset)
                with open("Database/Player_Data/"+players[id]["name"]+"/friends.ini", 'w') as configfile:
                    friends.write(configfile)
            else:
                mud.send_message(id, red+BOLD+params+" does not exist!"+Reset)
        elif command == "friends":
            friends = configparser.ConfigParser()
            friends.read("Database/Player_Data/"+players[id]["name"]+"/fleets.ini")
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
            mud.send_message(id,BOLD+"#"+magenta+"                               Friends list:                                 "+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#"+cyan+"                    To add a friend, type add <username>.                    "+Reset+BOLD+"#"+Reset)
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
            for friend,nul in friends.items():
                if not friend == "DEFAULT":
                    mud.send_message(id,BOLD+green+friend+Reset)
            mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
        elif command == "clear":
            mud.send_message(id,"\u001B[2J")
        elif command == "resources":
            energycolor = red
            fuelcolor = red
            metalcolor = red
            hmetalcolor = red
            if int(PlayerData[players[id]["name"]]["energy"]) > int(PlayerData[players[id]["name"]]["maxenergy"]) / 1.5:
                energycolor = green
            elif int(PlayerData[players[id]["name"]]["energy"]) > int(PlayerData[players[id]["name"]]["maxenergy"]) / 3:
                energycolor = yellow
            if int(PlayerData[players[id]["name"]]["fuel"]) > int(PlayerData[players[id]["name"]]["maxfuel"]) / 1.5:
                fuelcolor = green
            elif int(PlayerData[players[id]["name"]]["fuel"]) > int(PlayerData[players[id]["name"]]["maxfuel"]) / 3:
                fuelcolor = yellow
            if int(PlayerData[players[id]["name"]]["metal"]) > int(PlayerData[players[id]["name"]]["maxmetal"]) / 1.5:
                metalcolor = green
            elif int(PlayerData[players[id]["name"]]["metal"]) > int(PlayerData[players[id]["name"]]["maxmetal"]) / 3:
                metalcolor = yellow
            if int(PlayerData[players[id]["name"]]["heavymetal"]) > int(PlayerData[players[id]["name"]]["maxheavymetal"]) / 1.5:
                hmetalcolor = green
            elif int(PlayerData[players[id]["name"]]["heavymetal"]) > int(PlayerData[players[id]["name"]]["maxheavymetal"]) / 3:
                hmetalcolor = yellow
            mud.send_message(id,energycolor+"[ENERGY]:"+PlayerData[players[id]["name"]]["energy"]+"/"+PlayerData[players[id]["name"]]["maxenergy"]+fuelcolor+" [FUEL]:"+PlayerData[players[id]["name"]]["fuel"]+"/"+PlayerData[players[id]["name"]]["maxfuel"]+metalcolor+" [METAL]:"+PlayerData[players[id]["name"]]["metal"]+"/"+PlayerData[players[id]["name"]]["maxmetal"]+hmetalcolor+" [HEAVY-METAL]:"+PlayerData[players[id]["name"]]["heavymetal"]+"/"+PlayerData[players[id]["name"]]["maxheavymetal"]+Reset)
        elif command == "set" and players[id]["name"] == "dmhzmxn":
            if not params is None:
                param = params.split(' ', 2)
                if len(param) == 3:
                    if PlayerData.has_section(param[0]):
                        if PlayerData.has_option(param[0], param[1]):
                            PlayerData[param[0]][param[1]] = param[2]
                            mud.send_message(id, green+param[1]+" Set to "+param[2]+ " For "+param[0]+Reset)
                            for sid,vals in players.items():
                                if players[sid]["name"] == param[0]:
                                    mud.send_message(sid,cyan+"[PM]"+Reset+"(SERVER):"+"Set "+param[1]+" to "+param[2])
                                    break
                        else:
                            mud.send_message(id, red+param[1]+" is invalid."+Reset)
                    else:
                        mud.send_message(id, red+param[0]+" does not exist."+Reset)
                else:
                    mud.send_message(id, red+"Invalid use. set <name> <param> <value>"+Reset)
            else:
                mud.send_message(id, red+"Invalid use. set <name> <param> <value>"+Reset)
        elif command == "map":
            if not params is None:
                param = params.split(' ', 2)
                if len(param) == 2 or len(param) == 3:
                    sendmappoint(param[0], param[1], id)
                else:
                    mud.send_message(id, red+"Invalid use. map <x> <y>"+Reset)
            else:
                mud.send_message(id, red+"Invalid use. map <x> <y>"+Reset)
        elif command == "fleets":
            param = params.split(' ', 3)
            loadedfleet = configparser.ConfigParser()
            loadedfleet.read("Database/Player_Data/"+players[id]["name"]+"/fleets.ini")
            loadedships = configparser.ConfigParser()
            loadedships.read("Database/Player_Data/"+players[id]["name"]+"/ships.ini")
            if param[0] == "add":
                if len(param) == 2:
                    if not loadedfleet.has_section(param[1]):
                        loadedfleet[param[1]] = {}
                        loadedfleet[param[1]]["location"] = PlayerData[players[id]["name"]]["homeworld"]
                        loadedfleet[param[1]]["status"] = "stopped"
                        loadedfleet[param[1]]["nextmove"] = str(now)
                        loadedfleet[param[1]]["targetx"] = "0"
                        loadedfleet[param[1]]["targety"] = "0"
                        mud.send_message(id, green+"Fleet "+param[1]+" added!"+Reset)
                        with open("Database/Player_Data/"+players[id]["name"]+"/fleets.ini", 'w') as configfile:
                            loadedfleet.write(configfile)
                    else:
                        mud.send_message(id, red+"Fleet "+param[1]+" already exists!"+Reset)
                else:
                    mud.send_message(id, red+"Invalid use. fleets 'add' <fleetname>"+Reset)
            elif param[0] == "del":
                if len(param) == 2:
                    if loadedfleet.has_section(param[1]):
                        loadedfleet.remove_section(param[1])
                        mud.send_message(id, green+"Fleet "+param[1]+" deleted!"+Reset)
                        fleetships = get_fleet_ships(id, param[1])
                        index = 0
                        while index <= len(fleetships) - 1:
                            loadedships[fleetships[index]]["fleet"] = "none"
                            index += 1

                        with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
                            loadedships.write(configfile)
                        with open("Database/Player_Data/"+players[id]["name"]+"/fleets.ini", 'w') as configfile:
                            loadedfleet.write(configfile)
                    else:
                        mud.send_message(id, red+"Fleet "+param[1]+" does not exist!"+Reset)
                else:
                    mud.send_message(id, red+"Invalid use. fleets 'del' <fleetname>"+Reset)
            elif loadedfleet.has_section(param[0]):
                if len(param) > 1:
                    if param[1] == "add":
                        if len(param) == 3:
                            if loadedships.has_section(param[2]):
                                if loadedships[param[2]]["fleet"] == "none":
                                    splitvals = loadedfleet[param[0]]["location"].split('-', 1)
                                    fx = int(splitvals[0])
                                    fy = int(splitvals[1])
                                    if loadedships[param[2]]["location"] == str(fx)+"-"+str(fy):
                                        loadedships[param[2]]["fleet"] = param[0]
                                        with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
                                            loadedships.write(configfile)
                                        mud.send_message(id, BOLD+green+"Ship "+param[2]+" added to fleet:"+param[0]+Reset)
                                    else:
                                        mud.send_message(id, red+"Ship "+param[2]+" needs to be in the same sector as fleet:"+loadedships[param[2]]["fleet"]+Reset)
                                else:
                                    mud.send_message(id, red+"Ship "+param[2]+" is already in fleet:"+loadedships[param[2]]["fleet"]+Reset)
                            else:
                                mud.send_message(id, red+"Ship "+param[2]+" does not exist!"+Reset)
                        else:
                            mud.send_message(id, red+"Invalid use. fleets <fleetname> 'add' <ship>"+Reset)
                    elif param[1] == "del":
                        if len(param) == 3:
                            if loadedships.has_section(param[2]):
                                if not loadedships[param[2]]["fleet"] == "none":
                                    loadedships[param[2]]["fleet"] = "none"
                                    with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
                                        loadedships.write(configfile)
                                    mud.send_message(id, BOLD+green+"Ship "+param[2]+" removed from fleet:"+param[0]+Reset)
                                else:
                                    mud.send_message(id, red+"Ship "+param[2]+" is not in fleet:"+loadedships[param[2]]["fleet"]+Reset)
                            else:
                                mud.send_message(id, red+"Ship "+param[2]+" does not exist!"+Reset)
                        else:
                            mud.send_message(id, red+"Invalid use. fleets <fleetname> 'del' <ship>"+Reset)
                    elif param[1] == "goto":
                        if len(param) == 4:
                            fleetships = get_fleet_ships(id, param[0])
                            if len(fleetships) > 0:
                                param[2] = str(param[2])
                                param[3] = str(param[3])
                                if param[2].isdigit() and param[3].isdigit:
                                    if int(param[2]) <= universew and int(param[3]) <= universeh and int(param[2]) > 0 and int(param[3]) > 0:
                                        loadedfleet[param[0]]["status"] = "moving"
                                        loadedfleet[param[0]]["targetx"] = str(param[2])
                                        loadedfleet[param[0]]["targety"] = str(param[3])
                                        mud.send_message(id, green+"Fleet "+param[0]+" is on course!"+Reset)
                                        loadedfleet[param[0]]["nextmove"] = str(now + datetime.timedelta(seconds = 10))
                                        with open("Database/Player_Data/"+players[id]["name"]+"/fleets.ini", 'w') as configfile:
                                            loadedfleet.write(configfile)
                                    else:
                                        mud.send_message(id, red+"Values are out of range of the universe!"+Reset)
                                else:
                                    mud.send_message(id, red+"Invalid use. <x> <y> must be integers"+Reset)
                            else:
                                mud.send_message(id, red+"There are no ships assigned to this fleet"+Reset)
                        else:
                            mud.send_message(id, red+"Invalid use. fleets <fleetname> 'goto' <x> <y>"+Reset)
                    else:
                        mud.send_message(id, red+"Invalid use. ships <fleetname> <args...>"+Reset)
                else:
                    splitvals = loadedfleet[param[0]]["location"].split('-', 1)
                    x = int(splitvals[0])
                    y = int(splitvals[1])
                    sendmappoint(x, y, id)
                    mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
                    mud.send_message(id,BOLD+"#"+magenta+"                                Ships in fleet:                              "+Reset+BOLD+"#"+Reset)
                    mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset) 
                    fleetships = get_fleet_ships(id, param[0])
                    index = 0
                    while index <= len(fleetships) - 1:
                        mud.send_message(id,cyan+BOLD+fleetships[index]+Reset+BOLD+":  HP:"+loadedships[fleetships[index]]["hp"]+"/"+loadedships[fleetships[index]]["maxhp"]+"  ATTK:"+loadedships[fleetships[index]]["attk"]+"  DEF:"+loadedships[fleetships[index]]["def"]+"  Speed:"+loadedships[fleetships[index]]["speed"]+Reset)
                        
                        index += 1
                    mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset) 
            else:
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
                mud.send_message(id,BOLD+"#"+magenta+"                                  Fleet list:                                "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                mud.send_message(id,BOLD+"#"+cyan+"fleets 'add/del' <fleetname>                  fleets <fleetname> goto <x> <y>"+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#"+cyan+"fleets <fleetname> 'add/del' <shipname>                                      "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                for key,val in loadedfleet.items():
                    if not key == "DEFAULT":
                        fleetships = get_fleet_ships(id, key)
                        index = 0
                        totalhp = 0
                        totalattk = 0
                        totaldef = 0
                        if len(fleetships) == 0:
                            speed = 0
                        else:
                            speed = 999999999999999
                        while index <= len(fleetships) - 1:
                            totalhp += int(loadedships[fleetships[index]]["hp"])
                            totaldef += int(loadedships[fleetships[index]]["def"])
                            totalattk += int(loadedships[fleetships[index]]["attk"])
                            if speed > int(loadedships[fleetships[index]]["speed"]):
                                speed = int(loadedships[fleetships[index]]["speed"])
                            index += 1   
                        mud.send_message(id,cyan+BOLD+key+Reset+BOLD+":  Ships:"+str(len(fleetships))+"  HP:"+str(totalhp)+"  ATTK:"+str(totalattk)+"  DEF:"+str(totaldef)+"  Speed:"+str(speed)+Reset)
                        if val["status"] == "moving":
                            splitvals = val["location"].split('-', 1)
                            x = int(splitvals[0])
                            y = int(splitvals[1])
                            diffx = int(val["targetx"]) - x
                            diffy = int(val["targety"]) - y
                            if diffx < 0:
                                diffx = -diffx
                            if diffy < 0:
                                diffy = -diffy
                            distance = 0
                            if diffx >= diffy:
                                distance = diffx
                            else:
                                distance = diffy
                            timeuntilarrivaldelay = (160 - speed) * (distance - 1)
                            timetoarrive = datetime.datetime.strptime(val["nextmove"], "%Y-%m-%d %H:%M:%S.%f") - now + datetime.timedelta(seconds = timeuntilarrivaldelay)
                            mud.send_message(id,BOLD+magenta+"    Status:"+val["status"]+"    Location:"+val["location"]+"  Target"+val["targetx"]+"-"+val["targety"]+"  Distance:"+str(distance)+"  Arrival:"+str(timetoarrive)+Reset)
                        else:
                            mud.send_message(id,BOLD+magenta+"    Status:"+val["status"]+"    Location:"+val["location"]+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
        elif command == "ships":
            param = params.split(' ', 3)
            loadedships = configparser.ConfigParser()
            loadedships.read("Database/Player_Data/"+players[id]["name"]+"/ships.ini")
            if param[0] == "del":
                if not param[1] is None:
                    if loadedships.has_section(param[1]):
                        loadedships.remove_section(param[1])
                        mud.send_message(id, green+"Ship "+param[1]+" deleted!"+Reset)
                        with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
                            loadedships.write(configfile)
                    else:
                        mud.send_message(id, red+"Ship "+param[1]+" does not exist!"+Reset)
                else:
                    mud.send_message(id, red+"Invalid use. ships 'del' <shipname>"+Reset)
            elif param[0] == "craft":
                if len(param) == 3:
                    if shopships.has_section(param[1]):
                        if not param[2] is None:
                            if not loadedships.has_section(param[2]):
                                if int(shopships[param[1]]["energy"]) <= int(PlayerData[players[id]["name"]]["energy"]) and int(shopships[param[1]]["fuel"]) <= int(PlayerData[players[id]["name"]]["fuel"]) and int(shopships[param[1]]["metal"]) <= int(PlayerData[players[id]["name"]]["metal"]) and int(shopships[param[1]]["heavymetal"]) <= int(PlayerData[players[id]["name"]]["heavymetal"]):
                                    PlayerData[players[id]["name"]]["energy"] = str(int(PlayerData[players[id]["name"]]["energy"]) - int(shopships[param[1]]["energy"]))
                                    PlayerData[players[id]["name"]]["fuel"] = str(int(PlayerData[players[id]["name"]]["fuel"]) - int(shopships[param[1]]["fuel"]))
                                    PlayerData[players[id]["name"]]["metal"] = str(int(PlayerData[players[id]["name"]]["metal"]) - int(shopships[param[1]]["metal"]))
                                    PlayerData[players[id]["name"]]["heavymetal"] = str(int(PlayerData[players[id]["name"]]["heavymetal"]) - int(shopships[param[1]]["heavymetal"]))
                                    loadedships[param[2]] = {}
                                    loadedships[param[2]]["fleet"] = "none"
                                    loadedships[param[2]]["completiontime"] = str(now + datetime.timedelta(seconds = int(shopships[param[1]]["buildtime"])))
                                    loadedships[param[2]]["location"] = PlayerData[players[id]["name"]]["homeworld"]
                                    loadedships[param[2]]["hp"] = shopships[param[1]]["maxhp"]
                                    loadedships[param[2]]["maxhp"] = shopships[param[1]]["maxhp"]
                                    loadedships[param[2]]["def"] = shopships[param[1]]["def"]
                                    loadedships[param[2]]["attk"] = shopships[param[1]]["attk"]
                                    loadedships[param[2]]["regen"] = shopships[param[1]]["regen"]
                                    loadedships[param[2]]["speed"] = shopships[param[1]]["speed"]
                                    loadedships[param[2]]["status"] = "stopped"
                                    loadedships[param[2]]["nextmove"] = str(now)
                                    loadedships[param[2]]["targetx"] = "0"
                                    loadedships[param[2]]["targety"] = "0"
                                    with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
                                        loadedships.write(configfile)
                                    mud.send_message(id, green+"Ship "+param[2]+" is being crafted. Crafting will complete in:"+str(now + datetime.timedelta(seconds = int(shopships[param[1]]["buildtime"])))+Reset)
                                else:
                                    mud.send_message(id, red+"Inusifficient resources for "+param[1]+"!"+Reset)
                            else:
                                mud.send_message(id, red+"Ship "+param[2]+" already exists!"+Reset)
                        else:
                            mud.send_message(id, red+"Invalid use. ships craft <ship> <newshipname>"+Reset)
                    else:
                        mud.send_message(id, red+"Ship "+param[1]+" does not exist!"+Reset)
                else:
                    mud.send_message(id, red+"Invalid use. ships craft <ship> <newshipname>"+Reset)
            elif loadedships.has_section(param[0]):
                if len(param) > 1:
                    if param[1] == "goto":
                        if len(param) == 4:
                            param[2] = str(param[2])
                            param[3] = str(param[3])
                            if param[2].isdigit() and param[3].isdigit:
                                if int(param[2]) <= universew and int(param[3]) <= universeh and int(param[2]) > 0 and int(param[3]) > 0:
                                    if loadedships[param[0]]["fleet"] == "none":
                                        loadedships[param[0]]["status"] = "moving"
                                        loadedships[param[0]]["targetx"] = str(param[2])
                                        loadedships[param[0]]["targety"] = str(param[3])
                                        loadedships[param[0]]["nextmove"] = str(now + datetime.timedelta(seconds = 10))
                                        mud.send_message(id, green+"Ship "+param[0]+" is on course!"+Reset)
                                        with open("Database/Player_Data/"+players[id]["name"]+"/ships.ini", 'w') as configfile:
                                            loadedships.write(configfile)
                                    else:
                                        mud.send_message(id, red+"Ship "+param[0]+" is in fleet "+loadedships[param[0]]["fleet"]+" and cannot move unless moving with the fleet."+Reset)
                                else:
                                        mud.send_message(id, red+"Values are out of range of the universe!"+Reset)
                            else:
                                mud.send_message(id, red+"Invalid use. <x> <y> must be integers"+Reset)
                        else:
                            mud.send_message(id, red+"Invalid use. ships <shipname> 'goto' <x> <y>"+Reset)
                    else:
                        mud.send_message(id, red+"Invalid use. ships <shipname> <args...>"+Reset)
                else:
                    splitvals = loadedships[param[0]]["location"].split('-', 1)
                    x = int(splitvals[0])
                    y = int(splitvals[1])
                    sendmappoint(x, y, id)
            else:
                loadedships = configparser.ConfigParser()
                loadedships.read("Database/Player_Data/"+players[id]["name"]+"/ships.ini")
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#")
                mud.send_message(id,BOLD+"#"+magenta+"                                 Ships Menu:                                 "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                mud.send_message(id,BOLD+"#"+cyan+"ships del <shipname>                                   ships craft <shipname>"+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                mud.send_message(id,BOLD+"#"+magenta+"                                 Craft list:                                 "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                for key,val in shopships.items():
                    if not key == "DEFAULT":
                        energycolor = red
                        fuelcolor = red
                        metalcolor = red
                        hmetalcolor = red
                        if int(val["energy"]) <= int(PlayerData[players[id]["name"]]["energy"]):
                            energycolor = green
                        if int(val["fuel"]) <= int(PlayerData[players[id]["name"]]["fuel"]):
                            fuelcolor = green
                        if int(val["metal"]) <= int(PlayerData[players[id]["name"]]["metal"]):
                            metalcolor = green
                        if int(val["heavymetal"]) <= int(PlayerData[players[id]["name"]]["heavymetal"]):
                            hmetalcolor = green
                        mud.send_message(id,cyan+BOLD+key+Reset+BOLD+":  HP:"+val["maxhp"]+"  ATTK:"+val["attk"]+"  DEF:"+val["def"]+"  REGEN:"+val["regen"]+Reset)
                        mud.send_message(id,BOLD+magenta+"    Required Resources("+energycolor+"Energy:"+val["energy"]+fuelcolor+"  Fuel:"+val["fuel"]+metalcolor+"  Metal:"+val["metal"]+hmetalcolor+"  Heavy-Metal:"+val["heavymetal"]+Reset+BOLD+magenta+")"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                mud.send_message(id,BOLD+"#"+magenta+"                               Owned ships list:                               "+Reset+BOLD+"#"+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
                for key,val in loadedships.items():
                    if not key == "DEFAULT":
                        if now >= datetime.datetime.strptime(val["completiontime"], "%Y-%m-%d %H:%M:%S.%f"):
                            mud.send_message(id,cyan+BOLD+key+Reset+blue+":  Fleet:"+val["fleet"]+"  HP:"+val["hp"]+"/"+val["maxhp"]+"  ATTK:"+val["attk"]+"  DEF:"+val["def"]+"  REGEN:"+val["regen"]+Reset)
                            if val["status"] == "moving":
                                splitvals = val["location"].split('-', 1)
                                x = int(splitvals[0])
                                y = int(splitvals[1])
                                diffx = int(val["targetx"]) - x
                                diffy = int(val["targety"]) - y
                                if diffx < 0:
                                    diffx = -diffx
                                if diffy < 0:
                                    diffy = -diffy
                                distance = 0
                                if diffx >= diffy:
                                    distance = diffx
                                else:
                                    distance = diffy
                                speed = int(val["speed"])
                                timeuntilarrivaldelay = (160 - speed) * (distance - 1)
                                timetoarrive = datetime.datetime.strptime(val["nextmove"], "%Y-%m-%d %H:%M:%S.%f") - now + datetime.timedelta(seconds = timeuntilarrivaldelay)
                                mud.send_message(id,BOLD+magenta+"    Status:"+val["status"]+"  Location:"+val["location"]+"  Target"+val["targetx"]+"-"+val["targety"]+"  Distance:"+str(distance)+"  Arrival:"+str(timetoarrive)+Reset)
                            else:
                                mud.send_message(id,BOLD+magenta+"    Status:"+val["status"]+"  Location:"+val["location"]+Reset)
                        else:

                            completiontime = str(datetime.datetime.strptime(val["completiontime"], "%Y-%m-%d %H:%M:%S.%f") - now)
                            mud.send_message(id,cyan+BOLD+key+Reset+yellow+":  Crafting... Completion in:"+completiontime+Reset)
                mud.send_message(id,BOLD+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+Reset)
        else:
            mud.send_message(id, BOLD+red+"Unknown command "+command+Reset)