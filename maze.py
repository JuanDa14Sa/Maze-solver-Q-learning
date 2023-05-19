import pygame

width, height = 550, 550
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

fps = 60

grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 2]
]



def draw_window(color=(0, 0, 0)):
    win.fill(color)
    draw_rectangles()
    

def draw_rectangles():
    for i in range(11):
        for j in range(11):
            if grid[j][i] == 1:
                color = (255, 255, 255)
            elif grid[j][i] == 0:
                color = (255, 0, 0)
            elif grid[j][i] == 2:
                color = (0, 255, 0)
            pygame.draw.rect(win, color, (i*50, j*50, 48, 48), 0)
        

def main():
    x_pos = 25
    y_pos = 25
    clock = pygame.time.Clock()
    run = True
    pygame.draw.circle(win, (0, 0, 255), (x_pos, y_pos), 20, 0)
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
       
        draw_window()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] :
            x_pos -= 50
        if keys[pygame.K_RIGHT] :
            x_pos += 50
        if keys[pygame.K_UP] :
            y_pos -= 50
        if keys[pygame.K_DOWN] :
            y_pos += 50
        pygame.draw.circle(win, (0, 0, 255), (x_pos, y_pos), 20, 0)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()