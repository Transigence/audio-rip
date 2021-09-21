# audio-rip

## Introduction
_Audio-rip_ is a script in a set of media utilities centered around automating jobs that involve invocations of _ffmpeg_. The purpose of _audio-rip_ is to extract the audio tracks from all of the video container files in a specially-declared working folder, without transcoding them, and naming them with an appropriate extension. Each file will be probed to determine which file extension to use. Behavior on files that contain more than one audio track is undefined.

## Usage
```
usage: audio-rip.py [-h] [-to TO [TO ...]] [-f F [F ...]]

Extract audio tracks from all video files in a certain folder.

optional arguments:
  -h, --help       show this help message and exit
  -to TO [TO ...]  Transcode
  -f F [F ...]     Folderize
```

Example: `audio-rip`
This will search the internally-defined working folder for all files of a set of types (common video formats), probe them for audio tracks and deterime the audio codec, and extract them to files of the same base name but with the appropriate file extension for the codec found within.

Example: `audio-rip -f "converted"`
This will do the same as the former example, but the output files will be placed in a subfolder called "converted".

Example: `audio-rip -to opus`
This will probe the files to determine whether they contain an audio track, but it will ignore the codec, and transcode the file to the specified codec, naming the output files appropriately.

## Notes and limitations
* The working folder is determined internally, and is particular to my own workflow. You will either have to alter this or mimic my file system.
* There is not yet any way to pass any additional arguments to _ffmpeg._ Defaults will be used.

## Installation
1. Make a directory to contain binaries and scripts if you do not already have one (e.g. `c:\bin`). Let this be called the _bin_ directory.
2. Make sure the _bin_ directory is in the _search path._
3. Build or download _ffmpeg_ and _ffprobe_, and place the binaries in the _bin_ directory.
4. Configure your system to regard `.py` files as executables.
