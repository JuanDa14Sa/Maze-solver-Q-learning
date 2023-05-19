import pygame
import random
import numpy as np

width, height = 500, 500
win = pygame.display.set_mode((width, height))


fps = 1

grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 2]
]

actions = ['up', 'down', 'left', 'right']
q_table = np.zeros((10*10,4))
epsilon = 0.9
alpha = 0.1
gamma = 0.6

def draw_window(color=(0, 0, 0)):
    win.fill(color)
    draw_rectangles()
    

def draw_rectangles():
    for i in range(10):
        for j in range(10):
            if grid[j][i] == 1:
                color = (255, 255, 255)
            elif grid[j][i] == 0:
                color = (255, 0, 0)
            elif grid[j][i] == 2:
                color = (0, 255, 0)
            pygame.draw.rect(win, color, (i*50, j*50, 48, 48), 0)
        
def take_action(state):
   if random.random() < epsilon:
        return random.choice(actions)
   else:
        return np.argmax(q_table[state])
   
def update_q_table(state, action, reward, next_state):  
    q_table[state][actions.index(action)] += alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state][actions.index(action)])

def main():
    x_pos = 25
    y_pos = 25
    clock = pygame.time.Clock()
    run = True
    pygame.draw.circle(win, (0, 0, 255), (x_pos, y_pos), 20, 0)
    episode = 0
    state = 0

    while run:
        clock.tick(fps)
        pygame.display.set_caption(f"Maze Game - Episode {episode}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
       
        draw_window()
        action = take_action(state)
        print(action)

        if action=='left' and (x_pos > 25):
            x_pos -= 50
        if action=='right' and (x_pos < 525) :
            x_pos += 50
        if action=='up' and (y_pos > 25) :
            y_pos -= 50
        if action=='down' and (y_pos < 525):
            y_pos += 50

        pygame.draw.circle(win, (0, 0, 255), (x_pos, y_pos), 20, 0)
        pygame.display.flip()
        if grid[y_pos//50][x_pos//50] == 0:
            x_pos = 25
            y_pos = 25
            episode += 1
            reward = -1
            next_state = 0          
        if grid[y_pos//50][x_pos//50] == 2: 
            x_pos = 25
            y_pos = 25
            episode += 1
            reward = 1
            next_state = 0
        else:
            reward = 0
            next_state = y_pos//50 + x_pos//50
        update_q_table(state, action, reward, next_state)
        state = next_state  
                        
    pygame.quit()

if __name__ == "__main__":
    main()