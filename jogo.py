import pygame
import random

# Inicialização do pygame
pygame.init()

# Inicialização do mixer para música
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)  # Ajuste o volume conforme necessário
pygame.mixer.music.play(-1)  # Reproduz a música em loop

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definindo o tamanho da tela
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Ajustando as propriedades da raquete
paddle_width = 30  # Aumentando a largura da raquete
paddle_height = 150  # Aumentando a altura da raquete
paddle_speed = 6  # Velocidade da raquete

# Carregando imagens das raquetes
paddle1_image = pygame.image.load('paddle1.png')
paddle2_image = pygame.image.load('paddle2.png')

# Redimensionando as imagens das raquetes
paddle1_image = pygame.transform.scale(paddle1_image, (paddle_width, paddle_height))
paddle2_image = pygame.transform.scale(paddle2_image, (paddle_width, paddle_height))

# Definindo as propriedades da bola
ball_radius = 8
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = 4 * random.choice((1, -1))

# Posições iniciais
paddle1_y = HEIGHT // 2 - paddle_height // 2
paddle2_y = HEIGHT // 2 - paddle_height // 2
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

# Pontuação
score1 = 0
score2 = 0

# Controle do jogo
clock = pygame.time.Clock()
running = True
playing = False
single_player = False

# Função para desenhar os objetos na tela
def draw_objects():
    screen.fill(BLACK)
    screen.blit(paddle1_image, (10, paddle1_y))
    screen.blit(paddle2_image, (WIDTH - paddle_width - 10, paddle2_y))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)
    draw_score()
    pygame.display.flip()

# Função para desenhar a pontuação
def draw_score():
    font = pygame.font.Font(None, 74)
    text = font.render(str(score1), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(score2), 1, WHITE)
    screen.blit(text, (510, 10))

# Função para IA do jogador 2
def ai_opponent():
    global paddle2_y
    if paddle2_y + paddle_height // 2 < ball_y:
        paddle2_y += paddle_speed
    elif paddle2_y + paddle_height // 2 > ball_y:
        paddle2_y -= paddle_speed

# Função para desenhar o menu inicial
def draw_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title_text = font.render("Pong", 1, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    font = pygame.font.Font(None, 36)
    single_player_text = font.render("Single Player (vs Bot)", 1, WHITE)
    single_player_rect = single_player_text.get_rect(center=(WIDTH // 2, 300))
    screen.blit(single_player_text, single_player_rect)

    multiplayer_text = font.render("Multiplayer (2 Players)", 1, WHITE)
    multiplayer_rect = multiplayer_text.get_rect(center=(WIDTH // 2, 400))
    screen.blit(multiplayer_text, multiplayer_rect)

    pygame.display.flip()

    return single_player_rect, multiplayer_rect

# Função para verificar cliques nos botões do menu
def handle_menu_click(mouse_pos, single_player_rect, multiplayer_rect):
    global playing, single_player
    if single_player_rect.collidepoint(mouse_pos):
        single_player = True
        playing = True
    elif multiplayer_rect.collidepoint(mouse_pos):
        single_player = False
        playing = True

# Loop principal do jogo
while running:
    if not playing:
        single_player_rect, multiplayer_rect = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not playing:
            handle_menu_click(event.pos, single_player_rect, multiplayer_rect)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and playing:
                playing = False  # Volta para o menu principal

    if playing:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s] and paddle1_y < HEIGHT - paddle_height:
            paddle1_y += paddle_speed

        if single_player:
            ai_opponent()
        else:
            if keys[pygame.K_UP] and paddle2_y > 0:
                paddle2_y -= paddle_speed
            if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - paddle_height:
                paddle2_y += paddle_speed

        # Movimentação da bola
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Colisão com as paredes
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
            ball_speed_y *= -1

        # Colisão com as raquetes
        if (ball_x - ball_radius <= 20 and paddle1_y < ball_y < paddle1_y + paddle_height) or \
           (ball_x + ball_radius >= WIDTH - 20 and paddle2_y < ball_y < paddle2_y + paddle_height):
            ball_speed_x *= -1

        # Reiniciar a bola se ela sair da tela e atualizar a pontuação
        if ball_x < 0:
            score2 += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = 4 * random.choice((1, -1))
            ball_speed_y = 4 * random.choice((1, -1))
        if ball_x > WIDTH:
            score1 += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = 4 * random.choice((1, -1))
            ball_speed_y = 4 * random.choice((1, -1))

        draw_objects()
        clock.tick(60)

pygame.quit()
