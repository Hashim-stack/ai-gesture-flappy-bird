import pygame
import cv2
from settings import *
from game import Game
from gesture_control import GestureController

def cv2_to_pygame(frame):
    frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame.swapaxes(0, 1)
    return pygame.surfarray.make_surface(frame)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gesture Flappy Bird")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    bird_img = pygame.image.load("assets/bird.png").convert_alpha()
    pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()
    bg_img = pygame.image.load("assets/background.png").convert()

    bird_img = pygame.transform.scale(bird_img, (60, 45))
    pipe_img = pygame.transform.scale(pipe_img, (80, 500))
    bg_img = pygame.transform.scale(bg_img, (GAME_WIDTH, GAME_HEIGHT))

    game = Game(bird_img, pipe_img, bg_img)
    gesture = GestureController()

    running = True

    try:
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            frame, jump = gesture.get_frame_and_gesture()

            # Update game
            game.update(jump)

            # Draw background (right side)
            screen.blit(bg_img, (CAM_WIDTH, 0))

            # Draw webcam (left side)
            if frame is not None:
                cam_surface = cv2_to_pygame(frame)
                screen.blit(cam_surface, (0, 0))

            # Draw pipes & bird
            for pipe in game.pipes:
                pipe.draw(screen)
            game.bird.draw(screen)

            # Score
            score_text = font.render(f"Score: {game.score}", True, (255,255,255))
            screen.blit(score_text, (CAM_WIDTH + 10, 10))

            pygame.display.update()

    except Exception:
        print("GAME OVER")

    gesture.release()
    pygame.quit()


if __name__ == "__main__":
    main()
