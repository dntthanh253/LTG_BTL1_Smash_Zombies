import pygame
import sys
import random
import math
import time
from enum import Enum
from spritesheets.spritesheet import Spritesheet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
GAME_NAME = "Smash Zombies"
GAME_TIME = 21 #seconds

ZOMBIE_WIDTH = 94
ZOMBIE_HEIGHT = 94
ZOMBIE_LIFE_TIME = 2 #seconds
ZOMBIE_LIFE_TIME = random.randint(2,5) #seconds

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,250,160)

TURN_OFF_SOUND = False
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#####################################################################
class Image:
    def __init__(self):
        self.background = pygame.image.load('images/background.jpg') # Background image
        self.menu = pygame.image.load('images/menu.png') # Hammer image
        self.sword = pygame.image.load('images/sword.png') # Sword image
        self.click_sword = pygame.image.load('images/click_sword.png') # Click sword image
        self.pause = pygame.image.load('images/pause.png') # Pause image
        self.pause_background = pygame.image.load('images/pause_bg.png') # Pause background image
        self.game_over = pygame.image.load('images/game_over.png') # Game over image
    
image = Image()

#####################################################################

class Sound:    
    def __init__(self):
        pygame.mixer.init()
        self.background = pygame.mixer.Sound('sounds/maintrack.wav') # Main game sound
        self.click = pygame.mixer.Sound('sounds/typing.wav') # Click sound
        self.dead = pygame.mixer.Sound('sounds/dead.mp3') # Smash sound
        self.sword = pygame.mixer.Sound('sounds/sword.mp3') # Sword sound
        self.zombie = pygame.mixer.Sound('sounds/zombie.mp3') # Zombie sound
        # More sound here
    
    def turnOn(self, type):
        if (type == 'background'):
            self.background.play(-1)
        if (type == 'click'):
            self.click.play()
        if (type == 'dead'):
            self.dead.play()
        if (type == 'sword'):
            self.sword.play()
        if (type == 'zombie'):
            self.zombie.play()
            
    def turnOff(self, type):
        if (type == 'background'):
            self.background.stop()
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

my_spritesheet = Spritesheet('spritesheets/spritesheet.png')
spawn_frames = [
    my_spritesheet.parse_sprite('spawn1.png'), #du thi xoa bot
    my_spritesheet.parse_sprite('spawn2.png'),
    my_spritesheet.parse_sprite('spawn3.png'), 
    my_spritesheet.parse_sprite('spawn4.png'), 
    my_spritesheet.parse_sprite('spawn5.png'), 
    my_spritesheet.parse_sprite('spawn6.png'),
    my_spritesheet.parse_sprite('spawn7.png'),
]
idle_frames = [
    my_spritesheet.parse_sprite('idle1.png'), #du thi xoa bot
    my_spritesheet.parse_sprite('idle2.png'),
    my_spritesheet.parse_sprite('idle3.png'), 
    my_spritesheet.parse_sprite('idle4.png'), 
    my_spritesheet.parse_sprite('idle5.png'), 
    my_spritesheet.parse_sprite('idle6.png'),
    my_spritesheet.parse_sprite('idle7.png'),
]
dead_frames = [
    my_spritesheet.parse_sprite('dead1.png'), #du thi xoa bot
    my_spritesheet.parse_sprite('dead2.png'),
    my_spritesheet.parse_sprite('dead3.png'), 
    my_spritesheet.parse_sprite('dead4.png'), 
    my_spritesheet.parse_sprite('dead5.png'), 
    my_spritesheet.parse_sprite('dead6.png'),
    my_spritesheet.parse_sprite('dead7.png'),
    my_spritesheet.parse_sprite('dead8.png'),
]
escape_frames = [
    my_spritesheet.parse_sprite('escape1.png'), #du thi xoa bot
    my_spritesheet.parse_sprite('escape2.png'),
    my_spritesheet.parse_sprite('escape3.png'), 
    my_spritesheet.parse_sprite('escape4.png'), 
    my_spritesheet.parse_sprite('escape5.png'), 
    my_spritesheet.parse_sprite('escape6.png'),
    my_spritesheet.parse_sprite('escape7.png'),
    my_spritesheet.parse_sprite('escape8.png'),
    my_spritesheet.parse_sprite('escape9.png'),
    my_spritesheet.parse_sprite('escape10.png'),
    my_spritesheet.parse_sprite('escape11.png'),
    my_spritesheet.parse_sprite('escape12.png'),
    my_spritesheet.parse_sprite('escape13.png'),
    my_spritesheet.parse_sprite('escape14.png'),
]

class ZombieState(Enum):
    SPAWN = 0
    IDLE = 1
    DEAD = 2
    ESCAPE = 3
    NONE = 4

#####################################################################

class Zombie: 
    def __init__ (self, x, y, screen):
        self.state = ZombieState.SPAWN
        self.x = x
        self.y = y
        self.screen = screen
        self.hit_time = 0
        self.escape_time = 0
        self.life_time = ZOMBIE_LIFE_TIME
        self.current_spawn_frame = 0
        self.current_idle_frame = 0
        self.current_dead_frame = 0
        self.current_escape_frame = 0
        
    def changeState(self, new_state):
        self.state = new_state
        
    def draw(self):
        if self.state == ZombieState.SPAWN:
            if self.current_spawn_frame < len(spawn_frames):
                frame = spawn_frames[int(self.current_spawn_frame)]
                self.screen.blit(frame, (self.x, self.y))
                self.current_spawn_frame += 0.2
            else:
                self.changeState(ZombieState.IDLE)
                
        if self.state == ZombieState.IDLE: #when zombie is smashed, how to change current_frame to 0 ??
            frame = idle_frames[int(self.current_idle_frame)]
            self.screen.blit(frame, (self.x, self.y))
            self.current_idle_frame = (self.current_idle_frame + 0.2) % len(idle_frames)
            
        if self.state == ZombieState.DEAD:
            if self.current_dead_frame < len(dead_frames):
                frame = dead_frames[int(self.current_dead_frame)]
                self.screen.blit(frame, (self.x, self.y))
                self.current_dead_frame += 0.2

        if self.state == ZombieState.ESCAPE:    
            if self.current_escape_frame < len(escape_frames):
                frame = escape_frames[int(self.current_escape_frame)]
                self.screen.blit(frame, (self.x, self.y))
                self.current_escape_frame += 0.2           

    def canEscape(self):
        if self.life_time ==  0:
            return True
        self.life_time -= 1
#####################################################################

class Intro:
    def __init__ (self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        # time variables
        self.interval = 100 # in milliseconds
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
            
        if any(pygame.key.get_pressed()) or any(pygame.mouse.get_pressed()):
            self.state.setState('menu')  # switch screen
            sound.turnOn('background')
                
        self.screen.fill(BLACK)
        rendered_text = self.font.render(GAME_NAME[:self.index], True, WHITE)
        rectangle = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(rendered_text, rectangle)
        
        if self.index >= len(GAME_NAME):
            self.alpha += 5
            self.curtain.set_alpha(self.alpha)
            if self.alpha > 255:
                self.state.setState('menu')
                sound.turnOn('background')
            self.screen.blit(self.curtain, (0, 0))   
            sound.turnOff('click')

#####################################################################

class Menu:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.quit_hangover = False
        self.play_hangover = False
        self.volume_hangover = False
        
    def run(self):
        global TURN_OFF_SOUND
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
            if not TURN_OFF_SOUND:
                self.volume_text = self.font.render("Volume: On", True, YELLOW)
            else:
                self.volume_text = self.font.render("Volume: Off", True, YELLOW)
        else:
            if not TURN_OFF_SOUND:
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
                        self.state.setState('play_game')
                    if 29 <= mouse[0] <= 258 and 473 <= mouse[1] <= 555:
                        pygame.quit()
                        sys.exit()
                    if 542 <= mouse[0] <= 773 and 473 <= mouse[1] <= 555:
                        TURN_OFF_SOUND = not TURN_OFF_SOUND
                        if TURN_OFF_SOUND:    
                            sound.turnOff('background')
                        else:    
                            sound.turnOn('background') 
                            
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

        self.screen.blit(image.menu, (0, 0))
        self.screen.blit(self.play_text, (320, 530))
        self.screen.blit(self.quit_text, (64, 490))
        self.screen.blit(self.volume_text, (574, 490))
        window.blit(self.screen, (0,0))
        pygame.display.update()
        
#####################################################################

class PlayGame:
    def __init__ (self, screen, state):
        self.screen = screen
        self.state = state
        self.period = GAME_TIME
        self.countdown = self.period
        self.graves = [(195, 64), (516, 116), (143, 328), (625 , 328), (413, 434), (200 , 540), (571, 596)]
        
        self.cursor_img = image.sword
        self.cursor_rect = self.cursor_img.get_rect()
        self.pause_icon = image.pause
        self.pause_icon_rect = self.pause_icon.get_rect(topleft=(750, 10))
        
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.score = 0
        self.zombies = []
        self.generate_zombie = pygame.USEREVENT + 1
        self.appear_interval = 2000
        self.remove_interval = 2
        self.escape_count = 0
        
        pygame.time.set_timer(self.generate_zombie, self.appear_interval)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.time.set_timer(self.remove_interval, 1000)

    def resetState(self):
        self.countdown = self.period
        self.score = 0
        
    def getScore(self):
        return self.score
    
    def checkEmptyGraves(self, position):
        for zombie in self.zombies:
            if position == (zombie.x, zombie.y):
                return False
        return True
        
    def generateZombie(self):
        new_position = ()
        while True:
            index = random.randint(0, 6)
            new_position = self.graves[index]
            if self.checkEmptyGraves(new_position):
                break
        return new_position
    
    
    def drawZombies(self):
        for zombie in self.zombies:
            zombie.draw()
            
    def checkCollision(self, click_x, click_y, zombie_x, zombie_y):
        zombie_center = (zombie_x + 48, zombie_y + 48)
        distance = math.sqrt(math.pow(zombie_center[0] - click_x, 2) + math.pow(zombie_center[1] - click_y, 2))
        return distance < 48 
    
    def checkZombieSmashed(self, position):
        current = pygame.time.get_ticks()
        for zombie in self.zombies:
            if self.checkCollision(position[0], position[1], zombie.x, zombie.y) and zombie.state == ZombieState.IDLE:
                self.score += 1
                zombie.changeState(ZombieState.DEAD)
                if not TURN_OFF_SOUND:
                    sound.turnOn('dead')
                zombie.draw()
                zombie.hit_time = current
            if self.checkCollision(position[0], position[1], zombie.x, zombie.y) and zombie.state == ZombieState.SPAWN:
                self.score += 1
                zombie.changeState(ZombieState.DEAD)
                if not TURN_OFF_SOUND:
                    sound.turnOn('dead')
                zombie.draw()
                zombie.hit_time = current
            if self.checkCollision(position[0], position[1], zombie.x, zombie.y) and zombie.state == ZombieState.ESCAPE:
                self.score += 1
                zombie.changeState(ZombieState.DEAD)
                if not TURN_OFF_SOUND:
                    sound.turnOn('dead')
                zombie.draw()
                zombie.hit_time = current

    def removeZombie(self):
        for zombie in self.zombies:
            current = pygame.time.get_ticks()   
            if zombie.canEscape():
                if zombie.state == ZombieState.IDLE:
                    zombie.changeState(ZombieState.ESCAPE)
                    zombie.escape_time = current
                    self.escape_count += 1
                zombie.draw()
            if zombie.state == ZombieState.DEAD:
                self.zombies.remove(zombie)
            if zombie.state == ZombieState.ESCAPE and current - zombie.escape_time >= 2:
                self.zombies.remove(zombie)
                zombie.changeState(ZombieState.NONE)
                
    def displayMissed(self):
        missed_text = self.font.render("Missed: " + str(self.escape_count), True, WHITE)
        self.screen.blit(missed_text, (20, 10))
        
    def displayScore(self):
        score_text = self.font.render("Score: " + str(self.getScore()), True, WHITE)
        self.screen.blit(score_text, (20, 50))
            
    def displayTime(self):
        time_text = self.font.render("Time: " + str(self.countdown), True, WHITE)
        self.screen.blit(time_text, (20, 90))
        
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.cursor_img = image.click_sword
                    click_position = pygame.mouse.get_pos()
                    if self.pause_icon_rect.collidepoint(click_position):
                        self.state.setState('pause')
                    else:
                        self.checkZombieSmashed(click_position)
                        if not TURN_OFF_SOUND:
                            sound.turnOn('sword')
                else:
                    self.cursor_img = image.sword
                    
            if event.type == self.generate_zombie:
                if len(self.zombies) < 7:
                    new_position = self.generateZombie()
                    self.zombies.append(Zombie(new_position[0], new_position[1], self.screen))
            if event.type == self.remove_interval:
                self.removeZombie()
                
            if event.type == pygame.USEREVENT:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.zombies.clear()
                    self.state.setState('game_over')
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    self.state.setState('pause')
        
        self.screen.blit(image.background, (0, 0))
        self.screen.blit(self.pause_icon, (740, 15))
        self.drawZombies()
        
        self.displayScore()
        self.displayMissed()
        self.displayTime()
        
        pygame.mouse.set_visible(False)
        self.cursor_rect.center = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, self.cursor_rect)

#####################################################################

class PauseGame:
    def __init__ (self, screen, state, play_game):
        self.screen = screen
        self.state = state
        self.play_game = play_game
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.pause_center = image.pause.get_rect().center
        self.transition_speed = 10
        self.resume_hangover = False
        self.menu_hangover = False
        self.resume_text = self.font.render("Resume", True, WHITE)
        self.menu_text = self.font.render("Menu", True, WHITE)
    
    def run(self):
        pygame.mouse.set_visible(True)
        mouse = pygame.mouse.get_pos()
        
        if 285 <= mouse[0] <= 515 and 292 <= mouse[1] <= 375:
            self.resume_hangover = True
        else:
            self.resume_hangover = False
        if 285 <= mouse[0] <= 515 and 397 <= mouse[1] <= 480:
            self.menu_hangover = True
        else:
            self.menu_hangover = False
        
        if self.resume_hangover:
            self.resume_text = self.font.render("Resume", True, YELLOW)
        else: 
            self.resume_text = self.font.render("Resume", True, WHITE)
        if self.menu_hangover:
            self.menu_text = self.font.render("Menu", True, YELLOW)
        else:
            self.menu_text = self.font.render("Menu", True, WHITE)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 285 <= mouse[0] <= 515 and 292 <= mouse[1] <= 375:
                        self.state.setState('play_game')
                    if 285 <= mouse[0] <= 515 and 397 <= mouse[1] <= 480:
                        self.state.setState('menu')
                        self.play_game.resetState()
        
        self.screen.blit(image.pause_background, (0, 0))
        self.screen.blit(self.resume_text, (338, 310))
        self.screen.blit(self.menu_text, (360, 415))
        

#####################################################################

class GameOver:
    def __init__ (self, screen, state, play_game):
        self.screen = screen
        self.state = state
        self.play_game = play_game
        self.font = pygame.font.Font('fonts/m5x7.ttf', 50)
        self.game_over_center = image.game_over.get_rect().center
        self.transition_speed = 10
        self.menu_hangover = False
        self.play_again_hangover = False
        self.menu_text = self.font.render("Menu", True, WHITE)
        self.play_again_text = self.font.render("Play Again", True, WHITE)
        
    def run(self):
        pygame.mouse.set_visible(True)
        mouse = pygame.mouse.get_pos()
        
        if 285 <= mouse[0] <= 515 and 405 <= mouse[1] <= 488:
            self.play_again_hangover = True
        else:
            self.play_again_hangover = False
        if 285 <= mouse[0] <= 515 and 510 <= mouse[1] <= 593:
            self.menu_hangover = True
        else:
            self.menu_hangover = False
        
        if self.menu_hangover:
            self.menu_text = self.font.render("Menu", True, YELLOW)
        else: 
            self.menu_text = self.font.render("Menu", True, WHITE)
        if self.play_again_hangover:
            self.play_again_text = self.font.render("Play Again", True, YELLOW)
        else:
            self.play_again_text = self.font.render("Play Again", True, WHITE)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 285 <= mouse[0] <= 515 and 405 <= mouse[1] <= 488:
                        self.state.setState('play_game')
                        self.play_game.resetState()
                    if 285 <= mouse[0] <= 515 and 510 <= mouse[1] <= 593:
                        self.state.setState('menu')
                        self.play_game.resetState()
        
        self.screen.blit(image.game_over, (0, 0))
        self.screen.blit(self.play_again_text, (318, 420))
        self.screen.blit(self.menu_text, (360, 525))
        
        score_text = self.font.render("Score: " + str(self.play_game.getScore()), True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)
        
        missed_text = self.font.render("Missed: " + str(self.play_game.escape_count), True, WHITE)
        missed_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
        self.screen.blit(missed_text, missed_rect)
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
        self.play_game = PlayGame(self.screen, self.state)
        self.game_over = GameOver(self.screen, self.state, self.play_game)
        self.pause = PauseGame(self.screen, self.state, self.play_game)
        self.states = {'intro': self.intro, 'menu': self.menu, 'play_game': self.play_game, 'game_over': self.game_over, 'pause': self.pause}
        
    def run(self):
        while True: #loop every 1/60 seconds
            self.states[self.state.getState()].run()
            pygame.display.update()
            self.clock.tick(FPS)
            
#####################################################################

if __name__ == "__main__":  
    game = Game()
    game.run()
