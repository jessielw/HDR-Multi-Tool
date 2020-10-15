# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import tkinter as tk
import pathlib
import tkinter.scrolledtext as scrolledtextwidget
from TkinterDnD2 import *
from tkinter import messagebox

# Main Gui & Windows --------------------------------------------------------
root = TkinterDnD.Tk()
root.title("HDR10+ Parser Tool v1.0")
root.iconphoto(True, PhotoImage(file="Runtime/Images/hdrgui.png"))
root.configure(background="#434547")
window_height = 270
window_width = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)


# Bundled Apps --------------------------------------------------------------------------------------------------------
ffmpeg = '"Apps/FFMPEG/ffmpeg.exe"'
hdr10plus_parser = '"Apps/HDR10PlusParser/hdr10plus_parser.exe"'

# -------------------------------------------------------------------------------------------------------- Bundled Apps

def openaboutwindow():
    pass


# Menu Items and Sub-Bars ---------------------------------------------------------------------------------------------
my_menu_bar = Menu(root, tearoff=0)
root.config(menu=my_menu_bar)

file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Exit', command=root.destroy)

options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='Options', menu=options_menu)

options_submenu = Menu(root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Shell Options', menu=options_submenu)
shell_options = StringVar()
shell_options.set('Default')
options_submenu.add_radiobutton(label='Shell Closes Automatically', variable=shell_options, value="Default")
options_submenu.add_radiobutton(label='Shell Stays Open (Debug)', variable=shell_options, value="Debug")

help_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow)


# --------------------------------------------------------------------------------------------- Menu Items and Sub-Bars

# Frames --------------------------------------------------------------------------------------------------------------
# Video Frame -------------------------------------------------------------------------------------------
input_frame = LabelFrame(root, text=' Input ')
input_frame.grid(row=0, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
input_frame.configure(fg="white", bg="#434547", bd=3)

input_frame.rowconfigure(1, weight=1)
input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=1)

# -------------------------------------------------------------------------------------------- Video Frame

# Output Frame -------------------------------------------------------------------------------------------
output_frame = LabelFrame(root, text=' Output ')
output_frame.grid(row=2, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
output_frame.configure(fg="white", bg="#434547", bd=3)

output_frame.rowconfigure(1, weight=1)
output_frame.columnconfigure(0, weight=1)
output_frame.columnconfigure(1, weight=1)

# -------------------------------------------------------------------------------------------- Output Frame
# -------------------------------------------------------------------------------------------------------------- Frames

# Input Button Functions ----------------------------------------------------------------------------------------------
def input_button_commands():
    global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, VideoOutput
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=((
                                                           "MKV, MP4, HEVC, TS",
                                                           "*.mkv *.mp4 *.hevc *.ts"),
                                                       ("All Files", "*.*")))
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    file_extension = pathlib.Path(VideoInput).suffix
    supported_extensions = ['.mkv', '.mp4', '.hevc', '.ts']
    if VideoInput:
        if file_extension in supported_extensions:
            autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
            # Final command to get only the directory of fileinput
            autofilesave_dir_path = autofilesave_file_path.parents[0]
            VideoInputQuoted = '"' + VideoInput + '"'
            filename = pathlib.Path(VideoInput)
            VideoOut = filename.with_suffix('.json')
            autosavefilename = VideoOut.name
            VideoOutput = str(VideoOut)
            input_entry.configure(state=NORMAL)
            input_entry.insert(0, VideoInput)
            input_entry.configure(state=DISABLED)
            output_entry.configure(state=NORMAL)
            output_entry.delete(0, END)
            output_entry.configure(state=DISABLED)
            output_entry.configure(state=NORMAL)
            output_entry.insert(0, VideoOut)
            output_entry.configure(state=DISABLED)
            output_button.configure(state=NORMAL)
            start_button.configure(state=NORMAL)
        else:
            messagebox.showinfo(title="Wrong File Type",
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.")
    if not VideoInput:
        input_entry.configure(state=NORMAL)
        input_entry.delete(0, END)
        input_entry.configure(state=DISABLED)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        output_button.config(state=DISABLED)
        start_button.configure(state=DISABLED)

# ---------------------------------------------------------------------------------------------- Input Functions Button

# Drag and Drop Functions ---------------------------------------------------------------------------------------------
def drop_input(event):
    input_dnd.set(event.data)

def update_file_input(*args):
    global VideoInput, autofilesave_dir_path, VideoInputQuoted, VideoOutput, autosavefilename
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    VideoInput = str(input_dnd.get()).replace("{", "").replace("}", "")
    file_extension = pathlib.Path(VideoInput).suffix
    if file_extension == '.hevc' or file_extension == '.mkv' or file_extension == '.mp4' or file_extension == '.ts':
        autofilesave_file_path = pathlib.PureWindowsPath(VideoInput)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + VideoInput + '"'
        input_entry.insert(0, str(input_dnd.get()).replace("{", "").replace("}", ""))
        filename = pathlib.Path(VideoInput)
        VideoOut = filename.with_suffix('.json')
        autosavefilename = VideoOut.name
        VideoOutput = str(VideoOut)
        input_entry.configure(state=DISABLED)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        output_entry.configure(state=NORMAL)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        output_button.configure(state=NORMAL)
        start_button.configure(state=NORMAL)
    else:
        messagebox.showinfo(title="Wrong File Type", message="Try Again With a Supported File Type!\n\nIf this is a "
                                                             "file that should be supported, please let me know.")
# --------------------------------------------------------------------------------------------- Drag and Drop Functions

# File Output ---------------------------------------------------------------------------------------------------------
def file_save():
    global VideoOutput
    VideoOutput = filedialog.asksaveasfilename(defaultextension=".json", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("JSON", "*.json"), ("All Files", "*.*")))
    if VideoOutput:
        output_entry.configure(state=NORMAL)  # Enable entry box for commands under
        output_entry.delete(0, END)  # Remove current text in entry
        output_entry.insert(0, VideoOutput)  # Insert the 'path'
        output_entry.configure(state=DISABLED)  # Disables Entry Box

# --------------------------------------------------------------------------------------------------------- File Output

# Single Profile ------------------------------------------------------------------------------------------------------
single_profile = StringVar()
single_profile_checkbox = Checkbutton(root, text='Force Single Profile',
                                          variable=single_profile, onvalue='--force-single-profile ', offvalue='')
single_profile_checkbox.grid(row=1, column=0, columnspan=1, rowspan=1, padx=10, pady=(0, 0),
                                 sticky=N + S + E + W)
single_profile_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                      activeforeground="white", selectcolor="#434547",
                                      font=("Helvetica", 11))
single_profile.set('--force-single-profile ')


# ------------------------------------------------------------------------------------------------------ Single Profile

# Command -------------------------------------------------------------------------------------------------------------
# Start Job -----------------------------------------------------------------------------------------------------------
def start_job():
    VideoOutputQuoted = '"' + VideoOutput + '"'
    if pathlib.Path(VideoInput).suffix == '.hevc':
        finalcommand = '"' + hdr10plus_parser + ' -i ' + VideoInputQuoted + ' ' + single_profile.get() + '-o ' \
                       + VideoOutputQuoted + '"'
    elif pathlib.Path(VideoInput).suffix != '.hevc' and shell_options.get() == "Default":
        finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                       + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb \
                       -f hevc - -hide_banner -loglevel warning -stats|' \
                       + hdr10plus_parser + ' ' + single_profile.get() + '-o ' + VideoOutputQuoted + ' -' + '"'
    elif pathlib.Path(VideoInput).suffix != '.hevc' and shell_options.get() == "Debug":
        finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                       + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb -f hevc - |' \
                       + hdr10plus_parser + ' ' + single_profile.get() + '-o ' + VideoOutputQuoted + ' -' + '"'
    if shell_options.get() == "Default":
        subprocess.Popen('cmd /c ' + finalcommand)
    elif shell_options.get() == "Debug":
        subprocess.Popen('cmd /k ' + finalcommand)
# --------------------------------------------------------------------------------------------------------------- Start
# ------------------------------------------------------------------------------------------------------------- Command


# Buttons -------------------------------------------------------------------------------------------------------------
def input_button_hover(e):
    input_button["bg"] = "grey"

def input_button_hover_leave(e):
    input_button["bg"] = "#23272A"


input_dnd = StringVar()
input_dnd.trace('w', update_file_input)
input_button = tk.Button(input_frame, text="Open File", command=input_button_commands, foreground="white",
                         background="#23272A", borderwidth="3")
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', drop_input)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

input_entry = Entry(input_frame, width=35, borderwidth=4, background="#CACACA")
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', drop_input)


def output_button_hover(e):
    output_button["bg"] = "grey"

def output_button_hover_leave(e):
    output_button["bg"] = "#23272A"

output_button = Button(output_frame, text="Save File", command=file_save, state=DISABLED, foreground="white",
                       background="#23272A", borderwidth="3")
output_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
output_entry = Entry(output_frame, width=35, borderwidth=4, background="#CACACA")
output_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)\


def start_button_hover(e):
    start_button["bg"] = "grey"

def start_button_hover_leave(e):
    start_button["bg"] = "#23272A"

start_button = Button(root, text="Start Job", command=start_job, state=DISABLED, foreground="white",
                       background="#23272A", borderwidth="3", width=15)
start_button.grid(row=3, column=3, columnspan=1, padx=20, pady=5, sticky=E+N+S)
start_button.bind("<Enter>", start_button_hover)
start_button.bind("<Leave>", start_button_hover_leave)

# ------------------------------------------------------------------------------------------------------------- Buttons

# End Loop ------------------------------------------------------------------------------------------------------------
root.mainloop()
