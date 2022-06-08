import os
import queue
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ctypes
from PIL import ImageTk, Image
import subprocess
from subprocess import CREATE_NO_WINDOW
import threading
from utils import *
from ctypes import windll
import resources

# Main window containing all gui elements.

def youtube_page(root, parent):

    font_name = resources.font_name
    font_weight = resources.font_weight

    # Getting the window width and height.
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Global center location. Can be used to center everything that has anchor=CENTER.
    center_x_loc = (window_width/2)
    center_y_loc = (window_height/2)

    youtube_canvas = Canvas(parent, width=window_width,
                                    height=window_height, highlightthickness=0, background="red")

    youtube_canvas.create_text(center_x_loc, center_y_loc, 
                                    anchor=CENTER, text="\n\nIn Development", fill="white")

    return youtube_canvas