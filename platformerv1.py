from cmu_graphics import *
from PIL import Image 
import random 
import math
#Creates the comet class 
class comet():
    def __init__(self,num,plat_list):
        self.num = num 
        #Sets the position to above the start of the app, middle of the assigned platform and drops the comet
        self.x = int((plat_list[self.num].x +plat_list[self.num].x+ plat_list[self.num].width)/2)
        self.y = -10
        self.image = 'rock2.png'
        self.fall = False
        self.exploding = False
        self.ticker = 0
        self.show = True 
        self.lost = False 
    def step(self,plat_list,curr_plat,appHeight):
        if self.num == curr_plat and self.exploding == False:
            self.fall = True
        if self.fall:
            self.drop(appHeight,plat_list,curr_plat)
                 
    def drop(self,appHeight,plat_list,curr_plat):
        if not self.exploding:
            self.dy = appHeight*(1/200)
            self.y += self.dy
        if self.y >= plat_list[self.num].y-(10):
            self.exploding = True
            self.explode(curr_plat)
    def explode(self,curr_plat):
        #change images
        self.show = False
        if curr_plat == self.num:
            #lose game when it explodes and player is on the platform with a comet
            self.lost = True 
    #moves the comets alongside the rest of the things 
    def MoveLeft(self):
        self.x -= 3
        
    def MoveRight(self):
        self.x += 3


#my bootleg solution to scaling eveything to different app sizes 
#It is incomplete, so currently game only runs on 400x400
class Scaleable():
    def __init__(self,appWidth,appHeight): 
        self.appWidth = appWidth
        self.appHeight=appHeight
    def scale(self,appWidth,appHeight):
        self.appWidth = appWidth
        self.appHeight = appHeight

class Player(Scaleable):
    def __init__(self,x,y,width,height):
        super().__init__(width,height)
        self.image = "Punk_idle.png"
        self.animation_count = 0 
        self.Iwidth, self.Iheight = getImageSize(self.image)
        self.x=x
        self.y= width/2-self.Iheight
        self.dx = (self.appWidth*3)/400
        self.dy = (self.appWidth*3)/400
        self.curr_plat = 0  
       
    #moving player right 
    def moveRight(self,width,plat_list,moveable):
        if self.animation_count<= 4:
            self.animation_count += 0.3
        else:
            self.animation_count = 1
        self.image = f'player_run{int(self.animation_count)+2}.png'
        

        if self.x <= width and moveable:
            self.x+=self.dx
        #changes the next platform once x line breached to know which collision to check for
        if self.x > plat_list[self.curr_plat].x+plat_list[self.curr_plat].width:
            self.curr_plat += 1
            print(self.curr_plat)
        
         
            
    #moving the player left 
    def moveLeft(self,plat_list,moveable):
        if self.animation_count<= 4:
            self.animation_count += 0.3
        else:
            self.animation_count = 1
        self.image = f'runLeft-{int(self.animation_count)+2}.png'
        
        if self.x >=0 and moveable:
            self.x -= self.dx 
            #changes to next platform once x line breached to know which collision to check for
        if self.x < plat_list[self.curr_plat].x:
            self.curr_plat -= 1
            
    def isCollidedX(self,xRange):
        if self.x in range(xRange[0],xRange[1]):
            return True

    def isCollidedY(self,yLine):
        if self.y ==yLine:
            return True  
      
            
    def isCollided(self,curr,plat_list):
        xRange = (plat_list[curr].x,plat_list[curr].x+plat_list[curr].width)
        yLine = plat_list[curr].y-10
        #currently checks for y in onStep, so this part has been left blank 
        if self.isCollidedY(yLine):
            pass
        if self.isCollidedX(xRange):
            return True 
        else:
            return False 
#jumping code
    def jump(self):
        self.y -= (self.appWidth*5)/400
    def fall(self):
        #makes player fall after a jump
        self.y += (self.appWidth*5)/400
    def gravity(self):
        #moves player down if not in contact with a platform
        self.y += (self.appWidth*5)/400
        
class Platform(Scaleable):
    
    #initializes the platforms
    def __init__(self,plat_list,width,height,level):
        super().__init__(width,height)
        self.width = random.randint((self.appWidth*20/400),(self.appWidth*100/400))
        self.height = random.randint(self.appHeight*20/400,self.appHeight*50/400)
        if plat_list == []:
            self.x = 0 
            self.y = int(height/2)
        else:
            if level == 1:
                prior = plat_list[-1]
                
                self.x = random.randint(prior.x+prior.width+self.appWidth*30/400,prior.x+prior.width+self.appWidth*50/400)
                #Using the parabolic jump and the chosen x value, it gets an appropriate and solvabale y value 
                #The jump with maximum x distance can be modelled by the equation y=1/30*(x^2)-2x, so this must be the max y
                #This guarantees solvability 

                xDist = self.x-(prior.x+prior.width)
                increments_to_reach = xDist/3 #divides distance by steps per increment to get the increment
                if increments_to_reach < 10:
                    maxy = int(3*increments_to_reach)+prior.y
                elif increments_to_reach >= 10:
                    maxy = int(10-increments_to_reach)*3+prior.y
                #final check to rule out potential off by one for the range 
                if maxy <= prior.y:
                    maxy = prior.y
                
                #Also ensures that the platform doesn't go too high up or down low, adds a "margin"
                if prior.y >= self.appHeight*50/400 and prior.y <=height-self.appHeight*50/400:
                    #ydiv = random.randint(prior.y-self.appHeight*30/400,prior.y+self.appHeight*30/400)
                    ydiv = random.randint(prior.y-self.appHeight*30/400,maxy)
                    #generates a y divisible by 5 so that the collision algorithm will function properly
                    self.y = math.ceil(ydiv/5)*5
                elif prior.y >= height-(self.appHeight*50/400):
                    #ydiv = random.randint(prior.y-self.appHeight*30/400,prior.y)
                    ydiv = random.randint(prior.y-self.appHeight*30/400,prior.y)
                    self.y = math.ceil(ydiv/5)*5
                elif prior.y <=self.appWidth*50/400:
                    ydiv = random.randint(prior.y,maxy)
                    self.y = math.ceil(ydiv/5)*5
                

            
    def MoveLeft(self,num):
        self.x += num
        
    def MoveRight(self,num):
        self.x -= num
        
#generates platforms
def platGen(width,height,level):
    #keys to the dictionary 
    plat_list = []
    plat_dict = dict()
    for i in range(10):
        plat_list.append(Platform(plat_list,width,height,level))
    for i in plat_list:
        plat_dict[i] = (i.x,i.y,width,height)
    return (plat_list,plat_dict)

#generates comets
def cometGen(appWidth,appHeight,appLevel,plat_list):
    comet_list = []
    comet_list.append(comet(1,plat_list))

    s = set()
    seen = set()
    for i in range(9):
        pass #sets max
        #s.add(random.randint(1,9)) #picks some random number of comets w no duplicates 
    
    for i in range(1,8):
        comet_list.append(comet(i,plat_list))
        #print("comet:" , comet_list[-1].x)
    return comet_list


#CMU Graphics code

def onAppStart(app):
    app.motionInc = 3
    #app.player=Player(0,190,app.width,app.height)
    app.level = 1
    #app.plat_list,app.plat_dict = platGen(app.width,app.height,app.level)
    #app.comet_list = cometGen(app.width,app.height,app.level,app.plat_list)
    app.count = 0
    app.paused = False   
    app.moveR = False
    app.moveL = False  
    app.jump = False 
    app.fall = False
    app.onGround = True 
    app.startScreen = True
    app.moveable = True
    app.stepsPerSecond = 30
    app.won = False
    app.lost = False 
    app.movePlayer = True
    app.playing = False
    #scales the functions into working on different app sizes
    #This was added in relatively late  and does not work :(
    if app.width != 400:
        app.scale = 400/app.width 
        
    
#restarts a level when things go wrong and starts new ones 
def startLevel(width,height,level):
    pl,pd = platGen(width,height,level)
    return(pl,pd,Player(0,190))
def onMousePress(app, mouseX, mouseY):
    pass

def onKeyPress(app,key):
    if key == 'p':
        if app.startScreen:
            app.playing = True
            app.startScreen = False 
            app.player=Player(0,190,app.width,app.height)
            app.plat_list,app.plat_dict = platGen(app.width,app.height,app.level)
            app.comet_list = cometGen(app.width,app.height,app.level,app.plat_list)
    if key == 'space':
        #checks if player is on the ground before jumping
        if app.onGround and app.player.y+app.player.Iheight == app.plat_list[app.player.curr_plat].y:
            app.jump = True 
    if key == 'right'and app.moveable:
        app.moveR = True
    elif key == 'left' and app.moveable:
        app.moveL = True
def onKeyRelease(app,key):
    if key == 'right':
        app.moveR = False
    if key == 'left':
        app.moveL = False 
def redrawAll(app):
    if app.startScreen:
        drawRect(0,0,app.width,app.height,fill = 'black')
        drawLabel('ESCAPE FROM PLANET X',app.width/2,app.height/2, size = 12*app.width/400, font = 'arial', bold=True,fill='white')
        drawLabel('You have crash landed on a foreign planet. You must navigate to the rescue ship. ', app.width/2,3*app.height/5,size = 10*app.width/400, fill = 'white')
        drawLabel('If a falling rock lands on your platform, you will lose. Press p to play.', app.width/2,3*app.height/5+10*app.width/400,size = 10*app.width/400, fill = 'white')

    #draws game items when someone is playing 
    elif app.playing:
        for i in app.plat_dict:
            drawRect(i.x,i.y,i.width,i.height)
            
        for i in app.comet_list:
            if i.show:
                drawImage(i.image,i.x,i.y,width=10*app.width/400,height=10*app.width/400)
        drawImage(app.player.image,app.player.x,app.player.y)
    #Game over screen 
    elif app.lost:
        drawRect(0,0,app.width,app.height,fill = 'black')
        drawLabel('GAME OVER',app.width/2,app.height/2, size = 12*app.width/400, font = 'arial', bold=True,fill='white')
    #Winning Screen 
    elif app.won:
        drawRect(0,0,app.width,app.height,fill = 'black')
        drawLabel('You Won!',app.width/2,app.height/2, size = 12*app.width/400, font = 'arial', bold=True,fill='white')

def onStep(app):
    if app.won == False and app.lost == False and app.playing:
        print(app.width)
        app.player.scale(app.width,app.height)
        for i in app.plat_list:
            i.scale(app.width,app.height)
        for i in app.comet_list:
            i.step(app.plat_list,app.player.curr_plat, app.height)
            if i.lost:
                app.lost = True

        if app.moveR == True:
            if app.player.x >= int(app.width/2):
                app.movePlayer = False
            if (app.plat_list[-1].x+app.plat_list[-1].width <= app.width):
                app.movePlayer = True
            
            #passes through moveRight function but does not actually move the player when platforms move 
            #as collision check is called in this function 
            app.player.moveRight(app.width,app.plat_list,app.movePlayer)
            if app.plat_list[-1].x+app.plat_list[-1].width != app.width and not app.movePlayer:
                for i in app.plat_dict:
                    i.MoveRight(app.motionInc)
                for i in app.comet_list:
                    i.MoveLeft()
        if app.moveL == True:
            if app.player.x <= int(app.width/2):
                app.movePlayer = False
            if (app.plat_list[0].x>=0):
                app.movePlayer = True
           
            app.player.moveLeft(app.plat_list,app.movePlayer)
            if app.plat_list[0].x != 0 and not app.movePlayer:
                for i in app.plat_dict:
                    i.MoveLeft(app.motionInc)
                for i in app.comet_list:
                    i.MoveLeft()
        if app.jump == True and app.count<10:
            app.player.jump()
            app.count+=1
        if app.jump == True and app.count >= 10:
            app.player.jump()
            app.count = 0
            #app.fall = True
            app.jump = False 
        if app.fall == True and app.count <10:
            app.player.fall()
            app.count+=1
        if app.fall == True and app.count >= 10:
            app.player.fall()
            app.count = 0
            app.fall = False
        app.onGround = app.player.isCollided(app.player.curr_plat,app.plat_list)
        #falls when player is not on a platform 
        if app.jump == False: 
            if not app.onGround or app.player.y+app.player.Iheight != app.plat_list[app.player.curr_plat].y:
                app.moveable = False
                app.player.gravity()
            elif app.onGround and app.player.y+app.player.Iheight != app.plat_list[app.player.curr_plat].y:
                app.player.x -= 9         
                app.moveable = False
                app.player.gravity()
            else:
                app.moveable = True 
                if app.player.curr_plat == 9:
                    app.won = True 
                    app.playing = False
        #player loses if they fall off a platform 
        if app.player.y >350:
            app.lost = True
            app.playing = False
        
        else:
            app.moveable = True 
    
    
def main():
    runApp()

main()
    