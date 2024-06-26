[![04a_source__41230.png](https://thumbs2.imgbox.com/56/73/kifkH1E0_t.png)](https://imgbox.com/kifkH1E0)

[![04a_source__41230.png](https://thumbs2.imgbox.com/0a/1a/Um5w9hAh_t.png)](https://imgbox.com/Um5w9hAh)

[![04a_source__41230.png](https://thumbs2.imgbox.com/67/96/kIIaDLoF_t.png)](https://imgbox.com/kIIaDLoF)

A modern GUI to parse HDR10+ and Dolby Vision dynamic metadata for use with video encoding.

Supports **MKV, TS, MP4, and HEVC** as inputs right now. Please open an issue if there is any inputs that are not accepted that should be.

Supports drag and drop in the input area **(Windows only)**.

If you open a file that has both HDR10+ and Dolby Vision you will see dual option panels. Choose which you would
like to extract and configure the settings. Everything else is handled for you.

### Configuration

Tools Menu options `Auto Start Queue` and `Clean Up`

`Auto Start Queue`: This will automatically start the queue as soon as a job is added to it.

`Clean Up`: This will clean up files left behind for Dolby Vision processing.

### Dolby Vision Cropping

Now facilitates precise adjustment of Dolby Vision metadata offsets with cropping functionality. After initiating a Dolby Vision input, you can conveniently provide cropped values.

`Fix Negative Offsets`: Enable this option to automatically reset offsets to zero if they would otherwise become negative due to user-defined crops. This feature mirrors the behavior of the `-c` switch in `dolby_tool`, ensuring consistent functionality for specific scenes while maintaining dynamic adjustment for others.

If this is unchecked and there is negative offsets detected, the job will error out and the error message will be
displayed in the log file as well as a prompt letting the user know something went wrong.

### Supported Operating Systems

Supports Windows and Linux.

_Technically this will work on MacOS, I don't have a MacBook so cannot build and release, if someone is interested reach out_

### Requirements

[`dovi_tool`](https://github.com/quietvoid/dovi_tool): _minimum version is v2.1.0_

[`hdr10plus_tool`](https://github.com/quietvoid/hdr10plus_tool)

`ffmpeg`: A somewhat modern version

**Note:** The program checks for these files on the system PATH first, so it will prioritize
them over them being in a folder in the `apps` directory beside the executable.

### Note

As of **v2.0** the tkinter version of the app has been dropped. I have no plans to update/maintain that version of the app. However, I will leave it on the repository in the branch `old_tkinter` inside of the `tkinter` folder.
