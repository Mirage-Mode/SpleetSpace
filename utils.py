#Utility Functions/Variables
resources_path = "./resources/" #Global location of resource files
minsizew = 550
minsizeh = 900

#Switches the cursor to clickable hand
def on_cursor_overlap(canvas):
    canvas.config(cursor="hand2")

#Switches the cursor to regular hand
def on_cursor_endoverlap(canvas):
    canvas.config(cursor="")

# Returns an array containing the dimensions of the scaled image.
def scale_image_to_container(w_width, w_height, i_width, i_height):
    # It's slow not because of my code, but because tkinter is trash.
    # i_width and i_height are for the h and w of the background image supplied.
    # w_width and w_height are the w and h of the root window.
    w_scale = w_width / i_width
    h_scale = w_height / i_height

    if w_scale > h_scale:
        image_w = int(w_scale * i_width)
        image_h = int(w_scale * i_height)
    else:
        image_w = int(h_scale * i_width)
        image_h = int(h_scale * i_height)

    return [image_w, image_h]
        

# Helper class to keep track of canvas elements.
# Stores the canvas element and its width/height. We need this width and height for centering purposes.
class canvas_element:
    def __init__(self, element=None, width=0, height=0, x_offset=0, y_offset=0):
        self.element = element
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset