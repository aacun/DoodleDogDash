import os
import pygame
from random import randint

_ = os.system("cls")
pygame.init()
pygame.mixer.init()

# screen
SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# moving background
background=pygame.image.load('assets/environment/grass.jpg').convert_alpha()
backgroundrect=background.get_rect(center=(600,400))

rightbound = SCREEN_WIDTH-100
leftbound = SCREEN_WIDTH-1100 
upbound= SCREEN_HEIGHT-700
downbound = SCREEN_HEIGHT-100

# title screen
titlescreen=pygame.transform.scale(pygame.image.load('assets/environment/gametitle.png'),(1200,800)).convert_alpha() 

# frame rate
clock = pygame.time.Clock()

# font
font=pygame.font.Font('assets/font/Pangolin-Regular.ttf',50)

# timers
timer=pygame.USEREVENT + 1
pygame.time.set_timer(timer,2400)
enemytimer=pygame.USEREVENT + 2
pygame.time.set_timer(enemytimer,3000)

# point
point1=pygame.transform.scale(pygame.image.load('assets/treat/treat1.png'),(100,100)).convert_alpha() 
point2=pygame.transform.scale(pygame.image.load('assets/treat/treat2.png'),(100,100)).convert_alpha() 
point3=pygame.transform.scale(pygame.image.load('assets/treat/treat3.png'),(100,100)).convert_alpha() 
pointanimate=[point1,point2,point3]
pointrectlist=[]  
pointindex=0

# sounds
coin=pygame.mixer.Sound('assets/sounds/coin.mp3')
attacked=pygame.mixer.Sound('assets/sounds/attacked.mp3')
pygame.mixer.music.load('assets/sounds/bgm.mp3')

def collision():
    global screenval
    if pygame.sprite.spritecollide(player.sprite,enemygroup,False):
        attacked.play()
        return 3
    return screenval
    
####### PLAYER SPRITE
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        right1=pygame.transform.scale(pygame.image.load('assets/dog/dogright1.png'),(125,125)).convert_alpha()  # right
        right2=pygame.transform.scale(pygame.image.load('assets/dog/dogright2.png'),(125,125)).convert_alpha() 
        right3=pygame.transform.scale(pygame.image.load('assets/dog/dogright3.png'),(125,125)).convert_alpha() 
        self.rightlist=[right1,right2,right3]
        
        left1 = pygame.transform.flip(right1,1,0)
        left2 = pygame.transform.flip(right2,1,0)
        left3 = pygame.transform.flip(right3,1,0)
        self.leftlist=[left1,left2,left3]

        down1=pygame.transform.scale(pygame.image.load('assets/dog/dogdown1.png'),(125,125)).convert_alpha() # down
        down2=pygame.transform.scale(pygame.image.load('assets/dog/dogdown2.png'),(125,125)).convert_alpha() 
        down3=pygame.transform.scale(pygame.image.load('assets/dog/dogdown3.png'),(125,125)).convert_alpha() 
        self.downlist=[down1,down2,down3]

        up1=pygame.transform.scale(pygame.image.load('assets/dog/dogup1.png'),(125,125)).convert_alpha() # down
        up2=pygame.transform.scale(pygame.image.load('assets/dog/dogup2.png'),(125,125)).convert_alpha() 
        up3=pygame.transform.scale(pygame.image.load('assets/dog/dogup3.png'),(125,125)).convert_alpha() 
        self.uplist=[up1,up2,up3]

        self.playerindex = 0 
        self.speed = 6
        self.currentdirection = self.rightlist
        self.image = self.currentdirection[int(self.playerindex)]
        self.rect = self.image.get_rect(center=(600,400))
        self.right = self.rect.right

####### GET POSITION DATA
    def get_position(self):
        return self.rect.right,self.rect.left,self.rect.top,self.rect.bottom

####### SCROLLING BACKGROUND
    def scrolling(self):
        keys=pygame.key.get_pressed()
        if self.rect.right >= rightbound and keys[pygame.K_RIGHT]: # RIGHT
            self.rect.right = rightbound
            backgroundrect.right -= 7
            for pointrect in pointrectlist: pointrect.x -=7
            for sprite in enemygroup.sprites(): sprite.rect.x -= enemyspeed
            if backgroundrect.right <= SCREEN_WIDTH: # at border
                backgroundrect.right = SCREEN_WIDTH
                for pointrect in pointrectlist: pointrect.x +=7 # offset points
                for sprite in enemygroup.sprites(): sprite.rect.x += enemyspeed # offset enemies

        if self.rect.bottom >= downbound and keys[pygame.K_DOWN]: # DOWN
            self.rect.bottom = downbound
            backgroundrect.bottom -= 7
            for pointrect in pointrectlist: pointrect.y -=7
            for sprite in enemygroup.sprites(): sprite.rect.y -= enemyspeed
            if backgroundrect.bottom <= SCREEN_HEIGHT:
                backgroundrect.bottom = SCREEN_HEIGHT
                for pointrect in pointrectlist: pointrect.y +=7
                for sprite in enemygroup.sprites(): sprite.rect.y += enemyspeed

        if self.rect.left <= leftbound and keys[pygame.K_LEFT]: # LEFT
            self.rect.left = leftbound
            backgroundrect.left += 7
            for pointrect in pointrectlist: pointrect.x +=7
            for sprite in enemygroup.sprites(): sprite.rect.x += enemyspeed

            if backgroundrect.left >= 0:
                backgroundrect.left = 0
                for pointrect in pointrectlist: pointrect.x -=7
                for sprite in enemygroup.sprites(): sprite.rect.x -= enemyspeed

        if self.rect.top <= upbound and keys[pygame.K_UP]: # UP
            self.rect.top = upbound
            backgroundrect.top += 7
            for pointrect in pointrectlist: pointrect.y +=7
            for sprite in enemygroup.sprites(): sprite.rect.y += enemyspeed

            if backgroundrect.top >= 0:
                backgroundrect.top = 0
                for pointrect in pointrectlist: pointrect.y -=7
                for sprite in enemygroup.sprites(): sprite.rect.y -= enemyspeed

####### KEY MOVEMENT
    def key_input(self):
        keys=pygame.key.get_pressed()

        if keys[pygame.K_UP]: # move up
            self.currentdirection = self.uplist
            self.rect.y -= self.speed
            self.image = self.currentdirection[int(self.playerindex)]

        if keys[pygame.K_DOWN]: # move down
            self.currentdirection = self.downlist
            self.rect.y += self.speed
            self.image = self.currentdirection[int(self.playerindex)]

        if keys[pygame.K_LEFT]: # move left
            self.currentdirection = self.leftlist
            self.rect.x -= self.speed
            self.image = self.currentdirection[int(self.playerindex)]

        if keys[pygame.K_RIGHT]: # move right
            self.currentdirection = self.rightlist
            self.rect.x += self.speed
            self.image = self.currentdirection[int(self.playerindex)]

####### PLAYER ANIMATION
    def animation(self):
            self.playerindex += 0.15
            if self.playerindex >= len(self.currentdirection): self.playerindex = 0   

####### POINTS COLLISION
    def pointcollision(self,pointrectlist,coin):
        global score
        for pointrect in pointrectlist:
            if self.rect.colliderect(pointrect):
                coin.play()
                score+=1
                pointrectlist.remove(pointrect)

####### RESET LOCATION           
    def reset_location(self):
        self.playerindex = 0
        self.image = self.currentdirection[int(self.playerindex)]
        self.rect = self.image.get_rect(center=(600,400))

####### PLAYER UPDATE
    def update(self):
        # add all functions
        self.key_input()
        self.animation()
        self.get_position()
        self.scrolling()
        self.pointcollision(pointrectlist,coin)
##############################################################
##############################################################
##############################################################



enemyleft1=pygame.transform.scale(pygame.image.load('assets/enemy/enemyright1.png'),(125,125)).convert_alpha()
enemyleft2=pygame.transform.scale(pygame.image.load('assets/enemy/enemyright2.png'),(125,125)).convert_alpha()
enemyleft3=pygame.transform.scale(pygame.image.load('assets/enemy/enemyright3.png'),(125,125)).convert_alpha()

enemyright1 = pygame.transform.flip(enemyleft1,1,0)
enemyright2 = pygame.transform.flip(enemyleft2,1,0)
enemyright3 = pygame.transform.flip(enemyleft3,1,0)

enemydown1=pygame.transform.scale(pygame.image.load('assets/enemy/enemydown1.png'),(125,125)).convert_alpha()
enemydown2=pygame.transform.scale(pygame.image.load('assets/enemy/enemydown2.png'),(125,125)).convert_alpha()
enemydown3=pygame.transform.scale(pygame.image.load('assets/enemy/enemydown3.png'),(125,125)).convert_alpha()

enemyup1=pygame.transform.scale(pygame.image.load('assets/enemy/enemyup1.png'),(125,125)).convert_alpha()
enemyup2=pygame.transform.scale(pygame.image.load('assets/enemy/enemyup2.png'),(125,125)).convert_alpha()
enemyup3=pygame.transform.scale(pygame.image.load('assets/enemy/enemyup3.png'),(125,125)).convert_alpha()


####### ENEMY SPRITE
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'enemy1':
            self.right = [enemyleft1,enemyleft2,enemyleft3]
            self.left = [enemyright1,enemyright2,enemyright3]
            self.down = [enemydown1,enemydown2,enemydown3]
            self.up = [enemyup1,enemyup2,enemyup3]

        self.currentdirection = self.right
        self.index = 0
        self.image = self.currentdirection[self.index]
        self.rect = self.image.get_rect()
        self.rectlist = []
        self.rect = self.image.get_rect(center = (enemyx,enemyy))
        self.rectlist.append(self.rect)
        print(self.rectlist)

####### ENEMY ANIMATION
    def enemyanimation(self):
        self.index += 0.07
        if self.index >= len(self.currentdirection): self.index = 0
        self.image = self.currentdirection[int(self.index)]

####### CLEAR ENEMY LIST
    def clear_enemies(self):
        enemygroup.empty()

####### ENEMY UPDATE
    def update(self):
        self.enemyanimation()
        if location == 1: # bottom
            self.currentdirection = self.up
            self.rect.y -= enemyspeed
        elif location == 2: # top
            self.currentdirection = self.down
            self.rect.y += enemyspeed
        elif location == 3: # start left, going right
            self.rect.x += enemyspeed
            self.currentdirection = self.right
        elif location == 4: # start right, going left
            self.rect.x -= enemyspeed
            self.currentdirection = self.left

        if (self.rect.y < -80 or self.rect.y > SCREEN_HEIGHT + 80 or
            self.rect.x < -80 or self.rect.x > SCREEN_WIDTH + 80 or 
            len(self.rectlist) > 1):
            self.kill()

player=pygame.sprite.GroupSingle(Player())
enemygroup=pygame.sprite.Group()

# score calculations
score=0

yourscoresurf=pygame.transform.scale_by(pygame.image.load('assets/environment/scoreboard.png'),0.1).convert_alpha() 
def scoreboard():
    yourscorerect=yourscoresurf.get_rect(center=(550,100))
    screen.blit(yourscoresurf,yourscorerect)
    scoresurf=font.render(str(score), False, (0,0,0))
    scorerect=yourscoresurf.get_rect(center=(810,140))
    screen.blit(scoresurf,scorerect)

# different screens
screenval=1

run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

        if event.type==timer:
            if backgroundrect.right == SCREEN_WIDTH or backgroundrect.left == 0 \
            or backgroundrect.bottom == SCREEN_HEIGHT or backgroundrect.top == 0:
                x = randint(100,1100)
                y = randint(100,700)
                pointrect=pygame.Rect(x,y,96,96)
                pointrectlist.append(pointrect)
            else:
                x=randint(0,1200)
                y=randint(0,800)
                pointrect=pygame.Rect(x,y,96,96)
                pointrectlist.append(pointrect)

            if len(pointrectlist) >= 5:
                del pointrectlist[0]
            
        if event.type==enemytimer:
            global location, enemyx, enemyy
            if len(enemygroup) == 0: # ensure only one enemy at a time
                location = randint(1,4)
                enemyspeed = randint(6,10)

                # LOCATION 
                if location == 1: # bottom
                    enemyx = randint(100,1100)
                    enemyy = SCREEN_HEIGHT + 50
                elif location == 2: # top
                    enemyx = randint(100,1100)
                    enemyy = 0
                elif location == 3: # left
                    enemyx = 0
                    enemyy = randint(100,700)
                elif location == 4: # right
                    enemyx = SCREEN_WIDTH + 50
                    enemyy = randint(100,700)
            
                print('x: ' + str(enemyx) + ', y: ' + str(enemyy))
                enemygroup.add(Enemy('enemy1'))
                enemygroup.update()
            else:
                print('enemy still on screen')

    pressed = pygame.key.get_pressed()
    if screenval==1:
        score=0
        titlerect=titlescreen.get_rect(center=(600,400))
        screen.blit(titlescreen,titlerect)

        if pressed[pygame.K_SPACE]:
            pointrectlist.clear()
            Enemy.clear_enemies(enemygroup)
            screenval=2
            
    elif screenval==2:
        screen.blit(background,backgroundrect)
        
        screenval = collision()

        rightloc,leftloc,toploc,bottomloc = player.sprite.get_position()
        player.draw(screen)
        player.update()

        enemygroup.draw(screen)
        enemygroup.update()

        pointindex+=0.03
        if pointindex >= len(pointanimate):
            pointindex=0
        for pointrect in pointrectlist:
            screen.blit(pointanimate[int(pointindex)],pointrect)

        scoreboard()
    elif screenval==3:
        # clear all lists/scores  
        pointrectlist.clear()
        Enemy.clear_enemies(enemygroup)

        # reset player location
        Player.reset_location(player.sprite)
        
            
        # game over message
        screen.fill((25,10,50))
        score_message=font.render('Your Score: ' + str(score), False, (111,196,169))
        score_message_rect=score_message.get_rect(center=(600,100))

        gameover=font.render('GAME OVER! Press Space to Restart', False, (111,196,169))
        gameoverrect=gameover.get_rect(center=(600,500))
        screen.blit(score_message,score_message_rect)
        screen.blit(gameover,gameoverrect)

        pressM=font.render('Press M to go to Main Menu', False, (111,196,169))
        pressMrect=pressM.get_rect(center=(600,600))
        pressQ=font.render('Press Q to quit', False, (111,196,169))
        pressQrect=pressQ.get_rect(center=(600,700))
        screen.blit(pressM,pressMrect)
        screen.blit(pressQ,pressQrect)
   
        if pressed[pygame.K_SPACE]: 
            screenval=2
            score=0
        if pressed[pygame.K_m]: screenval=1
        if pressed[pygame.K_q]: run=False
    
    pygame.display.update()  # screen update, 60fps
    clock.tick(60)

pygame.quit()