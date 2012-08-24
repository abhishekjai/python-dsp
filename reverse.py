#!/usr/bin/python

# reverse.py: Reverse input WAV file and save as given output file
 
import sys
from audiofile import *

if len(sys.argv) < 3:
    print "Usage: reverse.py in_file out_file"
    sys.exit(1)

in_filename  = sys.argv[1]
out_filename = sys.argv[2]

fin = AudioFile(in_filename,'r')
fout = AudioFile(out_filename,'w')
fout.setparams(fin.getnchannels(), 
               fin.getsampwidth(), 
               fin.getframerate(), 
               0,
               'NONE',
               'not compressed')

num_frames = fin.getnframes()
num_channels = fin.getnchannels()

data = []
while (fin.tell() < num_frames):
    frame = fin.read(1)
    data.append(frame)

data.reverse()

for frame in data:
    for sample in frame:
        fout.write(sample)

fout.close()  
fin.close()
