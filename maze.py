import pygame
import random
import numpy as np
np.random.seed(0)
#random.seed(0)
size = 4
width = size * 50
height = size * 50
win = pygame.display.set_mode((width, height))
fps = 60

def create_grid(size):
    grid = np.random.choice([0, 1], (size,size), p=[.2, .8])
    goal_x = random.randint(0, size-1)
    goal_y = random.randint(0, size-1)
    grid[goal_y][goal_x] = 2
    return grid

grid = create_grid(size)
actions = ['up', 'down', 'left', 'right']
q_table = np.zeros((size*size,4))
max_epsilon = 1.0  # Exploration probability at start
min_epsilon = 0.05  # Minimum exploration probability
decay_rate = 0.0125  # Exponential decay rate for exploration prob
alpha = 0.7
gamma = 0.95

def get_epsilon(episode):
    return min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

def draw_window(win, grid):
    win.fill((0,0,0))
    draw_rectangles(win, grid)
    

def draw_rectangles(win, grid):
    size = len(grid)
    for i in range(size):
        for j in range(size):
            if grid[j][i] == 1:
                color = (255, 255, 255)
            elif grid[j][i] == 0:
                color = (255, 0, 0)
            elif grid[j][i] == 2:
                color = (0, 255, 0)
            pygame.draw.rect(win, color, (i*50, j*50, 48, 48), 0)
        
def take_action(state, epsilon):
   if random.random() < epsilon:
        return random.choice(actions)
   else:
        return actions[np.argmax(q_table[state])]
   
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
    steps = 0
    max_steps =10
    wins = 0
    max_episodes = 500
    while run & (episode < max_episodes):
        clock.tick(fps)
        epsilon = get_epsilon(episode)
        print(epsilon)
        pygame.display.set_caption(f"Maze Game - Episode {episode}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
       
        draw_window(win, grid)
        action = take_action(state, epsilon)
        #print(action)

        if action=='left' and (x_pos > 25):
            x_pos -= 50
        elif action=='right' and (x_pos < width-25) :
            x_pos += 50
        elif action=='up' and (y_pos > 25) :
            y_pos -= 50
        elif action=='down' and (y_pos < height-25):
            y_pos += 50
        steps += 1

        if steps > max_steps:
            x_pos = 25
            y_pos = 25
            episode += 1
            steps = 0
            next_state = 0
            reward = -1
            print(f"Episode {episode} finished after {max_steps} steps")

        pygame.draw.circle(win, (0, 0, 255), (x_pos, y_pos), 20, 0)
        pygame.display.flip()
        if grid[y_pos//50][x_pos//50] == 0:
            x_pos = 25
            y_pos = 25
            episode += 1
            reward = 0
            next_state = 0          
        if grid[y_pos//50][x_pos//50] == 2: 
            x_pos = 25
            y_pos = 25
            episode += 1
            reward = 1
            next_state = 0
            wins += 1
            print(f"Episode {episode} finished after {steps} steps")
        else:
            reward = 0
            next_state = y_pos//50 + x_pos//50
        update_q_table(state, action, reward, next_state)
        state = next_state  
                        
    pygame.quit()
    print(q_table)
    print(f'Wins {wins}')

if __name__ == "__main__":
    main()