#!/usr/bin/python

# amplify.py: Amplifies a WAV file by the given scaling factor
#             and output to specified file
 
import wave
import struct
import sys

if len(sys.argv) < 4:
    print "Usage: amplify.py in_file out_file scale_factor"
    sys.exit(1)

in_filename  = sys.argv[1]
out_filename = sys.argv[2]
scale_factor = float(sys.argv[3])

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

def transform(data,scale_factor):
    new_data = int(data * scale_factor)
    if new_data > 32767:
        new_data = 32767
    if new_data < -32768:
        new_data = -32768
    return new_data

while (fin.tell() < num_frames):
    frame = fin.readframes(1)
    frame_data = struct.unpack('%dh'%(num_channels), frame)
    for data in frame_data:
        out_frame = transform(data,scale_factor)
        packed_out_data = struct.pack('h', out_frame)
        fout.writeframes(packed_out_data)

fout.close()  
fin.close()
