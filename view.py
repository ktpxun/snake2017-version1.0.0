import Leap, sys, pygame, math, time
from model import *
from player import *

SCREEN_SIZE = (1000, 600)
ready = True

###############################################################################

class View:
  
  checkHand = True

  def __init__(self, screen):
    self.screen = screen
  
  def isGrab(self, hand):
      if(hand.grab_strength == 1):
        return True
      else:
        return False  
      
###############################################################################
      
class SpashScreen(View):

  def __init__(self, screen, ssnake):
    self.screen = screen
    self.ssnake = ssnake
    self.index = 1
    self.checkHand = False
    self.sbgm = pygame.mixer.Sound("resources/sound/win98.ogg")   #http://www.winhistory.de/more/winstart/winstart.htm.en
    self.background = pygame.image.load("resources/intro/black.png").convert()   
    self.csBG = pygame.image.load("resources/intro/cs.png").convert() 
    self.alpha = 255    
    self.clock = pygame.time.Clock()
    self.looper = 0
    self.loadBG()
    self.sbgm.play(-1)

  def processInput(self, frame):
    return

  def update(self, frame):


    if(self.index >= 8):
      self.index = 1
      if(self.alpha <= 0):
        self.looper += 1
      if(self.looper == 3):
        self.goToMenuScreen()
    else:
      self.index  += 1

    if(self.alpha >= 0):
      self.clock.tick(30)
      self.alpha -= 3
    else:
      self.clock.tick(3)
      self.csBG = self.panels[self.index-1]
    self.background.set_alpha(self.alpha)

  def render(self):
    self.screen.blit(self.csBG, [0, 0])
    self.screen.blit(self.background, [0, 0])

  def loadBG(self):
    self.panels = []
    for x in range(1,9):
      panel = pygame.image.load("resources/intro/" + str(x) + ".png").convert()
      self.panels.append(panel)

  def goToMenuScreen(self):
    self.sbgm.stop()
    self.ssnake.goToMenuScreen()


###############################################################################
    
    
class MenuScreen(View):

  def __init__(self, screen, ssnake):
    self.screen = screen
    self.ssnake = ssnake
    self.background = pygame.image.load("resources/menu/menu.png").convert()
    self.bgm = pygame.mixer.Sound("resources/sound/menuBGM.wav") #https://freesound.org/people/xsgianni/sounds/388079/
    self.click = pygame.mixer.Sound("resources/sound/click.wav")   
    self.addButtons()
    self.cursor = Cursor()
    self.bgm.play(-1)

  def addButtons(self):
    self.buttons = []
    self.play = PlayButton(150, 450,self.ssnake)
    self.howTo = HowToButton(385, 450, self.ssnake)
    self.credit = CreditButton(623, 450, self.ssnake)
    self.exit = ExitButton(835, 450, self.ssnake)
    self.buttons.append(self.play)
    self.buttons.append(self.howTo)
    self.buttons.append(self.credit)
    self.buttons.append(self.exit)
      
 
  def processInput(self, frame):
    self.hand = frame.hands[0]

  def update(self, frame):
    global ready
    
    interactionBox = frame.interaction_box
    position = interactionBox.normalize_point(self.hand.palm_position)
    x = position.x * SCREEN_SIZE[0]      
    y = SCREEN_SIZE[1] - (position.y * SCREEN_SIZE[1])
    
    
    self.cursor.setPos(x, y)
    if ready == False:
      if self.isGrab(self.hand) == False:
        ready = True
    else:
      for button in self.buttons:
        if button.isMouseOver(self.cursor):
          if self.isGrab(self.hand):
            self.click.play()
            self.bgm.stop()
            ready = False
            button.goToNextState()
            
          break
      


  def render(self):
    self.screen.blit(self.background, [0, 0])
    for button in self.buttons:
      self.screen.blit(button.image, button.rect)
    self.screen.blit(self.cursor.image, self.cursor.rect)
    pass
  
###############################################################################
  
  
class CreditScreen(View):
  def __init__(self, screen, ssnake):
    self.screen = screen
    self.ssnake = ssnake
    self.background = pygame.image.load("resources/credit/credit.png")
    self.background = pygame.transform.scale(self.background, (1000, 600))
    self.bgm = pygame.mixer.Sound("resources/sound/default bg.wav")
    self.click = pygame.mixer.Sound("resources/sound/click.wav")
    self.back = BackButton(100, 513, self.ssnake)
    self.cursor = Cursor()
    self.bgm.play(-1)

  def processInput(self, frame):
    self.hand = frame.hands[0]

  def update(self, frame):
    global ready
    interactionBox = frame.interaction_box
    position = interactionBox.normalize_point(self.hand.palm_position)
    x = position.x * SCREEN_SIZE[0]      
    y = SCREEN_SIZE[1] - (position.y * SCREEN_SIZE[1])
    
    self.cursor.setPos(x, y)
    
    if self.back.isMouseOver(self.cursor):
      if self.isGrab(self.hand):
        self.click.play()
        self.bgm.stop()
        self.back.goToNextState()
        ready = False


  def render(self):
    self.screen.blit(self.background, [0, 0])
    self.screen.blit(self.back.image, self.back.rect)
    self.screen.blit(self.cursor.image, self.cursor.rect)

###############################################################################
    
class PauseScreen(View):

  def __init__(self, screen, ssnake, previousState):
    self.screen = screen
    self.ssnake = ssnake
    self.checkHand = False
    self.previousState = previousState
    self.index = 0
    self.clock = pygame.time.Clock()
    self.loadBG()
    

  def processInput(self, frame):
    self.hands = frame.hands


  def update(self, frame):
    self.index += 1
    if(self.index >  8):
      self.index = 1


  def render(self):
    self.previousState.render()
    self.clock.tick(5)
    self.screen.blit(self.panels[self.index-1], [250, 150])

  def loadBG(self):
    self.panels = []
    for x in range(1,9):
      panel = pygame.image.load("resources/pause/pause" + str(x) + ".png")
      self.panels.append(panel)
      
###############################################################################      
      
class GameScreen(View):

  def __init__(self, screen, ssnake):
    self.screen = screen
    self.ssnake = ssnake
    

  def reset(self):
    self.speed = 1
    self.nextItemTime = 0
    self.currentFruit = [0]
    self.currentFruitPosition = [-200]
    
    self.FoodInSnakeMap = []
    self.FoodInSnakeMapPositionX = []
    self.FoodInSnakeMapPositionY = []
    self.FoodInSnakeTimeToOut = []
    
    self.basket1 = pygame.image.load("resources/item/basket_happy.png").convert_alpha()
    self.basket2 = pygame.image.load("resources/item/basket_mad.png").convert_alpha()
    self.basket = self.basket2
    
    self.bgm1 = pygame.mixer.Sound("resources/sound/stage1.wav")
    self.bgm2 = pygame.mixer.Sound("resources/sound/stage2.wav")
    self.bgm3 = pygame.mixer.Sound("resources/sound/stage3.wav")
    self.eat = pygame.mixer.Sound("resources/sound/eat.wav")
    self.bgm1.stop()
    self.bgm2.stop()
    self.bgm3.stop()
    self.bgm1.play(-1)
    
    self.life = 3;
    self.snakePosition = [300,300]
    self.font = pygame.font.Font("CHERI.TTF", 40)
    
    self.score = 0
    self.score_Label = self.font.render("Score: "+str(self.score), True, (250,247,117))
    self.stage = 1
    
    self.leftHand = 0
    self.rightHand = 0    
    self.hands = []
    
    
    self.background1 = pygame.image.load("resources/stage1/background.png").convert()
    self.backgroundStage1 = pygame.image.load("resources/stage1/background_game.png").convert()
    self.backgroundStage1 = pygame.transform.scale(self.backgroundStage1, (800, 560))
    
    self.background2 = pygame.image.load("resources/stage2/background.png").convert()
    self.backgroundStage2 = pygame.image.load("resources/stage2/background_game.png").convert()
    self.backgroundStage2 = pygame.transform.scale(self.backgroundStage2, (800, 560))
    
    self.background3 = pygame.image.load("resources/stage3/background.png").convert()
    self.backgroundStage3 = pygame.image.load("resources/stage3/background_game.png").convert()
    self.backgroundStage3 = pygame.transform.scale(self.backgroundStage3, (800, 560))   
    self.background = self.background1
    self.backgroundStage = self.backgroundStage1
    
    self.fruit = []
    self.fruit.append(pygame.image.load("resources/item/apple.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/banana.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/grape.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/pineapple.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/broccoli.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/carrot.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/fish.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/drumstick.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/shrimp.png").convert_alpha())
    self.fruit.append(pygame.image.load("resources/item/strawberry.png").convert_alpha())
    
    
    self.food = []
    self.food.append(pygame.image.load("resources/item/donut.png").convert_alpha())
    self.food.append(pygame.image.load("resources/item/pizza.png").convert_alpha())
    self.food.append(pygame.image.load("resources/item/hot-dog.png").convert_alpha())
    self.food.append(pygame.image.load("resources/item/french-fries.png").convert_alpha())
    self.food.append(pygame.image.load("resources/item/popcorn.png").convert_alpha())
    self.food.append(pygame.image.load("resources/item/hamburger.png").convert_alpha())
    
    
    self.lifeImg = pygame.image.load("resources/item/life.png").convert_alpha()
    self.lifeImg = pygame.transform.scale(self.lifeImg, (40, 40))
    
    self.snake = pygame.image.load("resources/item/snake.png").convert_alpha()
    

    
  def processInput(self, frame):
    self.hands = frame.hands
    
    for hand in self.hands:
      if(hand.is_left):
        self.leftHand = hand
      elif(hand.is_right):
        self.rightHand = hand

  def update(self, frame):
    self.nextItemTime += self.speed
    if self.nextItemTime > 500:
      self.currentFruit.append(random.randrange(0, len(self.fruit)+len(self.food) - 1))
      self.currentFruitPosition.append(-200)      
      self.nextItemTime = 0
    i = 0
    if self.gameOver():
      return    
    lowerfood = -1
    lowertype = -1
    while i < len(self.currentFruitPosition):
      self.currentFruitPosition[i]+=1
       
      if self.currentFruitPosition[i] >= 600:
        if self.currentFruit[i]-len(self.fruit)<0:
          self.life -= 1;         
        del self.currentFruit[i]
        del self.currentFruitPosition[i]
        i-=1
      elif self.currentFruitPosition[i] >= 450 and self.currentFruitPosition[i] < 500 :
        lowerfood = i
        lowertype = self.currentFruit[i]
      i+=1

    if type(self.rightHand) is int or type(self.leftHand) is int :
      self.hands = frame.hands
      for hand in self.hands:
        if(hand.is_left):
          self.leftHand = hand
        elif(hand.is_right):
          self.rightHand = hand
          
    interactionBox = frame.interaction_box
    position = interactionBox.normalize_point(self.rightHand.palm_position)
    x = 200+((position.x-0.4)/6*10 * 800)
    y = SCREEN_SIZE[1] - (position.y * SCREEN_SIZE[1])
    if x < 200:
      x = 200
    if x > 900:
      x = 900    
    if y < 40:
      y = 40
    if y > 500:
      y = 500 
      
    i=0
    
    while i<len(self.FoodInSnakeMap):
      itemX = self.FoodInSnakeMapPositionX[i]
      itemY = self.FoodInSnakeMapPositionY[i]
      self.FoodInSnakeTimeToOut[i]-=1
      if self.FoodInSnakeTimeToOut[i]<0:
        del self.FoodInSnakeMap[i]
        del self.FoodInSnakeMapPositionX[i]        
        del self.FoodInSnakeMapPositionY[i]    
        del self.FoodInSnakeTimeToOut[i]
      if abs(x-itemX)<100 and abs(itemY-y)<100:
        self.score += self.FoodInSnakeTimeToOut[i]/10
        del self.FoodInSnakeMap[i]
        del self.FoodInSnakeMapPositionX[i]        
        del self.FoodInSnakeMapPositionY[i] 
        del self.FoodInSnakeTimeToOut[i]
        self.eat.play()        
       
        self.score_Label = self.font.render("Score: "+str(self.score), True, (250,247,117))
        if self.score >=3000:
          self.background = self.background3
          self.backgroundStage = self.backgroundStage3
        elif self.score >=1000:
          self.background = self.background2
          self.backgroundStage = self.backgroundStage2  
          
        if self.score > 1000 and self.score < 3000:
          self.speed = 3
        elif self.score > 3000:
          self.speed = 5     
        
      i+=1   
      
    if self.score >=3000:
      self.bgm1.stop()
      self.bgm2.stop()
      self.bgm3.play(-1)
    elif self.score >=1000:
      self.bgm1.stop()
      self.bgm2.play(-1)
      
    if (type(self.rightHand) is int or type(self.leftHand) is int)==False:
      typefood = ''
      if lowertype >= 0:
        if lowertype>len(self.fruit)-1:
          typefood = "food"
        else:
          typefood = "fruit"
      
      
      self.basket
      if self.isGrab(self.leftHand) :
        self.basket = self.basket1
        if typefood == "fruit":
          self.FoodInSnakeMapPositionX.append(random.randrange(200, 948))
          self.FoodInSnakeMapPositionY.append(random.randrange(40, 548))
          self.FoodInSnakeMap.append(lowertype)        
          self.FoodInSnakeTimeToOut.append(1000)    
          del self.currentFruit[lowerfood]
          del self.currentFruitPosition[lowerfood]
        elif typefood == "food": 
          del self.currentFruit[lowerfood]
          del self.currentFruitPosition[lowerfood]
          self.life -=1        
      else: 
        self.basket = self.basket2

        
        
    
  
    self.snakePosition = [x,y]   
      

  def render(self):
    
    self.screen.blit(self.background, [0, 0])
    self.screen.blit(self.backgroundStage, [200,40])
    pygame.draw.line(self.screen, (139, 142, 143), [0, 450], [200,450], 2)
    self.screen.blit(self.snake, self.snakePosition)
    
    
    i=0
    while i<len(self.FoodInSnakeMap):
      if self.FoodInSnakeMap[i]>len(self.fruit)-1:
        self.screen.blit(self.food[self.FoodInSnakeMap[i]-len(self.fruit)], [self.FoodInSnakeMapPositionX[i],self.FoodInSnakeMapPositionY[i]])
      else:
        self.screen.blit(self.fruit[self.FoodInSnakeMap[i]], [self.FoodInSnakeMapPositionX[i],self.FoodInSnakeMapPositionY[i]])
      i+=1         
    
    
    i=0
    while i<len(self.currentFruitPosition):
      if self.currentFruit[i]>len(self.fruit)-1:
        self.screen.blit(self.food[self.currentFruit[i]-len(self.fruit)], [70,self.currentFruitPosition[i]])
      else:
        self.screen.blit(self.fruit[self.currentFruit[i]], [70,self.currentFruitPosition[i]])
      i+=1            
    
    
    
    self.screen.blit(self.basket, [30,450])
    
    for i in range(0, self.life):
          self.screen.blit(self.lifeImg, [201+(i*40),0])   
          
    
    self.screen.blit(self.score_Label, (750, 0))



  def gameOver(self):
    if self.life < 0:
      self.bgm1.stop()
      self.bgm2.stop()
      self.bgm3.stop()
      gameOverScreen = GameOverScreen(self.screen, self.ssnake,self.score)
      self.ssnake.state = gameOverScreen
      return True
    return False



  def changeBG(self, stage):
    self.background = pygame.image.load("resources/stage"+stage+"/background.png").convert()
    self.backgroundStage = pygame.image.load("resources/stage"+stage+"/background_game.png").convert()


###############################################################################


class HowToScreen(View):
  def __init__(self, screen, ssnake):
    self.screen = screen
    self.ssnake = ssnake
    self.background = pygame.image.load("resources/howto/1.png")
    self.background = pygame.transform.scale(self.background, (1000, 600))
    self.bgm = pygame.mixer.Sound("resources/sound/default bg.wav")
    self.click = pygame.mixer.Sound("resources/sound/click.wav")
    self.cursor = Cursor()
    self.bgm.play(-1)
    self.addButtons()

  def addButtons(self):
    self.back = BackButton(90, 540,self.ssnake)
    self.howTo = NextHowToButton(920, 540, self.ssnake)

  def processInput(self, frame):
    self.hand = frame.hands[0]

  def update(self, frame):
    global ready
    interactionBox = frame.interaction_box
    position = interactionBox.normalize_point(self.hand.palm_position)
    x = position.x * SCREEN_SIZE[0]      
    y = SCREEN_SIZE[1] - (position.y * SCREEN_SIZE[1])
    
    self.cursor.setPos(x, y)
    
    if ready == False:
      if self.isGrab(self.hand) == False:
        ready = True
    else:
        if self.back.isMouseOver(self.cursor):
          if self.isGrab(self.hand):
            self.click.play()
            self.bgm.stop()
            ready = False
            self.back.goToNextState()   
        if self.howTo.isMouseOver(self.cursor):
          if self.isGrab(self.hand):
            self.click.play()
            self.bgm.stop()
            ready = False
            self.howTo.goToNextState()           
    



  def render(self):
    self.screen.blit(self.background, [0, 0])
    self.screen.blit(self.back.image, self.back.rect)
    self.screen.blit(self.howTo.image, self.howTo.rect)
    self.screen.blit(self.cursor.image, self.cursor.rect)
    
    
###############################################################################    
    
    
class HowTo2Screen(View):
  def __init__(self, screen, ssnake):
    self.screen = screen
    self.ssnake = ssnake
    self.background = pygame.image.load("resources/howto/2.png")
    self.background = pygame.transform.scale(self.background, (1000, 600))
    self.bgm = pygame.mixer.Sound("resources/sound/default bg.wav")
    self.click = pygame.mixer.Sound("resources/sound/click.wav")
    self.cursor = Cursor()
    self.bgm.play(-1)
    self.addButtons()

  def addButtons(self):
    self.back1 = BackButton1(90, 540,self.ssnake)
    self.nexthowto = NextHowToButton2(920, 540, self.ssnake)

  def processInput(self, frame):
    self.hand = frame.hands[0]

  def update(self, frame):
    global ready
    interactionBox = frame.interaction_box
    position = interactionBox.normalize_point(self.hand.palm_position)
    x = position.x * SCREEN_SIZE[0]      
    y = SCREEN_SIZE[1] - (position.y * SCREEN_SIZE[1])
    
    self.cursor.setPos(x, y)
    
    if ready == False:
      if self.isGrab(self.hand) == False:
        ready = True
    else:
        if self.back1.isMouseOver(self.cursor):
          if self.isGrab(self.hand):
            self.click.play()
            self.bgm.stop()
            ready = False
            self.back1.goToNextState()   
        if self.nexthowto.isMouseOver(self.cursor):
          if self.isGrab(self.hand):
            self.click.play()
            self.bgm.stop()
            ready = False
            self.nexthowto.goToNextState()           
        
                 
    

  def render(self):
    self.screen.blit(self.background, [0, 0])
    self.screen.blit(self.back1.image, self.back1.rect)
    self.screen.blit(self.nexthowto.image, self.nexthowto.rect)
    self.screen.blit(self.cursor.image, self.cursor.rect)
    
###############################################################################
    
class HowTo3Screen(View):
  def __init__(self, screen, ssnake):
      self.screen = screen
      self.ssnake = ssnake
      self.background = pygame.image.load("resources/howto/3.png")
      self.background = pygame.transform.scale(self.background, (1000, 600))
      self.bgm = pygame.mixer.Sound("resources/sound/default bg.wav")
      self.click = pygame.mixer.Sound("resources/sound/click.wav")
      self.cursor = Cursor()
      self.bgm.play(-1)
      self.addButtons()
  
  def addButtons(self):
      self.backhowtoo = BackButton2(90, 545,self.ssnake)
      self.play = PlayButton(920, 540, self.ssnake)
    
  def processInput(self, frame):
      self.hand = frame.hands[0]
    
  def update(self, frame):
      global ready
      interactionBox = frame.interaction_box
      position = interactionBox.normalize_point(self.hand.palm_position)
      x = position.x * SCREEN_SIZE[0]      
      y = SCREEN_SIZE[1] - (position.y * SCREEN_SIZE[1])
      
      self.cursor.setPos(x, y)
      
      if ready == False:
        if self.isGrab(self.hand) == False:
          ready = True
      else:
          if self.backhowtoo.isMouseOver(self.cursor):
            if self.isGrab(self.hand):
              self.click.play()
              self.bgm.stop()
              ready = False
              self.backhowtoo.goToNextState()   
          if self.play.isMouseOver(self.cursor):
            if self.isGrab(self.hand):
              self.click.play()
              self.bgm.stop()
              ready = False
              self.play.goToNextState()           
        
    
  def render(self):
      self.screen.blit(self.background, [0, 0])
      self.screen.blit(self.backhowtoo.image, self.backhowtoo.rect)
      self.screen.blit(self.play.image, self.play.rect)
      self.screen.blit(self.cursor.image, self.cursor.rect)    

class GameOverScreen(View):

  def __init__(self, screen, ssnake, score):
    self.screen = screen
    self.ssnake = ssnake
    self.checkHand = False
    self.index = 0
    self.clock = pygame.time.Clock()
    self.font = pygame.font.Font("CHERI.TTF", 30)
    self.score = score
    self.score_Label2 = self.font.render(" Total Score : "+str(self.score), True, (250,247,117))  
    self.background = pygame.image.load("resources/gameover/gameover.png").convert()
    self.bgm = pygame.mixer.Sound("resources/sound/game over.wav")
    self.click = pygame.mixer.Sound("resources/sound/click.wav")    
    self.addButtons()
    self.cursor = Cursor()
    self.bgm.play()

  def addButtons(self):
    self.buttons = []
    self.play = RestartButton(160, 520,self.ssnake)
    self.gohome = HomeButton(845, 520, self.ssnake)
    self.buttons.append(self.play)
    self.buttons.append(self.gohome)


  def processInput(self, frame):
    self.hand = frame.hands[0]


  def update(self, frame):
    global ready
    interactionBox = frame.interaction_box
    position = interactionBox.normalize_point(self.hand.palm_position)
    x = position.x * SCREEN_SIZE[0]      
    y = SCREEN_SIZE[1] - (position.y * SCREEN_SIZE[1])
    self.cursor.setPos(x, y)
    
    for button in self.buttons:
      if button.isMouseOver(self.cursor):
        if self.isGrab(self.hand):
          self.click.play()
          self.bgm.stop()
          ready = False
          button.goToNextState()
        break

  def render(self):
    self.screen.blit(self.background, [0, 0]) 
    self.screen.blit(self.score_Label2, (300, 310))
    for button in self.buttons:
      self.screen.blit(button.image, button.rect)
    self.screen.blit(self.cursor.image, self.cursor.rect)
    pass    