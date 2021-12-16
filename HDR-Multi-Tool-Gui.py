# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar, messagebox, ttk
import tkinter as tk
import pathlib, subprocess, shutil, threading, webbrowser
from TkinterDnD2 import *
from Packages.about import openaboutwindow
from configparser import ConfigParser


# Main Gui & Windows --------------------------------------------------------
def root_exit_function():  # Asks if user wants to close main GUI + close all tasks
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                               "     Note: This will end all current tasks!",
                                       parent=root)
    if confirm_exit:
        try:
            subprocess.Popen(f"TASKKILL /F /im hdr10plus_tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.Popen(f"TASKKILL /F /im dovi_tool.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            root.destroy()
        except (Exception,):
            root.destroy()


root = TkinterDnD.Tk()  # Main GUI with TkinterDnD function (for drag and drop)
root.title("HDR-Multi-Tool-Gui v1.3")
root.iconphoto(True, PhotoImage(file="Runtime/Images/hdrgui.png"))
root.configure(background="#434547")
window_height = 400
window_width = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
root.protocol('WM_DELETE_WINDOW', root_exit_function)

for n in range(2):
    root.grid_columnconfigure(n, weight=1)
for n in range(5):
    root.grid_rowconfigure(n, weight=1)

# Bundled Apps --------------------------------------------------------------------------------------------------------
config_file = 'Runtime/config.ini'  # Creates (if it doesn't exist) and defines location of config.ini
config = ConfigParser()
config.read(config_file)

if not config.has_section('ffmpeg_path'):
    config.add_section('ffmpeg_path')
if not config.has_option('ffmpeg_path', 'path'):
    config.set('ffmpeg_path', 'path', '')

if not config.has_section('hdr10plus_parser_path'):
    config.add_section('hdr10plus_parser_path')
if not config.has_option('hdr10plus_parser_path', 'path'):
    config.set('hdr10plus_parser_path', 'path', '')

if not config.has_section('dolbyvision_tool_path'):
    config.add_section('dolbyvision_tool_path')
if not config.has_option('dolbyvision_tool_path', 'path'):
    config.set('dolbyvision_tool_path', 'path', '')

if not config.has_section('mediainfocli_path'):
    config.add_section('mediainfocli_path')
if not config.has_option('mediainfocli_path', 'path'):
    config.set('mediainfocli_path', 'path', '')

if not config.has_section('debug_option'):
    config.add_section('debug_option')
if not config.has_option('debug_option', 'option'):
    config.set('debug_option', 'option', '')

try:
    with open(config_file, 'w') as configfile:
        config.write(configfile)
except (Exception,):
    messagebox.showinfo(title='Error', message='Could Not Write to config.ini file, delete and try again')

# Menu Items and Sub-Bars ---------------------------------------------------------------------------------------------
my_menu_bar = Menu(root, tearoff=0)
root.config(menu=my_menu_bar)

file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Exit', command=root_exit_function)

options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='Options', menu=options_menu)

options_submenu = Menu(root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Shell Options', menu=options_submenu)
shell_options = StringVar()
shell_options.set(config['debug_option']['option'])
if shell_options.get() == '':
    shell_options.set('Default')
elif shell_options.get() != '':
    shell_options.set(config['debug_option']['option'])


def update_shell_option():
    try:
        config.set('debug_option', 'option', shell_options.get())
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    except (Exception,):
        pass


update_shell_option()
options_submenu.add_radiobutton(label='Progress Bars', variable=shell_options,
                                value="Default", command=update_shell_option)
options_submenu.add_radiobutton(label='CMD Shell (Debug)', variable=shell_options,
                                value="Debug", command=update_shell_option)


def set_ffmpeg_path():
    global ffmpeg
    path = filedialog.askopenfilename(title='Select Location to "ffmpeg.exe"', initialdir='/',
                                      filetypes=[('ffmpeg', 'ffmpeg.exe')])
    if path != '':
        ffmpeg = '"' + str(pathlib.Path(path)) + '"'
        config.set('ffmpeg_path', 'path', ffmpeg)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set "ffmpeg.exe" path', command=set_ffmpeg_path)


def set_hdr10plus_tool_path():
    global hdr10plus_tool
    path = filedialog.askopenfilename(title='Select Location to "hdr10plus_tool.exe"', initialdir='/',
                                      filetypes=[('hdr10plus_tool', 'hdr10plus_tool.exe')])
    if path != '':
        hdr10plus_tool = '"' + str(pathlib.Path(path)) + '"'
        config.set('hdr10plus_parser_path', 'path', hdr10plus_tool)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set "hdr10plus_tool.exe" path', command=set_hdr10plus_tool_path)


def set_dolbyvision_tool_path():
    global dolbyvision_tool
    path = filedialog.askopenfilename(title='Select Location to "dovi_tool.exe"', initialdir='/',
                                      filetypes=[('dovi_tool', 'dovi_tool.exe')])
    if path != '':
        dolbyvision_tool = '"' + str(pathlib.Path(path)) + '"'
        config.set('dolbyvision_tool_path', 'path', dolbyvision_tool)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set "dovi_tool.exe" path', command=set_dolbyvision_tool_path)


def set_mediainfocli_path():
    global mediainfocli
    path = filedialog.askopenfilename(title='Select Location to "MediaInfo.exe"', initialdir='/',
                                      filetypes=[('MediaInfo', 'MediaInfo.exe')])
    if path == '':
        pass
    elif path != '':
        mediainfocli = '"' + str(pathlib.Path(path)) + '"'
        config.set('mediainfocli_path', 'path', mediainfocli)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set "MediaInfo.exe" path', command=set_mediainfocli_path)

options_menu.add_separator()


def reset_config():
    msg = messagebox.askyesno(title='Warning', message='Are you sure you want to reset the config.ini file settings?')
    if msg:
        try:
            config.set('ffmpeg_path', 'path', '')
            config.set('hdr10plus_parser_path', 'path', '')
            config.set('mediainfocli_path', 'path', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo(title='Prompt', message='Please restart the program')
        except (Exception,):
            pass
        root.destroy()


options_menu.add_command(label='Reset Configuration File', command=reset_config)

help_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow)

# --------------------------------------------------------------------------------------------- Menu Items and Sub-Bars
# Bundled app path(s) -------------------------------------------------------------------------------------------------
ffmpeg = config['ffmpeg_path']['path']
hdr10plus_tool = config['hdr10plus_parser_path']['path']
mediainfocli = config['mediainfocli_path']['path']
dolbyvision_tool = config['dolbyvision_tool_path']['path']

if not pathlib.Path(ffmpeg.replace('"', '')).is_file():  # Checks config for bundled app paths path -------------------
    # FFMPEG -------------------------------------------------------------------------
    def write_path_to_ffmpeg():  # Writes path to ffmpeg to the config.ini file
        try:
            config.set('ffmpeg_path', 'path', ffmpeg)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    if shutil.which('ffmpeg') is not None:
        ffmpeg = str(pathlib.Path(shutil.which('ffmpeg'))).lower()
        messagebox.showinfo(title='Prompt!', message='ffmpeg.exe found on system PATH, '
                                                     'automatically setting path to location.\n\n'
                                                     'Note: This can be changed in the config.ini file'
                                                     ' or in the Options menu')
        if pathlib.Path("Apps/ffmpeg/ffmpeg.exe").is_file():
            rem_ffmpeg = messagebox.askyesno(title='Delete Included ffmpeg?',
                                             message='Would you like to delete the included FFMPEG?')
            if rem_ffmpeg:
                try:
                    shutil.rmtree(str(pathlib.Path("Apps/ffmpeg")))
                except (Exception,):
                    pass
        write_path_to_ffmpeg()
    elif pathlib.Path("Apps/ffmpeg/ffmpeg.exe").is_file():
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"ffmpeg.exe" located in the "Apps" folder')
        ffmpeg = str(pathlib.Path("Apps/ffmpeg/ffmpeg.exe"))
        write_path_to_ffmpeg()
    else:
        error_prompt = messagebox.askyesno(title='Error!',
                                           message='Cannot find ffmpeg, '
                                                   'please navigate to "ffmpeg.exe"')
        if not error_prompt:
            messagebox.showerror(title='Error!',
                                 message='Program requires ffmpeg.exe to work correctly')
            root.destroy()
        if error_prompt:
            set_ffmpeg_path()
            if not pathlib.Path(ffmpeg).is_file():
                messagebox.showerror(title='Error!',
                                     message='Program requires ffmpeg.exe to work correctly')
                root.destroy()

    # FFMPEG ------------------------------------------------------------------------------


if not pathlib.Path(hdr10plus_tool.replace('"', '')).is_file():  # Checks config for bundled app paths path
    # HDR10plus_tool -----------------------------------------------------------------------
    if pathlib.Path('Apps/HDR10PlusTool/hdr10plus_tool.exe').is_file():
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"hdr10plus_tool.exe" located in the "Apps" folder')
        hdr10plus_tool = '"' + str(pathlib.Path('Apps/HDR10PlusTool/hdr10plus_tool.exe')) + '"'
        try:
            config.set('hdr10plus_parser_path', 'path', hdr10plus_tool)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass
    elif not pathlib.Path("Apps/HDR10PlusTool/hdr10plus_tool.exe").is_file():
        messagebox.showerror(title='Error!', message='Please download hdr10plus_tool.exe and set path to '
                                                     'hdr10plustool.exe in the Options menu')
        webbrowser.open('https://github.com/quietvoid/hdr10plus_tool/releases')
    # hdr10plus_tool -------------------------------------------------------


if not pathlib.Path(mediainfocli.replace('"', '')).is_file():  # Checks config for bundled app paths path
    # mediainfocli -------------------------------------------------------------
    if pathlib.Path('Apps/MediaInfoCLI/MediaInfo.exe').is_file():
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"MediaInfo.exe" located in the "Apps" folder')
        mediainfocli = '"' + str(pathlib.Path('Apps/MediaInfoCLI/MediaInfo.exe')) + '"'
        try:
            config.set('mediainfocli_path', 'path', mediainfocli)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass
    elif not pathlib.Path('Apps/MediaInfoCLI/MediaInfo.exe').is_file():
        messagebox.showerror(title='Error!', message='Please download mediainfo.exe and set path to '
                                                     'mediainfo.exe in the Options menu')
        webbrowser.open('https://mediaarea.net/download/binary/mediainfo/21.09/MediaInfo_CLI_21.09_Windows_x64.zip')
    # mediainfocli ----------------------------------------------------------


# dolbyvision_tool --------------------------------------------------------
if not pathlib.Path(dolbyvision_tool.replace('"', '')).is_file():
    if pathlib.Path('Apps/dovi_tool/dovi_tool.exe').is_file():
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"dovi_tool.exe" located in the "Apps" folder')
        dolbyvision_tool = '"' + str(pathlib.Path('Apps/dovi_tool/dovi_tool.exe')) + '"'
        try:
            config.set('dolbyvision_tool_path', 'path', dolbyvision_tool)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass
    elif not pathlib.Path("Apps/dovi_tool/dovi_tool.exe").is_file():
        messagebox.showerror(title='Error!', message='Please download dovi_tool.exe and set path to '
                                                     'dovi_tool.exe in the Options menu')
        webbrowser.open('https://github.com/quietvoid/dovi_tool/releases')
    # dolbyvision_tool --------------------------------------------------------
# -------------------------------------------------------------------------------------------------------- Bundled Apps

# Frames --------------------------------------------------------------------------------------------------------------
# Input Frame -------------------------------------------------------------------------------------------
input_frame = LabelFrame(root, text=' Input ')
input_frame.grid(row=0, column=0, columnspan=5, sticky=E + W, padx=20, pady=(0, 0))
input_frame.configure(fg="white", bg="#434547", bd=3)

input_frame.rowconfigure(0, weight=1)
for n in range(6):
    input_frame.grid_columnconfigure(n, weight=1)

# -------------------------------------------------------------------------------------------- Input Frame

# Info Frame ---------------------------------------------------------------------------------------------
info_frame = LabelFrame(root, text=' Info ')
info_frame.grid(row=1, columnspan=4, sticky=E + W, padx=20, pady=(4, 10))
info_frame.configure(fg="white", bg="#434547", bd=3)
info_frame.columnconfigure(0, weight=1)
link_input_label = Label(info_frame, text='Please Open a Dolby Vision or HDR10+ compatible file', background="#434547",
                         foreground="white", height=1, font=("Helvetica", 10))
link_input_label.grid(row=1, column=0, columnspan=5, padx=10, pady=5, sticky=W + E + N)

# --------------------------------------------------------------------------------------------- Info Frame

# Output Frame -------------------------------------------------------------------------------------------
output_frame = LabelFrame(root, text=' Output ')
output_frame.grid(row=3, column=0, columnspan=5, sticky=E + W, padx=20, pady=(0, 0))
output_frame.configure(fg="white", bg="#434547", bd=3)

output_frame.rowconfigure(0, weight=1)
for n in range(3):
    output_frame.grid_columnconfigure(n, weight=1)

# -------------------------------------------------------------------------------------------- Output Frame
# -------------------------------------------------------------------------------------------------------------- Frames

# Tabs ----------------------------------------------------------------------------------------------------------------
hdr_tool_tabs = ttk.Notebook(root)
hdr_tool_tabs.grid(row=2, column=0, columnspan=4, sticky=E + W + N + S, padx=10, pady=(0, 0))
hdr_frame = Frame(hdr_tool_tabs, background="#434547")
dolby_frame = Frame(hdr_tool_tabs, background="#434547")
hdr_tool_tabs.add(hdr_frame, text='  HDR10+ ')
hdr_tool_tabs.add(dolby_frame, text='  Dolby Vision  ')
for n in range(1):
    hdr_frame.grid_columnconfigure(n, weight=1)
for n in range(2):
    hdr_frame.grid_rowconfigure(n, weight=1)
for n in range(2):
    dolby_frame.grid_columnconfigure(n, weight=1)
for n in range(3):
    dolby_frame.grid_rowconfigure(n, weight=1)


# ---------------------------------------------------------------------------------------------------------------- Tabs

# HDR Parse Checkbutton -----------------------------------------------------------------------------------------------
def hdr10plus_parse():
    dolbyvision_parse.set('off')


hdr_parse = StringVar()
hdr_parse_checkbox = Checkbutton(hdr_frame, text='Parse HDR10+ Metadata', variable=hdr_parse,
                                 onvalue='on', offvalue='off', command=hdr10plus_parse, takefocus=False)
hdr_parse_checkbox.grid(row=0, column=0, columnspan=1, rowspan=1, padx=10, pady=6, sticky=N + W)
hdr_parse_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                             activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
hdr_parse.set('off')


# ----------------------------------------------------------------------------------------------- HDR Parse Checkbutton

# Dolby Vision Checkbutton --------------------------------------------------------------------------------------------
def dolby_parse():
    hdr_parse.set('off')


dolbyvision_parse = StringVar()
dolbyvision_parse_checkbox = Checkbutton(dolby_frame, text='Parse Dolby Vision RPU', variable=dolbyvision_parse,
                                         onvalue='on', offvalue='off', command=dolby_parse, takefocus=False)
dolbyvision_parse_checkbox.grid(row=0, column=0, columnspan=1, rowspan=1, padx=10, pady=6, sticky=N + W)
dolbyvision_parse_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                     activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
dolbyvision_parse.set('off')


# -------------------------------------------------------------------------------------------- Dolby Vision Checkbutton

# Dolby Vision Crop Checkbutton ---------------------------------------------------------------------------------------
dolbyvision_crop = StringVar()
dolbyvision_crop_checkbox = Checkbutton(dolby_frame, text='Check if cropping encode', variable=dolbyvision_crop,
                                        onvalue=' -c', offvalue='', takefocus=False)
dolbyvision_crop_checkbox.grid(row=0, column=1, columnspan=2, rowspan=1, padx=10, pady=6, sticky=N + E)
dolbyvision_crop_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                    activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
dolbyvision_crop.set('')


# --------------------------------------------------------------------------------------- Dolby Vision Crop Checkbutton

# Dolby Vision Mode Menu ----------------------------------------------------------------------------------------------
def dobly_vision_mode_menu_hover(e):
    dobly_vision_mode_menu["bg"] = "grey"
    dobly_vision_mode_menu["activebackground"] = "grey"


def dobly_vision_mode_menu_hover_leave(e):
    dobly_vision_mode_menu["bg"] = "#23272A"


dobly_vision_mode = StringVar()
dobly_vision_mode_choices = {'RPU untouched': '-m 0',
                             'MEL: Converts RPU to be MEL compatible': '-m 1',
                             '8.1: Converts the RPU to be profile 8.1 compatible': '-m 2',
                             '5 to 8: Converts profile 5 to 8': '-m 3'}
dobly_vision_mode_menu_label = Label(dolby_frame, text="Parsing Mode :", background="#434547", foreground="white")
dobly_vision_mode_menu_label.grid(row=1, column=0, columnspan=1, padx=10, pady=0, sticky=W + S)
dobly_vision_mode_menu = OptionMenu(dolby_frame, dobly_vision_mode, *dobly_vision_mode_choices.keys())
dobly_vision_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15, anchor=W)
dobly_vision_mode_menu.grid(row=2, column=0, columnspan=1, padx=10, pady=(5, 5), sticky=W + N)
dobly_vision_mode.set('8.1: Converts the RPU to be profile 8.1 compatible')
dobly_vision_mode_menu["menu"].configure(activebackground="dim grey")
dobly_vision_mode_menu.bind("<Enter>", dobly_vision_mode_menu_hover)
dobly_vision_mode_menu.bind("<Leave>", dobly_vision_mode_menu_hover_leave)


# ---------------------------------------------------------------------------------------------- Dolby Vision Mode Menu

# Input Button Functions ----------------------------------------------------------------------------------------------
def check_for_hdr():
    hdr_format_mediainfocli = '"' + mediainfocli + " " + '"--Inform=Video;%HDR_Format/String%"' \
                              + " " + VideoInputQuoted + '"'
    try:
        mediainfo_duration = subprocess.Popen('cmd /c ' + hdr_format_mediainfocli,
                                              creationflags=subprocess.CREATE_NO_WINDOW,
                                              universal_newlines=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = mediainfo_duration.communicate()
        if 'HDR10+' in stdout:
            link_input_label.config(text=stdout.rstrip("\n"), anchor='center')
            hdr_tool_tabs.select(hdr_frame)
            hdr_parse.set('on')
            dolbyvision_parse.set('off')
        elif 'Dolby Vision' in stdout:
            link_input_label.config(text=stdout.rstrip("\n"), anchor=W)
            hdr_tool_tabs.select(dolby_frame)
            hdr_parse.set('off')
            dolbyvision_parse.set('on')
        else:
            link_input_label.config(text='No Parsing Needed', anchor='center')
            messagebox.showinfo(title="No Processing Needed", message="No need to parse anything other then an HDR10+"
                                                                      "or Dolby Vision file.\n\n If you see this in "
                                                                      "error please let me know on the github tracker "
                                                                      "with a sample of the source file.")
    except (Exception,):
        pass

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
            VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
            filename = pathlib.Path(VideoInput)
            VideoOut = filename.with_suffix('')
            autosavefilename = VideoOut.name
            VideoOutput = str(pathlib.Path(r'' + str(VideoOut)))
            input_entry.configure(state=NORMAL)
            input_entry.insert(0, VideoInput)
            input_entry.configure(state=DISABLED)
            output_entry.configure(state=NORMAL)
            output_entry.delete(0, END)
            output_entry.configure(state=DISABLED)
            output_entry.configure(state=NORMAL)
            output_entry.insert(0, str(VideoOut))
            output_entry.configure(state=DISABLED)
            output_button.configure(state=NORMAL)
            start_button.configure(state=NORMAL)
            check_for_hdr()
        else:
            link_input_label.config(text='Please Open a Dolby Vision or HDR10+ compatible file', anchor='center')
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
        autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + str(pathlib.Path(VideoInput)) + '"'
        input_entry.insert(0, str(input_dnd.get()).replace("{", "").replace("}", ""))
        filename = pathlib.Path(VideoInput)
        VideoOut = filename.with_suffix('')
        autosavefilename = VideoOut.name
        VideoOutput = str(pathlib.Path(r'' + str(VideoOut)))
        input_entry.configure(state=DISABLED)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        output_entry.configure(state=NORMAL)
        output_entry.insert(0, str(VideoOut))
        output_entry.configure(state=DISABLED)
        output_button.configure(state=NORMAL)
        start_button.configure(state=NORMAL)
        check_for_hdr()
    else:
        link_input_label.config(text='Please Open a Dolby Vision or HDR10+ compatible file', anchor='center')
        messagebox.showinfo(title="Wrong File Type", message="Try Again With a Supported File Type!\n\nIf this is a "
                                                             "file that should be supported, please let me know.")


# --------------------------------------------------------------------------------------------- Drag and Drop Functions

# File Output ---------------------------------------------------------------------------------------------------------
def file_save():
    global VideoOutput
    VideoOutput = filedialog.asksaveasfilename(defaultextension="", initialdir=autofilesave_dir_path,
                                               title="Select a Save Location", initialfile=autosavefilename)
    if VideoOutput:
        output_entry.configure(state=NORMAL)  # Enable entry box for commands under
        output_entry.delete(0, END)  # Remove current text in entry
        output_entry.insert(0, VideoOutput)  # Insert the 'path'
        output_entry.configure(state=DISABLED)  # Disables Entry Box


# --------------------------------------------------------------------------------------------------------- File Output

# Command -------------------------------------------------------------------------------------------------------------
# Start Job -----------------------------------------------------------------------------------------------------------
def start_job():
    if hdr_parse.get() == 'on':
        VideoOutputQuoted = '"' + VideoOutput + '.json"'
    if dolbyvision_parse.get() == 'on':
        VideoOutputQuoted = '"' + VideoOutput + '.bin"'

    if shell_options.get() == "Default":
        global total_duration
        mediainfocli_cmd = '"' + mediainfocli + " " + '--Inform="General;%FileSize%"' \
                           + " " + VideoInputQuoted + '"'

        try:
            mediainfo_duration = subprocess.Popen('cmd /c ' + mediainfocli_cmd,
                                                  creationflags=subprocess.CREATE_NO_WINDOW,
                                                  universal_newlines=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  stdin=subprocess.PIPE)
            stdout, stderr = mediainfo_duration.communicate()
            math = int(stdout) / 1000
            split = str(math)
            total_duration = split.rsplit('.', 1)[0]
        except (Exception,):
            pass

        def close_encode():
            confirm_exit = messagebox.askyesno(title='Prompt',
                                               message="Are you sure you want to stop the parser?", parent=window)
            if confirm_exit:
                try:
                    subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)
                    window.destroy()
                except (Exception,):
                    window.destroy()

        def close_window():
            threading.Thread(target=close_encode).start()

        window = tk.Toplevel(root)
        window.title(str(pathlib.Path(VideoInput).stem))
        window.configure(background="#434547")
        encode_label = Label(window, text='- ' * 20 + 'Progress' + ' -' * 20,
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
    if hdr_parse.get() == 'on':
        if shell_options.get() == "Default":
            finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                           + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb \
                           -f hevc - -hide_banner -loglevel warning -stats|' \
                           + hdr10plus_tool + ' ' + 'extract -o ' + str(VideoOutputQuoted) + '. -' + '"'
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                           + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb -f hevc - |' \
                           + hdr10plus_tool + ' ' + 'extract -o ' + str(VideoOutputQuoted) + ' -' + '"'
    if dolbyvision_parse.get() == 'on':
        if shell_options.get() == "Default":
            finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                           + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb ' \
                             '-f hevc - -hide_banner -loglevel warning -stats|' \
                           + dolbyvision_tool + ' ' + dobly_vision_mode_choices[dobly_vision_mode.get()] \
                           + dolbyvision_crop.get() + ' extract-rpu - -o ' + str(VideoOutputQuoted) + '"'
            print(finalcommand)
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + ' -analyzeduration 100M -probesize 50M -i ' + VideoInputQuoted \
                           + ' -map 0:v:0 -c:v:0 copy -vbsf hevc_mp4toannexb -f hevc - |' \
                           + dolbyvision_tool + ' ' + dobly_vision_mode_choices[dobly_vision_mode.get()] \
                           + dolbyvision_crop.get() + ' extract-rpu - -o ' + str(VideoOutputQuoted) + '"'
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
            except (Exception,):
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
                         background="#23272A", borderwidth="3", width=9)
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=W)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', drop_input)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

input_entry = Entry(input_frame, borderwidth=4, background="#CACACA", width=55)
input_entry.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky=E + W)
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
output_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=E + W)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)


# Start Button ------------------------------------------
def start_button_hover(e):
    start_button["bg"] = "grey"


def start_button_hover_leave(e):
    start_button["bg"] = "#23272A"


start_button = Button(output_frame, text="Start Job", command=lambda: threading.Thread(target=start_job).start(),
                      state=DISABLED, foreground="white", background="#23272A", borderwidth="3", width=15)
start_button.grid(row=0, column=4, columnspan=1, padx=(5, 5), pady=(0, 4), sticky=E + S)
start_button.bind("<Enter>", start_button_hover)
start_button.bind("<Leave>", start_button_hover_leave)

# ------------------------------------------------------------------------------------------------------------- Buttons
# End Loop ------------------------------------------------------------------------------------------------------------
root.mainloop()
