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
from YoutubePage import youtube_page
import resources

# Main window containing all gui elements.


class MainFrame:

    # This is the "constructor". 🏗
    def __init__(self, root):

        # Make the window respond to windows scaling
        windll.shcore.SetProcessDpiAwareness(1)
        self.que = queue.Queue()  # global thread status queue
        self.font_name = resources.font_name
        self.font_weight = resources.font_weight

        self.label_font_name = resources.label_font_name
        self.label_font_weight = resources.label_font_weight

        gdi32 = ctypes.WinDLL('gdi32')
        gdi32.AddFontResourceW(resources.font_path)
        gdi32.AddFontResourceW(resources.label_font_path)

        root.minsize(resources.minsizew, resources.minsizeh)
        window_x_location = (root.winfo_screenwidth()/2) - \
            (resources.minsizew/2)
        window_y_location = (root.winfo_screenheight() /
                             2) - (resources.minsizeh/2)
        self.root = root

        # Getting the window width and height.
        self.window_width = root.winfo_width()
        self.window_height = root.winfo_height()

        # Global center location. Can be used to center everything that has anchor=CENTER.
        self.center_x_loc = (self.window_width/2)
        self.center_y_loc = (self.window_height/2)

        # ------------------------------------------------------------------------------------
        # Loading Images/Resources (all loading should be done here in the future) and Colors
        # ------------------------------------------------------------------------------------
        self.bg_image = Image.open(resources.bg_image_path)
        self.browse_button_img = ImageTk.PhotoImage(
            Image.open(resources.browse_button_img_path))
        self.stems_bg = ImageTk.PhotoImage(Image.open(resources.stems_bg_path))
        self.black_pixel = PhotoImage(file=resources.black_pixel_path)
        self.check_on_img = PhotoImage(file=resources.check_on_img_path)
        self.check_off_img = PhotoImage(file=resources.check_off_img_path)
        self.freq_bg = ImageTk.PhotoImage(Image.open(resources.freq_bg_path))
        self.save_button_img = ImageTk.PhotoImage(
            Image.open(resources.save_button_img_path))
        self.split_button_img = ImageTk.PhotoImage(
            Image.open(resources.split_button_img_path))

        # Get the image dimensions needed to perfectly fit the window -> scale the image to those dimensions -> convert the img to TK image.
        image_dim = scale_image_to_container(root.winfo_screenwidth(
        ), root.winfo_screenheight(), self.bg_image.width, self.bg_image.height)
        self.resized_background_image = self.bg_image.resize(
            (image_dim[0], image_dim[1]), Image.ANTIALIAS)

        # Final render image.
        self.rend_image = ImageTk.PhotoImage(self.resized_background_image)
        # -------------------------------------------------------------


        # -------------------------------------------------------------
        # STYLES
        # -------------------------------------------------------------
        self.style = ttk.Style()
        # Set settings for the new style.
        self.style.theme_create("tabStyle", parent="classic",
                                settings={
                                    "TNotebook.Tab": {"configure": {"background": "#201B21", "foreground": "white", "focuscolor": "#2e2e2e", "font": (self.font_name, 10, self.font_weight),
                                                                    "padding": [49, 10], "borderwidth": 0},
                                                      "map": {"background": [("selected", "#7D50FF")]}},
                                    "TNotebook": {"configure": {"background": "#000000", "borderwidth": 0}}})

        self.style.theme_use("tabStyle")  # Use the new style we just made.
        # -------------------------------------------------------------------------


        # -------------------------------------------------------------------------
        # Tab Setup--make a Notebook widget first, whose parent is the root window.
        # -------------------------------------------------------------------------
        self.tab_controller = ttk.Notebook(root)

        # Contains the tabs
        self.spleet_frame = Frame(
            self.tab_controller, background="#000000", bd=0)
        self.youtube_frame = Frame(
            self.tab_controller, background="#000000", bd=0)
        self.help_frame = Frame(self.tab_controller,
                                background="#000000", bd=0)
        self.yt_help_frame = Frame(self.tab_controller,
                                   background="#000000", bd=0)

        # Adds the above frames onto the tab controller.
        self.tab_controller.add(self.spleet_frame, text="Split Songs")
        self.tab_controller.add(
            self.youtube_frame, text="Youtube Song Downloader")
        self.tab_controller.add(self.help_frame, text="Help")
        self.tab_controller.pack(fill=BOTH, expand=1)
        # -------------------------------------------------------------


        # -------------------------------------------------------------
        # Canvas Setup for the 3 tabs
        # -------------------------------------------------------------
        self.spleet_canvas = Canvas(self.spleet_frame, width=self.window_width,
                                    height=self.window_height, highlightthickness=0, background="#000000")

        # It's apparently okay to pack the canvas before drawing things.
        self.spleet_canvas.pack(expand=1, fill=BOTH)

        self.youtube_page = youtube_page(
            root, self.youtube_frame, self.rend_image)
        self.youtube_canvas = self.youtube_page.youtube_canvas
        self.youtube_canvas.pack(expand=1, fill=BOTH)

        self.help_canvas = Canvas(self.help_frame, width=self.window_width,
                                  height=self.window_height, highlightthickness=0, background="#000000")

        self.help_canvas.pack(expand=1, fill=BOTH)
        # -------------------------------------------------------------



        # -------------------------------------------------------------
        # Background Setup
        # -------------------------------------------------------------
        # Create the backgrounds for each canvas.
        self.spleet_bg = self.spleet_canvas.create_image(
            self.center_x_loc, self.center_y_loc, anchor=CENTER, image=self.rend_image)

        # self.youtube_bg = self.youtube_canvas.create_image(
        #     self.center_x_loc, self.center_y_loc, anchor=CENTER, image=self.rend_image)

        # self.youtube_canvas.tag_lower(self.youtube_bg)

        self.help_bg = self.help_canvas.create_image(
            self.center_x_loc, self.center_y_loc, anchor=CENTER, image=self.rend_image)
        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        # File Load Browser
        # --------------------------------------------------------------------------
        self.file_location = ""
        load_glob_off = 165  # increase to move up

        file_browser_frame = Frame(
            self.spleet_canvas, background="#000000", bd=0)
        self.file_label_border = Frame(
            file_browser_frame, highlightbackground=resources.button_color, highlightthickness=2, bd=0, background="black")
        self.chosen_file_label = Label(self.file_label_border, text="File", bg="black", fg="white", width=26, height=1, font=(
            self.font_name, 13, self.font_weight), bd=4, anchor='w')
        self.chosen_file_label.grid(row=0, column=0, padx=5)
        self.file_label_border.grid(row=0, column=0)

        self.file_browser_container = canvas_element()
        self.file_browser_container.x_offset = 66
        self.file_browser_container.y_offset = 160 + load_glob_off
        self.file_browser_container.element = self.spleet_canvas.create_window(self.center_x_loc, self.center_y_loc + self.file_browser_container.y_offset,
                                                                               anchor=CENTER, window=file_browser_frame)

        self.file_title = canvas_element()
        self.file_title.x_offset = 203
        self.file_title.y_offset = 198 + load_glob_off
        self.file_title.element = self.spleet_canvas.create_text(self.center_x_loc - self.file_title.x_offset, self.center_y_loc - self.file_title.y_offset, anchor=W,
                                                                 text="Song", fill="white", font=(self.label_font_name, 14, self.label_font_weight))

        self.file_browser_button = canvas_element()
        self.file_browser_button.x_offset = 154
        self.file_browser_button.y_offset = 160 + load_glob_off
        self.file_browser_button.element = self.spleet_canvas.create_image(self.center_x_loc,
                                                                           self.center_y_loc + self.file_browser_button.y_offset, tags="browseButton", image=self.browse_button_img, anchor="center")
        self.spleet_canvas.tag_bind(
            "browseButton", "<Button-1>", self.browse_files)
        self.spleet_canvas.tag_bind(
            "browseButton", "<Enter>", lambda event: on_cursor_overlap(self.spleet_canvas))
        self.spleet_canvas.tag_bind(
            "browseButton", "<Leave>", lambda event: on_cursor_endoverlap(self.spleet_canvas))
        # --------------------------------------------------------------------------



        # ----------------------------------------------------------------------------------
        # Stems Code
        # ----------------------------------------------------------------------------------
        stems_glob_off = 145  # increase to move up

        self.stems_container = canvas_element()
        self.stems_container.width = 190
        self.stems_container.height = 55
        self.stems_container.y_offset = -55 - stems_glob_off

        # This var gets updated with whatever the radio button's value is.
        self.stem_option_selection = IntVar()

        stems_radio_frame = Frame(
            self.spleet_canvas, background="#000000", bd=0)

        self.stems_label = canvas_element()
        self.stems_label.x_offset = 177
        self.stems_label.y_offset = 80 + stems_glob_off
        self.stems_label.element = self.spleet_canvas.create_text(self.center_x_loc - self.stems_label.x_offset, self.center_y_loc - self.stems_label.y_offset, anchor=W,
                                                                  text="Number of Stems", fill="white", font=(self.label_font_name, 14, self.label_font_weight))

        self.two_stem = Radiobutton(stems_radio_frame, text="Two", variable=self.stem_option_selection, value=2, command=self.set_stem_option,
                                    activebackground="black", activeforeground=resources.mid_block_color, selectcolor="black", bg="black", fg=resources.mid_block_color, font=(self.font_name, 13, self.font_weight))
        self.four_stem = Radiobutton(stems_radio_frame, text="Four", variable=self.stem_option_selection, value=4, command=self.set_stem_option,
                                     activebackground="black", activeforeground=resources.mid_block_color, selectcolor="black", bg="black", fg=resources.mid_block_color, font=(self.font_name, 13, self.font_weight))
        self.five_stem = Radiobutton(stems_radio_frame, text="Five", variable=self.stem_option_selection, value=5, command=self.set_stem_option,
                                     activebackground="black", activeforeground=resources.mid_block_color, selectcolor="black", bg="black", fg=resources.mid_block_color, font=(self.font_name, 13, self.font_weight))

        self.two_stem.grid(row=0, column=0, padx=15)
        self.four_stem.grid(row=0, column=2, padx=15)
        self.five_stem.grid(row=0, column=3, padx=15)
        self.two_stem.select()
        stems_radio_frame.pack()

        self.stems_frame_canvas = canvas_element()
        self.stems_frame_canvas.y_offset = -30 - stems_glob_off
        self.stems_frame_canvas.element = self.spleet_canvas.create_window(self.center_x_loc, self.center_y_loc + self.stems_frame_canvas.y_offset,
                                                                           anchor=CENTER, window=stems_radio_frame)

        self.stems_bg_image = self.spleet_canvas.create_image(self.center_x_loc + 5,
                                                              self.center_y_loc + self.stems_label.y_offset, image=self.stems_bg, anchor="center")
        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        # CheckBox Code
        # --------------------------------------------------------------------------
        check_glob_off = -195  # increase to move up
        self.freq_selection = IntVar()

        self.freq_frame = Frame(self.spleet_canvas, background="#000000", bd=0)

        self.frequency_checkbox = Checkbutton(self.freq_frame, variable=self.freq_selection, onvalue=1, offvalue=0, background="#000000", fg="black", bg="black", offrelief="flat", relief="flat", highlightthickness=0, bd=0, command=self.freq_checkbox_handler,
                                              highlightbackground="black", highlightcolor="black", selectimage=self.check_on_img, image=self.check_off_img, selectcolor="black", activebackground="black", indicatoron=1, anchor=CENTER)

        self.frequency_checkbox.pack()
        self.freq_frame.pack()

        self.freq_container = canvas_element()
        self.freq_container.y_offset = 110 + check_glob_off
        self.freq_container.x_offset = -157
        self.freq_container.element = self.spleet_canvas.create_window(self.center_x_loc - self.freq_container.x_offset, self.center_y_loc + self.freq_container.y_offset,
                                                                       anchor=CENTER, window=self.freq_frame)

        self.freq_bg_image = canvas_element()
        self.freq_bg_image.x_offset = 0
        self.freq_bg_image.y_offset = 130 + check_glob_off
        self.freq_bg_image.element = self.spleet_canvas.create_image(self.center_x_loc,
                                                                     self.center_y_loc + self.freq_container.y_offset, image=self.freq_bg, anchor="center")

        self.freq_label = canvas_element()
        self.freq_label.x_offset = 21
        self.freq_label.y_offset = self.freq_container.y_offset
        self.freq_label.element = self.spleet_canvas.create_text(self.center_x_loc - self.freq_label.x_offset, self.center_y_loc + self.freq_label.y_offset, anchor=CENTER,
                                                                 text="Include High Frequencies (16 kHz) ", fill="white", font=(self.font_name, 14, self.font_weight))

        self.black_pixel_label = Label(
            self.spleet_canvas, image=self.black_pixel, bd=0)
        self.black_pixel_label.pack()

        self.black_pixel_cv = canvas_element()
        self.black_pixel_cv.x_offset = -147
        self.black_pixel_cv.y_offset = 110 + check_glob_off
        self.black_pixel_cv.element = self.spleet_canvas.create_window(self.center_x_loc - self.black_pixel_cv.x_offset, self.center_y_loc + self.black_pixel_cv.y_offset,
                                                                       anchor=CENTER, window=self.black_pixel_label)

        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        # File Save Browser
        # --------------------------------------------------------------------------
        self.save_location = ""
        save_glob_off = 239  # increase to move up
        self.file_save_title = canvas_element()
        self.file_save_title.x_offset = 203
        self.file_save_title.y_offset = -225 + save_glob_off
        self.file_save_title.element = self.spleet_canvas.create_text(self.center_x_loc - self.file_save_title.x_offset, self.center_y_loc - self.file_save_title.y_offset, anchor=W,
                                                                      text="Save Location", fill="white", font=(self.label_font_name, 14, self.label_font_weight))

        file_save_frame = Frame(self.spleet_canvas, background="#000000", bd=0)
        self.file_save_border = Frame(
            file_save_frame, highlightbackground=resources.button_color, highlightthickness=2, bd=0, background="black")
        self.save_file_label = Label(self.file_save_border, text="Save Location", bg="black", fg="white",
                                     width=26, height=1, font=(self.font_name, 13, self.font_weight), bd=4, anchor='w')
        self.save_file_label.grid(row=0, column=0, padx=5)
        self.file_save_border.grid(row=0, column=0)

        self.file_save_container = canvas_element()
        self.file_save_container.x_offset = 66
        self.file_save_container.y_offset = -265 + save_glob_off
        self.file_save_container.element = self.spleet_canvas.create_window(self.center_x_loc, self.center_y_loc + self.file_save_container.y_offset,
                                                                            anchor=CENTER, window=file_save_frame)

        self.save_browser_button = canvas_element()
        self.save_browser_button.x_offset = 154
        self.save_browser_button.y_offset = -265 + save_glob_off
        self.save_browser_button.element = self.spleet_canvas.create_image(self.center_x_loc,
                                                                           self.center_y_loc + self.file_browser_button.y_offset, tags="saveButton", image=self.save_button_img, anchor="center")
        self.spleet_canvas.tag_bind(
            "saveButton", "<Button-1>", self.browse_save_location)
        self.spleet_canvas.tag_bind(
            "saveButton", "<Enter>", lambda event: on_cursor_overlap(self.spleet_canvas))
        self.spleet_canvas.tag_bind(
            "saveButton", "<Leave>", lambda event: on_cursor_endoverlap(self.spleet_canvas))
        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        # Split Button
        # --------------------------------------------------------------------------
        split_glob_off = 120  # increase to move down

        self.split_button = canvas_element()
        self.split_button.x_offset = 0
        self.split_button.y_offset = split_glob_off
        self.split_button.element = self.spleet_canvas.create_image(self.center_x_loc,
                                                                    self.center_y_loc + self.split_button.y_offset, tags="splitButton", image=self.split_button_img, anchor="center")
        self.spleet_canvas.tag_bind(
            "splitButton", "<Button-1>", self.split_song)
        self.spleet_canvas.tag_bind(
            "splitButton", "<Enter>", lambda event: on_cursor_overlap(self.spleet_canvas))
        self.spleet_canvas.tag_bind(
            "splitButton", "<Leave>", lambda event: on_cursor_endoverlap(self.spleet_canvas))
        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        # Progress Bar
        # --------------------------------------------------------------------------
        self.prog_bar_running = False  # Is the prog bar running or not.
        prog_glob_off = 193

        self.style.configure("green.Horizontal.TProgressbar",
                             troughcolor='black', background=resources.prog_bar_color, border=0,  borderwidth=0, highlightthickness=0, relief="flat")

        prog_bar_frame = Frame(
            self.spleet_canvas, background="#000000", borderwidth=0)
        self.prog_bar = ttk.Progressbar(prog_bar_frame, orient="horizontal",
                                        length=400, mode="indeterminate", style="green.Horizontal.TProgressbar")

        prog_bar_frame.pack()

        # To test the prog bar, set the prog_bar_running to true and uncomment these lines ->
        # self.prog_bar.grid(row=0, column=0) #For testing
        # self.run_progbar_anim() #for testing

        self.prog_bar_container = canvas_element()
        self.prog_bar_container.y_offset = 0 + prog_glob_off
        self.prog_bar_container.element = self.spleet_canvas.create_window(self.center_x_loc, self.center_y_loc + self.prog_bar_container.y_offset,
                                                                           anchor=CENTER, window=prog_bar_frame)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # Output Box
        # --------------------------------------------------------------------------
        output_glob_off = 133  # increase to move down

        self.output_border = Frame(self.spleet_canvas, highlightbackground="#b096ff",
                                   highlightcolor="#b096ff", highlightthickness=2, bd=0, background="black")
        self.output_label = Text(self.output_border, bg="black", fg="white", width=50, height=5, font=(
            self.font_name, 10, self.font_weight), bd=0)
        self.output_label.insert(
            END, "Welcome to Spleet Space.\nWaiting for input...")
        self.output_label.grid(row=0, column=0, padx=10, pady=10)
        self.output_border.grid(row=0, column=0, padx=5)

        self.output_border.pack()

        self.output_container = canvas_element()
        self.output_container.y_offset = 120 + output_glob_off
        self.output_container.element = self.spleet_canvas.create_window(self.center_x_loc, self.center_y_loc + self.output_container.y_offset,
                                                                         anchor=CENTER, window=self.output_border)
        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        # Help Page Code
        # --------------------------------------------------------------------------
        # help section's body of text:
        help_text_label = '''

        Stems:  The song can be split into the following sets of tracks:
        2 stems: Vocals and Accompaniment (all the music)
        4 stems: Vocals, drums, bass, and all other sounds
        5 stems: Vocals, drums, bass, piano, and all other sounds

            Note:   If sounds bleed into the wrong tracks, separating the song into a different number of stems might work better; The previous output will be overwritten. You can also edit the stems' audio in other software.
            

        Include Up to 16 kHz Frequency: By default, the audio separation process discards frequencies above 11kHz. If the 16 kHz option is checked, the exported tracks will include frequencies up to 16kHz. Using the 16kHz option might result in unexpected artifacting in the exported tracks.
        

        Song to Separate: Pick an audio track to separate into stems. The supported file types are .mp3, .mp4, .m4a, .wav, .wma, .flac, .aiff, .webm, .ogg.


        Split: The stems from a song separation will be outputted as .wav tracks and saved in a folder to the location you chose.

_____________________________________________________________________________________________________________________________________________


        Youtube Download URL: Please make sure the video is public, not paid content (Members-Only), not age-restricted, not a livestream, and not removed, otherwise the download won't work.


        Download: Youtube videos are saved to the specified location as audio-only .mp4 files.'''


        self.help_text_label = self.help_canvas.create_text(self.center_x_loc, self.center_y_loc - 20, width=1000 if (self.window_width - 50) > 1000 else self.window_width - 50,
                                                            anchor=CENTER, text=help_text_label, fill="white", font=(self.font_name, 10, self.font_weight), justify="center")
        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        # Binding the resizers of each canvas
        # --------------------------------------------------------------------------
        self.spleet_canvas.bind("<Configure>", self.resize_handler)
        # self.youtube_canvas.bind("<Configure>", self.resize_handler)
        self.help_canvas.bind("<Configure>", self.resize_handler)
        # --------------------------------------------------------------------------

        # Finally show the window!
        self.root.state("normal")
        self.root.focus_force()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        root.geometry('%dx%d+%d+%d' % (resources.minsizew,
                      resources.minsizeh, window_x_location, window_y_location))




    # Gets called on exit. Removes the font resource from windows.
    def on_exit(self):
        self.root.destroy()
        gdi32 = ctypes.WinDLL('gdi32')
        gdi32.RemoveFontResourceW(resources.font_path)
        gdi32.RemoveFontResourceW(resources.label_font_path)




    # Starts the prog bar animation
    def run_progbar_anim(self):
        if self.prog_bar_running:
            self.prog_bar.step(2)
            self.root.after(10, self.run_progbar_anim)




    # Function for splitting songs
    # Starts a thread to split the song.
    # A thread is necessary so the gui doesn't freeze up while the song is being split
    def split_song(self, event):

        if self.save_location != "" and self.file_location != "":
            self.output_label.insert(
                END, "\n\nSplitting Song: " + os.path.split(self.file_location)[1])
            self.output_label.see(END)

            self.prog_bar.grid(row=0, column=0)
            self.prog_bar_running = True
            self.run_progbar_anim()

            # Create and start the splitting thread.
            self.spleet_thread = threading.Thread(target=lambda: self.splitter_thread(
                self.stem_option_selection.get(), self.freq_selection.get(), self.que))
            self.spleet_thread.daemon = True
            self.spleet_thread.start()
            self.monitor_splitting_thread(self.spleet_thread)

        else:
            self.output_label.insert(
                END, "\n\nERROR: You must pick a song and save location.")
            self.output_label.see(END)




    # The thread responsible for splitting the song.
    def splitter_thread(self, stems, freq, que):

        freq_option = ""
        if (freq):
            freq_option = "-16kHz"

        # This gets just the song name without path.
        song_name = os.path.split(self.file_location)[1]

        command = [".\lib\python.exe", "-W", "ignore", "-m", "spleeter", "separate", "-p", "spleeter:" +
                   str(stems) + "stems" + freq_option, "-o", self.save_location + "/output_" + song_name + freq_option, self.file_location]

        process = subprocess.run(
            command, creationflags=CREATE_NO_WINDOW, capture_output=True, text=True)
        que.put(process.stdout)




    # Monitors the splitting thread to see when it finishes.
    def monitor_splitting_thread(self, thread):
        if thread.is_alive():
            self.root.after(100, lambda: self.monitor_splitting_thread(thread))
        else:
            song_name = os.path.split(self.file_location)[1]
            self.prog_bar_running = False
            self.prog_bar.grid_remove()
            output = self.que.get()
            # if output[0] == 'E':
            #     self.output_label.insert(END, "\n\n" + output)
            # else:
            self.output_label.insert(
                    END, "\n\nSplitting Complete! " + song_name + " has been split and saved at " + self.save_location)
            self.output_label.see(END)
            # self.que.queue.clear()




    # Radio Button Handler for Frequency
    def freq_checkbox_handler(self):
        if self.freq_selection.get():
            self.output_label.insert(
                END, "\n\nFrequency Range set to: 0-16 kHz (not always recommended)")
        else:
            self.output_label.insert(
                END, "\n\nFrequency Range set to: 0-11 kHz")

        self.output_label.see(END)




    # Radio Button Handler for Stems
    def set_stem_option(self):
        self.output_label.insert(
            END, "\n\nStem Option set to: " + str(self.stem_option_selection.get()))
        self.output_label.see(END)




    # Function for opening the file Browser
    def browse_files(self, event):

        self.file_location = filedialog.askopenfilename(
            initialdir="/", title="Select a File", filetypes=[("Audio File", "*.mp3 *mp4 *.m4a *.wav *.ogg *.wma *.flac *.aiff *.webm")])

        if (self.file_location == ""):
            self.chosen_file_label.configure(text="File Location")
            self.chosen_file_label.configure(anchor="w")
            self.output_label.insert(
                END, "\n\nDid not load a file. Please load a file!")

        else:
            self.chosen_file_label.configure(
                text="" + os.path.split(self.file_location)[1])
            self.chosen_file_label.configure(anchor="center")
            self.output_label.insert(
                END, "\n\nLoaded Song File: " + os.path.split(self.file_location)[1])

        self.output_label.see(END)




    # Function for opening the file Browser
    def browse_save_location(self, event):

        self.save_location = filedialog.askdirectory()
        if (self.save_location == ""):
            self.save_file_label.configure(text="Save Location")
            self.save_file_label.configure(anchor="w")
            self.output_label.insert(
                END, "\n\nDid not pick a save location. Please pick a save location!")

        else:
            self.save_file_label.configure(text="" + self.save_location)
            self.save_file_label.configure(anchor="e")
            self.output_label.insert(
                END, "\n\nSave location set to: " + self.save_location)

        self.output_label.see(END)





    # This function gets fired every time the windows is resized or moved. Updates the position of each UI element.
    def resize_handler(self, event):

        # Update our window width/height variables since the window size changed.
        self.window_width = event.width
        self.window_height = event.height + 57

        # Update the center location since the window size changed.
        self.center_x_loc = (self.window_width/2)
        self.center_y_loc = (self.window_height/2)

        # canvas resize
        self.spleet_canvas.coords(
            self.spleet_bg, self.center_x_loc, self.center_y_loc)

        # self.youtube_canvas.tag_lower(self.youtube_bg)

        # self.youtube_canvas.coords(
        # self.youtube_bg, self.center_x_loc, self.center_y_loc)

        self.help_canvas.coords(
            self.help_bg, self.center_x_loc, self.center_y_loc)

        # File Load Browser
        self.spleet_canvas.coords(self.file_browser_container.element, self.center_x_loc -
                                  self.file_browser_container.x_offset, self.center_y_loc - self.file_browser_container.y_offset)
        self.spleet_canvas.coords(self.file_title.element, self.center_x_loc -
                                  self.file_title.x_offset, self.center_y_loc - self.file_title.y_offset)
        self.spleet_canvas.coords(self.file_browser_button.element, self.center_x_loc +
                                  self.file_browser_button.x_offset, self.center_y_loc - self.file_browser_button.y_offset)

        # File Save Browser
        self.spleet_canvas.coords(self.file_save_container.element, self.center_x_loc -
                                  self.file_save_container.x_offset, self.center_y_loc - self.file_save_container.y_offset)
        self.spleet_canvas.coords(self.file_save_title.element, self.center_x_loc -
                                  self.file_save_title.x_offset, self.center_y_loc - self.file_save_title.y_offset)
        self.spleet_canvas.coords(self.save_browser_button.element, self.center_x_loc +
                                  self.save_browser_button.x_offset, self.center_y_loc - self.save_browser_button.y_offset)

        # Stems
        self.spleet_canvas.coords(self.stems_bg_image, self.center_x_loc,
                                  self.center_y_loc + self.stems_container.y_offset)
        self.spleet_canvas.coords(self.stems_frame_canvas.element, self.center_x_loc,
                                  self.center_y_loc + self.stems_frame_canvas.y_offset)

        # Freq Checkbox
        self.spleet_canvas.coords(self.freq_container.element, self.center_x_loc -
                                  self.freq_container.x_offset, self.center_y_loc + self.freq_container.y_offset)
        self.spleet_canvas.coords(self.freq_bg_image.element, self.center_x_loc,
                                  self.center_y_loc + self.freq_bg_image.y_offset)
        self.spleet_canvas.coords(self.freq_label.element, self.center_x_loc -
                                  self.freq_label.x_offset, self.center_y_loc + self.freq_label.y_offset)
        self.spleet_canvas.coords(self.black_pixel_cv.element, self.center_x_loc -
                                  self.black_pixel_cv.x_offset, self.center_y_loc + self.black_pixel_cv.y_offset)

        # Split Button
        self.spleet_canvas.coords(self.split_button.element, self.center_x_loc -
                                  self.split_button.x_offset, self.center_y_loc + self.split_button.y_offset)
        self.spleet_canvas.coords(self.prog_bar_container.element, self.center_x_loc -
                                  self.prog_bar_container.x_offset, self.center_y_loc + self.prog_bar_container.y_offset)
        self.spleet_canvas.coords(self.output_container.element, self.center_x_loc -
                                  self.output_container.x_offset, self.center_y_loc + self.output_container.y_offset)

        # Updating the location of the Help Canvas's texts
        self.help_canvas.coords(self.help_text_label,
                                self.center_x_loc, self.center_y_loc - 50)
        self.help_canvas.itemconfigure(self.help_text_label, width=1000 if (
            self.window_width - 50) > 1000 else self.window_width - 50)