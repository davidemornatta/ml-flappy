import random
import pygame
import numpy as np
from gym import spaces

WIDTH = 480
HEIGHT = 800


class FlappyEnv:

    def __init__(self):
        # Game Variables
        self.gravity = 0.20
        self.bird_movement = 0
        self.score = 0
        self.high_score = 0
        self.pipe_list = []
        self.pipe_height = [400, 500, 600]

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('04B_19.ttf', 40)
        self.bg_surface = pygame.image.load('assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface, (WIDTH, HEIGHT))

        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (WIDTH, int(HEIGHT / 3)))
        self.floor_x_position = 0

        self.bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
        self.bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
        self.bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
        self.bird_downflap = pygame.transform.scale(self.bird_downflap,
                                                    (
                                                        int(self.bird_downflap.get_width() * 1.5),
                                                        int(self.bird_downflap.get_height() * 1.5)))
        self.bird_midflap = pygame.transform.scale(self.bird_midflap,
                                                   (int(self.bird_midflap.get_width() * 1.5),
                                                    int(self.bird_midflap.get_height() * 1.5)))
        self.bird_upflap = pygame.transform.scale(self.bird_upflap,
                                                  (int(self.bird_upflap.get_width() * 1.5),
                                                   int(self.bird_upflap.get_height() * 1.5)))
        self.bird_frames = [self.bird_downflap, self.bird_upflap, self.bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(80, HEIGHT / 3))
        self.pipe_surface = pygame.image.load('assets/pipe-green.png')
        self.pipe_surface = pygame.transform.scale(self.pipe_surface,
                                                   (int(self.pipe_surface.get_width() * 1.5),
                                                    int(self.pipe_surface.get_height() * 1.5)))

        self.action_space = spaces.Discrete(2)
        self.done = False

        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)

    def draw_floor(self):
        self.screen.blit(self.floor_surface, (self.floor_x_position, 650))
        self.screen.blit(self.floor_surface, (self.floor_x_position + WIDTH, 650))

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(WIDTH, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(WIDTH, random_pipe_pos - 200))
        return bottom_pipe, top_pipe

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 3

    def draw_pipes(self):
        for pipe in self.pipe_list:
            if pipe.bottom >= HEIGHT:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def check_collision(self):
        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                return True
        if self.bird_rect.top <= -70 or self.bird_rect.bottom >= 650:
            return True
        return False

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 2, 1)
        return new_bird

    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(80, self.bird_rect.centery))
        return new_bird, new_bird_rect

    def score_display(self):
        score_surface = self.game_font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH / 2, 80))
        self.screen.blit(score_surface, score_rect)

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self):
        self.pipe_list.clear()
        self.bird_rect.center = (80, HEIGHT / 3)
        self.bird_movement = 0
        self.score = 0

    def render(self):
        self.screen.blit(self.bg_surface, (0, 0))
        rotated_bird = self.rotate_bird(self.bird_surface)
        self.screen.blit(rotated_bird, self.bird_rect)
        self.draw_pipes()
        self.score_display()
        # Floor
        self.floor_x_position -= 1
        self.draw_floor()
        if self.floor_x_position < -WIDTH:
            self.floor_x_position = 0

        self.clock.tick(120)
        pygame.display.update()

    def step(self, action):
        if action == 1:
            self.bird_movement = -7

        for event in pygame.event.get():
            if event.type == self.SPAWNPIPE:
                self.pipe_list.extend(self.create_pipe())
                if len(self.pipe_list) > 2:
                    self.pipe_list.pop(0)

            if event.type == self.BIRDFLAP:
                if self.bird_index < 2:
                    self.bird_index += 1
                else:
                    self.bird_index = 0
                self.bird_surface, self.bird_rect = self.bird_animation()

        # Bird
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

        done = self.check_collision()
        if done:
            reward = 0
        else:
            reward = 1
            self.score += 1

        # Pipes
        self.move_pipes()

        if len(self.pipe_list) > 0:
            state = (self.bird_rect.centery, self.bird_movement, self.pipe_list[0].centerx, self.pipe_list[0].centery)
        else:
            state = (self.bird_rect.centery, self.bird_movement, WIDTH, 0)

        return np.array(state), reward, done
