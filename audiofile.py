#!/usr/bin/python

# audiofile.py: Container class for an audio file
    
import wave
import struct

class AudioFile:
    """Container class for an audio file.  This class allows
       for reading and writing wave files with translation of
       packed data into unpacked data for manipulation by other
       programs."""

    def __init__(self,filename,mode):
        """Creates a new AudioFile instance with the given filename.  
           Mode should be one of 'r' (read) or 'w' (write)."""
        self.file_handle = wave.open(filename,mode)
        if mode == 'w':
            channels = 1
            sample_width = 2
            frame_rate  = 44100
            self.file_handle.setparams((channels,
                                        sample_width,
                                        frame_rate,
                                        0,
                                        'NONE',
                                        'not compressed'))

    def close(self):
        """Close the underlying file represented by this instance."""
        self.file_handle.close()

    def write(self,sample):
        """Write a sample to the underlying file.
           The sample is checked to ensure it fits in the
           size of the word the file expects."""
        sample = self.check_clip(sample)
        packed_out_data = struct.pack('h', sample)
        self.file_handle.writeframes(packed_out_data)

    def check_clip(self,sample):
        """Clip samples that are larger than the word size
           the underlying file supports.  Right now this is
           hardcoded to 16 bit signed word size."""
        if sample > 32767:
            sample = 32767
        if sample < -32768:
            sample = -32768
        return sample

