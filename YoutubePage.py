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
from pytube import YouTube, extract, request

# Main window containing all gui elements for the download from YouTube tab.
class youtube_page:

    def __init__(self, root, parent, bg_img):
        self.font_name = resources.font_name
        self.font_weight = resources.font_weight

        # Getting the window width and height.
        self.window_width = root.winfo_width()
        self.window_height = root.winfo_height()

        # Global center location. Can be used to center everything that has anchor=CENTER.
        self.center_x_loc = (self.window_width / 2)
        self.center_y_loc = (self.window_height / 2)

        self.youtube_canvas = Canvas(parent, width=self.window_width,
                                     height=self.window_height, highlightthickness=0, background="black")

        self.youtube_bg = self.youtube_canvas.create_image(
            self.center_x_loc, self.center_y_loc, anchor=CENTER, image=bg_img)

        # -------------------------------------------------------------
        # Loading Images/Resources (all loading should be done here in the future) and Colors
        # -------------------------------------------------------------
        self.bg_image = Image.open(resources.bg_image_path)
        self.download_pg_browse_button_img = ImageTk.PhotoImage(
            Image.open(resources.download_pg_browse_button_img_path))
        self.stems_bg = ImageTk.PhotoImage(Image.open(resources.stems_bg_path))
        self.black_pixel = PhotoImage(file=resources.black_pixel_path)
        self.check_on_img = PhotoImage(file=resources.check_on_img_path)
        self.check_off_img = PhotoImage(file=resources.check_off_img_path)
        self.freq_bg = ImageTk.PhotoImage(Image.open(resources.freq_bg_path))
        self.download_pg_browse_button_img_path = ImageTk.PhotoImage(
            Image.open(resources.download_pg_browse_button_img_path))
        self.download_button_img = ImageTk.PhotoImage(
            Image.open(resources.download_button_img_path))
        # -------------------------------------------------------------

        # --------------------------------------------------------------------------
        # URL/Text input box
        # --------------------------------------------------------------------------
        self.file_location = ""
        load_glob_off = 140  # increase to move up

        file_browser_frame = Frame(
            self.youtube_canvas, background="#000000", bd=0)

        self.file_label_border = Frame(
            file_browser_frame, highlightbackground=resources.download_pg_frame_color, highlightthickness=3, bd=0, background="black", highlightcolor=resources.download_pg_frame_color)

        self.chosen_file_label = Text(self.file_label_border, bg="black", fg="white", width=36, height=1,
                                      font=(self.font_name, 13, self.font_weight), bd=0, highlightthickness=0)

        # Placeholder text for the URL box:
        self.chosen_file_label.insert(END, "https://youtu.be/zliasEkWx0M")  # Skrillex, Starrah & Four Tet - Butterflies (Official Music Video)

        self.chosen_file_label.grid(row=0, column=0, padx=5)
        self.file_label_border.grid(row=0, column=0)

        self.file_browser_container = canvas_element()
        self.file_browser_container.x_offset = 0
        self.file_browser_container.y_offset = 160 + load_glob_off
        self.file_browser_container.element = self.youtube_canvas.create_window(self.center_x_loc, self.center_y_loc + self.file_browser_container.y_offset,
                                                                                anchor=CENTER, window=file_browser_frame)

        self.file_title = canvas_element()
        self.file_title.x_offset = 203
        self.file_title.y_offset = 198 + load_glob_off
        self.file_title.element = self.youtube_canvas.create_text(self.center_x_loc - self.file_title.x_offset, self.center_y_loc - self.file_title.y_offset, anchor=W,
                                                                  text="Youtube URL", fill="white", font=(self.font_name, 14, self.font_weight))
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # Save Location's File Browser
        # --------------------------------------------------------------------------
        self.save_location = ""
        save_glob_off = 450  # increase to move up
        self.file_save_title = canvas_element()
        self.file_save_title.x_offset = 203
        self.file_save_title.y_offset = -225 + save_glob_off
        self.file_save_title.element = self.youtube_canvas.create_text(self.center_x_loc - self.file_save_title.x_offset, self.center_y_loc - self.file_save_title.y_offset, anchor=W,
                                                                       text="Save Location", fill="white", font=(self.font_name, 14, self.font_weight))

        file_save_frame = Frame(self.youtube_canvas,
                                background="#000000", bd=0)
        self.file_save_border = Frame(
            file_save_frame, highlightbackground=resources.download_pg_frame_color, highlightthickness=2, bd=0, background="black")
        self.save_file_label = Label(self.file_save_border, text="Save Location", bg="black", fg="white",
                                     width=26, height=1, font=(self.font_name, 13, self.font_weight), bd=4, anchor='w')
        self.save_file_label.grid(row=0, column=0, padx=5)
        self.file_save_border.grid(row=0, column=0)

        self.file_save_container = canvas_element()
        self.file_save_container.x_offset = 66
        self.file_save_container.y_offset = -265 + save_glob_off
        self.file_save_container.element = self.youtube_canvas.create_window(self.center_x_loc, self.center_y_loc + self.file_save_container.y_offset,
                                                                             anchor=CENTER, window=file_save_frame)

        self.save_browser_button = canvas_element()
        self.save_browser_button.x_offset = 154
        self.save_browser_button.y_offset = -265 + save_glob_off
        self.save_browser_button.element = self.youtube_canvas.create_image(self.center_x_loc,
                                                                            self.center_y_loc, tags="browseButton", image=self.download_pg_browse_button_img, anchor="center")
        self.youtube_canvas.tag_bind(
            "browseButton", "<Button-1>", self.browse_save_location)
        self.youtube_canvas.tag_bind(
            "browseButton", "<Enter>", lambda event: on_cursor_overlap(self.youtube_canvas))
        self.youtube_canvas.tag_bind(
            "browseButton", "<Leave>", lambda event: on_cursor_endoverlap(self.youtube_canvas))

        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # YT Download Button
        # --------------------------------------------------------------------------
        download_glob_off = -76  # increase to move down
        self.download_button = canvas_element()
        self.download_button.x_offset = 0
        self.download_button.y_offset = download_glob_off
        self.download_button.element = self.youtube_canvas.create_image(self.center_x_loc,
                                                                        self.center_y_loc + self.download_button.y_offset, tags="downloadButton", image=self.download_button_img, anchor="center")
        self.youtube_canvas.tag_bind(
            "downloadButton", "<Button-1>", self.download_song)
        self.youtube_canvas.tag_bind(
            "downloadButton", "<Enter>", lambda event: on_cursor_overlap(self.youtube_canvas))
        self.youtube_canvas.tag_bind(
            "downloadButton", "<Leave>", lambda event: on_cursor_endoverlap(self.youtube_canvas))
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # Output Box
        # --------------------------------------------------------------------------
        output_glob_off = 40  # increase to move down

        # magenta:
        self.output_border = Frame(self.youtube_canvas, highlightbackground="#B20057",
                                   highlightcolor="#B20057", highlightthickness=2, bd=0, background="black")

        self.output_label = Text(self.output_border, bg="black", fg="white", width=49, height=15, font=(
            self.font_name, 10, self.font_weight), bd=0)
        self.output_label.insert(
            END, "Welcome to the Youtube MP3 Downloader!\nType into the URL box, set a location to save the file into, and then click 'Download'. You will recieve a .MP4 file upon success.")
        self.output_label.grid(row=0, column=0, padx=10, pady=10)
        self.output_border.grid(row=0, column=0, padx=5)

        self.output_border.pack()

        self.output_container = canvas_element()
        self.output_container.y_offset = 120 + output_glob_off
        self.output_container.element = self.youtube_canvas.create_window(self.center_x_loc, self.center_y_loc + self.output_container.y_offset,
                                                                          anchor=CENTER, window=self.output_border)
        # --------------------------------------------------------------------------

        self.youtube_canvas.bind("<Configure>", self.resize_handler)

    # --------------------------------------------------------------------------
    # Function for opening the file Browser to save the video to.
    # --------------------------------------------------------------------------
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
                END, "\n\nSave location set to: " + self.save_location + "\n")

        self.output_label.see(END)
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Download a Song's audio-only from YouTube
    # --------------------------------------------------------------------------

    def download_song(self, event):
        self.song_link = self.chosen_file_label.get("1.0", END)

        # Checking for empty save location
        if (self.save_location == ""):
            self.output_label.insert(
            END, "\n\nPlease pick a location to save the downloaded song to before clicking 'Download'.\n")
            self.output_label.see(END)

        # Checking for empty song link here.
        elif (self.song_link == ""):
            # corresponds to blank input for URL.
                # TODO this is also thrown when the video is age restricted and probably when the video is private too :/
            self.output_label.insert(
                END, "\n\nThere's something wrong with the link you entered. Make sure you entered it correctly and that it's not blank.\n")
            self.output_label.see(END)


        else:  # If we reach this line, we have a valid URL and save location

                try:
                    # Assume that the video is public and not age-restricted. Proceed to download the audio stream only.
                    self.yt = YouTube(self.song_link)  # make a YouTube object from the video link
                    self.output_label.insert(END, "\n\nStarting to download your song now.\n")
                    self.output_label.see(END)
                    self.audio_stream = self.yt.streams.filter(only_audio=True).first()  # returns an MP4 by default.
                    self.output_label.insert(
                        END, "\nRetrieved the audio stream.\n")
                    self.output_label.see(END)
                    self.audio_stream.download(output_path=self.save_location)
                    self.output_label.insert(
                        END, "\n\nSuccessfully downloaded the song to: " + self.save_location + "\n")
                    self.output_label.see(END)


                except Exception: # is supposed to correspond to a general VideoUnavailable error

                    self.watch_html = request.get(url=self.song_link) 

                    # Check if the video is private.                    
                    if (extract.is_private(self.watch_html)):
                       self.output_label.insert(END, "\nDownloading the song failed. The video is private. Please change the video link to a public video.\n")
                       self.output_label.see(END)

                    # Check if age restrcicted
                    elif (extract.is_age_restricted(self.watch_html)):
                            self.output_label.insert(
                                END, "\n\nDownloading the song failed because the video for it is age-restricted. Try to find a non-age restricted video containing this song and try again. Error: \n")
                            self.output_label.see(END)
                    else:
                        self.output_label.insert(
                            END, "\n\nDownloading the song failed. The video is Unavailable. Make sure the video wasn't removed, is public, is not Members-only (paid content), and is NOT age-restricted. The video cannot be a livestream either. Please find an alernative video to download.\n\n")
                        self.output_label.see(END)           
    # --------------------------------------------------------------------------------------------




    # --------------------------------------------------------------------------------------------
    def resize_handler(self, event):

        # Update our window width/height variables since the window size changed.
        self.window_width = event.width
        self.window_height = event.height + 57

        # Update the center location since the window size changed.
        self.center_x_loc = (self.window_width/2)
        self.center_y_loc = (self.window_height/2)

        # Background setup
        self.youtube_canvas.coords(
            self.youtube_bg, self.center_x_loc, self.center_y_loc)

        # File Load Browser
        self.youtube_canvas.coords(self.file_browser_container.element, self.center_x_loc -
                                   self.file_browser_container.x_offset, self.center_y_loc - self.file_browser_container.y_offset)
        self.youtube_canvas.coords(self.file_title.element, self.center_x_loc -
                                   self.file_title.x_offset, self.center_y_loc - self.file_title.y_offset)

        # File Save Browser
        self.youtube_canvas.coords(self.file_save_container.element, self.center_x_loc -
                                   self.file_save_container.x_offset, self.center_y_loc - self.file_save_container.y_offset)
        self.youtube_canvas.coords(self.file_save_title.element, self.center_x_loc -
                                   self.file_save_title.x_offset, self.center_y_loc - self.file_save_title.y_offset)
        self.youtube_canvas.coords(self.save_browser_button.element, self.center_x_loc +
                                   self.save_browser_button.x_offset, self.center_y_loc - self.save_browser_button.y_offset)

        # Download Button
        self.youtube_canvas.coords(self.download_button.element, self.center_x_loc -
                                   self.download_button.x_offset, self.center_y_loc + self.download_button.y_offset)
        self.youtube_canvas.coords(self.output_container.element, self.center_x_loc -
                                   self.output_container.x_offset, self.center_y_loc + self.output_container.y_offset)
      
        # Output box
        self.youtube_canvas.coords(self.output_container.element, self.center_x_loc -
                                   self.output_container.x_offset, self.center_y_loc + self.output_container.y_offset)