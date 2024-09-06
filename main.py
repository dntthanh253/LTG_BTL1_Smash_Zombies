import pygame
import sys
from enum import Enum

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
GAME_NAME = "Smash Zombies"

ZOMBIE_WIDTH = 100
ZOMBIE_HEIGHT = 100
ZOMBIE_TIME = 2000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,250,160)

#####################################################################

class Image:
    def __init__(self):
        self.background = pygame.image.load('images/background.jpg') # Background image
        self.menu = pygame.image.load('images/menu.jpg') # Hammer image
        self.game_over = pygame.image.load("") # Game over image
        self.volume_on = pygame.image.load("") # Volume images
        self.volume_off = pygame.image.load("")
        self.zombie = pygame.image.load("") # Zombie images
    
image = Image()

#####################################################################

class Sound:    
    def __init__(self):
        self.mainTrack = pygame.mixer.Sound('sounds/maintrack.wav') # Main game sound
        self.click = pygame.mixer.Sound('sounds/typing.wav') # Click sound
        self.smash = pygame.mixer.Sound("") # Smash sound
        self.game_over = pygame.mixer.Sound("") # Game over sound
        self.background = pygame.mixer.Sound("") # Background sound
        self.intro = pygame.mixer.Sound("") # Intro sound
        # More sound here
    
    def turnOn(self, type):
        if (type == 'mainTrack'):
            self.mainTrack.play(-1)
        if (type == 'click'):
            self.click.play()
            
    def turnOff(self, type):
        if (type == 'mainTrack'):
            self.mainTrack.stop()
        if (type == 'click'):
            self.click.stop()
        
sound = Sound()

#####################################################################

class StateManager:
    def __init__(self, init_state):
        self.state = init_state
        
    def getState(self):
        return self.state
    
    def setState(self, new_state):
        self.state = new_state

#####################################################################

class ZombieState(Enum):
    SPAWN = 0
    IDLE = 1
    SMASHED = 2
    DEAD = 3
    ESCAPE = 4

#####################################################################

class Zombie:
    def __init__ (self, x, y, screen):
        self.state = ZombieState.SPAWN
        self.x = x
        self.y = y
        self.screen = screen
        
    def changeState(self, new_state):
        self.state = new_state
        
    def draw(self):
        

#####################################################################

class Intro:
    def __init__ (self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        # time variables
        self.interval = 500 # in milliseconds
        self.delay = 100
        self.current = pygame.time.get_ticks() # time count tu luc lib pygame duoc chay den thoi diem hien tai
        self.next = self.current + self.interval
        self.index = 0
        
        self.curtain = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.curtain.fill(BLACK)
        self.alpha = 0;
    
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        self.current = pygame.time.get_ticks()
        if self.current > self.next and self.index < len(GAME_NAME):
            self.next = self.current + self.interval
            self.index += 1
            sound.turnOn('click');
            
        self.display.fill(BLACK)
        rendered_text = self.font.render(GAME_NAME[self.index], True, WHITE)
        rectangle = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(rendered_text, rectangle)
        
        if self.index >= len(GAME_NAME):
            self.alpha += 5
            self.curtain.set_alpha(self.alpha)
            if self.alpha > 255:
                self.state.setState('menu')
                sound.turnOn('mainTrack')
            self.screen.blit(self.curtain, (0, 0))   
            sound.turnOff('click')

#####################################################################

class Menu:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.volume_on = True
        self.quit_hangover = False
        self.play_hangover = False
        self.volume_hangover = False
        
    def run(self):
        mouse = pygame.mouse.get_pos()
        
        if self.quit_hangover:
            self.quit_text = self.font.render("Quit Game", True, YELLOW)
        else:
            self.quit_text = self.font.render("Quit Game", True, WHITE)
            
        if self.play_hangover:
            self.play_text = self.font.render("Play Game", True, YELLOW)
        else:
            self.play_text = self.font.render("Play Game", True, WHITE)
            
        if self.volume_hangover:
            if self.volume_on:
                self.volume_text = self.font.render("Volume: On", True, YELLOW)
            else:
                self.volume_text = self.font.render("Volume: Off", True, YELLOW)
        else:
            if self.volume_on:
                self.volume_text = self.font.render("Volume: On", True, WHITE)
            else:
                self.volume_text = self.font.render("Volume: Off", True, WHITE)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left button clicked
                    if 285 <= mouse[0] <= 515 and 514 <= mouse[1] <= 596:
                        self.state.setState('game')
                    if 29 <= mouse[0] <= 258 and 473 <= mouse[1] <= 555:
                        pygame.quit()
                        sys.exit()
                    if 542 <= mouse[0] <= 773 and 473 <= mouse[1] <= 555:
                        if self.volume_on:    
                            sound.turnOff('mainTrack')
                        else:    
                            sound.turnOn('mainTrack') 
                        self.volume_on = not self.volume_on       
            
        self.screen.blit(image.menu, (0, 0))
        self.display.blit(self.play_text, (320, 530))
        self.display.blit(self.quit_text, (64, 490))
        self.display.blit(self.volume_text, (566, 490))

        if 285 <= mouse[0] <= 515 and 514 <= mouse[1] <= 596:
            self.play_hangover = True
        else:
            self.play_hangover = False
        if 29 <= mouse[0] <= 258 and 473 <= mouse[1] <= 555:
            self.quit_hangover = True
        else:
            self.quit_hangover = False
        if 542 <= mouse[0] <= 773 and 473 <= mouse[1] <= 555:
            self.volume_hangover = True
        else:
            self.volume_hangover = False

#####################################################################

class PlayGame:
    def __init__ (self):
#####################################################################

class Pause:
    def __init__ (self):

#####################################################################

class GameOver:
    def __init__ (self):
    
        
############## MAIN CLASS ###########################################

class Game:
    def __init__(self):
        # Initialize Pygame
        self.clock = pygame.time.Clock()
        pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        self.state = StateManager('intro')
        self.intro = Intro(self.screen, self.state)
        self.menu = Menu(self.screen, self.state)
        # self.play_game = PlayGame(self.screen, self.state)
        # self.game_over = GameOver(self.screen, self.state, self.play_game)
        # self.pause = PauseGame(self.screen, self.state, self.play_game)
        self.states = {'intro': self.intro, 'menu': self.menu, 'play_game': self.play_game, 'game_over': self.game_over, 'pause': self.pause}
        
    def run(self):
        while True: #loop every 1/60 seconds
            self.states[self.state.getState()].run()
            pygame.display.update()
            self.clock.tick(FPS)
            
#####################################################################

if __name__ == "__main__":  # run the class Game
    game = Game()
    game.run()
