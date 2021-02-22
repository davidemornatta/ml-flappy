import pygame
import sys
import random

WIDTH = 480
HEIGHT = 800


def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 650))
    screen.blit(floor_surface, (floor_x_position + WIDTH, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(WIDTH, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(WIDTH, random_pipe_pos - 200))
    return bottom_pipe, top_pipe


def move_pipes(pipes, i):
    for pipe in pipes:
        pipe_oldx = pipe.centerx
        pipe.centerx -= 3
        if pipe_oldx > 80 and pipe.centerx <= 80:
            i += 1
    return pipes, i


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -70 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(80, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH / 2, 80))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH / 2, 80))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {high_score}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(WIDTH / 2, 120))
        screen.blit(high_score_surface, high_score_rect)


def update_score(s, hs):
    if s > hs:
        hs = s
    return hs


pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# Game Variables
gravity = 0.20
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (WIDTH, int(HEIGHT / 3)))
floor_x_position = 0

bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap,
                                       (int(bird_downflap.get_width() * 1.5), int(bird_downflap.get_height() * 1.5)))
bird_midflap = pygame.transform.scale(bird_midflap,
                                      (int(bird_midflap.get_width() * 1.5), int(bird_midflap.get_height() * 1.5)))
bird_upflap = pygame.transform.scale(bird_upflap,
                                     (int(bird_upflap.get_width() * 1.5), int(bird_upflap.get_height() * 1.5)))
bird_frames = [bird_downflap, bird_upflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(80, HEIGHT / 3))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface,
                                      (int(pipe_surface.get_width() * 1.5), int(pipe_surface.get_height() * 1.5)))
pipe_list = []
pipe_height = [400, 500, 600]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (
    int(game_over_surface.get_width() * 1.5), int(game_over_surface.get_height() * 1.5)))
game_over_rect = game_over_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (80, HEIGHT / 3)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list, score = move_pipes(pipe_list, score)
        draw_pipes(pipe_list)

        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_position -= 1
    draw_floor()
    if floor_x_position < -WIDTH:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(120)
