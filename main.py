import pygame
import sys
import random
import arrow
import time
import os
from levels import player


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

def process_hits(arrows, pressed_keys, score, lineColor, lastHitTime, currentImage, images):
    for key in pressed_keys:
        if key in LANE_KEY_MAP:
            lane, rotation = LANE_KEY_MAP[key]

        for thisArrow in arrows[:]:
            if (HIT_LINE_Y - ARROW_OUTLINE_HEIGHT < thisArrow.y < HIT_LINE_Y + 50
            and thisArrow.rotation == rotation):
                arrows.remove(thisArrow)
                score += 100
                lineColor = GREEN
                currentImage = images[lane]
                lastHitTime = time.time()
                break
    return score, lineColor, lastHitTime,currentImage

def main():
    running = True
    playing = False
    clock = pygame.time.Clock()
    arrows = []
    spawn_timer = 0
    score = 0
    pressed_keys = []
    won = False
    lineColor = RED
    lastHitTime = 0 
    ArrowClass = arrow.Arrow
    currentImage = None

    images = [
        pygame.image.load(os.path.join('dans-fotos', 'Left-blue.png')),
        pygame.image.load(os.path.join('dans-fotos', 'Down-blue.png')),
        pygame.image.load(os.path.join('dans-fotos', 'Up-blue.png')),
        pygame.image.load(os.path.join('dans-fotos', 'Right-blue.png'))
    ]
    

    numArray = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            handle_input(event, pressed_keys)
            if event.type == pygame.KEYDOWN:
                if event.key in numArray:
                    number = numArray.index(event.key) - 1
                    number %= len(os.listdir('./nummers'))

                    selected_song = f'nummers/{os.listdir("./nummers")[number]}'
                    player.loadSong(selected_song)
                if event.key == pygame.K_SPACE and won:
                    playing = True
                    won = False
                    spawn_timer = 0
                    score = 0
                    arrows = []
                    pressed_keys = []
                    ArrowClass = arrow.Arrow
                    player.playMusic()
                if event.key == pygame.K_SPACE and not playing:
                    playing = True
                    won = False
                    spawn_timer = 0
                    score = 0
                    arrows = []
                    pressed_keys = []  
                    ArrowClass = arrow.Arrow
                    player.playMusic()
                if event.key == pygame.K_SPACE and won:
                    playing = True
                    won = False
                    spawn_timer = 0
                    score = 0
                    arrows = []
                    pressed_keys = []  
                    ArrowClass = arrow.Arrow
                    player.playMusic()
                

        if not playing:
            screen.fill(BLACK)
            text = font.render("Press SPACE to start", True, WHITE)
            nummers = os.listdir('./nummers')
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            for i in range(len(nummers)):
                if ("nummers/"+nummers[i]) == player.source:
                    text = font.render(f"{i+1}. {nummers[i]}", True, GREEN)
                else: 
                    text = font.render(f"{i+1}. {nummers[i]}", True, WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100 +  HEIGHT // 2 + ((text.get_height() - 100) * (-i+1))// 2))
        
              
                
        if playing:
            spawn_timer += clock.get_time()
            tolerance = 0.01 
            dropTime = 1430 # Het duurt 1.34 sec om te vallen
            songEndBuffer = 3 
            for sec in player.beat_times:
                if abs((spawn_timer + dropTime) / 1000 - sec) < tolerance:
                    random.seed(sec) # zorg ervoor dat sequentie van willekeur altijd hetzelfde is bij ieder nummera
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
                if player.beat_times[-1] + songEndBuffer < (spawn_timer + dropTime) / 1000:
                    won = True
                    break
           

            for thisArrow in arrows[:]:
                thisArrow.update()
                if thisArrow.y > HIT_LINE_Y + ARROW_OUTLINE_HEIGHT:
                    arrows.remove(thisArrow)
                    if score - 50 > 0:
                        score -= 50
                
            if not won:
                score, lineColor, lastHitTime, currentImage = process_hits(arrows, pressed_keys, score, lineColor, lastHitTime, currentImage, images)

                if time.time() - lastHitTime >= 0.3:
                    lineColor = RED 

                screen.fill(WHITE)
                
                if currentImage is not None:
                    maxWidth = WIDTH // 2
                    maxHeight = HEIGHT // 2

                    scaleFactor = min(maxWidth / currentImage.get_width(), maxHeight / currentImage.get_height())

                    newWidth = int(currentImage.get_width() * scaleFactor)
                    newHeight = int(currentImage.get_height() * scaleFactor)

                    scaledImage = pygame.transform.smoothscale(currentImage, (newWidth, newHeight))

                    # Blit the scaled image to the center of the screen
                    screen.blit(scaledImage, (WIDTH // 2 - newWidth // 2, HEIGHT // 2 - newHeight // 2))

                for thisArrow in arrows:
                    thisArrow.draw()
                pygame.draw.line(screen, lineColor, (0, HIT_LINE_Y), (WIDTH, HIT_LINE_Y), 2)
                score_text = font.render(f"Score: {score}", True, BLACK)

               

                screen.blit(score_text, (10, 10))
            
            if won: 
                screen.fill(BLACK)
                text = font.render(f"Your score: {score}", True, WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, (HEIGHT // 2 + text.get_height() // 2) + 100))
                text = font.render(f"You scored: {round((score)/(len(player.beat_times)), 1)}%", True, WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2))
                text = font.render("Press SPACE to play again", True, WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
           

        pygame.display.flip()
        clock.tick(60)
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()
    


if __name__ == "__main__":
    main()
