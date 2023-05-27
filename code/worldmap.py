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
    world_map = createPositions(height, width, pattern_chance, patterns, world_map)
    
    # Post-processing step to remove dead ends
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if world_map[y][x] == 'x' and is_dead_end(world_map, x, y):
                world_map[y][x] = ' '
                

    return world_map

def createPositions(height, width, pattern_chance, patterns, world_map):
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

def is_dead_end(world_map, x, y):
    # Check if the tile at (x, y) is a dead end
    return (
        world_map[y][x+1] == 'x' and
        world_map[y][x-1] == 'x' and
        world_map[y+1][x] == 'x' and
        world_map[y-1][x] == 'x'
    )

def generate_dungeon(width, height, num_rooms):
    dungeon = [['x'] * width for _ in range(height)]

    rooms = []
    for _ in range(num_rooms):
        room_width = random.randint(3, 6)
        room_height = random.randint(3, 6)
        room_x = random.randint(1, width - room_width - 1)
        room_y = random.randint(1, height - room_height - 1)

        if is_room_valid(dungeon, room_x, room_y, room_width, room_height):
            create_room(dungeon, room_x, room_y, room_width, room_height)
            rooms.append((room_x, room_y, room_width, room_height))

    for i in range(len(rooms) - 1):
        x1, y1, _, _ = rooms[i]
        x2, y2, _, _ = rooms[i + 1]
        connect_rooms(dungeon, x1, y1, x2, y2)

    player_x, player_y = random.choice(rooms)[:2]
    dungeon[player_y][player_x] = 'p'

    remove_dead_ends(dungeon)

    return dungeon

def is_room_valid(dungeon, x, y, width, height):
    for i in range(y - 1, y + height + 1):
        for j in range(x - 1, x + width + 1):
            if dungeon[i][j] != 'x':
                return False
    return True

def create_room(dungeon, x, y, width, height):
    for i in range(y, y + height):
        for j in range(x, x + width):
            dungeon[i][j] = ' '

def connect_rooms(dungeon, x1, y1, x2, y2):
    if random.random() < 0.5:
        create_horizontal_tunnel(dungeon, x1, x2, y1)
        create_vertical_tunnel(dungeon, y1, y2, x2)
    else:
        create_vertical_tunnel(dungeon, y1, y2, x1)
        create_horizontal_tunnel(dungeon, x1, x2, y2)

def create_horizontal_tunnel(dungeon, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon[y][x] = ' '

def create_vertical_tunnel(dungeon, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon[y][x] = ' '

def remove_dead_ends(dungeon):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    done = False

    while not done:
        done = True
        for y in range(1, len(dungeon) - 1):
            for x in range(1, len(dungeon[0]) - 1):
                if dungeon[y][x] == ' ':
                    neighbors = 0
                    for dx, dy in directions:
                        if dungeon[y + dy][x + dx] == ' ':
                            neighbors += 1
                    if neighbors <= 1:
                        dungeon[y][x] = 'x'
                        done = False
