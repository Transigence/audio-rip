import sys, argparse
import os, subprocess
import re

TEST = False

KNOWN_VIDEO_EXTENSIONS = {"mp4", "webm", "mov", "mpeg2", "ts"}
ENCODER_MAP = {"opus": "libopus", "aac": "aac", "mp3": "libmp3lame", "flac": "flac", "ogg": "libvorbis"}
WORK_DIR = "D:\\Videos\\Audio-Rip\\"
DEST_DIR = WORK_DIR
files = os.listdir(WORK_DIR)
vid_files: list
vid_info: list
r = re.compile("Audio: (\S+) ")
transcodec = None
folder = None

HELP_EPILOG = """
"""
def codec_extract(ext):
    return "copy", ext

def codec_transcode(ext):
    return ENCODER_MAP[transcodec], transcodec


def get_args():
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Extract audio tracks from all video files in a certain folder.",
        epilog=HELP_EPILOG
        )
    argparser.add_argument("-to", type=str, nargs="+", help="Transcode")
    argparser.add_argument("-f", type=str, nargs="+", help="Folderize")
    return argparser.parse_args()

if __name__ == "__main__":
    args=get_args()
    if args.f:
        DEST_DIR = os.path.join(WORK_DIR, args.f[0])
        print("Outputting to folder: \"" + DEST_DIR + "\"")

    for f in files:
        if os.path.splitext(f)[1][1:] in KNOWN_VIDEO_EXTENSIONS:
            vid_files.append(f)

    if args.to:
        print("Transcoding all files to \"" + args.to[0] + ".\"")
        transcodec = args.to[0]
        set_codec = codec_transcode
    else:
        set_codec = codec_extract

    for vid_file in vid_files:
        proc = subprocess.run(["ffprobe", os.path.join(WORK_DIR, vid_file)], capture_output = True)
        probe_result = proc.stderr.decode("UTF-8")
        print(probe_result)
        match = r.search(probe_result)
        if match:
            codec, ext = set_codec(match.group(1))
            vid_info.append((vid_file, codec, ext))
        else:
            print("Video file \"%s\" didn't contain an audio stream. Skipping..." % vid_file)
            continue
    #sys.exit(-1)

    if args.f:
        if os.path.exists(DEST_DIR):
            if os.path.isdir(DEST_DIR):
                print("Destination folder already exists.")
        else:
            if not TEST:
                os.mkdir(DEST_DIR)
            else:
                print("mkdir %s" % DEST_DIR)

    for info in vid_info:
        #print(info)
        basename = os.path.splitext(info[0])[0]
        newname = basename + ".%s" % info[2]
        codec = info[1]
        command = " ".join(["ffmpeg", "-i", "\"" + os.path.join(WORK_DIR, info[0]) + "\"", "-c:a " + codec +  " -vn ", "\"" + os.path.join(DEST_DIR, newname) + "\""])

        if not TEST:
            subprocess.run(command)
        else:
            print(command)
