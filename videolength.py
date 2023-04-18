import os
import wave
import contextlib

def get_length(filename):
    # get the length of an audio file in seconds
    with contextlib.closing(wave.open(filename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)

def get_video_length(filename):
    # get the length of a video file in seconds
    # by extracting the audio track and measuring its length
    # this assumes that the video has an audio track and it is in sync with the video
    # you may need to adjust the ffmpeg command depending on your system and video format
    audio_file = filename + ".wav"
    os.system("ffmpeg -i \"" + filename + "\" -vn -acodec pcm_s16le -ar 44100 -ac 2 \"" + audio_file + "\"")
    length = get_length(audio_file)
    os.remove(audio_file)
    return length

def get_total_length(dir):
    # get the total length of all video files in a directory and its subdirectories in seconds
    total = 0
    for root, dirs, files in os.walk(dir): # use os.walk to traverse the directory tree
        for file in files:
            if file.endswith(".mp4"): # or any other video format you want
                total += get_video_length(os.path.join(root, file)) # join the root and file names
    return total

def format_time(seconds):
    # format the time in seconds into hours, minutes and seconds
    hours, remainder = divmod(seconds, 3600) # divide by 3600 and get the quotient and remainder
    minutes, seconds = divmod(remainder, 60) # divide by 60 and get the quotient and remainder
    seconds = round(seconds) # round the seconds to the nearest integer
    hours = round(hours) # round the hours to the nearest integer
    minutes = round(minutes) # round the minutes to the nearest integer
    return f"{hours} hours {minutes} minutes {seconds} seconds" # return a formatted string

print(format_time(get_total_length("."))) # print the total length of all videos in the current directory and its subdirectories in hours, minutes and seconds format
