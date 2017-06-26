import Leap, sys, pygame, math

from pygame.locals import *
from view import *
from model import *
from player import *

SCREEN_SIZE = (1000, 600)
BG_COLOR = (106, 189, 255)

class Controller:
  def __init__(self):
    # LEAP motion initialization
    self.controller = Leap.Controller()
    self.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)  
    
    # pygame initialization
    pygame.init()
    pygame.display.set_caption("Snake Game")
    self.screen = pygame.display.set_mode(SCREEN_SIZE)   
    
    self.state = SpashScreen(self.screen, self) 
    
    self.gameScreen = GameScreen(self.screen, self)
    
    
  def start(self):
    while  True:
      frame = self.controller.frame()
      self.processInput(frame)
      self.update(frame)
      self.render()
      
  def processInput(self, frame):
    self.hands = frame.hands
    for event in pygame.event.get():
        self.event_handler(event)
    self.state.processInput(frame)  
      
  def update(self, frame):
    if(len(self.hands) < 2 and self.state.checkHand):
      self.previousScreen = self.state
      if(self.previousScreen.__class__ == GameScreen):
          self.state = PauseScreen(self.screen, self, self.previousScreen)
    elif(self.state.__class__ == PauseScreen and len(self.hands) >= 2):
      self.state = self.previousScreen
    self.state.update(frame)

  def render(self):
    self.state.render()
    pygame.display.flip()

  def goToGameScreen(self):
    self.state = self.gameScreen
    self.state.reset()

  def goToMenuScreen(self):
    self.state = MenuScreen(self.screen, self)

  def goToHowToScreen(self):
    self.state = HowToScreen(self.screen, self)
    
  def goToHowTo2Screen(self):
    self.state = HowTo2Screen(self.screen, self)
    
  def goToHowTo3Screen(self):
    self.state = HowTo3Screen(self.screen, self)  
    

  def goToCreditScreen(self):
    self.state = CreditScreen(self.screen, self)

  def quit(self):
    pygame.quit()
    sys.exit(0)

  def event_handler(self, event):
    if event.type == pygame.QUIT :
      self.quit()
    if event.type == KEYDOWN and event.key == K_ESCAPE:
      self.quit()
    if event.type == KEYDOWN and event.key == K_f:
      if self.screen.get_flags() & FULLSCREEN:
        pygame.display.set_mode(SCREEN_SIZE)
      else:
        pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)