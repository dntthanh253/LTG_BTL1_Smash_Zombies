import pygame

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60
GAME_NAME = "Smash Zombies"

ZOMBIE_WIDTH = 100
ZOMBIE_HEIGHT = 100
ZOMBIE_TIME = 2000

#####################################################################

class Image:
    def __init__(self):
        self.menu = pygame.image.load("") # Menu image
        self.background = pygame.image.load("") # Background image
        self.hammer = pygame.image.load("") # Hammer image
        self.game_over = pygame.image.load("") # Game over image
        self.button_play = pygame.image.load("") # Button images
        self.volume_on = pygame.image.load("") # Volume images
        self.volume_off = pygame.image.load("")
        self.zombie1 = pygame.image.load("") # Zombie images
        self.zombie2 = pygame.image.load("")
        self.zombie3 = pygame.image.load("")
        # More asset here
    
image = Image()

#####################################################################

class Sound:    
    def __init__(self):
        self.click = pygame.mixer.Sound("") # Click sound
        self.smash = pygame.mixer.Sound("") # Smash sound
        self.game_over = pygame.mixer.Sound("") # Game over sound
        self.background = pygame.mixer.Sound("") # Background sound
        self.intro = pygame.mixer.Sound("") # Intro sound
        # More sound here
        
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
#####################################################################

class Intro:
    def __init__ (self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.SysFont(None, 50)
        # time variables
        self.interval = 500 # in milliseconds
        self.delay = 100
        self.current = pygame.time.get_ticks()
        self.next = self.current + self.interval
        self.index = 0
        
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        

############## MAIN CLASS ###################################

class Game:
    def __init__(self):
        # Initialize Pygame
        self.clock = pygame.time.Clock()
        pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
