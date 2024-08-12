"""
Author: Mahenur Master Nisharg Patel Sneha Malhotra Siddharth Patel 
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
import poke_api
import image_lib
import ctypes

# Retrieve the script's directory and prepare the images directory path
script_directory = os.path.dirname(os.path.abspath(__file__))
images_directory = os.path.join(script_directory, 'images')

# Ensure the images directory exists
if not os.path.exists(images_directory):
    os.makedirs(images_directory)

# Set up the main application window
main_window = Tk()
main_window.title("Pokemon Viewer")
main_window.geometry('600x600')
main_window.minsize(500, 600)
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(0, weight=1)

# Set the application icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
main_window.iconbitmap(os.path.join(script_directory, 'poke_ball.ico'))

# Create and configure the main frame
frame = ttk.Frame(main_window)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
frame.grid(sticky=NSEW)

# Initialize with a default image
default_image_path = os.path.join(script_directory, 'poke_ball.png')
default_photo = PhotoImage(file=default_image_path)
image_label = ttk.Label(frame, image=default_photo)
image_label.grid(row=0, column=0, padx=10, pady=10)

# Function to update the desktop background
def update_desktop_background():
    if current_image_path:
        image_lib.set_desktop_background_image(current_image_path)

# Button to set the selected image as the desktop wallpaper
set_background_button = ttk.Button(main_window, text='Set as Desktop Image', command=update_desktop_background)
set_background_button.grid(row=2, column=0, padx=20, pady=10)
set_background_button.state(['disabled'])

# Handle Pokemon selection and update displayed image
def on_pokemon_selected(event):
    selected_name = pokemon_selector.get()
    global current_image_path
    current_image_path = poke_api.download_pokemon_artwork(pokemon_name=selected_name, folder_path=images_directory)
    if current_image_path:
        updated_photo = PhotoImage(file=current_image_path)
        image_label.config(image=updated_photo)
        image_label.image = updated_photo  # Keep a reference to avoid garbage collection
        set_background_button.state(['!disabled'])

# Create a dropdown for Pokemon selection
pokemon_names = poke_api.fetch_pokemon_names()
pokemon_selector = ttk.Combobox(main_window, values=pokemon_names, state='readonly')
pokemon_selector.set('Select a Pokemon')
pokemon_selector.grid(row=1, column=0, padx=10, pady=10)
pokemon_selector.bind('<<ComboboxSelected>>', on_pokemon_selected)

current_image_path = None

# Start the application
main_window.mainloop()
