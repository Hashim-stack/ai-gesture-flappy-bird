import pygame
import random
from settings import *

class Bird:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(BIRD_X, HEIGHT//2))
        self.velocity = 0

    def update(self, jump):
        if jump:
            self.velocity = JUMP_STRENGTH

        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Pipe:
    def __init__(self, image):
        self.image = image
        self.gap = PIPE_GAP
        self.top_height = random.randint(100, 400)

        self.top_rect = pygame.Rect(
            WIDTH,
            0,
            image.get_width(),
            self.top_height
        )

        self.bottom_rect = pygame.Rect(
            WIDTH,
            self.top_height + self.gap,
            image.get_width(),
            HEIGHT
        )

    def update(self):
        self.top_rect.x -= PIPE_SPEED
        self.bottom_rect.x -= PIPE_SPEED

    def draw(self, screen):
        flipped = pygame.transform.flip(self.image, False, True)
        screen.blit(flipped, self.top_rect)
        screen.blit(self.image, self.bottom_rect)

    def off_screen(self):
        return self.top_rect.right < 0


class Game:
    def __init__(self, bird_img, pipe_img, bg_img):
        self.bird = Bird(bird_img)
        self.pipe_img = pipe_img
        self.bg = bg_img

        self.pipes = []
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()

    def spawn_pipe(self):
        now = pygame.time.get_ticks()
        if now - self.last_pipe > PIPE_FREQUENCY:
            self.pipes.append(Pipe(self.pipe_img))
            self.last_pipe = now

    def update(self, jump):
        self.bird.update(jump)
        self.spawn_pipe()

        for pipe in self.pipes:
            pipe.update()

        self.pipes = [p for p in self.pipes if not p.off_screen()]

        self.check_collision()

    def check_collision(self):
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= HEIGHT:
            raise Exception("Game Over")

        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or \
               self.bird.rect.colliderect(pipe.bottom_rect):
                raise Exception("Game Over")

    def draw(self, screen, font):
        screen.blit(self.bg, (0, 0))

        for pipe in self.pipes:
            pipe.draw(screen)

        self.bird.draw(screen)

        score_text = font.render(f"Score: {self.score}", True, (255,255,255))
        screen.blit(score_text, (10,10))
