import os
import json
import random
import pygame
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

#Configurations, variables declaration and loading of music files
root = TkinterDnD.Tk()
root.title("Music Player")
root.resizable(False, False)
root.iconbitmap("icons/music.ico")
root.configure(bg="black")

config_file = "config.json"
playlist_file = "music.txt"

music_pos = 0 # music position in milliseconds
characters = 25 # characters to display in the music name
volume = 100 # volume of the music
closed = False # music list closed
first = True # first time playing music
stopped = True # music stopped
repeat_mode = False # repeat mode
shuffle_mode = False # shuffle mode

music = [] # music files
music_name = [] # music names in the list

# Loading of images
prev_img = ImageTk.PhotoImage(Image.open("icons/prev.png"))
pause_img = ImageTk.PhotoImage(Image.open("icons/pause.png"))
play_img = ImageTk.PhotoImage(Image.open("icons/play.png"))
next_img = ImageTk.PhotoImage(Image.open("icons/next.png"))
list_img = ImageTk.PhotoImage(Image.open("icons/list.png"))
add_song_img = ImageTk.PhotoImage(Image.open("icons/add_song.png"))
circle_img = ImageTk.PhotoImage(Image.open("icons/circle.png"))
close_img = ImageTk.PhotoImage(Image.open("icons/close.png"))
repeat_on_img = ImageTk.PhotoImage(Image.open("icons/repeat_on.png"))
repeat_off_img = ImageTk.PhotoImage(Image.open("icons/repeat_off.png"))
remix_on_img = ImageTk.PhotoImage(Image.open("icons/remix_on.png"))
remix_off_img = ImageTk.PhotoImage(Image.open("icons/remix_off.png"))

pygame.mixer.init() # initialize the mixer


def load_config(): # load the configuration of the music player from the config file
    global volume, repeat_mode, shuffle_mode, music, music_name, music_now, music_length, return_name

    try:
        with open(config_file, "r") as file:
            config = json.load(file)
            volume = config.get("volume", 100)
            repeat_mode = config.get("repeat_mode", False)
            shuffle_mode = config.get("shuffle_mode", False)

            with open(playlist_file, "r", encoding='utf-8') as music_file: # load the music files from the playlist file
                music = [item.replace("'", "").strip() for item in music_file.read().replace("[", "").replace("]", "").split(", ")]
            
            if music:    
                music_now = music[0]
            else: 
                ''
            
            if music_now: # get the length of the music
                music_length = pygame.mixer.Sound(music_now).get_length() * 1000
                return_name = os.path.basename(music_now)

            music_name = [os.path.basename(item) for item in music]
            
            return volume, repeat_mode, shuffle_mode

    except FileNotFoundError:
        return 100, False, False


def update_icons(): # update the icons of the repeat and shuffle buttons
    if repeat_mode:
        repeat_button['image'] = repeat_on_img
    else:
        repeat_button['image'] = repeat_off_img
    
    if shuffle_mode:
        shuffle_button['image'] = remix_on_img
    else:
        shuffle_button['image'] = remix_off_img


volume, repeat_mode, shuffle_mode = load_config() # load the configuration of the music player
pygame.mixer.music.set_volume(volume / 100) # set the volume of the music player


def play_music(): # play or pause the music
    global music_now
    global stopped
    global first

    if stopped: 
        play_pause_button['image'] = play_img

        if music_now != "":
            pygame.mixer.music.pause()
        stopped = False

    else:
        if first and music_now != "":
            pygame.mixer.music.load(music_now)
            pygame.mixer.music.play()
            first = False
            play_pause_button['image'] = pause_img
            stopped = True

        elif music_now != "":
            play_pause_button['image'] = pause_img
            pygame.mixer.music.unpause()
            stopped = True


def delete_music(): # delete the music from the playlist
    global music
    selected = music_list.curselection()

    if selected:
        index = selected[0]
        deleted_track = music.pop(index)
        music_list.delete(index)
        open(playlist_file, "r+").truncate()
        open(playlist_file, "w").write(str(music))
        
        global music_now, first, stopped
        if music_now == deleted_track: # if the music is playing, stop it
            pygame.mixer.music.stop()
            music_now = ''
            first = True
            stopped = True
            play_pause_button['image'] = play_img


def set_track(new_track=None): # set the track to play
    global music_now, music_length, music_pos, first, stopped
    global characters
    global return_name

    if new_track:
        music_now = new_track
    
    if music_now != "":
        music_length = pygame.mixer.Sound(music_now).get_length() * 1000

    music_pos = 0
    pygame.mixer.music.pause()
    first = True
    stopped = False
    return_name = os.path.splitext(music_now.split("/")[-1])[0]
    play_music()
    pygame.mixer.music.unpause()


def next_track(): # play the next track
    global music_now, music_length, music_pos, first, stopped
    global characters, return_name
    global repeat_mode

    if not music:
        return
    
    if shuffle_mode:
        if music:
            prev_music = music_now

            while len(music) > 1 and music_now == prev_music:
                music_now = random.choice(music)

    else:
        for item in range(len(music)):
            if music[item] == music_now:
                next_index = (item + 1) % len(music)
                music_now = music[next_index]
                break

    if music_now:
        pygame.mixer.music.load(music_now)
        pygame.mixer.music.play()
        music_length = pygame.mixer.Sound(music_now).get_length() * 1000
        music_pos = 0
        first = False
        stopped = False
        return_name = music_now.split("/")[-1]
        play_music()
        pygame.mixer.music.unpause()


def prev_track(): # play the previous track
    global music_now, music_length, music_pos, first, stopped
    global characters, return_name

    for item in range(len(music)):

        if music[item] == music_now:
            prev_index = (item - 1) % len(music)
            pygame.mixer.music.pause()
            music_pos = 0
            music_now = music[prev_index]
            music_length = pygame.mixer.Sound(music_now).get_length() * 1000
            first = True
            stopped = False
            return_name = music_now.split("/")[-1]
            play_music()
            pygame.mixer.music.unpause()
            break


def add_song(): # add a song to the playlist
        global music
        file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3;*.wav")])

        if file not in music:
            music.append(file)
            open(playlist_file, "r+").truncate()
            open(playlist_file, "w").write(str(music))
            music_list.insert("end", file.split("/")[-1])
            set_track(music[-1])


def toggle_repeat(): # toggle the repeat mode
    global repeat_mode, shuffle_mode
    repeat_mode = not repeat_mode

    if repeat_mode: # if repeat mode is on, turn off shuffle mode
        shuffle_mode = False
        shuffle_button['image'] = remix_off_img
    else:
        repeat_button['image'] = repeat_off_img

    if repeat_mode:
        repeat_button['image'] = repeat_on_img
    else:
        repeat_off_img

    save_config()


def toggle_shuffle(): # toggle the shuffle mode
    global shuffle_mode, repeat_mode
    shuffle_mode = not shuffle_mode

    if shuffle_mode: # if shuffle mode is on, turn off repeat mode
        repeat_mode = False
        repeat_button['image'] = repeat_off_img

    if shuffle_mode:
        shuffle_button['image'] = remix_on_img

    else:
        remix_off_img

    save_config()


def set_volume(val=None): # set the volume of the music player
    global volume
    if val is not None:
        volume = int(val)
    pygame.mixer.music.set_volume(volume / 100)
    save_config()


def save_config(): # save the configuration of the music player
    config = {
        "volume": volume,
        "repeat_mode": repeat_mode,
        "shuffle_mode": shuffle_mode
    }
    with open(config_file, "w") as file:
        json.dump(config, file)


def position(): # set the position of the music player when clicked on the music bar to change the position of the music
        global music_pos
        if not first:
            if music_now != "":
                positionx = frame.winfo_pointerx() - frame.winfo_rootx()
                music_pos = ((positionx - 50) / 200 * music_length)
                pygame.mixer.music.stop()
                pygame.mixer.music.play()
                pygame.mixer.music.set_pos(music_pos / 1000)
                
                if not stopped:
                    pygame.mixer.music.pause()


def find_x(): # find the x position of the circle in the music bar and the elapsed time of the music
    global music_length
    if music_now != "":
        pos = pygame.mixer.music.get_pos()
        
        if pos != -1: # if the music is playing
            elapsed_time = int(pos + music_pos)

            if elapsed_time >= music_length: # if the music is finished, play the next track
                next_track()
                elapsed_time = 0

            return elapsed_time, ((elapsed_time / music_length) * 200 + 50) # return the elapsed time and the x position of the circle
        
    return 0, 50


def format_time(ms): # format the time in minutes and seconds
    seconds = int(ms / 1000)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"


def text(track_name): # display the track name function
    global characters
    max_visible_length = 25
    spacing = " " * 10

    if len(track_name) <= max_visible_length: 
        padding = (max_visible_length - len(track_name)) // 2

        return " " * padding + track_name + " " * padding
    
    else:
        full_track_name = track_name + spacing
        if characters >= len(track_name):
            characters = 0

        display_name = full_track_name[characters:] + full_track_name[:characters]
        characters += 1

        return display_name


def handle_drop(event): # handle the drop of the music file
    global music
    music_files = root.tk.splitlist(event.data)
    for music_file in music_files:
        if music_file.lower().endswith(('.mp3', '.wav')):
            if music_file not in music:
                music.append(music_file)
                open(playlist_file, "r+").truncate()
                open(playlist_file, "w").write(str(music))
                music_list.insert("end", music_file.split("/")[-1])
                set_track(music[-1])


def update(): # update the music player
    global music_now, music_list, stopped, first, music_pos

    update_icons()

    if music_now: # music
        elapsed_time, pos_x = find_x()
        time_label['text'] = format_time(elapsed_time)
        name['text'] = text(os.path.splitext(music_now.split("/")[-1])[0])
        name.configure(anchor="center")
        circle_pos.place(x=pos_x, y=128)

    else: # no music
        name['text'] = ""
        time_label['text'] = "00:00"
        circle_pos.place(x=50, y=128)

    if not pygame.mixer.music.get_busy() and stopped and not first: # music finished
        if repeat_mode:
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            music_pos = 0

        elif shuffle_mode: # play a random track
            random_track = random.choice(music)
            set_track(random_track)

        else: # play the next track
            next_track()

    if not closed: # music list
        selection = music_list.curselection()
        
        if selection:
            selected_index = selection[0]
            
            if music_now != music[selected_index]:
                set_track(music[selected_index])

    root.after(200, update)


def music_UI(): # open or close the music list
    global closed
    if closed:
        root.geometry("300x400")
        closed = False
        list_button['image'] = close_img

    else:
        root.geometry("300x200")
        closed = True
        list_button['image'] = list_img


# GUI of the music player
frame = Frame(root)
frame.pack(fill=tk.BOTH, expand=False)

prev_button = Button()
prev_button.configure(bg="black", image=prev_img, command=prev_track)
prev_button.place(x=35, y=35)

play_pause_button = Button()
play_pause_button.configure(bg="black", image=play_img, command=play_music)
play_pause_button.place(x=115.5, y=35)

volume_slider = Scale()
volume_slider.configure(from_=100, to=0, orient="vertical", command=set_volume, bg="black", fg="white", highlightbackground="black", troughcolor="gray", sliderrelief="flat", label="Volume")
volume_slider.set(volume)
volume_slider.place(x=260, y=10, height=180)

next_button = Button()
next_button.configure(bg="black", image=next_img, command=next_track)
next_button.place(x=196, y=35)

list_button = Button()
list_button.configure(bg="black", image=list_img, command=music_UI)
list_button.place(x=10, y=170)

add_song_button = Button()
add_song_button.configure(bg="black", image=add_song_img, command=add_song)
add_song_button.place(x=10, y=360)

repeat_button = Button()
repeat_button.configure(bg="black", image=repeat_off_img, command=toggle_repeat)
repeat_button.place(x=7.5, y=43)

shuffle_button = Button()
shuffle_button.configure(bg="black", image=remix_off_img, command=toggle_shuffle)
shuffle_button.place(x=7.5, y=75)

music_bar = Button()
music_bar.configure(bg="black", command=position)
music_bar.place(x=50, y=130, width=200, height=5)

time_label = Label()
time_label.configure(bg="black", fg="white", font=("Arial", 10), text="00:00")
time_label.place(x=10, y=122, width=40, height=20)

circle_pos = Label()
circle_pos.configure(bg="black", image=circle_img)

name = Label()
name.configure(bg="black", fg="white", font=("Arial", 12), anchor="center")
name.place(x=50, y=150, width=200, height=30)

delete_button = Button()
delete_button.configure(text="Delete Song", bg="red", fg="white", command=delete_music)
delete_button.place(x=115, y=360)

music_list = Listbox(listvariable=StringVar(value=music_name))
music_list.configure(bg="black", fg="white", highlightcolor="white", relief=FLAT, selectmode=EXCEPTION)
music_list.place(x=10, y=200, width=280, height=150)
music_list.drop_target_register(DND_FILES)
music_list.dnd_bind('<<Drop>>', handle_drop)


if __name__ == "__main__": # run the player
    music_UI()

    update()
    root.mainloop()
