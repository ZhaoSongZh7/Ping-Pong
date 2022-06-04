import pygame
from sys import exit

def player1_score_func():
    player1_score_render = score_font.render(f'Player 1 Score: {player1_score}', False, (255, 255, 255))
    screen.blit(player1_score_render, (100, 100))

def player2_score_func():
    player2_score_render = score_font.render(f'Player 2 Score: {player2_score}', False, (255, 255, 255))
    screen.blit(player2_score_render, (650, 100))

def starting_text_func():
    starting_text_render = score_font.render(f'PRESS ANY KEY TO START', False, (255, 255, 255))
    screen.blit(starting_text_render, (315, 230))

def continue_text_func():
    continue_text = score_font.render(f'PRESS ANY KEY TO CONTINUE', False, (255, 255, 255))
    screen.blit(continue_text, (315, 230))

pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fast Pong V2')
icon = pygame.image.load('C:/Users/Owner/Downloads/pingpongicon.png')
pygame.display.set_icon(icon)
game_active = False
game_active2 = True

# Sounds
paddle_pong_sfx = pygame.mixer.Sound('C:/Users/Owner/Downloads/Paddle Pong SFX.wav')
wall_pong_sfx = pygame.mixer.Sound('C:/Users/Owner/Downloads/Wall Pong SFX.wav')
score_pong_sfx = pygame.mixer.Sound('C:/Users/Owner/Downloads/Score Pong SFX.wav')

# Score Font
player1_score = 0
player2_score = 0
score_font = pygame.font.Font('C:/Users/Owner/Downloads/Pixeltype.ttf', 50)

# Rectangles
player1 = pygame.Rect(20, 200, 15, 140)
player1_y_change = 0

player2 = pygame.Rect(965, 200, 15, 140)
player2_y_change = 0

ballX = 485
ballY = 285
ball = pygame.Rect(485, 285, 30, 30)
ball_x_change = 0.6
ball_y_change = 0.6

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            game_active = True
            if event.key == pygame.K_r:
                game_active = False
                game_active2 = True
                player1_score = 0
                player2_score = 0
                player1.x, player1.y, player2.x, player2.y = 20, 200, 965, 200
                ballX, ballY = 485, 285
            if event.key == pygame.K_w:
                player1_y_change = -1
            if event.key == pygame.K_s:
                player1_y_change = 1
            if event.key == pygame.K_i:
                player2_y_change = -1
            if event.key == pygame.K_k:
                player2_y_change = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1_y_change = 0
            if event.key == pygame.K_i or event.key == pygame.K_k:
                player2_y_change = 0

    # Player 1 Boundaries
    if game_active:
        player1.y += player1_y_change
        if player1.y <= 10:
            player1.y = 10
        elif player1.y >= 450:
            player1.y = 450
        
        # Player 2 Boundaries
        player2.y += player2_y_change
        if player2.y <= 10:
            player2.y = 10
        elif player2.y >= 450:
            player2.y = 450
        
        # Ball Boundaries
        ballX += ball_x_change
        ballY += ball_y_change
        ball.x = round(ballX)
        ball.y = round(ballY)
        if ball.y <= 0 or ball.y >= 570:
            ball_y_change *= -1
            wall_pong_sfx.play()

        elif ball.x < 0:
            ballX = width/2 - 15
            ballY = height/2 - 15
            player2_score += 1
            score_pong_sfx.play()
            game_active = False
            game_active2 = False

        elif ball.x > 970:
            ballX = width/2 - 15
            ballY = height/2 - 15
            player1_score += 1
            score_pong_sfx.play()
            game_active = False
            game_active2 = False

        # Collision
        collide_status = False
        if ball.colliderect(player1) and ball_x_change < 0:
            if abs(ball.left - player1.right) < 10:
                ball_x_change *= -1
                collide_status = True
            elif abs(ball.bottom - player1.top) < 10 and ball_y_change > 0:
                ball_y_change *= -1
            elif abs(ball.top - player1.bottom) < 10 and ball_y_change < 0:
                ball_y_change *= -1
        
        if ball.colliderect(player2) and ball_x_change > 0:
            if abs(ball.right - player2.left) < 10:
                ball_x_change *= -1
                collide_status = True
            elif abs(ball.bottom - player2.top) < 10 and ball_y_change > 0:
                ball_y_change *= -1
            elif abs(ball.top - player2.bottom) < 10 and ball_y_change < 0:
                ball_y_change *= -1

        if collide_status == True:
            paddle_pong_sfx.play()
            collide_status = False

    pygame.draw.aaline(screen, (200, 200, 200), (width/2, 0), (width/2, height))
    pygame.draw.rect(screen, (200, 200, 200), (player1), border_radius=20)
    pygame.draw.rect(screen, (200, 200, 200), (player2), border_radius=20)
    pygame.draw.ellipse(screen, (200, 200, 200), (ball))
    if game_active:
        player1_score_func()
        player2_score_func()
    elif game_active == False and game_active2 == True:
        starting_text_func()
        ball.x = 485
        ball.y = 285
    elif game_active == False and game_active2 == False:
        continue_text_func()
        ball.x = 485
        ball.y = 285
        player1_score_func()
        player2_score_func()

    pygame.display.flip()