import pygame, random, math

    
class Button(pygame.sprite.Sprite):

  name = "button"
  height = 1
  width = 1

  def __init__(self, x, y, snake):
    
    self.image1 = pygame.image.load("resources/menu/"+self.name + ".png").convert_alpha()
    self.image2 = pygame.image.load("resources/menu/"+self.name + "1.png").convert_alpha()
    self.image = self.image1
    
    self.width = self.image.get_width()
    self.height = self.image.get_height()    

    self.rect = self.image.get_rect()
    self.rect.centerx = x
    self.rect.centery = y
    self.snake = snake

  
  def isMouseOver(self,cursor):
    if (abs( self.rect.centerx - cursor.realx ) <= self.width and abs( self.rect.centery - cursor.realy ) <= self.height):
      self.image = self.image2;
      return True
    self.image = self.image1;
    return False  


  def goToNextState(self):
    return

class PlayButton(Button):
  name = "play"  
  def goToNextState(self):
    self.snake.goToGameScreen()
    
class RestartButton(Button):
  name = "restart"  
  def goToNextState(self):
    self.snake.goToGameScreen()


class HowToButton(Button):
  name = "howto"
  def goToNextState(self):
    self.snake.goToHowToScreen()

class CreditButton(Button):
  name = "credit"
  def goToNextState(self):
    self.snake.goToCreditScreen()

class ExitButton(Button):
  name = "exit"
  def goToNextState(self):
    self.snake.quit()

class BackButton(Button):
  name = "back"
  def goToNextState(self):
    self.snake.goToMenuScreen()
    
class BackButton1(Button):
  name = "backhowto"
  def goToNextState(self):
    self.snake.goToHowToScreen()

class BackButton2(Button):
  name = "backhowtoo"
  def goToNextState(self):
    self.snake.goToHowTo2Screen()
    
class HomeButton(Button):
  name = "gohome"
  def goToNextState(self):
    self.snake.goToMenuScreen()
    
    
class NextHowToButton(Button):
  name = "nexthowto"
  def goToNextState(self):
    self.snake.goToHowTo2Screen()
    
class NextHowToButton2(Button):
  name = "nexthowtoo"
  def goToNextState(self):
    self.snake.goToHowTo3Screen()
    
class Cursor(pygame.sprite.Sprite):
  height = 1
  width = 1
  realx = 1
  realy = 1
  def __init__(self):
    self.pos = [200,200]
    self.image = pygame.image.load("resources/item/hand.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.width = self.image.get_width()
    self.height = self.image.get_height()  
    

  def setPos(self,x,y):
    self.rect.centerx = x
    self.rect.centery = y
    self.realx = x
    self.realy = y