import time
import board
import adafruit_dotstar as dotstar
from tkinter import Tk, Button, Label, colorchooser
import subprocess

# Initialize DotStar LED strip
dots = dotstar.DotStar(board.SCK, board.MOSI, 72, brightness=0.2)

# Function to set the LEDs to a chosen color
def set_color(r, g, b):
    dots.fill((r, g, b))
    dots.show()

# Callback for Red button
def red():
    set_color(255, 0, 0)

# Callback for Green button
def green():
    set_color(0, 255, 0)

# Callback for Blue button
def blue():
    set_color(0, 0, 255)

# Callback for White button
def white():
    set_color(255, 255, 255)

# Callback for the color picker
def choose_color():
    color = colorchooser.askcolor()[0]  # Returns (R, G, B) tuple
    if color:
        r, g, b = map(int, color)
        set_color(r, g, b)

# Callback to turn off LEDs
def turn_off():
    set_color(0, 0, 0)

# Callback to start OpenMV camera
def start_openmv():
    # Replace 'openmv_script.py' with the actual name of your OpenMV script
    subprocess.Popen(["python3", "capture_1.py"])

# Create the GUI
root = Tk()
root.title("DotStar LED and OpenMV Controller")

# Add buttons to control LEDs
Label(root, text="DotStar LED Controller", font=("Helvetica", 16)).pack(pady=10)

Button(root, text="Red", command=red, bg="red", fg="white", width=10).pack(pady=5)
Button(root, text="Green", command=green, bg="green", fg="white", width=10).pack(pady=5)
Button(root, text="Blue", command=blue, bg="blue", fg="white", width=10).pack(pady=5)
Button(root, text="White", command=white, bg="white", fg="black", width=10).pack(pady=5)
Button(root, text="Choose Color", command=choose_color, bg="gray", fg="white", width=10).pack(pady=5)
Button(root, text="Turn Off", command=turn_off, bg="black", fg="white", width=10).pack(pady=10)

# Add button to start OpenMV camera
Label(root, text="OpenMV Camera", font=("Helvetica", 16)).pack(pady=10)
Button(root, text="Start Camera", command=start_openmv, bg="orange", fg="white", width=15).pack(pady=5)

# Run the GUI loop
root.mainloop()
