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
fout.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

num_frames = fin.getnframes()

def transform(data,scale_factor):
    new_data = int(data * scale_factor)
    if new_data > 32767:
        new_data = 32767
    if new_data < -32768:
        new_data = -32768
    return new_data

while (fin.tell() < num_frames):
    frame = fin.readframes(1)
    frame_data = struct.unpack('<h', frame)
    out_frame = transform(frame_data[0],scale_factor)
    print frame_data[0], out_frame
    packed_out_data = struct.pack('h', out_frame)
    fout.writeframes(packed_out_data)

fout.close()  
fin.close()
