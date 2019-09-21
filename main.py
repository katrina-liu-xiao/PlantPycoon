# Original code from CMU 15112 Socket Manuel by Rohan Varma adapted by Kyle Chin
# Some changes have been made to the code
import socket
import threading
from queue import Queue

HOST = "127.0.0.1"#  Enter server IP address here
PORT = 50001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST,PORT))
print("connected to server")


def handleServerMsg(server,serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")


#   All images and audios are from Plant Tycoon by Last Day of Work

import pygame
from game import PygameGame
from achievements import Achievement
import copy,random

class plantPycoon(PygameGame):
    def __init__(self, width=800, height=600, fps=50, title="Plant Pycoon",serverMsg = None,server = None):
        super().__init__(width,height,fps,title,serverMsg,server)
        self.currScreen = "menu"
        self.font = pygame.font.SysFont("comicsansms", 24)
    def init(self):
        self.mouse = None
        self.timer = 0
        self.playing = False
        #   Menu Page
        self.menuBg = pygame.image.load("images/Menu_BG.jpg")
        self.playButtonImage = pygame.image.load("images/buttons/play.png")
        self.playButtonPos = (200,200)
        self.continueButtonImage = pygame.image.load("images/buttons/play.png")
        self.continueButtonPos = (150,350)
        self.helpButtonImage = pygame.image.load("images/buttons/play.png")
        self.helpButtonPos = (200,500)
        self.saveButtonImage = pygame.image.load("images/buttons/play.png")
        self.saveButtonPos = (500,400)
        self.saved = False
        self.achievementButtonImage = pygame.image.load("images/buttons/play.png")
        self.achievementButtonPos = (600,300)
        #   Help Page
        self.help = [pygame.image.load("images/help_1.png"),pygame.image.load("images/help_5.png")]
        self.helpIndex = 0
        #   Enter Username Page
        self.enterBg = pygame.image.load("images/Menu_BG.jpg")
        self.enterPos = (self.width//2-90,self.height//2-60,180,36)
        self.name = ""
        self.repeat = False
        self.backButtonImage = pygame.image.load("images/buttons/play.png")
        self.backButtonPos = (600,500)
        
        #   Continue Page
        self.localUsernames = plantPycoon.readFile("userData/localUsername.txt")
        self.namePos = [(350,250),(350,350)]
        self.nameColor = [(255,255,255),(255,255,255)]
        
        #   Achievement Page
        self.achievementVisit = Achievement("visit",5,1)
        self.achievementPlant = Achievement("plant",5,1)
        self.achievementSell = Achievement("sell",5,1)
        self.achievementMoney = Achievement("money",1000,1)
        self.achievementPos = [(100,150),(100,200),(100,250),(100,300),(100,350)]
        #   Main Page
        self.mainBg = pygame.image.load("images/main_bg.png")
        self.hoseImage = pygame.image.load("images/hose.png")
        self.potImage = pygame.image.load("images/goldpot.png")
        self.sellButtonImage = pygame.image.load("images/buttons/sell.png")
        self.sellAllButtonImage = pygame.image.load("images/buttons/sell.png")
        self.sellButtonPos = (114,408)
        self.sellAllButtonPos = (34,408)
        self.seed = copy.copy([False]*15)
        x,y = 290,100
        dx,dy = 95,145
        self.potPos = [(x,y),(x+dx,y),(x+2*dx,y),(x+3*dx,y),(x+4*dx,y),
                (x,y+dy),(x+dx,y+dy),(x+2*dx,y+dy),(x+3*dx,y+dy),(x+4*dx,y+dy),
    (x,y+2*dy),(x+dx,y+2*dy),(x+2*dx,y+2*dy),(x+3*dx,y+2*dy),(x+4*dx,y+2*dy),]
        self.trashbinImage = pygame.image.load("images/tools/trashbin1.png")
        self.focusedPlant = 0
        self.focusedPlantImage = pygame.image.load("images/plant_focus.png")
        self.money = 500
        self.moneyPos = (100,542)
        self.plantType = copy.copy([-1]*15)
        self.plantStage = copy.copy([-1]*15)
        self.plantAge = copy.copy([-1]*15)
        self.carrySeedNum = copy.copy([-1]*15)
        self.flower = copy.copy([-1]*15)
        self.plantPrice = copy.copy([-1]*15)
        self.bug = pygame.image.load("images/pest.png")

            #   Tools
        self.waterbucketLevel = 1
        self.waterbucketImage = pygame.image.load("images/tools/waterbucket%d.png"%self.waterbucketLevel)
        self.water = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.pesticideImage = pygame.image.load("images/tools/pesticide.png")
        self.pesticideDose = 3
        self.health = copy.copy([148] *15)
        self.magicImage = pygame.image.load("images/tools/magic.png")
        self.magicDose = 3
        self.strongMagicImage = pygame.image.load("images/tools/strongmagic.png")
        self.strongMagicDose = 3
        self.leftdose = None
        
        #   Seedbox Page
        self.SeedboxBg = pygame.image.load("images/SeedBox_BG.jpg")
        self.additionalSeedboxImage = pygame.image.load("images/addlSeedBox.png") 
        self.addSeedboxPos = [(240,200),(240,350)]
        self.seedList = [pygame.image.load("images/seeds/seed1.png"),
        pygame.image.load("images/seeds/seed2.png"),
        pygame.image.load("images/seeds/seed3.png"),
        pygame.image.load("images/seeds/seed4.png"),
        pygame.image.load("images/seeds/seed5.png")]
        self.seedBox = copy.copy([-1]*120)
        for i in range(10):
            self.seedBox[i] = random.randint(0,4)
        self.seedboxLevel = 1
        self.seedBoxPos = []
        seedx,seedy,dseedx,dseedy = 243,44,53,36
        for i in range(10):
            for j in range(4):
                self.seedBoxPos.append((seedx+i*dseedx,seedy+j*dseedy))
        self.currSeed = None
        sx,sy,dsx,dsy = 20,28,42,35
        self.miniSeedbox = copy.copy([-1]*8)
        self.miniSeedboxPos = [(sx,sy),(sx+dsx,sy),(sx+2*dsx,sy),(sx+3*dsx,sy),
                (sx,sy+dsy),(sx+dsx,sy+dsy),(sx+2*dsx,sy+dsy),(sx+3*dsx,sy+dsy)]
        for i in range(8):
            self.miniSeedbox[i] = random.randint(0,4)
        
        #   Store Page
        self.StoreBg = pygame.image.load("images/Store_BG.jpg")
        self.checkmark = pygame.image.load("images/CHECKMARK.png")
        self.waterbucketLevel = 1
        self.soilLevel = 1
        self.storeSeed = [random.randint(0,4) for i in range(6)]
        self.storeSeedPos = [(670,60),(670,130),(670,200),(670,300),(670,370),(670,435)]

        bx,by = 250,540
        dbx = 100
        self.mainButtons = [True,False,False,False,False]
        self.buttonPos = [(bx,by),(bx+1*dbx,by),(bx+2*dbx,by),(bx+3*dbx,by),
                                                            (bx+4*dbx,by)]
        #   Visiting page
        self.VisitBg = pygame.image.load("images/main_bg.png")
        self.visitingMode = False
        self.beingVisited = False
        self.msg = ""
        
        
    def mousePressed(self, x, y):
        self.saved = False
        if self.currScreen == "menu":
            #   New Game Button
            if 200 < x < 320 and 200 < y < 250:
                self.currScreen = "enter"
                self.name = ""
                self.mainButtons = [True,False,False,False,False]
            #   Continue Button
            elif 150 < x < 270 and 350 < y < 400:
                self.currScreen = "continue"
            elif 500 < x < 620 and 400 < y < 450:
                path = "userData/" + self.name + ".txt"
                plantPycoon.saveProgress(self,path)
                self.saved = True
            elif 600 < x < 720 and 300 < y < 350:
                self.currScreen = "achievements"
            elif 200 < x < 320 and 500 < y < 550:
                self.currScreen = "help"
        elif self.currScreen == "help":
            if self.helpIndex == 1:
                self.currScreen = "menu"
                self.helpIndex = 0
            else:
                self.helpIndex = 1
            
        elif self.currScreen == "enter" or self.currScreen == "achievements":
            if 600 < x < 720 and 500 < y < 550:
                self.currScreen = "menu"
        elif self.currScreen == "continue":
            if 600 < x < 720 and 500 < y < 550:
                self.currScreen = "menu"
            localUsernames = plantPycoon.readFile("userData/localUsername.txt").strip()
            for i in range(len(self.namePos)):
                namex,namey = self.namePos[i]
                if namex < x < namex+80 and namey < y < namey+30:
                    self.name = localUsernames.split("\n")[i]
                    path = "userData/" + self.name + ".txt"
                    plantPycoon.readProgress(self,path)
                    self.playing = True
                    self.currScreen = "main"
        
                    
        else:
            
            
            #   Main Buttons Clicking
            if y >= 540:
                if self.currScreen != "main" and 290 <= x <= 390 and self.visitingMode == False:
                    self.mainButtons = [True,False,False,False,False]
                    self.currScreen = "main"
                elif self.currScreen != "seedbox" and 390 <= x <= 490 and self.visitingMode == False:
                    self.mainButtons = [False,True,False,False,False]
                    self.currScreen = "seedbox"
                elif self.currScreen != "store" and 490 <= x <= 590 and self.visitingMode == False:
                    self.mainButtons = [False,False,True,False,False]
                    self.currScreen = "store"
                # Cannot visit when being visited
                elif self.currScreen != "visit" and self.beingVisited == False \
                            and 590 <= x <= 690 and self.visitingMode == False:
                    path = "userData/" + self.name + ".txt"
                    plantPycoon.saveProgress(self,path)
                    msg = "request\n"                                                                                   
                    self.server.send(msg.encode())
                    self.visitingMode = True
                    self.mainButtons = [False,False,False,True,False]
                    self.achievementVisit.gain(1)
                    self.currScreen = "visit"
                elif 690 <= x <= 790:
                    if self.visitingMode:
                        path = "userData/" + self.name + ".txt"
                        self.readProgress(path)
                        self.visitingMode = False
                        self.server.send(("done\n").encode())
                    self.mainButtons = [True,False,False,False,False]
                    self.currScreen = "menu"
            
            
            #   Main Page
            if self.currScreen == "main" or self.currScreen == "visit":
                #   ToolBox
                if 30 <= x <= 80 and 140 <= y <= 180:
                    if self.mouse != "waterbucket":
                        self.mouse = "waterbucket"
                    else:
                        self.mouse = None
                elif 80 < x <= 130 and 140 <= y <= 180:
                    if self.pesticideDose > 0 and self.mouse != "pesticide":
                        self.mouse = "pesticide"
                    else:
                        self.mouse = None
                elif 30 <= x <= 80 and 180 <= y <= 240:
                    if self.magicDose > 0 and self.mouse != "magic":
                        self.mouse = "magic"
                    else:
                        self.mouse = None
                elif 80 < x <= 130 and 180 <= y <= 240:
                    if self.strongMagicDose > 0 and self.mouse != "strongmagic":
                        self.mouse = "strongmagic"
                    else:
                        self.mouse = None
                #   Plants
                plantClicked = False
                for i in range(len(self.potPos)):
                    pos = self.potPos[i]
                    posx,posy= pos
                    if posx <= x < posx+80 and posy <= y < posy+95:
                        self.focusedPlant = i
                        plantClicked = True
                        if self.mouse != None and self.mouse.startswith("seed") and not self.seed[i]:
                            self.seed[i] = True
                            self.plantType[i] = int(self.mouse[-1])
                            self.plantStage[i] = 0
                            self.plantAge[i] = 0
                            self.plantPrice[i] = 10 
                            self.mouse = None
                if not plantClicked:
                    self.focusedPlant = -1
                
                
                if 34 < x < 100 and 408 < y < 438:
                    self.sellAllButtonImage = pygame.image.load("images/buttons/sell1.png")
                    for i in range(15):
                        if self.plantStage[i] == 3:
                            plantPycoon.sellPlant(self,i)
                elif 114 < x < 180 and 408 < y < 438:
                    if self.focusedPlant >= 0 and self.seed[self.focusedPlant]:
                        self.sellButtonImage = pygame.image.load("images/buttons/sell1.png")
                        plantPycoon.sellPlant(self,self.focusedPlant)
            #   Mini Seedbox
            if self.currScreen == "main" or self.currScreen == "seedbox" or self.currScreen == "visit":
                for i in range(len(self.miniSeedbox)):
                    sx,sy = self.miniSeedboxPos[i]
                    if self.miniSeedbox[i] != -1 and sx<x<sx+42 and sy<y<sy+35:
                        self.mouse = "seed" + str(self.miniSeedbox[i])
                        self.currSeed = self.seedList[self.miniSeedbox[i]]
                        self.miniSeedbox[i] = -1
                    elif self.miniSeedbox[i] == -1 and sx<x<sx+42 and sy<y<sy+35:
                        if self.mouse.startswith("seed"):
                            self.miniSeedbox[i] = int(self.mouse[-1])
                            self.currSeed = None
                            self.mouse = None
            if self.currScreen == "seedbox":
                for i in range(len(self.seedBoxPos)):
                    sx,sy = self.seedBoxPos[i]
                    if self.seedBox[i] != -1 and sx<x<sx+53 and sy<y<sy+36 :
                        if self.mouse == None or not self.mouse.startswith("seed"):
                            self.mouse = "seed" + str(self.seedBox[i])
                            self.currSeed = self.seedList[self.seedBox[i]]
                            self.seedBox[i] = -1
                    elif self.seedBox[i] == -1 and self.mouse != None \
                                                    and sx<x<sx+53 and sy<y<sy+36:
                        self.seedBox[i] = int(self.mouse[-1])
                        self.currSeed = None
                        self.mouse = None
            
            #   Mouse
            if self.mouse != None:
                if self.mouse == "waterbucket":
                    if not (30 <= self.mousex <= 80 and 140 <= self.mousey <= 200):
                        self.waterbucketImage = pygame.image.load("images/tools/waterbucket%d_clicked.png"\
                                                                %self.waterbucketLevel)
                elif self.mouse == "pesticide":
                    if not (80 < x <= 130 and 140 <= y <= 180):
                        self.pesticideImage = pygame.image.load("images/tools/pesticide1.png")
                        if self.focusedPlant >= 0 and self.pesticideDose > 0:
                            self.health[self.focusedPlant] += 20
                            if self.health[self.focusedPlant] > 148:
                                self.health[self.focusedPlant] = 148
                            self.pesticideDose -= 1
                elif self.mouse == "magic":
                    if not (30 < x <= 80 and 180 <= y <= 220):
                        self.magicImage = pygame.image.load("images/tools/magic1.png")
                        if self.focusedPlant >= 0 and self.magicDose > 0:
                            if self.plantStage[self.focusedPlant] < 3:
                                self.plantStage[self.focusedPlant] += 1
                                self.magicDose -= 1
                                
                elif self.mouse == "strongmagic":
                    if not (80 < x <= 130 and 180 <= y <= 220):
                        self.strongMagicImage = pygame.image.load("images/tools/strongmagic1.png")
                        if self.strongMagicDose > 0:
                            for i in range(15):
                                if self.seed and self.plantStage[i] < 3:
                                    self.plantStage[i] += 1
                                    self.magicDose -= 1
            
            #   Store
            if self.currScreen == "store":
                # Upgrade waterbucket
                if 270 < x < 320:
                    for i in range(3):
                        if i >= self.waterbucketLevel and 60+i*65<y< 110 + i*65:
                            self.money -= i*500
                            self.waterbucketLevel += 1
                            self.waterbucketImage = pygame.image.load("images/tools/waterbucket%d.png"\
                                                                    %self.waterbucketLevel)
                # Upgrade soil
                if 350 < x < 400:
                    for i in range(3):
                        if i >= self.soilLevel and 60+i*65<y< 110 + i*65:
                            self.money -= i*500
                            self.soilLevel += 1
                # Upgrade seedbox
                if 450 < x < 500:
                    for i in range(3):
                        if i >= self.seedboxLevel and 60+i*65<y< 110 + i*65:
                            self.money -= i*500
                            self.seedboxLevel += 1
                            seedx,seedy = self.addSeedboxPos[self.seedboxLevel-2]
                            dseedx,dseedy = 53,36
                            for i in range(10):
                                for j in range(4):
                                    self.seedBoxPos.append((seedx+i*dseedx,seedy+j*dseedy))
                # Buy tools
                if 350 < x < 400 and y > 300:
                    if y < 350:
                        self.pesticideDose += 3
                        self.money -= 100
                    if 370 < y < 420:
                        self.magicDose += 3
                        self.money -= 250
                    if 440 < y < 490:
                        self.strongMagicDose += 3
                        self.money -= 1500
                # Buy seeds [(670,60),(670,130),(670,200),(670,300),(670,370),(670,435)]
                if -1 in self.seedBox[:40*self.seedboxLevel] and 670 < x < 700:
                    pos = self.seedBox[:40*self.seedboxLevel].index(-1)
                    for i in range(6):
                        posy = self.storeSeedPos[i][1]
                        if posy < y < posy + 40:
                            self.seedBox[pos] = self.storeSeed[i]
                            self.money -= 100
            #   Trash
            if self.currScreen == "main" or self.currScreen == "seedbox":
                if self.mouse != None and self.mouse.startswith("seed"):
                    if 150 <= x <= 230 and 520 <= y <= self.height:
                        self.mouse = None
                        self.currSeed = None
                        self.money += 5

    
    def mouseReleased(self, x, y):
        if self.mouse != None:
            if self.mouse == "waterbucket":
                self.waterbucketImage = pygame.image.load("images/tools/waterbucket%d.png"\
                                                            %self.waterbucketLevel)
            elif self.mouse == "pesticide":
                self.pesticideImage = pygame.image.load("images/tools/pesticide.png")
            elif self.mouse == "magic":
                self.magicImage = pygame.image.load("images/tools/magic.png")
            elif self.mouse == "strongmagic":
                self.strongMagicImage = pygame.image.load("images/tools/strongmagic.png")
        if self.currScreen == "main":
            self.sellAllButtonImage = pygame.image.load("images/buttons/sell.png")
            self.sellButtonImage = pygame.image.load("images/buttons/sell.png")
    #   To check for in image position
    
    def mouseMotion(self, x, y):
        self.mousex,self.mousey = x,y
        if self.currScreen == "menu":
            if 200 < x < 320 and 200 < y < 250:
                self.playButtonImage = pygame.image.load("images/buttons/play1.png")
            elif 150 < x < 270 and 350 < y < 400:
                self.continueButtonImage = pygame.image.load("images/buttons/play1.png")
            elif 200 < x < 320 and 500 < y < 550:
                self.helpButtonImage = pygame.image.load("images/buttons/play1.png")
            elif 500 < x < 620 and 400 < y < 450:
                self.saveButtonImage = pygame.image.load("images/buttons/play1.png")
            elif 600 < x < 720 and 300 < y < 350:
                self.achievementButtonImage = pygame.image.load("images/buttons/play1.png")
            else:
                self.playButtonImage = pygame.image.load("images/buttons/play.png")
                self.continueButtonImage = pygame.image.load("images/buttons/play.png")
                self.helpButtonImage = pygame.image.load("images/buttons/play.png")
                self.saveButtonImage = pygame.image.load("images/buttons/play.png")
                self.achievementButtonImage = pygame.image.load("images/buttons/play.png")
        elif self.currScreen == "continue":
            for i in range(len(self.namePos)):
                namex,namey = self.namePos[i]
                if namex < x < namex+80 and namey < y < namey+30:
                    self.nameColor[i] = (0,0,0)
                else:
                    self.nameColor[i] = (255,255,255)
        elif self.currScreen == "enter" or self.currScreen == "continue" or\
         self.currScreen == "achievements":
            if 600 < x < 720 and 500 < y < 550:
                self.backButtonImage = pygame.image.load("images/buttons/play1.png")
            else:
                self.backButtonImage = pygame.image.load("images/buttons/play.png")
        elif self.currScreen == "main" or self.currScreen == "seedbox":
            if 150 <= x <= 230 and 520 <= y <= self.height:
                self.trashbinImage = pygame.image.load("images/tools/trashbin2.png")
            else:
                self.trashbinImage = pygame.image.load("images/tools/trashbin1.png")
        elif self.currScreen == "main":
            if 80 < x <= 130 and 140 <= y <= 200:
                self.leftdose = "pesticide"
            else:
                self.leftdose = None
                
    def keyPressed(self, keyCode, modifier):
        if self.currScreen == "enter" and len(self.name) <= 10:
            if 48 <= keyCode <= 57:
                self.name += chr(keyCode)
            elif 97 <= keyCode <= 122:
                self.name += chr(keyCode) 
            elif keyCode == 8 and len(self.name) > 0:
                self.name = self.name[:-1]
            elif keyCode == 13:
                if plantPycoon.nameRepeats(self.name):
                    self.name = ""
                    self.repeat = True
                else:
                    self.repeat = False
                    name = self.name
                    self.init()
                    self.name = name
                    localContent = plantPycoon.readFile("userData/localUsername.txt")
                    if localContent.count("\n") >= 2:
                        localContent = localContent.split("\n")[-2] + "\n" 
                    localContent += self.name + "\n"
                    plantPycoon.writeFile("userData/localUsername.txt", localContent)
                    potStatus = "pot 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n"
                    plantPycoon.writeFile("userData/"+self.name+".txt",potStatus)
                    self.playing = True
                    self.currScreen = "main"
        elif keyCode == 32 and self.currScreen == "main" and self.focusedPlant >= 0:
            if self.seed[self.focusedPlant]:
                self.plantAge[self.focusedPlant] += 20
                
    
    def timerFired(self, dt):
        for i in range(len(self.water)):
            if self.water[i] - 0.002 >= 0:
                self.water[i] -= 0.002
            if self.water[i] <= 50 and self.seed[i] and self.health[i] > 0:
                self.health[i] -= 0.5
                if self.health[i] <= 0:
                    plantPycoon.sellPlant(self,i)
        if self.playing:
            self.timer += 1
            if self.timer > 0 and self.timer % 200 == 0:
                for i in range(len(self.plantAge)):
                    if self.seed[i]:
                        self.plantAge[i] += 1
                        if self.plantAge[i] >= 100:
                            plantPycoon.sellPlant(self,i)
                    if self.plantAge[i] > 0 and self.plantAge[i] % 20 == 0 and self.plantStage[i] < 3:
                        self.plantStage[i] += 1
                        if self.plantStage[i] == 3:
                            self.achievementPlant.gain(1)
                    if self.plantStage[i]  == 3 and self.plantAge[i] % 10 == 0:
                        self.carrySeedNum[i] += 1 
                    
        if self.mouse == "waterbucket" and pygame.mouse.get_pressed()[0] == True\
                                    and self.water[self.focusedPlant] <= 148:
            self.water[self.focusedPlant] += self.waterbucketLevel
            if self.currScreen == "visit":
                if self.focusedPlant >= 0 :
                    msg = "watering " + str(self.focusedPlant) + "\n"
                    self.server.send(msg.encode())
        #   Receiving Msgs
        while (self.serverMsg.qsize() > 0):
            msg = self.serverMsg.get(False)
            print()
            try:
                print("rec:" + msg)
                if msg.startswith("request"):
                    if self.visitingMode == False:
                        path = "userData/" + self.name + ".txt"
                        plantPycoon.saveProgress(self,path)
                        content = plantPycoon.readFile(path)
                        sendMsg = ""
                        for command in content.split("\n"):
                            if command.startswith("pot") or command.startswith("water")\
                            or  command.startswith("health") or command.startswith("plantstage")\
                            or command.startswith("age") or command.startswith("type"):
                                sendMsg += command + "\n"
                        print(sendMsg)
                        self.server.send(sendMsg.encode())
                        self.beingVisited = True
                #   planting potnum seednum
                elif msg.startswith("watering"):
                    focusedPlant = int(msg[-1])
                    if self.water[focusedPlant] <= 148:
                        self.water[focusedPlant] += 1                    
                elif msg.startswith("done"):
                    self.beingVisited = False
                else:
                    progress = msg
                    for command in progress.split("\n"):
                        if command.startswith("pot"):
                            potStatus = command.split(" ")[1:]
                            for i in range(15):
                                if potStatus[i] != "0":
                                    self.seed[i] = True
                                else:
                                    self.seed[i] = False
                        elif command.startswith("water"):
                            water = command.split(" ")[1:]
                            for i in range(15):
                                self.water[i] = int(water[i])
                        elif command.startswith("health"):
                            health = command.split(" ")[1:]
                            for i in range(15):
                                self.health[i] = int(health[i])
                        elif command.startswith("plantstage"):
                            plantStage = command.split(" ")[1:]
                            for i in range(15):
                                self.plantStage[i] = int(plantStage[i])
                        elif command.startswith("age"):
                            Ages = command.split(" ")[1:]
                            for i in range(15):
                                self.plantAge[i] = int(Ages[i])
                        elif command.startswith("type"):
                            type = command.split(" ")[1:]
                            for i in range(15):
                                self.plantType[i] = int(type[i])
            except:
                print("failed")
            self.serverMsg.task_done()
    @staticmethod
    def nameRepeats(name):
        content = plantPycoon.readFile("userData/localUsername.txt")
        for n in content.split("\n"):
            if name == n:
                return True
        return False
            
                
    @staticmethod            
    def writeFile(path, contents):
        with open(path, "wt") as f:
            f.write(contents)
    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()
    def saveProgress(self, path):
        content = ""
        pot = "pot"
        for i in self.seed:
            if i == True:
                pot += " 1"
            else:
                pot += " 0"
        content += pot + "\n"
        water = "water"
        for i in self.water:
            water += " " + str(int(i))
        content += water + "\n"
        health = "health"
        for h in self.health:
            health += " " + str(int(h))
        content += health + "\n"
        plantStage = "plantstage"
        for stage in self.plantStage:
            plantStage += " " + str(stage)
        content += plantStage + "\n"
        content += "waterbucket " + str(self.waterbucketLevel) + "\n"
        miniseeds = "mini"
        for seed in self.miniSeedbox:
            miniseeds += " " + str(seed)
        content += miniseeds + "\n"
        box = "box " + str(self.seedboxLevel) + "\n"
        content += box
        soil = "soil " + str(self.soilLevel) + "\n"
        seeds = "seed"
        for seed in self.seedBox:
            seeds += " " + str(seed)
        content += seeds + "\n"
        age = "age"
        for i in self.plantAge:
            age += " " + str(i)
        content += age + "\n"
        type = "type"
        for i in self.plantType:
            type += " " + str(i)
        content += type + "\n"
        dose = "dose %d %d %d" % (self.pesticideDose,self.magicDose,self.strongMagicDose)
        content += dose + "\n"
        carry = "carry"
        for i in self.carrySeedNum:
            carry += " " + str(i)
        content += carry + "\n"
        content += "money " + str(self.money) + "\n"
        achieve = "achieve " + str(self.achievementMoney.level) + "," + \
        str(self.achievementMoney.target)+ "," + str(self.achievementMoney.progress) + " "\
        + str(self.achievementVisit.level) + "," + \
        str(self.achievementVisit.target)+ "," + str(self.achievementVisit.progress) + " "\
        + str(self.achievementSell.level) + "," + \
        str(self.achievementSell.target)+ "," + str(self.achievementSell.progress) + " "\
        + str(self.achievementPlant.level) + "," + \
        str(self.achievementPlant.target)+ "," + str(self.achievementPlant.progress) + "\n"
        content += achieve
        plantPycoon.writeFile(path,content)
        
    def readProgress(self,path):
        progress = plantPycoon.readFile(path)
        for command in progress.split("\n"):
            if command.startswith("pot"):
                potStatus = command.split(" ")[1:]
                for i in range(15):
                    if potStatus[i] != "0":
                        self.seed[i] = True
                    else:
                        self.seed[i] = False
            elif command.startswith("water "):
                water = command.split(" ")[1:]
                for i in range(15):
                    self.water[i] = int(water[i])
            elif command.startswith("health"):
                health = command.split(" ")[1:]
                for i in range(15):
                    self.health[i] = int(health[i])
            elif command.startswith("plantstage"):
                plantStage = command.split(" ")[1:]
                for i in range(15):
                    self.plantStage[i] = int(plantStage[i])
            elif command.startswith("waterbucket"):
                self.waterbucketLevel = int(command[-1])
                self.waterbucketImage = pygame.image.load("images/tools/waterbucket%d.png"\
                                        %self.waterbucketLevel)
            elif command.startswith("age"):
                Ages = command.split(" ")[1:]
                for i in range(15):
                    self.plantAge[i] = int(Ages[i])
            elif command.startswith("box"):
                self.seedboxLevel = int(command[-1])
                for level in range(2,self.seedboxLevel+1):
                    seedx,seedy = self.addSeedboxPos[level-2]
                    dseedx,dseedy = 53,36
                    for i in range(10):
                        for j in range(4):
                            self.seedBoxPos.append((seedx+i*dseedx,seedy+j*dseedy))
            elif command.startswith("soil"):
                self.soilLevel = int(command[-1])
            elif command.startswith("seed"):
                seeds = command.split(" ")[1:]
                for i in range(120):
                    self.seedBox[i] = int(seeds[i])
            elif command.startswith("mini"):
                mini = command.split(" ")[1:]
                for i in range(8):
                    self.miniSeedbox[i] = int(mini[i])
            elif command.startswith("type"):
                type = command.split(" ")[1:]
                for i in range(15):
                    self.plantType[i] = int(type[i])
            elif command.startswith("dose"):
                Dose = command.split(" ")[1:]
                self.pesticideDose = int(Dose[0])
                self.magicDose = int(Dose[1])
                self.strongMagicDose = int(Dose[2])
            elif command.startswith("carry"):
                Carry = command.split(" ")[1:]
                for i in range(15):
                    self.carrySeedNum[i] = int(Carry[i])
            elif command.startswith("money"):
                self.money = int(command.split(" ")[-1])
            elif command.startswith("achieve"):
                lst = [self.achievementMoney,self.achievementVisit,
                self.achievementSell,self.achievementPlant]
                achieve = command.split(" ")[1:]
                for i in range(len(achieve)):
                    level = achieve[i].split(",")[0]
                    target,progress = achieve[i].split(",")[1],achieve[i].split(",")[1]
                    if i == 0:
                        self.achievementMoney = Achievement("money",int(target),int(level))
                        self.achievementMoney.gain(int(progress))
                    elif i == 1:
                        self.achievementVisit = Achievement("visit",int(target),int(level))
                        self.achievementVisit.gain(int(progress))
                    elif i == 2:
                        self.achievementSell = Achievement("sell",int(target),int(level))
                        self.achievementSell.gain(int(progress))
                    elif i == 3:
                        self.achievementPlant = Achievement("plant",int(target),int(level))
                        self.achievementPlant.gain(int(progress))
                
    
    def drawGrid(self,screen):
        for i in range(8):
            pygame.draw.line(screen,(0,0,0),(i*100,0),(i*100,self.height))
        for j in range(6):
            pygame.draw.line(screen,(0,0,0),(0,j*100),(self.width,j*100))
    def drawPot(self,screen):
        for i in range(len(self.potPos)):
            pos = self.potPos[i]
            x,y = pos
            if i == self.focusedPlant:
                screen.blit(self.focusedPlantImage,(x-15,y+25))
            screen.blit(self.potImage,(x,y))
    def drawSoil(self,screen):
        soilImage = pygame.image.load("images/soil/soil1.png")
        soilImageSeed = pygame.image.load("images/soil/soil1_seed.png")
        for i in range(15):
            x,y = self.potPos[i]
            d = 3
            if self.seed[i] == False:
                screen.blit(soilImage,(x+d,y+d))
            else:
                screen.blit(soilImageSeed,(x+d,y+d))
    def drawButtons(self,screen):
        buttonImage = pygame.image.load("images/buttons/main.png")
        currButtonImage = pygame.image.load("images/buttons/main1.png")
        buttonName = ["Main","Seedbox","Store","Visit","Back"]
        for i in range(5):
            pos = self.buttonPos[i]
            if self.mainButtons[i] == True:
                screen.blit(currButtonImage,pos)
            else:
                screen.blit(buttonImage, pos)
        Main = self.font.render("Main", True, (193,205,205))
        Seeds = self.font.render("Seeds",True,(193,205,205))
        Store = self.font.render("Store",True,(193,205,205))
        Visit = self.font.render("Visit",True,(193,205,205))
        Back = self.font.render("Back",True,(193,205,205))
        screen.blit(Main,(275,550))
        screen.blit(Seeds,(370,550))
        screen.blit(Store,(470,550))
        screen.blit(Visit,(575,550))
        screen.blit(Back,(678,550))
    def drawTrashbin(self,screen):
        x,y = 130,520
        screen.blit(self.trashbinImage,(x,y))
    def drawToolbox(self,screen):
        plantPycoon.drawWaterbucket(self,screen)
        plantPycoon.drawPesticide(self,screen)
        plantPycoon.drawMagic(self,screen)
        plantPycoon.drawStrongmagic(self,screen)
    def drawPesticide(self,screen):
        x,y = 80,135
        if self.mouse != "pesticide":
            screen.blit(self.pesticideImage,(x,y))
    def drawMagic(self,screen):
        x,y = 30,180
        if self.mouse != "magic":
            screen.blit(self.magicImage,(x,y))
    def drawStrongmagic(self,screen):
        x,y = 80,180
        if self.mouse != "strongmagic":
            screen.blit(self.strongMagicImage,(x,y))
    def drawWaterbucket(self,screen):
        x,y = 30,140
        if self.mouse != "waterbucket":
            screen.blit(self.waterbucketImage,(x,y))
    def drawWater(self,screen):
        if self.focusedPlant >= 0:
            waterAmount = self.water[self.focusedPlant]
            if waterAmount > 0:
                pygame.draw.rect(screen,(135,206,250),(13,440-waterAmount,14,waterAmount))
    def drawHealth(self,screen):
        color = (60,179,113)
        if self.focusedPlant >= 0:
            health = self.health[self.focusedPlant]
            if health > 0:
                pygame.draw.rect(screen,color,(200,440-health,14,health))
    def drawMouse(self,screen):
        if self.mouse != None:
            if self.mouse == "waterbucket":
                screen.blit(self.waterbucketImage,(self.mousex-20,self.mousey-20))
            elif self.mouse.startswith("seed") and self.currSeed != None:
                i = int(self.mouse[-1])
                screen.blit(self.currSeed,(self.mousex-20,self.mousey-20))
            elif self.mouse == "pesticide":
                screen.blit(self.pesticideImage,(self.mousex-20,self.mousey-20))
            elif self.mouse == "magic":
                screen.blit(self.magicImage,(self.mousex-20,self.mousey-20))
            elif self.mouse == "strongmagic":
                screen.blit(self.strongMagicImage,(self.mousex-20,self.mousey-20))
    def drawSeeds(self,screen):
        for i in range(8):
            if self.miniSeedbox[i] != -1:
                x,y = self.miniSeedboxPos[i]
                screen.blit(self.seedList[self.miniSeedbox[i]],(x,y))
        if self.currScreen == "seedbox":
            for j in range(120):
                if self.seedBox[j] != -1:
                    x,y = self.seedBoxPos[j]
                    screen.blit(self.seedList[self.seedBox[j]],(x,y))
    def drawBug(self,screen):
        for i in range(15):
            if self.seed[i] == True and self.health[i] < 60 :
                x,y = self.potPos[i]
                screen.blit(self.bug,(x-10,y-55))
                
    def drawFlower(self,screen):
        for i in range(15):
            if self.seed[i] and self.plantStage[i] > 0 and self.plantType[i] >= 0:
                x,y = self.potPos[i]
                flower = pygame.image.load("images/leaves/leaf_%d%d.png"%\
                                    (self.plantType[i]+1,self.plantStage[i]))
                screen.blit(flower,(x-10,y-60))
    def drawAge(self,screen):
        x,y = 30,460
        if self.currScreen == "main" and self.focusedPlant >= 0:
            if self.seed[self.focusedPlant] and self.plantAge[self.focusedPlant] >= 0:
                age = self.font.render(str(self.plantAge[self.focusedPlant]),True,(0,0,0))
                screen.blit(age,(x,y))
            
    def drawStore(self,screen):
        
        for i in range(3):
            water = pygame.image.load("images/tools/waterbucket"+str(i+1)+".png")
            soil = pygame.image.load("images/tools/soil"+ str(i+1) +".png")
            seedbox = pygame.image.load("images/tools/seedbox.png")
            screen.blit(water,(270,60+i*65))
            screen.blit(soil,(350,50+i*65))
            screen.blit(seedbox,(450,55+i*65))
            if i < self.waterbucketLevel:
                screen.blit(self.checkmark,(270,60+i*65))
            if i < self.soilLevel:
                screen.blit(self.checkmark,(370,60+i*65))
            if i < self.seedboxLevel:
                screen.blit(self.checkmark,(470,65+i*65))
            if i > 0:
                screen.blit(self.font.render(str(500*i),True,(255,255,255)),(200,60 +i*65))
        screen.blit(self.pesticideImage,(350,300))
        screen.blit(self.font.render(str(100),True,(255,255,255)),(320,300))
        screen.blit(self.magicImage,(350,365))
        screen.blit(self.font.render(str(250),True,(255,255,255)),(320,365))
        screen.blit(self.strongMagicImage,(350,425))
        screen.blit(self.font.render(str(1500),True,(255,255,255)),(320,425))
        screen.blit(self.font.render(str(50),True,(255,255,255)),(600,60))
        for i in range(len(self.storeSeed)):
            screen.blit(self.seedList[self.storeSeed[i]],self.storeSeedPos[i])
            
        
    def drawCarrySeed(self,screen):
        pos = (124,340)
        if self.focusedPlant >= 0 and self.carrySeedNum[self.focusedPlant] >= 0:
            screen.blit(self.seedList[self.plantType[self.focusedPlant]],pos)
            num = self.font.render(str(self.carrySeedNum[self.focusedPlant]),True,(0,0,0))
            screen.blit(num,pos)
    def drawLeftDose(self,screen,x,y):
        if self.leftdose != None:
            if self.leftdose == "pesticide":
                 s = self.font.render("Left dose:%d" %self.pesticideDose,True,(0,0,0))
            pygame.draw.rect(screen,(255,255,255),(x,y,70,40))
            screen.blit(s,(x+7,y+4))
    
    def sortAchievements(self):
        achievements = [self.achievementMoney,self.achievementPlant,
                        self.achievementSell,self.achievementVisit]
        p1 = self.achievementMoney.ratio()
        p2 = self.achievementPlant.ratio()
        p3 = self.achievementSell.ratio()
        p4 = self.achievementVisit.ratio()
        lst = [p1,p2,p3,p4]
        lst.sort()
        result = [None,None,None,None]
        for i in range(4):
            if lst[i] == p1 and achievements[0] not in result:
                result[i] = achievements[0]
            elif lst[i] == p2 and achievements[1] not in result:
                result[i] = achievements[1]
            elif lst[i] == p3 and achievements[2] not in result:
                result[i] = achievements[2]
            else:
                result[i] = achievements[3]
        return result
        
    def drawAchievements(self,screen):
        achievementList = plantPycoon.sortAchievements(self)
        color = (255,255,255)
        for i in range(4):
            x,y = self.achievementPos[i]
            name = self.font.render(str(achievementList[i]),True,(0,0,0))
            pygame.draw.rect(screen,color,(x,y,600,50))
            screen.blit(name,(x+2,y+3))
            
    def sellPlant(self,num):
        self.money += self.plantPrice[num]
        self.achievementSell.gain(1)
        self.achievementMoney.gain(self.plantPrice[num])
        self.seed[num] = False
        self.plantType[num] = -1
        self.plantStage[num] = -1
        self.plantAge[num] = -1
        self.plantPrice[num] = -1
                            
    def redrawAll(self,screen):
        if self.currScreen == "menu":
            screen.blit(self.menuBg,(0,0))
            screen.blit(self.playButtonImage,self.playButtonPos)
            screen.blit(self.continueButtonImage,self.continueButtonPos)
            screen.blit(self.helpButtonImage,self.helpButtonPos)
            screen.blit(self.saveButtonImage,self.saveButtonPos)
            screen.blit(self.achievementButtonImage,self.achievementButtonPos)
            New = self.font.render("New", True, (100, 0, 100))
            screen.blit(New,(240,201))
            Continue = self.font.render("Continue",True,(100,0,100))
            screen.blit(Continue, (165,351))
            Help = self.font.render("Help",True,(100,0,100))
            screen.blit(Help,(235,501))
            Save = self.font.render("Save",True,(100,0,100))
            screen.blit(Save,(530,401))
            Achieve = self.font.render("Badges",True,(100,0,100))
            screen.blit(Achieve,(620,301))
            if self.saved:
                Success = self.font.render("Game saved successfully!",True,(255,0,0))
                screen.blit(Success,(500,430))
        elif self.currScreen == "help":
            screen.blit(self.help[self.helpIndex],(0,0))
        elif self.currScreen == "enter":
            screen.blit(self.enterBg,(0,0))
            pygame.draw.rect(screen,(255,255,255),self.enterPos)
            Name = self.font.render(self.name,True,(0,0,0))
            x,y = self.enterPos[0], self.enterPos[1]
            screen.blit(Name,(x+10,y))
            Enter = self.font.render("Enter name here:",True,(255,255,255))
            screen.blit(Enter,(x,y-35))
            if self.repeat:
                Repeat = self.font.render("Username has been taken!", True,(255,0,0))
                screen.blit(Repeat,(x-40,y+35))
            screen.blit(self.backButtonImage, self.backButtonPos)
            Back = self.font.render("Back",True, (100,0,100))
            screen.blit(Back,(635,500))
            
        elif self.currScreen == "continue":
            screen.blit(self.menuBg,(0,0))
            localUsernames = plantPycoon.readFile("userData/localUsername.txt").strip()
            for i in range(len(localUsernames.split("\n"))):
                name = localUsernames.split("\n")[i]
                Name = self.font.render(name,True,self.nameColor[i])
                screen.blit(Name,self.namePos[i])
            screen.blit(self.backButtonImage, self.backButtonPos)
            Back = self.font.render("Back",True, (100,0,100))
            screen.blit(Back,(635,500))
        elif self.currScreen == "achievements":
            screen.blit(self.menuBg,(0,0))
            plantPycoon.drawAchievements(self,screen)
            screen.blit(self.backButtonImage, self.backButtonPos)
            Back = self.font.render("Back",True, (100,0,100))
            screen.blit(Back,(635,500))
            
        elif self.currScreen == "main":
            screen.blit(self.mainBg,(0,0))
            plantPycoon.drawPot(self,screen)
            plantPycoon.drawSoil(self,screen)
            plantPycoon.drawButtons(self,screen)
            plantPycoon.drawTrashbin(self,screen)
            plantPycoon.drawToolbox(self,screen)
            plantPycoon.drawLeftDose(self,screen,self.mousex,self.mousey)
            screen.blit(self.sellButtonImage,self.sellButtonPos)
            screen.blit(self.sellAllButtonImage,self.sellAllButtonPos)
            sell = self.font.render("Sell", True,(255,255,255))
            x,y = self.sellButtonPos
            screen.blit(sell,(x+13,y+3))
            sellAll = self.font.render("Sell all",True,(255,255,255))
            x,y = self.sellAllButtonPos
            screen.blit(sellAll,(x,y+3))
            plantPycoon.drawSeeds(self,screen)
            plantPycoon.drawFlower(self,screen)
            Money = self.font.render(str(self.money),True,(0,0,0))
            screen.blit(Money, self.moneyPos)
            plantPycoon.drawWater(self,screen)
            plantPycoon.drawHealth(self,screen)
            plantPycoon.drawAge(self,screen)
            plantPycoon.drawBug(self,screen)
            screen.blit(self.hoseImage,(0,0))
        elif self.currScreen == "seedbox":
            screen.blit(self.SeedboxBg,(0,0))
            plantPycoon.drawButtons(self,screen)
            plantPycoon.drawTrashbin(self,screen)
            if self.seedboxLevel > 1:
                if self.seedboxLevel >= 2:
                    screen.blit(self.additionalSeedboxImage,self.addSeedboxPos[0])
                if self.seedboxLevel == 3:
                    screen.blit(self.additionalSeedboxImage,self.addSeedboxPos[1])
            plantPycoon.drawToolbox(self,screen)
            plantPycoon.drawSeeds(self,screen)
        elif self.currScreen == "store":
            screen.blit(self.StoreBg,(0,0))
            plantPycoon.drawButtons(self,screen)
            plantPycoon.drawToolbox(self,screen)
            plantPycoon.drawSeeds(self,screen)
            plantPycoon.drawStore(self,screen)
            Money = self.font.render(str(self.money),True,(0,0,0))
            screen.blit(Money, self.moneyPos)
        elif self.currScreen == "visit":
            screen.blit(self.VisitBg,(0,0))
            plantPycoon.drawPot(self,screen)
            plantPycoon.drawSoil(self,screen)
            plantPycoon.drawButtons(self,screen)
            plantPycoon.drawTrashbin(self,screen)
            plantPycoon.drawToolbox(self,screen)
            plantPycoon.drawSeeds(self,screen)
            plantPycoon.drawFlower(self,screen)
            Visit = self.font.render("Visiting...", True,(255,255,255))
            screen.blit(Visit,(400,0))
            Money = self.font.render(str(self.money),True,(0,0,0))
            screen.blit(Money, self.moneyPos)
            plantPycoon.drawWater(self,screen)
            plantPycoon.drawHealth(self,screen)
            plantPycoon.drawAge(self,screen)
            screen.blit(self.hoseImage,(0,0))
        if self.beingVisited:
            Word = self.font.render("Someone is watching you...",True,(255,255,255))
            screen.blit(Word,(400,0))
            
        plantPycoon.drawMouse(self,screen)
        
        
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

def main():
    game = plantPycoon()
    game.run(serverMsg,server)
    

if __name__ == '__main__':
    main()