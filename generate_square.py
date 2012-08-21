#!/usr/bin/python

# generate_square.py: Generates a square wave with the given frequency
 
import wave
import struct
import sys
import math

if len(sys.argv) < 3:
    print "Usage: generate_square.py out_file frequency"
    sys.exit(1)

out_filename = sys.argv[1]
frequency    = float(sys.argv[2])

seconds = 1
amplitude = 10000

channels = 1
sample_width = 2
frame_rate = 44100
fout = wave.open(out_filename,'w')
fout.setparams((channels,
                sample_width,
                frame_rate,
                0,
                'NONE',
                'not compressed'))

num_samples = frame_rate * seconds
frames_per_cycle = frame_rate / frequency

def check_clip(sample):
    if sample > 32767:
        sample = 32767
    if sample < -32768:
        sample = -32768
    return sample

def generate_harmonic(angle, multiplier, amplitude):
    return int(math.sin(angle * multiplier) * (amplitude))
 
def generate_sample(frame_num, frames_per_cycle, amplitude):
    radians = ((frame_num % frames_per_cycle) * 2 * math.pi) / frames_per_cycle
    sample = int(math.sin(radians) * amplitude)
    for i in range(3,30,2):
        sample += generate_harmonic(radians, i, amplitude / i)
    sample = check_clip(sample)
    return sample

for i in range(0,num_samples):
    sample = generate_sample(i, frames_per_cycle, amplitude)
    packed_out_data = struct.pack('h', sample)
    fout.writeframes(packed_out_data)

fout.close()  
