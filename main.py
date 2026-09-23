import pygame
import random 
import asyncio
import sys

pygame.init()
WIDTH = 800
HEIGHT = 800
BACKGROUND_COLOR = (255, 209, 220)
BUTTON_COLOR = (70,130, 180)
SCREEN_COLOR = (255, 209, 220)
MORE_COLOR = (56, 21, 56)

button_rect = pygame.Rect(120, 150, 160, 50)
endb_rect = pygame.Rect(70, 135, 260, 50)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project 1 | Cupcake Collector")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)
big_font =  pygame.font.SysFont(None, 90)

async def main():
    
    intro = True
    end = False

    #load player and the cupcake assest
    player_image = pygame.image.load("assets/player.png").convert_alpha()
    player_image = pygame.transform.scale(
        player_image,
        (50, 50)
    )

    cupcake_image = pygame.image.load(
        "assets/cupcake.png"
    ).convert_alpha()

    cupcake_image = pygame.transform.scale(
        cupcake_image,
        (30, 30)
    )

    #important vars related to character 
    player_x = 50
    player_y = 300
    player_dy = 0
    gravity = 0.5
    jump_speed = -10
    on_ground = True
    score = 0
    running = True

    #platform
    platforms = [
        pygame.Rect(0, 350, 600, 40),
        pygame.Rect(100, 270, 150, 20),
        pygame.Rect(350, 220, 150, 20),
        pygame.Rect(600, 600, 150, 20),
        pygame.Rect(250, 700, 200, 20)
    ]

    #cupcake (RANDOMIZED)

    cupcakes = []

    for i in range(20):
        x = random.randint(0, 780)
        y = random.randint(0, 780)
        cupcakes.append(pygame.Rect(x,y, 30,30))
        
    while intro:
        screen.fill(SCREEN_COLOR)
        title = big_font.render('Cupcake Collector', True, (119, 71, 88))
        title_rect = title.get_rect(center =(WIDTH//2, HEIGHT//2 - 80))
        screen.blit(title, title_rect)
        
        button_rect.center = (WIDTH//2, HEIGHT//2 + 20)
        pygame.draw.rect(screen, (255, 192, 203), button_rect)
        button_text = font.render("Start", True, (119, 71, 88))
        button_text_rect = button_text.get_rect(center= button_rect.center)
        screen.blit(button_text, button_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        intro = False
                        
        pygame.display.update()




    while running:
        
        screen.fill(BACKGROUND_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if len(cupcakes) == 0:
            running = False 
            end = True
        #character move
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= 5

        if keys[pygame.K_RIGHT]:
            player_x += 5
        
        if keys[pygame.K_UP] and on_ground:
            player_dy = jump_speed
            on_ground = False
            
        if player_x <0: 
            player_x = 0
        if player_x > WIDTH - 50:
            player_x = WIDTH - 50
            
        player_dy += gravity
        player_y += player_dy

        if player_y >= HEIGHT:
            running = False 
            end = True
            
        if player_y >= HEIGHT:
            player_y = HEIGHT - 50
            player_dy = 0
            on_ground = True
        

            
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        
        on_ground = False 
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_dy >0:
                    player_y = platform.top - 50
                    player_dy =0
                    on_ground = True
        


        player_rect = pygame.Rect(
            player_x,
            player_y,
            50,
            50
        )
        
        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)
                score += 1
            
        for platform in platforms: 
            pygame.draw.rect(screen, MORE_COLOR, platform)
            
        for cupcake in cupcakes:
            screen.blit(
                cupcake_image,
                (cupcake.x, cupcake.y)
            )
            
        screen.blit(player_image, (player_x, player_y))
        
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


    while end:
        screen.fill(BACKGROUND_COLOR)
        endb_rect.center =(WIDTH//2, HEIGHT//2 + 100)
        pygame.draw.rect(screen, (255, 192, 203), endb_rect)
        end_text = big_font.render("Game Over", True, (119, 71, 88))
        end_rect = end_text.get_rect(center =(WIDTH//2, HEIGHT//2 -90))
        screen.blit(end_text, end_rect)
        
        
        score_text = font.render(f"Score: {score}", True, (119, 71, 88))
        score_rect = score_text.get_rect(center =(WIDTH//2, HEIGHT//2 + 90))
        screen.blit(score_text, score_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
        pygame.display.update()
        await asyncio.sleep(0)


    pygame.quit()
    sys.exit()
asyncio.run(main())

        