from sense_hat import SenseHat
from random import randint
from time import sleep

# open connection with the sense hat
sense = SenseHat()

# set colour globals
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# x and y co-ords of the astronaut (which are used as globals,
# and i know this is terrible but that's what the simple tutorial did)
x, y = 0, 0

# another global, i know, but stores game state
game_over = False

# initialise the game board
matrix = [[BLUE for column in range(8)] for row in range(8)]

# function to flatten the 2D matrix structure into a 1D list that 
# can be passed into the set_pixels() function
def flatten(matrix):
   return [pixel for row in matrix for pixel in row]

# creates the obstacles
def gen_pipes(matrix):
    for row in matrix:
        row[7] = RED

    gap = randint(1,6)

    matrix[gap-1][-1] = BLUE
    matrix[gap][-1] = BLUE
    matrix[gap+1][-1] = BLUE

    return matrix 

# makes the obstacles move right to left on the screen
def move_pipes(matrix):
    for row in matrix:
        for index in range(7):
            row[index] = row[index+1]
        row[-1] = BLUE
    
    return(matrix)

# makes the astronaut a yellow pixel that responds to the joystick
def draw_astronaut(event):
    global x
    global y
    global game_over
    sense.set_pixel(x, y, BLUE)

    if event.action == "pressed":
        if event.direction == "up" and y > 0:
            y -= 1
        elif event.direction == "down" and y < 7:
            y += 1
        elif event.direction == "right" and x < 7:
            x += 1
        elif event.direction == "left" and x > 0:
            x -= 1
        sense.set_pixel(x, y, YELLOW)

    # this i dont quite get - it syncs the game_over variable to the 
    # joystick moves so you can ghost through walls accidently
    if matrix[y][x] == RED:
        game_over = True

# returns TRUE if the astronaut has hit a pipe obstacle
def check_collision(matrix):
    if matrix[y][x] == RED:
        return True
    return False



# create astronaut initially
sense.stick.direction_any = draw_astronaut

# game loop
while not game_over:
    matrix = gen_pipes(matrix)
    if check_collision(matrix):
        game_over = True
    for i in range(3):
        matrix = move_pipes(matrix)
        sense.set_pixels(flatten(matrix))
        sense.set_pixel(x, y, YELLOW)
        if check_collision(matrix):
            game_over = True
        sleep(1)

sense.show_message("You Suck")
