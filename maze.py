import pygame
import random
import numpy as np

# Initialize pygame and window dimensions
pygame.init()
width, height = 500, 500
win = pygame.display.set_mode((width, height))

# Game settings
fps = 120
max_moves = 100
max_episodes = 500

# Grid definition
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 2]
]

# Actions and Q-table initialization
actions = ['up', 'down', 'left', 'right']
q_table = np.zeros((10 * 10, 4))

# Exploration-exploitation parameters
max_epsilon = 1.0  # Exploration probability at start
min_epsilon = 0.05  # Minimum exploration probability
decay_rate = 0.0005  # Exponential decay rate for exploration prob

def get_epsilon(episode):
    epsilon =  epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
    return epsilon

alpha = 0.7
gamma = 0.95

def draw_window(color=(0, 0, 0)):
    # Draw the window with specified color
    win.fill(color)
    draw_rectangles()

def draw_rectangles():
    # Draw the rectangles based on the grid
    for i in range(10):
        for j in range(10):
            if grid[j][i] == 1:
                color = (255, 255, 255)
            elif grid[j][i] == 0:
                color = (255, 0, 0)
            elif grid[j][i] == 2:
                color = (0, 255, 0)
            pygame.draw.rect(win, color, (i * 50, j * 50, 48, 48), 0)

def take_action(state, epsilon):
    # Choose an action based on epsilon-greedy policy
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        return actions[np.argmax(q_table[state])]

def update_q_table(state, action, reward, next_state):
    # Update the Q-table based on the Bellman equation
    q_table[state, actions.index(action)] += alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state, actions.index(action)])

def main():
    # Initialize variables
    x_pos = 25
    y_pos = 25
    clock = pygame.time.Clock()
    run = True
    episode = 0
    state = 0
    moves = 0
    wins = 0

    while run:
        clock.tick(fps)
        pygame.display.set_caption(f"Maze Game - Episode {episode}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
        pygame.draw.circle(win, (0, 0, 255), (x_pos, y_pos), 20, 0)
        epsilon = get_epsilon(episode)
        action = take_action(state, epsilon)
        moves += 1



        if action == 'left' and x_pos > 25:
            x_pos -= 50
        elif action == 'right' and x_pos < 425:
            x_pos += 50
        elif action == 'up' and y_pos > 25:
            y_pos -= 50
        elif action == 'down' and y_pos < 425:
            y_pos += 50

        pygame.display.flip()

        if grid[y_pos // 50][x_pos // 50] == 0:
            x_pos = 25
            y_pos = 25
            episode += 1
            reward = -1
            next_state = 0
        elif grid[y_pos // 50][x_pos // 50] == 2:
            x_pos = 25
            y_pos = 25
            episode += 1
            reward = 1
            next_state = 0
            wins += 1
            print("Win #", wins)
        else:
            next_state = y_pos // 50 + x_pos // 50
            reward = 0

        if moves > max_moves:
            print("Max moves reached")
            x_pos = 25
            y_pos = 25
            episode += 1
            moves = 0
            reward = -1
        update_q_table(state, action, reward, next_state)
        state = next_state

        if episode == max_episodes:
            run = False

    pygame.quit()
    print(q_table)
    print("Wins:", wins)

if __name__ == "__main__":
    main()