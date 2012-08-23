#!/usr/bin/python

# generate_sine.py: Generates a sine wave with the given frequency
 
import sys
import math
from audiofile import *

if len(sys.argv) < 3:
    print "Usage: generate_sine.py out_file frequency"
    sys.exit(1)

out_filename = sys.argv[1]
frequency    = float(sys.argv[2])

seconds = 1
amplitude = 10000

channels = 1
sample_width = 2
frame_rate = 44100
fout = AudioFile(out_filename,'w')

num_samples = frame_rate * seconds
frames_per_cycle = frame_rate / frequency

def generate_sample(frame_num, frames_per_cycle, amplitude):
    radians = ((frame_num % frames_per_cycle) * 2 * math.pi) / frames_per_cycle
    sample = int(math.sin(radians) * amplitude)
    return sample

for i in range(0,num_samples):
    sample = generate_sample(i, frames_per_cycle, amplitude)
    fout.write(sample)

fout.close()  
