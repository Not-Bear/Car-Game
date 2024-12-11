import tkinter
import math
from tkinter import *

# Window + score ----------------------------------------------------------------
root = tkinter.Tk()
root.configure(background='black')
root.title('Smashy Road')
root.geometry("800x800")
root.resizable(width=False, height=False)

score = tkinter.Label(root, text='Score:')
score.configure(background='white')
score.pack(side='top')
# Window + score ----------------------------------------------------------------

canvas = tkinter.Canvas(root, width=700, height=700, bg="gray")
canvas.pack()
width, height = 700, 700

# Initial car coordinates 
original_vertices = [(190, 310), (190, 350), (210, 350), (210, 310)] 
car_center = (200, 330)
car = canvas.create_polygon(*original_vertices, fill="blue") # ( * ) used to unpack the list of coordinates

# Movement variables
dx, dy = 0, -2  # Initial movement direction
alfa = -math.pi / 2  # Initial angle to align the car's nose pointing upward

# Function to move the car ------------------------------------------------------
def move_car():
    global dx, dy
    canvas.move(car, dx, dy)
    pos = canvas.coords(car)
    canvas.after(20, move_car)

    # Check for collisions with the window boundaries --- remove later
    if pos[0] <= 0 or pos[2] >= width:  # Left or right wall
        dx = -dx
    if pos[1] <= 0 or pos[3] >= height:  # Top or bottom wall
        dy = -dy

# Function to calculate the center of the car
def calculate_center(vertices):
    x_coords = [vertices[i] for i in range(0, len(vertices), 2)]
    y_coords = [vertices[i + 1] for i in range(0, len(vertices), 2)]
    return sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords)

# Function to rotate a point around a center
def rotate_point(px, py, cx, cy, angle):
    dxh = px - cx
    dyh = py - cy
    new_x = cx + dxh * math.cos(angle) - dyh * math.sin(angle)
    new_y = cy + dxh * math.sin(angle) + dyh * math.cos(angle)
    return new_x, new_y

# Rotate car
def click():
    global dx, dy, alfa, car_center

    # Increment angle of movement and car rotation
    alfa += math.pi / 4
    dx = 2 * math.cos(alfa)
    dy = 2 * math.sin(alfa)

    # Get current coordinates of the car
    current_coords = canvas.coords(car)

    # Calculate current center of the car
    car_center = calculate_center(current_coords)

    # Rotate car vertices around the center
    rotated_vertices = [
        rotate_point(current_coords[i], current_coords[i + 1], car_center[0], car_center[1], math.pi / 4)
        for i in range(0, len(current_coords), 2)
    ]

    # Update the car's coordinates
    canvas.coords(car, *sum(rotated_vertices, ()))  # Flatten the list of tuples
def clickleft():
    for i in range(7):
        click()

button = Button(root, text='←',command=clickleft)
button.pack(side='left')

button = Button(root, text='→', command=click)
button.pack(side='left')



# Start car movement
move_car()
root.mainloop()
