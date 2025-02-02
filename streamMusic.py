import os
from pydub import AudioSegment
from pydub.playback import play
import time
import threading
import waves
import loadLyrics

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def load_audio(file, obj):
    obj[0] = AudioSegment.from_file(file, "mp3")

def display_data(m, d, start_time, total_time, song_title, artists):
    # this function will first display the waveforms and then the lyrics
    # to print the lyrics, check the closest lyric that has passed in terms of time elapsed
    # if this lyric == "" meaning no lyrics have passed, we mark the starting lyric as first one
    # if this lyric is not "", then we check the count of lyrics above it
    #       if count >= 4: we print the first 4, then this, then the remaining/remaining four
    #       if count < 4: we print till the current lyric, then 9-n

    os.system("clear")
    for matrix in m:
        i = 0
        count = 0
        time_elapsed = int(time.time() - start_time)
        n = 0
        for key in d.keys():
            if (key > time_elapsed):
                break 
            n += 1

        start_at = 0

        if (n == 0):
            start_at = 0
        elif (n == len(d)-1):
            start_at = n-13
        elif (n < 6):
            start_at = 0
        else:
            start_at = n-6

        for row in matrix:
            if (i < 3):
                i += 1
                continue
            elif (i == 20):
                print("           \u2500\u2500\u2591", end="")
            else:
                print("              ", end="")

            for val in row:
                if (i == 20):
                    print("\u2591", end="\u2591")
                elif (val == 1): 
                    print("\u2591", end=" ")
                else:
                    print(" ", end=" ")

            if (i == 20):
                print("\u2500\u2500", end=" ")
            
            if (i >= 14 and i <= 26):
                g = 0
                printed = 0
                for key in d.keys():
                    if (g >= start_at+count and count < 13):
                        if (i != 20):
                            print("   ", end="")
                        if (time_elapsed > key):
                            print(f"\033[36m                     {d[key]}\033[0m")
                        else:
                            print("                    ",d[key], sep=" ")
                        count += 1
                        printed = 1
                        break
                    g += 1

                if (printed == 0):
                    print()
            else:
                print()
            i += 1
        s = " " * len(song_title)
        print(f" \033[47m {s} \033[00m")
        print(f" \033[47m\033[31m {song_title} \033[00m {artists}")
        print(f" \033[47m {s} \033[00m\n")
        bar_length = 142
        minutes = int(time_elapsed // 60)
        seconds = int(time_elapsed % 60)
        minutes_total = int(total_time // 60)
        seconds_total = int(total_time % 60)
        formatted_elapsed_time =  f"{minutes:02}:{seconds:02}"
        formatted_total_time = f"{minutes_total:02}:{seconds_total:02}"
        progress = time_elapsed / total_time if total_time > 0 else 0
        filled_length = int(bar_length * progress)
        remaining_length = bar_length - filled_length
        filled_bar = "\033[32m█\033[0m" * filled_length
        remaining_bar = "\033[37m░\033[0m" * remaining_length
        print(f"{formatted_elapsed_time} [{filled_bar}{remaining_bar}] {formatted_total_time}")
        time.sleep(0.1)
        os.system("clear")

def play_and_rewrite(url, total_duration, title, artists):
    print("Loading...")
    v = loadLyrics.download_lyrics(title)

    if (not v):
        print("There was an error while trying to fetch lyrics from spotify.")
        exit(0)

    d = {}
    loadLyrics.load_lyrics_to_dict(d)
    os.system(f'yt-dlp -x --audio-format mp3 --postprocessor-args "-ss 0 -t 20.07" -q --no-warnings --force-overwrites -o "part1.mp3" "{url}"')
    thread1 = threading.Thread(target=os.system, args=(f'yt-dlp -x --audio-format mp3 -q --no-warnings --postprocessor-args "-ss 20 -t 40.07" --force-overwrites -o "part2.mp3" "{url}"',))
    thread1.start()
    waves_normalized_samples = []
    m = []
    waves.createNormalizedSamples(waves_normalized_samples, "part1.mp3")
    waves.fillMatricies(waves_normalized_samples, m)
    thread2 = StoppableThread(target=display_data, args=(m,d, time.time(), total_duration, title, artists))
    thread2.start()
    start = time.time()
    os.system("mpg321 -q part1.mp3")
    thread1.join()
    start_time = 60
    file_currently_playing = 2
    prev = 40

    while(start_time <= total_duration):
        output_file = f"part{file_currently_playing}.mp3"
        file_to_be_overwritten = 3-file_currently_playing
        writeFile = f"part{file_to_be_overwritten}.mp3"
        waves_normalized_samples = []
        m = []
        waves.createNormalizedSamples(waves_normalized_samples, output_file)
        waves.fillMatricies(waves_normalized_samples, m)
        thread1 = threading.Thread(target=os.system, args=(f'yt-dlp -x --audio-format mp3 -q --no-warnings --postprocessor-args "-ss {start_time} -t {prev+20}.07" --force-overwrites -o "{writeFile}" "{url}"',))
        thread1.start()
        thread2.stop()
        thread2 = StoppableThread(target=display_data, args=(m,d,int(start), total_duration, title, artists))
        thread2.start()
        os.system(f"mpg321 -q part{file_currently_playing}.mp3")
        thread1.join()
        start_time += prev + 20
        prev+=20
        file_currently_playing = file_to_be_overwritten
    thread2 = StoppableThread(target=display_data, args=(m,d,int(start), total_duration, title, artists))
    thread2.start()
    os.system(f"mpg321 -q part{file_currently_playing}.mp3")
