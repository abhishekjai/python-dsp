#!/usr/bin/python

# sum.py: Sum two audio signals together
#         output = (ratio * signal1) + ((1.0 - ratio) * signal2)
    
import sys
from audiofile import *

if len(sys.argv) < 5:
    print "Usage: sum.py in_file1 in_file2 out_file ratio_file1"
    sys.exit(1)

in_filename1  = sys.argv[1]
in_filename2  = sys.argv[2]
out_filename  = sys.argv[3]
ratio_signal1 = float(sys.argv[4])

fin1 = AudioFile(in_filename1,'r')
fin2 = AudioFile(in_filename2,'r')
fout = AudioFile(out_filename,'w')

num_frames1 = fin1.getnframes()
num_frames2 = fin2.getnframes()
num_channels = fin1.getnchannels()

def sum(sample1, sample2, ratio_sample1):
    mix_sample1 = ratio_sample1 * sample1
    mix_sample2 = (1.0 - ratio_sample1) * sample2
    sum_sample = mix_sample1 + mix_sample2
    return sum_sample

for frame_cnt in range(0,max(num_frames1,num_frames2)):
    frame1      = None
    frame_data1 = None
    frame2      = None
    frame_data2 = None

    if fin1.tell() < num_frames1:
        frame_data1 = fin1.read(1)
    if fin2.tell() < num_frames2:
        frame_data2 = fin2.read(1)

    if frame_data1 and frame_data2:
        for i in range(0,len(frame_data1)):
            out_frame = sum(frame_data1[i],frame_data2[i],ratio_signal1)
            fout.write(out_frame)
    elif frame_data1:
        for i in range(0,len(frame_data1)):
            out_frame = sum(frame_data1[i],0,ratio_signal1)
            fout.write(out_frame)
    elif frame_data2:
        for i in range(0,len(frame_data2)):
            out_frame = sum(0,frame_data2[i],ratio_signal1)
            fout.write(out_frame)

    
fout.close()  
fin1.close()
fin2.close()
