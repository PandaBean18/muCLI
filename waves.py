from pydub import AudioSegment
import numpy as np
import os
import time

def fillMatricies(normalized_samples, m):
    i = 0
    while (i < len(normalized_samples)):
        current = np.zeros((41, 20))        
        j = 0
        while (j <= 20):
            k = 0
            while (k < 20 and ((k+i) < len(normalized_samples))):
                if (normalized_samples[k+i] - j >= 0):
                    current[20-j][k] = 1
                    if (j != 0):
                        current[20+j][k] = 1
                k += 1
            j += 1

        i += 20
        m.append(current)
        
def printFromMatricies(m):
    os.system("clear")
    for matrix in m:
        i = 0
        for row in matrix:
            if (i == 20):
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
                print("\u2500\u2500")
            else:
                print()
            i += 1
        time.sleep(0.1)
        os.system("clear")

def createNormalizedSamples(normalized_samples, file_name):
    audio = AudioSegment.from_mp3(file_name)
    raw_data = audio.raw_data  # Returns bytes

    samples = np.frombuffer(raw_data, dtype=np.int16)

    frame_rate = audio.frame_rate

    duration = len(samples) / (frame_rate*2)
    bars_per_second = 200

    total_bars = int(duration * bars_per_second)

    chunk_size = len(samples) // total_bars
    downsampled_samples = [np.mean(np.abs(samples[i * chunk_size : (i + 1) * chunk_size])) for i in range(total_bars)]

    max_amplitude = max(downsampled_samples)
    console_height = 12
    s = [int((sample / max_amplitude) * console_height) for sample in downsampled_samples]

    for x in s:
        normalized_samples.append(x)


# display_chunks(normalized_samples)
# m = []
# fillMatricies(normalized_samples, m)
# printFromMatricies(m)
