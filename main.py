import pygame
import sys
import random
import arrow
import levels
import time

pygame.init()

pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
LANE_COUNT = 4
LANE_WIDTH = WIDTH // LANE_COUNT
HIT_LINE_Y = HEIGHT - 100
ARROW_OUTLINE_HEIGHT = 50
SPAWNRATE = 500
GLOBAL_GRAVITY = 5

# kleuren
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Izza's Rhythm Spel")
font = pygame.font.Font(None, 36)

LANE_KEY_MAP = {
    pygame.K_LEFT: (0, 0),
    pygame.K_DOWN: (1, 90),
    pygame.K_UP: (2, -90),
    pygame.K_RIGHT: (3, 180),
}


def handle_input(event, pressed_keys):
    if event.type == pygame.KEYDOWN:
        pressed_keys.append(event.key)
    elif event.type == pygame.KEYUP:
        if event.key in pressed_keys:
            pressed_keys.remove(event.key)


def process_hits(arrows, pressed_keys, score):
    for key in pressed_keys:
        if key in LANE_KEY_MAP:
            lane, rotation = LANE_KEY_MAP[key]
            for thisArrow in arrows[:]:
                if (HIT_LINE_Y - ARROW_OUTLINE_HEIGHT < thisArrow.y <
                        HIT_LINE_Y + 50 and thisArrow.rotation == rotation):
                    arrows.remove(thisArrow)
                    score += 100
                    break
    return score


def main():
    running = True
    clock = pygame.time.Clock()
    arrows = []
    spawn_timer = 0
    score = 0
    pressed_keys = []

    ArrowClass = arrow.Arrow

    time.sleep(10)
    
    levels.playMusic()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_input(event, pressed_keys)

        spawn_timer += clock.get_time()
        tolerance = 0.01 
        dropTime = 1430 # Het duurt 1.43 sec om te vallen
        for sec in levels.beat_times:
            if abs((spawn_timer + dropTime) / 1000 - sec) < tolerance:
                random.seed(sec) # zorg ervoor dat sequentie van willekeur altijd hetzelfde is bij ieder nummer
                lane_index = random.randint(0, LANE_COUNT - 1)
                rotation = [90, 180, 0, -90][lane_index]
                arrows.append(
                    ArrowClass(
                        screen,
                        x=lane_index * LANE_WIDTH + LANE_WIDTH // 2 - 25,
                        y=0,
                        width=50,
                        height=50,
                        gravity=GLOBAL_GRAVITY,
                        rotation=rotation,
                    ))

        for thisArrow in arrows[:]:
            thisArrow.update()
            if thisArrow.y > HIT_LINE_Y + ARROW_OUTLINE_HEIGHT:
                arrows.remove(thisArrow)
                score -= 50

        score = process_hits(arrows, pressed_keys, score)

        screen.fill(WHITE)
        for thisArrow in arrows:
            thisArrow.draw()

        pygame.draw.line(screen, RED, (0, HIT_LINE_Y), (WIDTH, HIT_LINE_Y), 2)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.quit()
    pygame.quit()
    sys.exit()
    


if __name__ == "__main__":
    main()
