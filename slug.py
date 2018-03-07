from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()

# Variables -----------------
slug = [[2,4],[3,4],[4,4]]

direction = "up"

white = (255,255,255)
blank = (0,0,0)

grid_length = 8

# Functions -----------------
def draw_slug():
    for s in slug:
        sense.set_pixel(s[0], s[1], white)

def move():
    # Find the last and first items in the slug list
    last = slug[-1]
    first = slug[0]
    next = list(last) # create copy of the last item

    # Find the next pixel in teh direction the slug is moving
    if direction == "right":
      
        # Move along the column
        next[0] = last[0] + 1

    elif direction == "left":

        next[0] = last[0] - 1

    elif direction == "up":

        next[1] = last[1] - 1
    
    elif direction == "down":
        next[1] = last[1] + 1
    
    # Add this pixel at the end of the slug list
    slug.append(next)

    # Set the new pixel to the slug's colour
    sense.set_pixel(next[0]%grid_length, next[1]%grid_length, white)

    # Set the first pixel in the slug list to blank
    sense.set_pixel(first[0]%grid_length,first[1]%grid_length, blank)

    # Remove the first pixel from the list
    slug.remove(first)


def joystick_moved(event):
    global direction
    direction = event.direction


def make_veg():
    x, y = randint(0,7), randint(0,7)

    global slug
    if [x,y] not in slug:
        sense.set_pixel(x, y, (255,0,0))

# Main Program --------------
draw_slug()

while True:
    sense.stick.direction_any = joystick_moved
    move()
    make_veg()
    sleep(0.5)
