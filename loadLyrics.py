import subprocess
def get_lyrics(spotify_id):
    subprocess.Popen("syrics "+spotify_id, shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).wait()

def download_lyrics(track_name):
    import spotifyClient
    s = spotifyClient.get_spotify_url(track_name)
    if (s == ""):
        return False
    
    get_lyrics(s)
    return True

def load_lyrics_to_dict(d):
    f = open("./.lyrics/lyrics.lrc", "r")
    i = 0
    while i < 4:
        current = f.readline()
        i += 1

    while 1:
        current = f.readline()

        if (current == ""):
            break

        s = current.find("[")    
        e = current.find("]")

        if (s == -1 or e == -1):
            return 

        minutes = int(current[s+1:e].split(":")[0])
        seconds = int(float(current[s+1:e].split(":")[1]))
        if (current[e+2:-1] != "♪"): 
            d[(60*minutes)+seconds] = current[e+2:-1]
