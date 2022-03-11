from tkinter import * 
from MainFrame import MainFrame
from resources import resources_path, minsizew, minsizeh



# Code for the Main GUI Window.
# Takes in a splash window to destroy. 
def main_window(splash_window):
    
    splash_window.destroy() # Destroy the splash screen.
    
    #Window setup
    window = Tk()
    window.configure(background="#000000") 
    window.state("withdrawn") # Start maximized.
    window.iconbitmap(resources_path + 'icon.ico')
    window.title("Spleet Space")
    main_window = MainFrame(window) #Create main window from MainFrame class.
 
    window.mainloop()


# Main function.
def main():

    # -------------- Splash Screen Setup ---------------------
    splash_window = Tk() 
    splash_window.overrideredirect(True) #Gets rid of the window border.
    splash_window.attributes('-topmost',True); # Forces this window to be on top of everything.

    # Dimensions of the splash screen.
    splash_width = 500
    splash_height = 300
    screen_width = splash_window.winfo_screenwidth()
    screen_height = splash_window.winfo_screenheight()

    x_location = (screen_width/2) - (splash_width/2) 
    y_location = (screen_height/2) - (splash_height/2)  

    splash_window.geometry('%dx%d+%d+%d' % (splash_width, splash_height, x_location, y_location))
    
    img = PhotoImage(file=resources_path + "splashArt.png")  

    canvas = Canvas(splash_window, width=500, height=300, highlightthickness=0)
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.pack()  
    # ---------------------------------------------------

    # Here we call that main_window function after 3.14 seconds have passed.
    splash_window.after(800, lambda: main_window(splash_window))
    mainloop()

 
if __name__ == "__main__":
    main()
