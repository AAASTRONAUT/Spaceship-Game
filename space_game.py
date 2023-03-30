import pygame
import os
pygame.font.init()
pygame.mixer.init()

CLOCK = pygame.time.Clock()
FPS = 60
WHITE = (255 ,255 , 255)
BLACK = (0,0,0)
RED = (255 , 0 , 0)
YELLOW = (255 , 255 , 0)
WIDTH , HEIGHT = 1200 , 800
#spaceship constants
INIT_POSITION_RED , INIT_POSITION_YELLOW = [1000 , 400] , [200 , 400]
SHIP_WIDTH = 100
SHIP_HEIGHT = 82.6
VELOCITY = 8

#fonts
HEALTH_FONT = pygame.font.SysFont('comicsans' , 40)
WINNER_FONT = pygame.font.SysFont('comicsans' , 200)

#sounds
SHOOT_SOUND = pygame.mixer.Sound(os.path.join('space_game_assets' , 'fire.mp3'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('space_game_assets' , 'hit.mp3'))

#bullet constants
B_VEL = 15
MAX_BULLETS = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2 - 5 , 0 , 10 , HEIGHT)
game_view = pygame.display.set_mode((WIDTH , HEIGHT))

RED_SHIP_IMAGE = pygame.image.load(os.path.join('space_game_assets', 'spaceship_red.png'))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMAGE , (SHIP_WIDTH , SHIP_HEIGHT)) , 270)
YELLOW_SHIP_IMAGE = pygame.image.load(os.path.join('space_game_assets', 'spaceship_yellow.png'))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_IMAGE , (SHIP_WIDTH , SHIP_HEIGHT)) , 90)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space_game_assets' ,'space.png')) , (WIDTH , HEIGHT))

def shoot_bullets(red_bullet , yellow_bullet , red , yellow):
    for bullet in yellow_bullet:
        bullet.x += B_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullet.remove(bullet)

    for bullet in red_bullet:
        bullet.x -= B_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)

def create_env(red , yellow , red_bullet , yellow_bullet , red_health , yellow_health):
    game_view.blit(SPACE , (0,0))
    pygame.draw.rect(game_view , BLACK , BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {red_health}" , 1 , WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}" , 1 , WHITE)

    game_view.blit(red_health_text , (WIDTH - red_health_text.get_width() - 10 , 10))
    game_view.blit(yellow_health_text , (10 , 10))

    game_view.blit(RED_SHIP , (red.x , red.y))
    game_view.blit(YELLOW_SHIP , (yellow.x , yellow.y))
    for bullet in red_bullet:
        pygame.draw.rect(game_view , RED , bullet)
    
    for bullet in yellow_bullet:
        pygame.draw.rect(game_view , YELLOW , bullet)
    pygame.display.update()

def draw_winner(winner_text):
    winner_text_object = WINNER_FONT.render(winner_text , 1 , WHITE)
    game_view.blit(winner_text_object , (WIDTH/2 - winner_text_object.get_width()/2 , HEIGHT/2 - winner_text_object.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def move_yellow_ship(keys , yellow):
    if keys[pygame.K_a] and yellow.x - VELOCITY > -5:
        yellow.x -= VELOCITY
    if keys[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x + 20: 
        yellow.x += VELOCITY
    if keys[pygame.K_w] and yellow.y - VELOCITY > -5:
        yellow.y -= VELOCITY
    if keys[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 20:
        yellow.y += VELOCITY

def move_red_ship(keys , red):
    if keys[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if keys[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH +25:
        red.x += VELOCITY
    if keys[pygame.K_UP] and red.y - VELOCITY > -5:
        red.y -= VELOCITY
    if keys[pygame.K_DOWN] and red.y + VELOCITY + red.width < HEIGHT:
        red.y += VELOCITY  

def main():
    red = pygame.Rect(INIT_POSITION_RED[0] , INIT_POSITION_RED[1] , SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(INIT_POSITION_YELLOW[0] , INIT_POSITION_YELLOW[1] , SHIP_WIDTH , SHIP_HEIGHT)
    
    red_health = 10
    yellow_health = 10 

    yellow_bullet = []
    red_bullet = []
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullet) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width , yellow.y + yellow.height//2 + 5, 10 , 5)
                    yellow_bullet.append(bullet)
                    SHOOT_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullet) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 +5 , 10 , 5)
                    red_bullet.append(bullet)
                    SHOOT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()
                
        winner_text = " "
        if red_health == 0:
            winner_text = "Yellow Wins!"
        elif yellow_health == 0:
            winner_text = "Red Wins!"
        if winner_text != " ":
            draw_winner(winner_text)
            break
        
        keys = pygame.key.get_pressed()
        move_yellow_ship(keys , yellow)
        move_red_ship(keys , red)
        shoot_bullets(red_bullet , yellow_bullet , red , yellow)
        create_env(red , yellow , red_bullet , yellow_bullet , red_health , yellow_health)
        CLOCK.tick(FPS)

    main()

if __name__ == "__main__":
    main()