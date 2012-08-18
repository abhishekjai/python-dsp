#!/usr/bin/python

# reverse.py: Reverse input WAV file and save as given output file
 
import wave
import struct
import sys

if len(sys.argv) < 3:
    print "Usage: reverse.py in_file out_file"
    sys.exit(1)

in_filename  = sys.argv[1]
out_filename = sys.argv[2]

fin = wave.open(in_filename,'r')
fout = wave.open(out_filename,'w')
fout.setparams((fin.getnchannels(), 
                fin.getsampwidth(), 
                fin.getframerate(), 
                0,
                'NONE',
                'not compressed'))

num_frames = fin.getnframes()
num_channels = fin.getnchannels()

data = []
while (fin.tell() < num_frames):
    frame = fin.readframes(1)
    data.append(struct.unpack('%dh'%(num_channels), frame))


data.reverse()

for frame in data:
    for data in frame:
        packed_out_data = struct.pack('h', data)
        fout.writeframes(packed_out_data)

fout.close()  
fin.close()
