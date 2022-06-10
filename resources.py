from tkinter import Image
import tkinter as tk
from PIL import ImageTk, Image

minsizew = 560
minsizeh = 755
resources_path = "./resources/"  # Global location of resource files


# -------------------------------------------------------------
# Fonts
# -------------------------------------------------------------
font_name = "Work Sans Regular"
font_weight = "normal"
font_path = resources_path + "WorkSans-Regular.ttf"

# -------------------------------------------------------------
# Loading Images/Resources (all loading should be done here in the future) and Colors
# -------------------------------------------------------------
bg_image_path = resources_path + "StarBackground.png"
browse_button_img_path = resources_path + "Button1.png"
stems_bg_path = resources_path + "StemOptions.png"
black_pixel_path = resources_path + "blackPixel.png"
check_on_img_path = resources_path + "checkOn.png"
check_off_img_path = resources_path + "checkOff.png"
freq_bg_path = resources_path + "FreqLine2.png"
save_button_img_path = resources_path + "Button1.png"
split_button_img_path = resources_path + "SplitButton.png"

download_pg_browse_button_img_path = resources_path + "Button2.png"
download_button_img_path = resources_path + "DownloadButton.png"

# Colors
mid_block_color = "#AAFF65"  # radio button fill-in color: bright green
button_color = "#7D50FF"  # purple box color
prog_bar_color = "#EABEFF"  # orchid purple progress bar

download_pg_frame_color = "#DA5578"  # light pink frames.

# -------------------------------------------------------------
