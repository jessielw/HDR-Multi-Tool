# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import tkinter as tk
import pathlib
from TkinterDnD2 import *
from tkinter import messagebox
import shutil
import threading
from tkinter import ttk
from Packages.about import openaboutwindow
from configparser import ConfigParser

# Main Gui & Windows --------------------------------------------------------
def root_exit_function():  # Asks if user wants to close main GUI + close all tasks
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                               "     Note: This will end all current tasks!",
                                       parent=root)
    if confirm_exit == False:
        pass
    elif confirm_exit == True:
        try:
            subprocess.Popen(f"TASKKILL /F /im HDR10PlusParser.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            root.destroy()
        except:
            root.destroy()

root = TkinterDnD.Tk()  # Main GUI with TkinterDnD function (for drag and drop)
root.title("HDR10+ Parser Tool v1.21")
root.iconphoto(True, PhotoImage(file="Runtime/Images/hdrgui.png"))
root.configure(background="#434547")
window_height = 300
window_width = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
root.protocol('WM_DELETE_WINDOW', root_exit_function)

for n in range(4):
    root.grid_columnconfigure(n, weight=1)
for n in range(3):
    root.grid_rowconfigure(n, weight=1)

# Bundled Apps --------------------------------------------------------------------------------------------------------
config_file = 'Runtime/config.ini'  # Creates (if doesn't exist) and defines location of config.ini
config = ConfigParser()
config.read(config_file)

try:  # Create config parameters
    config.add_section('ffmpeg_path')
    config.set('ffmpeg_path', 'path', '')
    config.add_section('parser_path')
    config.set('parser_path', 'path', '')  # First is section, second is key, and third is the value
    with open(config_file, 'w') as configfile:
        config.write(configfile)
except:
    pass

# Bundled app path(s) -------------------------------
ffmpeg = config['ffmpeg_path']['path']
hdr10plus_parser = config['parser_path']['path']
mediainfocli = '"Apps/MediaInfoCLI/MediaInfo.exe"'
# Bundled app path(s) -------------------------------

def check_ffmpeg():
    global ffmpeg
    # FFMPEG --------------------------------------------------------------
    if shutil.which('ffmpeg') != None:
        ffmpeg = '"' + str(pathlib.Path(shutil.which('ffmpeg'))).lower() + '"'
        messagebox.showinfo(title='Prompt!', message='ffmpeg.exe found on system PATH, '
                                                     'automatically setting path to location.\n\n'
                                                     '             Note: This can be changed in the config.ini file')
        rem_ffmpeg = messagebox.askyesno(title='Delete Included ffmpeg?',
                                         message='Would you like to delete the included FFMPEG?')
        if rem_ffmpeg == True:
            shutil.rmtree(str(pathlib.Path("Apps/ffmpeg")))
        try:
            config.set('ffmpeg_path', 'path', ffmpeg)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except:
            pass
    elif ffmpeg == '' and shutil.which('ffmpeg') == None:
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"ffmpeg.exe" located in the "Apps" folder')
        ffmpeg = '"' + str(pathlib.Path("Apps/ffmpeg/ffmpeg.exe")) + '"'
        try:
            config.set('ffmpeg_path', 'path', ffmpeg)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except:
            pass
    # FFMPEG ------------------------------------------------------------------
def check_hdr10plus_parser():
    global hdr10plus_parser
    # HDR10plus_parser --------------------------------------------------------
    if shutil.which('hdr10plus_parser') != None:
        hdr10plus_parser = '"' + str(pathlib.Path(shutil.which('hdr10plus_parser'))).lower() + '"'
        messagebox.showinfo(title='Prompt!', message='hdr10plus_parser.exe found on system PATH, '
                                                     'automatically setting path to location.\n\n'
                                                     '             This can be changed in the config.ini file')
        try:
            config.set('parser_path', 'path', hdr10plus_parser)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except:
            pass
    elif hdr10plus_parser == '' and shutil.which('hdr10plus_parser') == None:
            messagebox.showinfo(title='Info', message='Program will use the included '
                                                      '"hdr10plus_parser.exe" located in the "Apps" folder')
            hdr10plus_parser = '"' + str(pathlib.Path('Apps/HDR10PlusParser/hdr10plus_parser.exe')) + '"'
            try:
                config.set('parser_path', 'path', hdr10plus_parser)
                with open(config_file, 'w') as configfile:
                    config.write(configfile)
            except:
                pass
    # HDR10plus_parser --------------------------------------------------------


# -------------------------------------------------------------------------------------------------------- Bundled Apps

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

def set_ffmpeg_path():
    global ffmpeg
    path = filedialog.askopenfilename(title='Select Location to "ffmpeg.exe"', initialdir='/',
                                      filetypes=[('ffmpeg', 'ffmpeg.exe')])
    if path == '':
        pass
    elif path != '':
        ffmpeg = '"' + str(pathlib.Path(path)) + '"'
        config.set('ffmpeg_path', 'path', ffmpeg)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    print(path)

options_menu.add_command(label='Set "ffmpeg.exe" path', command=set_ffmpeg_path)

def set_hdr10plus_parser_path():
    global hdr10plus_parser
    path = filedialog.askopenfilename(title='Select Location to "hdr10plus_parser.exe"', initialdir='/',
                                      filetypes=[('hdr10plus_parser', 'hdr10plus_parser.exe')])
    if path == '':
        pass
    elif path != '':
        hdr10plus_parser = '"' + str(pathlib.Path(path)) + '"'
        config.set('parser_path', 'path', hdr10plus_parser)
        with open(config_file, 'w') as configfile:
            config.write(configfile)

options_menu.add_command(label='Set "hdr10plus_parser.exe" path', command=set_hdr10plus_parser_path)

def reset_config():
    msg = messagebox.askyesno(title='Warning', message='Are you sure you want to reset the config.ini file settings?')
    if msg == False:
       pass
    if msg == True:
        try:
            config.set('ffmpeg_path', 'path', '')
            config.set('parser_path', 'path', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo(title='Prompt', message='Please restart the program')
        except:
            pass
        root.destroy()

options_menu.add_command(label='Reset Configuration File', command=reset_config)

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

# Options Frame -------------------------------------------------------------------------------------------
options_frame = LabelFrame(root, text=' Options ')
options_frame.grid(row=1, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
options_frame.configure(fg="white", bg="#434547", bd=3)

options_frame.rowconfigure(1, weight=1)
options_frame.columnconfigure(0, weight=1)
options_frame.columnconfigure(1, weight=1)

# -------------------------------------------------------------------------------------------- Options Frame

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
                                            filetypes=(("MKV, MP4, HEVC, TS", "*.mkv *.mp4 *.hevc *.ts"),
                                                       ("All Files", "*.*")))
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    file_extension = pathlib.Path(VideoInput).suffix
    supported_extensions = ['.mkv', '.mp4', '.ts', '.hevc']
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
single_profile_checkbox = Checkbutton(options_frame, text='Force Single Profile',
                                          variable=single_profile, onvalue='--force-single-profile ', offvalue='')
single_profile_checkbox.grid(row=0, column=0, columnspan=1, rowspan=1, padx=10, pady=(0, 0), sticky=N + S + W)
single_profile_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                      activeforeground="white", selectcolor="#434547",
                                      font=("Helvetica", 11))
single_profile.set('--force-single-profile ')

# ------------------------------------------------------------------------------------------------------ Single Profile

# Command -------------------------------------------------------------------------------------------------------------
# Start Job -----------------------------------------------------------------------------------------------------------
def start_job():
    VideoOutputQuoted = '"' + VideoOutput + '"'

    if shell_options.get() == "Default":
        global total_duration
        mediainfocli_cmd = '"' + mediainfocli + " " + '--Inform="General;%FileSize%"' \
                       + " " + VideoInputQuoted + '"'

        try:
            mediainfo_duration = subprocess.Popen('cmd /c ' + mediainfocli_cmd, creationflags=subprocess.CREATE_NO_WINDOW,
                                                  universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                  stdin=subprocess.PIPE)
            stdout, stderr = mediainfo_duration.communicate()
            math = int(stdout) / 1000
            split = str(math)
            total_duration = split.rsplit('.', 1)[0]
        except:
            pass

        def close_encode():
            confirm_exit = messagebox.askyesno(title='Prompt',
                                               message="Are you sure you want to stop the parser?", parent=window)
            if confirm_exit == False:
                pass
            elif confirm_exit == True:
                try:
                    subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)
                    window.destroy()
                except:
                    window.destroy()

        def close_window():
            threading.Thread(target=close_encode).start()

        window = tk.Toplevel(root)
        window.title(str(pathlib.Path(VideoInput).stem))
        window.configure(background="#434547")
        encode_label = Label(window, text= '- ' * 20 + 'Progress' + ' -' * 20,
                             font=("Times New Roman", 14), background='#434547', foreground="white")
        encode_label.grid(column=0, row=0)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.protocol('WM_DELETE_WINDOW', close_window)
        window.geometry("600x140")
        encode_window_progress = Text(window, height=2, relief=SUNKEN, bd=3)
        encode_window_progress.grid(row=1, column=0, pady=(10, 6), padx=10, sticky=E + W)
        encode_window_progress.insert(END, '')
        app_progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, mode='determinate')
        app_progress_bar.grid(row=2, pady=(10, 10), padx=15, sticky=E + W)

    if shell_options.get() == "Default":
        finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                       + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb \
                       -f hevc - -hide_banner -loglevel warning -stats|' \
                       + hdr10plus_parser + ' ' + single_profile.get() + '-o ' + VideoOutputQuoted + ' -' + '"'
    elif shell_options.get() == "Debug":
        finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                       + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb -f hevc - |' \
                       + hdr10plus_parser + ' ' + single_profile.get() + '-o ' + VideoOutputQuoted + ' -' + '"'
    if shell_options.get() == "Default":
        job = subprocess.Popen('cmd /c ' + finalcommand, universal_newlines=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        for line in job.stdout:
            try:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, 'Starting Job...')
                if line.split('=', 1)[0] == 'frame':
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    size = line.split('size=', 1)[1].split()[0].rsplit('k', 1)[0]
                    percent = '{:.1%}'.format(int(size) / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = percent
            except:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
        window.destroy()
    elif shell_options.get() == "Debug":
        subprocess.Popen('cmd /k ' + finalcommand)
# --------------------------------------------------------------------------------------------------------------- Start
# ------------------------------------------------------------------------------------------------------------- Command


# Buttons -------------------------------------------------------------------------------------------------------------
# Input Button --------------------------------------
def input_button_hover(e):
    input_button["bg"] = "grey"

def input_button_hover_leave(e):
    input_button["bg"] = "#23272A"

# Drag and Drop Function for Input Button
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


# Output Button --------------------------------------
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

# Start Button ------------------------------------------
def start_button_hover(e):
    start_button["bg"] = "grey"

def start_button_hover_leave(e):
    start_button["bg"] = "#23272A"

start_button = Button(root, text="Start Job", command=lambda:threading.Thread(target=start_job).start(),
                      state=DISABLED, foreground="white", background="#23272A", borderwidth="3", width=15)
start_button.grid(row=3, column=3, columnspan=1, padx=20, pady=5, sticky=E+N+S)
start_button.bind("<Enter>", start_button_hover)
start_button.bind("<Leave>", start_button_hover_leave)

# ------------------------------------------------------------------------------------------------------------- Buttons

# Checks config for bundled app paths path ---------------
if config['ffmpeg_path']['path'] == '':
    check_ffmpeg()
if config['parser_path']['path'] == '':
    check_hdr10plus_parser()
# Checks config for bundled app paths path ---------------
# End Loop ------------------------------------------------------------------------------------------------------------
root.mainloop()
