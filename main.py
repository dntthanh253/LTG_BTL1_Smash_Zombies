import pygame

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60
GAME_NAME = "Smash Zombies"


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

############## MAIN CLASS ###################################

class Game:
    def __init__(self):
        # Initialize Pygame
        self.clock = pygame.time.Clock()
        pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        
        
        self.running = True
        self.playing = False
        self.volume = True
        self.font = pygame.font.Font(None, 36)
        self.load_data()
        self.new()
        
    def load_data(self):
        pass
    
    def new(self):
        pass
    
    def run(self):
        pass
    
    def events(self):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        pass
    
    def show_start_screen(self):
        pass
    
    def show_game_over_screen(self):
        pass
