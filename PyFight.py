# PyFight v_a.05 by Charlie Warren and Marco Perez
# Sprites and Code by Charlie Warren
# Menu designs and Code by Marco Perez

# Import all modules and external files to be used
import pygame
import time
import menu

# Initialize pygame
pygame.init()
# S_PUNCH = pygame.mixer.Sound("AUDIO\\PUNCH.wav")
# S_WIN = pygame.mixer.Sound("AUDIO\\WIN.wav")
# pygame.mixer.music.load("AUDIO\\SONG.wav")
# pygame.mixer.music.play(-1)
WIN_WID = 800
WIN_HEI = 600

# Set the display
win = pygame.display.set_mode((WIN_WID, WIN_HEI))
win.fill((255, 255, 255))
pygame.display.update()
pygame.display.set_caption("PyFight")

# Set the variables for boundaries and the fps limit
L_BOUND, R_BOUND, T_BOUND, B_BOUND = 0, 745, 0, 495
dt, clock = 0, pygame.time.Clock()

jimbob, billy = pygame.image.load("SPRITES\\PLAYERS\\JIMBOB.png"), pygame.image.load("SPRITES\\PLAYERS\\BILLY.png")
jimbob_cd, billy_cd = pygame.image.load("SPRITES\\PLAYERS\\JIMBOB_CD.png"), pygame.image.load("SPRITES\\PLAYERS\\BILLY_CD.png")
fist = pygame.image.load("SPRITES\\WEAPONS\\FIST.png")
grass, wood = pygame.image.load("SPRITES\\TILES\\GRASS.png"), pygame.image.load("SPRITES\\TILES\\WOOD.png")

global rdir, ldir
rdir, ldir = "", ""

global SKYBLUE
SKYBLUE = (135, 176, 235)

# Variables used for scoring and weapon blits
global p1_points, p2_points, p1_dead, p2_dead
p1_points = 0
p2_points = 0
p1_dead, p2_dead = False, False
p1_gun, p2_gun = fist, fist
p1_gun_flip, p2_gun_flip = pygame.transform.flip(fist, flip_x=True, flip_y=False), pygame.transform.flip(fist, flip_x=True, flip_y=False)

global Round
Round = 1

# Generic class for handling players, enemies, projectiles etc
class thing(object):
    def __init__(self, texture, x, y, jh, fg, yvel, vel, jump, type, special):
        self.texture = texture # Texture of the thing
        self.x = x # x location
        self.y = y # y location
        self.jh = jh # jump height
        self.fg = fg # Force of p.gravity
        self.yvel = yvel # Y velocity
        self.vel = vel # velocity
        self.jump = jump
        self.type = type # Type of object
        self.special = special # Special identifier
    
    def fire(self, wHit, wDir, cd_texture, pos, special):
        
        if special == 0:
            # pygame.mixer.Sound.play(S_PUNCH)
            self.texture = cd_texture

            if wDir == "l": 
                toRect = pygame.Rect((pos[0] - 50, pos[1]), (15, 50))
                punch = pygame.draw.rect(win, (SKYBLUE), toRect)
            else: 
                toRect = pygame.Rect((pos[0] + 50, pos[1]), (15, 50))
                punch = pygame.draw.rect(win, (SKYBLUE), toRect)
            
            col = wHit.colliderect(punch)
            self.special = 3.5 * 50
            if col: return True
            else: return False
        else: return False

# Generic class for handling tiles
class tile(pygame.Rect):
    def __init__(self, x, y, wid, hei, texture):
        self.x = x
        self.y = y
        self.wid = wid
        self.hei = hei
        self.texture = texture

    def draw(self):
        win.blit(self.texture, (self.x, self.y))

# Players
global p1, p2
p1 = thing(jimbob, 100.0, 350.0, 20, 1, 20, 7.5, False, "player", 0)
p2 = thing(billy, 600.0, 350.0, 20.0, 1, 20.0, 7.5, False, "player", 0)

# Hitboxes for the players
p1_box, p2_box = p1.texture.get_rect(), p2.texture.get_rect()

# Tiles that make up the map
floor = [tile(0, 550, 50, 50, grass), tile(50, 550, 50, 50, grass), tile(100, 550, 50, 50, grass), tile(150, 550, 50, 50, grass), tile(200, 550, 50, 50, grass), tile(250, 550, 50, 50, grass), tile(300, 550, 50, 50, grass), tile(350, 550, 50, 50, grass), tile(400, 550, 50, 50, grass), tile(450, 550, 50, 50, grass), tile(450, 550, 50, 50, grass), tile(500, 550, 50, 50, grass), tile(550, 550, 50, 50, grass), tile(600, 550, 50, 50, grass), tile(650, 550, 50, 50, grass), tile(700, 550, 50, 50, grass), tile(750, 550, 50, 50, grass)]

global font
font = pygame.font.SysFont("arialblack", 40)
font2 = pygame.font.SysFont("arialblack", 30)
def text(txt, font, txt_col):
    img = font.render(txt, True, txt_col)
    return img

def reset(round):

    p1.x, p1.y = 100.0, 350.0
    p2.x, p2.y = 250.0, 350.0
    p1.special = 0
    p2.special = 0
    round += 1
    return round

pygame.display.set_icon(pygame.image.load("JIMBOB.ico"))
#menu.menu(win, font, fist)

# Main game loop
global going
going = False
running = True
while running:

    p1_box.x = p1.x
    p1_box.y = p1.y
    p2_box.x = p2.x
    p2_box.y = p2.y

    if p1.special > 0:
        p1.texture = jimbob_cd 
        p1.special -= 1
    else:
        p1.texture = jimbob
    if p2.special > 0:
        p2.texture = billy_cd
        p2.special -= 1
    else:
        p2.texture = billy

    pygame.display.set_caption(f'PyFight | dt = {dt * 1000}')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    # Player one movement
    if keys[pygame.K_a]: 
        rdir="l"
        p1_flip = pygame.transform.flip(p1.texture, flip_x=True, flip_y=False)   
        p1.x -= p1.vel
    if p1.x < L_BOUND:
        p1.x = L_BOUND
    if keys[pygame.K_d]:
        rdir="r"
        p1.x += p1.vel
    if p1.x > R_BOUND:
        p1.x = R_BOUND
    if keys[pygame.K_w]:
        p1.jump = True
    if keys[pygame.K_s]:
        p1.y += p1.vel
    if p1.y > B_BOUND:
        p1.y = B_BOUND
    if keys[pygame.K_q]:
        pos = (p1.x, p1.y)
        p1_kill = p1.fire(p2_box, rdir, jimbob_cd, pos, p1.special)
        if p1_kill: p2_dead = True

    # Player one jumping
    if p1.jump:
        p1.y -= p1.yvel
        p1.yvel -= p1.fg
        if p1.yvel < -p1.jh:
            p1.jump=False
            p1.yvel = p1.jh
    else: 
        p1.y += p1.fg * p1.vel

    # Player 2 movement
    if keys[pygame.K_LEFT]:
        ldir="l"
        p2_flip = pygame.transform.flip(p2.texture, flip_x=True, flip_y=False)
        p2.x -= p2.vel
    if p2.x < L_BOUND:
        p2.x = L_BOUND
    if keys[pygame.K_RIGHT]:
        ldir="r"
        p2.x += p2.vel
    if p2.x > R_BOUND:
        p2.x = R_BOUND
    if keys[pygame.K_UP]:
        p2.jump = True
    if p2.y < T_BOUND:
        p2.y = T_BOUND
    if keys[pygame.K_DOWN]:
        p2.y += p2.vel
    if p2.y > B_BOUND:
        p2.y = B_BOUND
    if keys[pygame.K_RCTRL]:
        pos = (p2.x, p2.y)
        p2_kill = p2.fire(p1_box, ldir, billy_cd, pos, p2.special)
        if p2_kill: p1_dead = True

    # Player two jumping
    if p2.jump:
        p2.y -= p2.yvel
        p2.yvel -= p2.fg
        if p2.yvel < -p2.jh:
            p2.jump=False
            p2.yvel = p2.jh
    else: 
        p2.y += p2.fg * p2.vel

    if p1_dead:

        p2_points += 1
        p1_dead = False

        # Display the winner of the round, and reset the game
        msg = "Player 2 wins round " + str(Round)
        msg = text(msg, font, (0, 0, 0))
        win.blit(msg, (180, 250))
        pygame.display.update()
        time.sleep(3)
        r = reset(Round)
        Round = r

    if p2_dead:

        p1_points += 1
        p2_dead = False
        msg = "Player 1 wins round " + str(Round)
        msg = text(msg, font, (0, 0, 0))
        win.blit(msg, (180, 250))
        pygame.display.update()
        time.sleep(3)
        r = reset(Round)
        Round = r

    # Checks to ensure that the speed will remain consistent by speeding it up when the game slows down
    dtr = dt * 1000
    if dtr > 20 and dtr < 30:
        p1.vel = 8.5
        p2.vel = 8.5
    elif dtr > 30 and dtr < 40:
        p1.vel = 9.5
        p2.vel = 9.5
    elif dtr > 40 and dtr < 50:
        p1.vel = 10.5
        p2.vel = 10.5
    elif dtr > 50:
        p1.vel = 11.5
        p2.vel = 11.5
    else:
        p1.vel = 7.5
        p2.vel = 7.5
    if not(going):
        win.fill((SKYBLUE))
        pygame.draw.rect(win, "white", ((125, 125), (80, 40)))
        pygame.draw.rect(win, "white", ((250, 100), (100, 50)))
        # Checking if p1 is facing left or right
        if rdir == "l":
            win.blit(p1_flip, (p1.x, p1.y))
            win.blit(p1_gun_flip, (p1.x - 25, p1.y))
        else:
            win.blit(p1.texture, (p1.x, p1.y))
            win.blit(p1_gun, (p1.x + 25, p1.y))

        # Checking if p2 is facing left or right
        if ldir == "l":
            win.blit(p2_flip, (p2.x, p2.y))
            win.blit(p2_gun_flip, (p2.x - 25, p2.y))
        else:
            win.blit(p2.texture, (p2.x, p2.y))
            win.blit(p2_gun, (p2.x + 25, p2.y))


        # Draw all of the tiles to the screen using tile.draw()
        for i in range(0,17):
            floor[i].draw()

    # Code to check for the winner

    keys = pygame.key.get_pressed()

    if keys[pygame.K_h]:

        if keys[pygame.K_e]:

            if keys[pygame.K_y]:

                p1_points = 3

    if keys[pygame.K_KP_1]:

        if keys[pygame.K_KP_5]:

            if keys[pygame.K_KP_9]:

                p2_points = 3

    going = False        
    winner = ""
    if p1_points == 3:
        goint = True
        # pygame.mixer.Sound.play(S_WIN)
        winner = "Player One Wins!"
        winner = text(winner, font, (0, 0, 0))
        win.blit(winner, (180, 250))
        pygame.display.update()
        time.sleep(3); pygame.quit()
    elif p2_points == 3:
        going = True
        # pygame.mixer.Sound.play(S_WIN)
        winner = "Player Two Wins!"
        winner = text(winner, font, (0, 0, 0))
        win.blit(winner, (180, 250))
        pygame.display.update()
        time.sleep(3); pygame.quit()

    while going:

        pygame.init()

        Clock = pygame.time.Clock()

        #pygame.mixer.music.load("20190724.wav")
        #pygame.mixer.music.play(-1)

        quit = pygame.display.set_mode((800,600))
        quit_prompt = text("Press Q to Quit and Press Enter to Play Again", font2, "white")
        quit.fill((255, 255, 255))
        quit.fill("black")
        quit.blit(quit_prompt, (160, 325))
        pygame.display.update()

        Clock.tick(60) / 1000

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:

            pygame.quit()
 
        elif keys[pygame.K_RETURN]:

            break
            
        p1 = thing(jimbob, 100.0, 350.0, 20.0, 7.5, "player", 0)
        p2 = thing(billy, 600.0, 350.0, 20.0, 7.5, "player", 0)

        p1_points = 0
        p2_points = 0

        reset(Round)

        Round = 1

    fonty = pygame.font.SysFont("arialblack", 20)
    p1_p_display = text(f'P1 Points: {p1_points}', fonty, (0, 0, 0))
    p2_p_display = text(f'P2 Points: {p2_points}', fonty, (0, 0, 0))

    win.blit(p1_p_display, (10, 10))
    win.blit(p2_p_display, (10, 30))

    pygame.display.update()
    dt = clock.tick(60) / 1000
