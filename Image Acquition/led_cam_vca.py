import time
import board
import adafruit_dotstar as dotstar
from tkinter import Tk, Button, Label, colorchooser
import subprocess
import os

# Initialize DotStar LED strip

dots = dotstar.DotStar(board.SCK, board.MOSI, 72, brightness=.5)

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

# Callback to launch OpenMV IDE
def launch_openmv_ide():
    openmv_path = "/home/pi/openmv-ide/bin/openmvide"  # Update this with the actual path
    try:
        subprocess.Popen([openmv_path])
    except FileNotFoundError:
        print("OpenMV IDE not found. Check the installation path.")

# Callback to run the spectral unmixing script
def run_spectral_unmixing():
    script_path = "/home/pi/python_vca.py"  # Update this with your actual script path
    try:
        subprocess.Popen(['python3', script_path])
    except FileNotFoundError:
        print(f"Spectral unmixing script not found at {script_path}. Check the path.")

# Create the GUI
root = Tk()
root.title("DotStar LED Controller")

# Add buttons to control LEDs
Label(root, text="DotStar LED Controller", font=("Helvetica", 16)).pack(pady=10)

Button(root, text="631nm", command=red, bg="red", fg="white", width=10).pack(pady=5)
Button(root, text="520nm", command=green, bg="green", fg="white", width=10).pack(pady=5)
Button(root, text="464nm", command=blue, bg="blue", fg="white", width=10).pack(pady=5)
Button(root, text="White", command=white, bg="white", fg="black", width=10).pack(pady=5)
Button(root, text="Choose Color", command=choose_color, bg="gray", fg="white", width=10).pack(pady=5)
Button(root, text="Turn Off", command=turn_off, bg="black", fg="white", width=10).pack(pady=10)

# Add button to launch OpenMV IDE
Button(root, text="OpenMV IDE", command=launch_openmv_ide, bg="orange", fg="white", width=15).pack(pady=10)

# Add button to run spectral unmixing
Button(root, text="Spectral Unmixing", command=run_spectral_unmixing, bg="purple", fg="white", width=15).pack(pady=10)

# Run the GUI loop
root.mainloop()
