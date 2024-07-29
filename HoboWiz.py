import pygame 
import random
import time
import sys

boundary = 0
COLOR = (255, 100, 98) 
SURFACE_COLOR = (0, 0, 0) 
WIDTH = 1200
HEIGHT = 800
startx = 300
starty = 600
circle_center = [startx+80, starty+130]
circle_radius=150
numTracks = 0
numTrains = 0
trainWidth = 0
trainY = 100
roundCount = 0
showTime = 5000
startTime = pygame.time.get_ticks()
planeX = 0
planeY = 0
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Character:
    def __init__(self, image, x, y): 
        self.x=x
        self.y=y
        #I cant find a good png for this 
        self.image = pygame.image.load(image).convert_alpha()
        self.positive = random.randint(0,1)==1
        self.vis = True
    def moveRight(self, pixels):
        self.x+=pixels
    def moveLeft(self, pixels):
        self.x-=pixels
    def moveDown(self, pixels):
        self.y+=pixels
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def setx(self,v):
        self.x=v
    def sety(self,v):
        self.y=v
    def setAlpha(self, num):
        self.image.set_alpha(num)
    def positive(self):
        return self.positive
    def setPositive(self, val):
        self.positive=val
    def setVis(self, bol):
        self.vis = bol
    def getVis(self):
        return self.vis

pygame.init()
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 36)
bg_colour = (234, 212, 252)
screen= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Hogwarts Hobo')
screen.fill(bg_colour)
all_sprites_list = pygame.sprite.Group() 
pygame.display.flip()
clock = pygame.time.Clock() 
player = Character("character.png", startx,starty)
randomx = random.randint(200,1000)
hobo1 = Character("hobo.png", randomx ,starty+100)
hobo2 = Character("hobo.png", randomx-100 ,starty+100)
hobo3 = Character("hobo.png", randomx-50 ,starty+150)
hints = ["Hints: "]
mp3_sound = pygame.mixer.Sound("weather.mp3")
train_sounds = pygame.mixer.Sound("trainSounds.mp3")
randomBool = 0
def instructions_page():
    text_font = pygame.font.Font(None, 20)
    while True:
        screen.fill(BLACK)

        # Render text
        intro_text = (
            "Introduction:\n"
            "Welcome to the perilous yet exhilarating world of \"Hobo Tracks: The Railroad Survival Challenge\"! "
            "In this immersive game, players embark on a daring quest to navigate the\n treacherous railroad tracks "
            "near Hogwarts School of Witchcraft and Wizardry. Aspiring Hogwarts students must prove their agility, "
            "wit, and resilience as they face the constant threat\n of oncoming trains, unpredictable weather, and "
            "unreliable information from fellow hobos.\n\n"
            "Set against the backdrop of a dimly lit tunnel exit, players find themselves stranded on the tracks, "
            "seeking refuge from the elements while striving to avoid the imminent danger of\n passing trains. With "
            "multiple tracks to traverse, each with its own timing dynamics, players must make split-second decisions"
            "to jump from track to track in a bid \n to prolong their survival.\n\n"
            "But beware! The railway is fraught with uncertainty. As trains thunder past, players must gauge the "
            "optimal moment to leap to safety, all while contending with the possibility of \n mistimed jumps, unforeseen "
            "obstacles, and the occasional deceitful hobo.\n\n"
            "In \"Hobo Tracks,\" every decision counts. Players must strategize their movements, gather intelligence "
            "from paper plane messengers, and even collaborate with fellow hobos to\n synchronize jumps and maximize "
            "their chances of survival. With randomized patterns including train spawning, "
            "inter-train distances, and hobo population, no two \ngames are ever the same.\n\n"
            "Your objective? To outlast your rivals and emerge as the last hobo standing, all while preserving your "
            "precious health and minimizing the toll of train collisions. Remember, while a \n collision may not spell"
            "immediate doom, each hit diminishes your health and inches you closer to defeat.\n\n"
            "So gather your courage, sharpen your senses, and prepare for the ultimate test of survival in "
            "\"Hobo Tracks: The Railroad Survival Challenge.\" Are you ready to defy the odds and \n prove your mettle "
            "amidst the chaos of the railway? The adventure awaits! (Press escape to return)"
        )

        # Splitting the text into lines
        lines = intro_text.split('\n')

        # Render and blit each line
        for i, line in enumerate(lines):
            text_render = text_font.render(line, True, WHITE)
            screen.blit(text_render, (50, 50 + i * 30))  # Adjust Y position for each line

        pygame.display.flip()


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
def randomGeneration(round):
    global numTrains
    global numTracks 
    global trainWidth
    global randomBool
    # if(round<2):
    #     numTracks = random.randint(3,4)
    #     numTrains = numTracks-2
    #     #airplanesNum = random.randint(1,2)
    
    # elif(round<5):
    #     numTracks = random.randint(5,6)
    #     numTrains = numTracks-2
    # else: 
    #     numTracks = random.randint(3,7)
    #     numTrains = numTracks - random.randint(1,2)
    numTracks = 4
    numTrains = 2
    trainWidth = WIDTH//numTracks
    randomBool = random.randint(0,1)==1
def main_menu():
    global roundCount
    roundCount = 0
    pygame.mixer.stop()
    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # Draw title
        title_text = title_font.render("Hogwarts Hobo", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH/2, 100))
        screen.blit(title_text, title_rect)

        # Draw buttons
        play_button = pygame.Rect(500, 300, 200, 50)
        instructions_button = pygame.Rect(500, 400, 200, 50)
        quit_button = pygame.Rect(500, 500, 200, 50)

        pygame.draw.rect(screen, GRAY, play_button)
        pygame.draw.rect(screen, GRAY, instructions_button)
        pygame.draw.rect(screen, GRAY, quit_button)

        # Check for button hover
        if play_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BLUE, play_button)
        if instructions_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GREEN, instructions_button)
        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, RED, quit_button)

        # Render button text
        play_text = button_font.render("Play", True, BLACK)
        instructions_text = button_font.render("Instructions", True, BLACK)
        quit_text = button_font.render("Quit", True, BLACK)

        screen.blit(play_text, (play_button.x + 50, play_button.y + 15))
        screen.blit(instructions_text, (instructions_button.x + 15, instructions_button.y + 15))
        screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 15))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    while True:
                        randomGeneration(5)
                        preparation_phase(15)
                        countdown_timer(20)
                elif instructions_button.collidepoint(mouse_pos):
                    instructions_page()
                    # Call your instructions function here
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def preparation_phase(seconds):
    mp3_sound.play()
    train_sounds.stop()
    global hints
    hints = ["Hints: "]
    start_time = time.time()
    fade = 5
    num = 255
    ctr = 0
    click = True
    airplanes = []
    hitboxes = []
    positions = []
    information = ["The tracks are dark, though you can probably already tell", 
                    "The surroundings are very loud, even though you can tell already", 
                    "As soon as the trains dissapear, new trains will appear",
                    "Try to stay in the middle of the tracks as the edges are dangerous",
                    "None of the first trains will be at the first track",
                    "There may or may not be hobos that block you"]
    random.shuffle(information)
    ptr = 0
     # Define snowflake properties
    NUM_SNOWFLAKES = 200
    snowflakes = []

    # Generate initial snowflakes
    
    for _ in range(NUM_SNOWFLAKES):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        speed = random.randint(1, 3)
        snowflakes.append([x, y, speed])
    for i in range(3):
        rand = random.randint(0,1200)
        airplane = Character("plane.png", rand, 0)
        airplanes.append(airplane)
        positions.append(rand)
        hitboxes.append(pygame.Rect(positions[i], Character.gety(airplanes[i]), 200, 160))
    
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = seconds - elapsed_time
        planeFade = fade - elapsed_time
        font = pygame.font.Font(None, 36)
        if(remaining_time <= 0):
            break
        if(remaining_time>0):
                        
            for event in pygame.event.get(): 
            
                # Check for QUIT event       
                if event.type == pygame.QUIT: 
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        # Check if mouse click occurred within the character's hitbox
                        for i in range(len(hitboxes)):
                            if hitboxes[i].collidepoint(mouse_pos):
                                if click and planeFade>1:
                                    Character.setVis(airplanes[i], False)
                                    hints.append(information[ptr])
                                    ptr+=1



            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if(Character.getx(player)-20>-80):
                    Character.moveLeft(player, 20)
                    circle_center[0]-=20
            if keys[pygame.K_RIGHT]:
                if(Character.getx(player)+20<1100):
                    Character.moveRight(player, 20)
                    circle_center[0]+=20
                
            screen.fill(SURFACE_COLOR)
            #hobo.draw(screen)

            pygame.draw.circle(screen, (255,255,255), circle_center, circle_radius)
            for i in range(1,numTracks):
                pygame.draw.rect(screen, (255,255,0), (i*(WIDTH//numTracks),0,5, 800))
            player.draw(screen)
            if(num<0):
                num = 0
            else:
                num-=1
            for i in range(len(airplanes)):
                Character.setAlpha(airplanes[i], num)
                if(Character.positive(airplanes[i])):
                    if((Character.getx(airplanes[i])+5<1100)):
                        Character.moveRight(airplanes[i], 5)
                        positions[i]+=5
                        if (Character.gety(airplanes[i])+5<650):
                            Character.moveDown(airplanes[i], 5)
                    else:
                        Character.setPositive(airplanes[i], False)
                else:
                    if((Character.getx(airplanes[i])-5>0)):
                        Character.moveLeft(airplanes[i], 5)
                        positions[i]-=5
                        if (Character.gety(airplanes[i])+5<650):
                            Character.moveDown(airplanes[i], 5)
                    else:
                        Character.setPositive(airplanes[i], True)

                if(planeFade > 1 and Character.getVis(airplanes[i])):
                    hitboxes[i] = pygame.Rect(positions[i], Character.gety(airplanes[i]), 200, 160)
                    pygame.draw.rect(screen, (0,0,0), hitboxes[i])
                    airplanes[i].draw(screen)
            for airplane in airplanes:
                if (Character.getVis(airplane)==False):
                    ctr+=1
            if (ctr==len(airplanes)):
                click = False
            else:
                ctr = 0
                    
            hint_y = 50
            for hint in hints:
                hint_text = font.render(hint, True, (255,255,255))
                hint_rect = hint_text.get_rect(midleft=(10, hint_y))  # Adjust position as needed
                screen.blit(hint_text, hint_rect)
                hint_y += 30  # Increase y-coordinate for the next hint

            for i in range(NUM_SNOWFLAKES):
                snowflakes[i][1] += snowflakes[i][2]  # Move snowflake down by its speed
                if snowflakes[i][1] > HEIGHT:  # If snowflake goes below the screen, reset its position
                    snowflakes[i][1] = random.randint(-10, 0)
                    snowflakes[i][0] = random.randint(0, WIDTH)

                # Draw snowflake
                if randomBool:
                    pygame.draw.circle(screen, WHITE, (snowflakes[i][0], snowflakes[i][1]), 2)
                else:
                    NUM_SNOWFLAKES = 60
                    screen.blit(pygame.image.load("raindrop.png"), (snowflakes[i][0], snowflakes[i][1]))

            text = font.render(f"Time Left: {int(remaining_time)} seconds", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2 - 20, 30))
            screen.blit(text, text_rect) 
            pygame.display.update()
            clock.tick(60)

#make airplane go either left to right or right to left (random int between 1 or 2)
    


def countdown_timer(seconds):
    global randomBool
    global numTracks
    global numTrains
    global trainY
    global roundCount
    train_sounds.set_volume(0.1)
    roundCount+=1
    hp = 100
    lb = -80
    rb = 1100
    hpLost = False
    trains = [-1]
    start_time = time.time()
    trk = -1
    firstTrains=True
    train_sounds.play()
    hoboLeft = True
    location = 150
    # Define snowflake properties
    NUM_SNOWFLAKES = 200
    snowflakes = []
    if(roundCount>=2):
        Character.setx(hobo1,Character.getx(player)-20)
        Character.setx(hobo2,Character.getx(player)-120)
        Character.setx(hobo3,Character.getx(player)-70)
    # Generate initial snowflakes
    if(roundCount>=3):
        if(random.randint(0,1)==1):
            location = 1050
            rb = 1100-trainWidth
        else:
            lb = -80+trainWidth
            
        hobo4 = Character("hobo.png", location ,starty+100)
        hobo5 = Character("hobo.png", location-100 ,starty+100)
        hobo6 = Character("hobo.png", location-50 ,starty+150)
    for _ in range(NUM_SNOWFLAKES):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        speed = random.randint(1, 3)
        snowflakes.append([x, y, speed])
    while (len(trains) != numTrains+1):
        trk = random.randint(0,numTracks-1)
        if trk not in trains:
            trains.append(trk)
    while hp>0:
        elapsed_time = time.time() - start_time
        remaining_time = seconds - elapsed_time
        font = pygame.font.Font(None, 36)
        if remaining_time<=0:
            break
        if remaining_time > 0:
            if(roundCount<2):
                if(hoboLeft):
                    Character.moveLeft(hobo1, 5)
                    Character.moveLeft(hobo2, 5)
                    Character.moveLeft(hobo3, 5)
                    if(Character.getx(hobo1)<40):
                        hoboLeft = False
                else:
                    Character.moveRight(hobo1, 5)
                    Character.moveRight(hobo2, 5)
                    Character.moveRight(hobo3, 5)
                    if(Character.getx(hobo1)>1100):
                        hoboLeft = True
            if(hp==20):
                randomBool=True
                NUM_SNOWFLAKES=200
                snowflakes = []
                for _ in range(NUM_SNOWFLAKES):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    speed = random.randint(1,3)
                    snowflakes.append([x, y, speed])
            if trainY+80<800:
                trainY+=10
            else:
                hpLost = False
                firstTrains=False
                trainY=0
                trains = [-1]
                trk = -1
                while (len(trains) != numTrains+1):
                    trk = random.randint(0,numTracks-1)
                    if trk not in trains:
                        trains.append(trk)
            for event in pygame.event.get(): 
            
                # Check for QUIT event       
                if event.type == pygame.QUIT: 
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if(Character.getx(player)-20>lb):
                    Character.moveLeft(player, 20)
                    circle_center[0]-=20
                    if(roundCount>=2):
                        Character.moveLeft(hobo1, 20)
                        Character.moveLeft(hobo2, 20)
                        Character.moveLeft(hobo3, 20)
            if keys[pygame.K_RIGHT]:
                if(Character.getx(player)+20<rb):
                    Character.moveRight(player, 20)
                    circle_center[0]+=20
                    if(roundCount>=2):
                        Character.moveRight(hobo1, 20)
                        Character.moveRight(hobo2, 20)
                        Character.moveRight(hobo3, 20)
            screen.fill(SURFACE_COLOR)
            #hobo.draw(screen)
            for i in range(NUM_SNOWFLAKES):
                snowflakes[i][1] += snowflakes[i][2]  # Move snowflake down by its speed
                if snowflakes[i][1] > HEIGHT:  # If snowflake goes below the screen, reset its position
                    snowflakes[i][1] = random.randint(-10, 0)
                    snowflakes[i][0] = random.randint(0, WIDTH)

                # Draw snowflake
                if randomBool:
                    pygame.draw.circle(screen, WHITE, (snowflakes[i][0], snowflakes[i][1]), 2)
                else:
                    NUM_SNOWFLAKES = 60
                    screen.blit(pygame.image.load("raindrop.png"), (snowflakes[i][0], snowflakes[i][1]))

            pygame.draw.circle(screen, (255,255,255), circle_center, circle_radius)
            
            #print(numTracks)
            #This creates the tracks on screen
            tracks = []
            for i in range(1,numTracks):
                tracks.append(i)

            
            for i in trains:
                if (i!=-1):
                    if firstTrains:
                        if (i!=0):
                            pygame.draw.rect(screen, (128,128,128), (((i)*WIDTH//numTracks), trainY,trainWidth, 90))
                            pygame.draw.rect(screen, (255,255,0), ((((i)*WIDTH//numTracks)+(1/4*(trainWidth)), trainY+80,trainWidth//30, 20)))
                            pygame.draw.rect(screen, (255,255,0), ((((i)*WIDTH//numTracks)+(3/4*(trainWidth)), trainY+80,trainWidth//30, 20)))
                    else:
                        pygame.draw.rect(screen, (128,128,128), (((i)*WIDTH//numTracks), trainY,trainWidth, 90))
                        pygame.draw.rect(screen, (255,255,0), ((((i)*WIDTH//numTracks)+(1/4*(trainWidth)), trainY+80,trainWidth//30, 20)))
                        pygame.draw.rect(screen, (255,255,0), ((((i)*WIDTH//numTracks)+(3/4*(trainWidth)), trainY+80,trainWidth//30, 20)))
                    if((Character.getx(player)+30 <= ((i)*WIDTH//numTracks)+trainWidth and Character.getx(player) >= ((i)*WIDTH//numTracks)) and not hpLost):
                        if(trainY+80>=Character.gety(player)):
                            hp-=20
                            hpLost = True


            for i in range(1,numTracks):
                pygame.draw.rect(screen, (255,255,0), (i*(WIDTH//numTracks),0,5, 800))

                
            text = font.render(f"Time Left: {int(remaining_time)} seconds", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2 - 20, 30))
            hp_text = font.render(f"HP: {hp}", True, (255,255,255))
            hp_text_rect = hp_text.get_rect(topright=(100, 10))  # Adjust position as needed
            hint_y = 50
            for hint in hints:
                hint_text = font.render(hint, True, (255,255,255))
                hint_rect = hint_text.get_rect(midleft=(10, hint_y))  # Adjust position as needed
                screen.blit(hint_text, hint_rect)
                hint_y += 30  # Increase y-coordinate for the next hint
            # Display HP text
            screen.blit(hp_text, hp_text_rect)
            screen.blit(text, text_rect)  # Blit the text onto the screen
            player.draw(screen)
            hobo1.draw(screen)
            hobo2.draw(screen)
            hobo3.draw(screen)
            if(roundCount>=3):
                hobo4.draw(screen)
                hobo5.draw(screen)
                hobo6.draw(screen)
            pygame.display.update()
            clock.tick(60)
    else:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill the screen with red color
            screen.fill((255,0,0))
            
            # Render the text "You have fainted"
            text = font.render(f"You have fainted, you survived {roundCount} rounds!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text on the screen
            
            # Blit the text onto the screen
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(5000)
            main_menu()
running=True
while running:
    main_menu()
    
        

