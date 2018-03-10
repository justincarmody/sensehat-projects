from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()

# colours
r = (255, 0, 0)
b = (0, 0, 0)
w = (255, 255, 255)
g = (0, 255, 0)

# other variables
game_over = False

# create the maze
maze = [[r, r, r, r, r, r, r, r],
 [r, b, b, b, b, b, b, r],
 [r, r, r, b, r, b, b, r],
 [r, b, r, b, r, r, r, r],
 [r, b, b, b, b, b, b, r],
 [r, b, r, r, r, r, b, r],
 [r, g, b, r, b, b, b, r],
 [r, r, r, r, r, r, r, r]]

# create the marble 
x, y = 1, 1

# function to move the marble around
def move_marble(pitch, roll, x, y):
    new_x = x
    new_y = y

    if 1 < pitch < 179 and x != 0:
        new_x -= 1
    elif 181 < pitch < 359 and x != 7:
        new_x += 1

    if 1 < roll < 179 and y != 7:
        new_y += 1
    elif 179 < roll < 359 and y != 0:
        new_y -= 1

    new_x, new_y = check_wall(x, y, new_x, new_y)
    return new_x, new_y

def check_wall(x, y, new_x, new_y):
    if maze[new_y][new_x] != r:
        return new_x, new_y
    elif maze[new_y][x] != r:
        return x, new_y
    elif maze[y][new_x] != r:
        return new_x, y
    else:
        return x, y

while not game_over:
    # get gyro data
    o = sense.get_orientation()
    pitch, roll, yaw = o["pitch"], o["roll"], o["yaw"]
    
    # move the marble
    x, y = move_marble(pitch, roll, x, y)

    if maze[y][x] == g:
        game_over = True
        while True:    
            sense.show_message("You are winner HA HA HA")

    # set the pixel where the marble is to white
    maze[y][x] = w

    # update the pixels on the board
    sense.set_pixels(sum(maze, []))

    sleep(0.1)
    maze[y][x] = b


