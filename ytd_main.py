"""
Youtube Downloader application using Pytube and Tkinter libraries
scripted and developed by Vedant Raghuwanshi
A huge shout out to developers of Pytube and Tkinter libraries
Contact : raghuvedant00@gmail.com
"""

import pytube
import math
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, StringVar, IntVar, Entry
import re     # module for regular expression
import time
import os

# Graphical User Input(GUI)*********************************************************************************************
def create_GUI_layout(window):

    def modify_folder():
        down_dir = filedialog.askdirectory(initialdir="/", parent=window)
        folder_text.set(down_dir)

    def initiate_downloads():
        # extract the inputs from the dialogs and checkboxes
        down_link = entry_link.get()
        down_dir = download_entry.get()
        audio = audio_var.get()
        video = video_var.get()
        video_only = video_only_var.get()
        #do the download
        initiate_download(down_link, down_dir, audio, video, video_only)

    def display_about():
        messagebox.showinfo('ABOUT',
                            "Youtube Downloader v1.0\n"
                            'Developed by : Vedant Raghuwanshi\n'
                            'Python Version: 3.7.3'
                            'Libraries:Tkinter v4.2.0, Pytube v9.5.0\n'
                            'Contact: raghuvedant00@gmail.com\n'
                            'Github: 007vedant\n'
                            'hackerrank/hackerearth/codechef: perplexed_v')

    def display_help():
        messagebox.showinfo("HELP",
                            'Hi! Welcome to Youtube Downloader v1.0.\n\n'
                            'Multiple options have been provided to download video as per user'+"'"+'s choice.'
                            ' Presently v1.0 supports download of audio, 720p video and video without audio.'
                            ' Users can select the options as per required via checkboxes.'
                            ' Users can also download files in their desired folder.\n \n'
                            ' Thank You and Enjoy !'
                            )

    # Main title label
    title = tk.Label(window, text="YouTube Downloader", font=('Arial Bold', 20), fg='black')
    title.place(x=385, y=20, anchor="center")

    # Display about button
    display_help_button = tk.Button(window, text='About ?', font=("Arial Bold", 10),command=display_about)
    display_help_button.place(x=15, y=455)

    # Shop help button
    display_help_file_button = tk.Button(window, text="Show help", font=("Arial Bold", 10),command=display_help)
    display_help_file_button.place(x=650, y=455)

    # Label for Youtube link
    link_label = tk.Label(window, text=" Enter video URL here: ", font=("Arial Bold", 10))
    link_label.place(x=300, y=75)

    down_link_text = StringVar()
    entry_link = Entry(window, width=85, textvariable=down_link_text) #textbox for user entry
    entry_link.pack()
    entry_link.focus_set()  # moves the keyboard input to the textbox
    entry_link.place(x=125, y=100)

    # audio and video checkboxes
    option_label = tk.Label(window, text="Download options available:", font=("Arial Bold", 10))
    option_label.place(x=285, y=175)

    audio_var = IntVar()
    option_button_audio = tk.Checkbutton(window, text="MP3 Audio Track", font=("Arial Bold", 10), variable=audio_var)
    option_button_audio.place(x=190, y=200)

    video_var = IntVar()
    option_button_video = tk.Checkbutton(window, text="720p Video", font=("Arial Bold", 10), variable=video_var)
    option_button_video.place(x=331, y=200)

    video_only_var = IntVar()
    option_button_video_only = tk.Checkbutton(window, text="720p Video(no audio)", font=("Arial Bold", 10), variable=video_only_var)
    option_button_video_only.place(x=435, y=200)

    # output folder selection
    download_folder_label = tk.Label(window, text="Select your download folder:", font=("Arial Bold", 10))
    download_folder_label.place(x=285, y=255)

    folder_text = StringVar()
    download_entry = Entry(window, width=85, textvariable=folder_text)
    desktop_address = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') #gets the address of the user's desktop
    folder_text.set(desktop_address)
    download_entry.pack()
    download_entry.place(x=125, y=280)

    modify_folder_button = tk.Button(window,text="Select Folder",font=("Arial Bold", 10),command=modify_folder)
    modify_folder_button.place(x=330, y=305)

    # download button - triggers data extraction and download actions
    download_button = tk.Button(window, text="Start Download", font=("Arial Bold", 20), command=initiate_downloads)
    download_button.place(x=265, y=350)


# DOWNLOAD *******************************************************************************************************
def initiate_download(down_link, down_dir, audio, video, video_only):
    start = time.time()

    # create input warnings
    if len(down_link) == 0:
        messagebox.showinfo("Warning !", 'You have not provided a link for download.\nPlease paste or enter a YouTube link')
    elif audio + video + video_only == 0:
        messagebox.showinfo("Warning !", 'You have not selected a file type to download.\nPlease select atleast one of the options to download')

    # proceed if no input warnings are required
    else:
        print("File or link being operated: ", down_link)
        print("Download directory: ", down_dir)

        # Use regular expressions to check if the link is a txt document and process the contents into a list
        pattern = r"txt$"

        # this section will process txt files containing YouTube links
        if re.findall(pattern, down_link): # looks for the "txt" at the end and if found it treats it as a file
            file = open(down_link)
            content = file.readlines()
            links_processed = [x.strip() for x in content]  # to remove whitespace
            file.close()

            number_of_links = len(links_processed)
            total_files_to_download = (audio + video + video_only) * number_of_links

            individual_link_count = 0
            for each_link in links_processed:
                print("Attempting to download:", each_link)

                get_label = tk.Label(window, text="Obtaining stream info (10 secs...)", font=("Arial Bold", 20))
                get_label.place(x=260, y=250)
                canvas.update_idletasks()

                yt = pytube.YouTube(each_link) # this link takes around 10 seconds due to the need to contact YouTube for stream info
                yt.register_on_progress_callback(display_progress)  # set the on_progress_callback to run the display_progress function at each trifle

                stream = []
                if video == 1:
                    all_video_streams = yt.streams.filter(subtype='mp4', progressive=True).all()
                    stream.append(all_video_streams[0])
                if audio == 1:
                    all_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').all()
                    stream.append(all_audio_streams[0])
                if video_only == 1:
                    all_video_only_streams = yt.streams.filter(subtype='mp4', only_video=True).order_by('resolution').all()
                    stream.append(all_video_only_streams[0])

                end = time.time()
                print("Time Elapsed:", end - start, "seconds")
                get_label.destroy()
                canvas.update() # destroy canvas object using .update()

                for item in stream:
                    individual_link_count += 1
                    print("Downloading:",item)
                    items_label = tk.Label(window, text="Downloading file " + str(individual_link_count) + " of " + str(total_files_to_download), font=("Arial Bold", 20))
                    items_label.place(x=260, y=290)
                    canvas.update_idletasks()

                    #create a different filename for audio, video, and video only so that files don't get overwritten with the same name
                    if item.has_audio is False and item.has_video is True:
                        item_type = "video (no sound)"
                    elif item.has_audio is True and item.has_video is True:
                        item_type = "video"
                    elif item.has_audio is True and item.has_video is False:
                        item_type = "audio"
                    else:
                        item_type = ""  # this line should never eventuate
                    filename = str(item.default_filename)+" - "+item_type

                    item.download(down_dir, filename)  # download process here
                    print("\nDownload complete")
                    end = time.time()
                    print("Time Elapsed:", end - start, "seconds")

        else:   # processing if 1 link given
            print("Attempting to download:", down_link)
            individual_link_count = 0
            total_files_to_download = (audio + video + video_only)

            get_label = tk.Label(window, text="Getting stream info (takes 10 sec)", font=("Arial Bold", 20))
            get_label.place(x=260, y=250)
            canvas.update_idletasks()

            yt = pytube.YouTube(down_link) # time: 10 secs for connecting to Youtube
            yt.register_on_progress_callback(display_progress)  #_progress_callback to run the display_progress function at each trifle

            stream = []
            if audio == 1:
                all_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').all()
                stream.append(all_audio_streams[0])
            if video == 1:
                all_video_streams = yt.streams.filter(subtype='mp4', progressive=True).all()
                stream.append(all_video_streams[0])
            if video_only == 1:
                all_video_only_streams = yt.streams.filter(subtype='mp4', only_video=True).order_by('resolution').all()
                stream.append(all_video_only_streams[0])

            end = time.time()
            print("Current Runtime:", end - start, "seconds")
            get_label.destroy()
            canvas.update()  # destroy canvas object using .update()

            for item in stream:
                individual_link_count += 1
                print("Downloading:", item)
                items_label = tk.Label(window, text="Downloading file " + str(individual_link_count) + " of " + str(total_files_to_download), font=("Arial Bold", 20))
                items_label.place(x=260, y=290)
                canvas.update_idletasks()

                # naming files differently to avoid overwrite
                if item.has_audio is False and item.has_video is True:
                    item_type = "video (no sound)"
                elif item.has_audio is True and item.has_video is True:
                    item_type = "video"
                elif item.has_audio is True and item.has_video is False:
                    item_type = "audio"
                else:
                    item_type = ""  # error case/ 0 occurrence
                filename = str(item.default_filename) + " - " + item_type

                item.download(down_dir, filename)
                print("\nDownload complete")
                end = time.time()
                print("Time Elapsed:", end - start, "seconds")
                

def display_progress(stream, trifle, file_handle, bytes_left):
    bytes_downloaded = file_handle.tell()
    total_bytes = bytes_left + bytes_downloaded
    percentage_progess = math.floor((bytes_downloaded / total_bytes)*100)
    print('\rProgress: '+str(percentage_progess)+' %',end="")

    progress_label = tk.Label(window, text="Progress: " + str(percentage_progess) + "%    ", font=("Arial Bold", 20))
    progress_label.place(x=260, y=330)
    canvas.update_idletasks()

# Init action for tkinter window and canvas


window = tk.Tk()
window.config(bg='red')
window.title('Youtube Downloader v1.0')
canvas = Canvas(window, width=750, height=500, bg='red')
canvas.pack()
window.resizable(0,0)
create_GUI_layout(window)
window.mainloop()