#!/usr/bin/python

# sum.py: Sum two audio signals together
#         output = (ratio * signal1) + ((1.0 - ratio) * signal2)
    
import wave
import struct
import sys

if len(sys.argv) < 5:
    print "Usage: sum.py in_file1 in_file2 out_file ratio_file1"
    sys.exit(1)

in_filename1  = sys.argv[1]
in_filename2  = sys.argv[2]
out_filename  = sys.argv[3]
ratio_signal1 = float(sys.argv[4])

fin1 = wave.open(in_filename1,'r')
fin2 = wave.open(in_filename2,'r')
fout = wave.open(out_filename,'w')
fout.setparams((fin1.getnchannels(), 
                fin1.getsampwidth(), 
                fin1.getframerate(), 
                0,
                'NONE',
                'not compressed'))

num_frames1 = fin1.getnframes()
num_frames2 = fin2.getnframes()
num_channels = fin1.getnchannels()

def check_clip(sample):
    if sample > 32767:
        sample = 32767
    if sample < -32768:
        sample = -32768
    return sample

def sum(sample1, sample2, ratio_sample1):
    mix_sample1 = ratio_sample1 * sample1
    mix_sample2 = (1.0 - ratio_sample1) * sample2
    sum_sample = mix_sample1 + mix_sample2
    sum_sample = check_clip(sum_sample)
    return sum_sample

for frame_cnt in range(0,max(num_frames1,num_frames2)):
    frame1      = None
    frame_data1 = None
    frame2      = None
    frame_data2 = None

    if fin1.tell() < num_frames1:
        frame1 = fin1.readframes(1)
        frame_data1 = struct.unpack('%dh'%(num_channels), frame1)
    if fin2.tell() < num_frames2:
        frame2 = fin2.readframes(1)
        frame_data2 = struct.unpack('%dh'%(num_channels), frame2)

    if frame_data1 and frame_data2:
        for i in range(0,len(frame_data1)):
            out_frame = sum(frame_data1[i],frame_data2[i],ratio_signal1)
            packed_out_data = struct.pack('h', out_frame)
            fout.writeframes(packed_out_data)
    elif frame_data1:
        for i in range(0,len(frame_data1)):
            out_frame = sum(frame_data1[i],0,ratio_signal1)
            packed_out_data = struct.pack('h', out_frame)
            fout.writeframes(packed_out_data)
    elif frame_data2:
        for i in range(0,len(frame_data2)):
            out_frame = sum(0,frame_data2[i],ratio_signal1)
            packed_out_data = struct.pack('h', out_frame)
            fout.writeframes(packed_out_data)

    
fout.close()  
fin1.close()
fin2.close()
