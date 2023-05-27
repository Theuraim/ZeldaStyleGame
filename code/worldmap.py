import random
from settings import WIDTH, HEIGTH

def generate_map(width, height, wall_chance):
    # Create an initial map filled with wall tiles
    world_map = [['x'] * width for _ in range(height)]  # Initialize a wall-filled map

    # Generate empty spaces
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if random.random() > wall_chance:
                world_map[y][x] = ' '

    # Add predefined patterns
    pattern1 = [
        [' ', ' ', ' '],
        [' ', 'p', ' '],
        [' ', ' ', ' ']
    ]
    pattern2 = [
        [' ', ' ', ' '],
        [' ', 'x', 'x'],
        [' ', ' ', ' ']
    ]

    # Place patterns randomly on the map
    patterns = [pattern1, pattern2]
    pattern_chance = 0.1
    player_placed = False

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if ((not player_placed) and (random.random() < pattern_chance)):
                pattern = random.choice(patterns)
                pattern_height = len(pattern)
                pattern_width = len(pattern[0])
                if y + pattern_height < height - 1 and x + pattern_width < width - 1:
                    for i in range(pattern_height):
                        for j in range(pattern_width):
                            #places the player in map
                            if pattern[i][j] == 'p':
                                if (((j < WIDTH/128) and (i < HEIGTH/128)) and ((x < WIDTH/128) and (y < HEIGTH/128))):
                                    world_map[y + i][x + j] = pattern[i][j]
                                    player_placed = True
                            else: #else it places the empty space and the walls
                                world_map[y + i][x + j] = pattern[i][j]
    return world_map