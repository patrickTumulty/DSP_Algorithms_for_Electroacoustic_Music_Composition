# Last Updated : Nov 12th, 2019
# Patrick Tumulty 

import SignalLibrary as sl
import matplotlib.pyplot as plt

# ==== IMPORT AUDIO ==============================================================

audio_file = "ExampleAudioFile.wav"

sig = sl.WavFile(audio_file) # creates teh WavFile object

# ==== CREATE ENVELOPE ===========================================================
#       This section creates an envelope of your imported audio data
#       Recommended to use default settings for this section. 
bunch       = 35  # Affects the resolution of the envelope 
lpf         = 100 # Cut off frequency for low pass filter 
filt_order  = 4   # low pass filter slope 

env = sig.get_env_pd(sig.data, bunch, lpf, filt_order, sig.sample_rate)

# ==== SIGNAL ENVELOPE PLOT ======================================================
#       Uncomment lines below to vew this graph

# plt.title("Envelope over Signal")
# plt.xlabel("Time (samples)")
# plt.ylabel("Amplitude")
# plt.plot(sig.data)
# plt.plot(env)
# plt.show()

# ==== CALCULATE THE AUDIO SHIFTING ==============================================
#       This section is where you can edit the parameters that effect
#       your final composition.
atk_thresh  = 0.06   # atk and rel threshold, see SIGNAL ENVELOPE PLOT above
rel_thresh  = 0.007
gConst      = 2  # how much will the various audio events displace eachother in time 
rPow        = 2  # 2 in this case represents the distance squared in between each audio event
panRatio    = 5  # compression ratio for panning values
panThresh   = 30 # compresstion threshold for pan values (between 0 - 100)
mag_scale   = 'RMS'  # LUFS is also an option (still needs work)

sig.calc_shift(sig.data, env, atk_thresh, rel_thresh, gConst, rPow, panRatio, panThresh, mag_scale)

# ==== RECONSTRUCT SIGNAL ========================================================
#       Reconstruct your signal

length = len(sig.data) # get length of original audio signal

r = sl.Reconstruct().new_stereo(length) # create a stereo array of zeros with the length of the original data
r = sl.Reconstruct().reconstruct_stereo(r, sig.audio_events) # add the shifted audio events to the new array

r = sl.Reconstruct().new_mono(length)
r = sl.Reconstruct().reconstruct_mono(r, sig.audio_events)
#       Note: To output a mono file instead of a stereo file simply change 
#       new_stereo and reconstruct_stereo to new_mono and reconstruct_mono
# ==== WRITE TO A NEW WAVFILE ====================================================

new_file = "NewAudioFile.wav" # write your new audio file to the current working directory. 

sig.write2wav(new_file, r) # comment out this line if you don't want this script to write a new file

# ==== PLOT NEW SIGNAL ===========================================================
#       This plot allows you to see the timeline of your new signal overlayed with your original audio 
#       To view this graph with no shifting simply add applyShift="N" as an argument in the calc_shift() method. 
#       Blue dots in this graph represent panning values. Negative values are panned left and positive values are 
#       Panned right. 
#       Uncomment lines below to view this graph

# plt.title("Reconstructed Signal Over Original Signal")
# plt.xlabel("Time (samples)")
# plt.ylabel("Amplitude")
# plt.plot(sig.data, 'red') # red is the original signal
# plt.plot(r, 'green')      # green is the new signal
# plt.plot([item.peakIdx + item.offset for item in sig.audio_events],[item * 0.01 for item in sig.panValues], 'b.')
# plt.show()

#       Note: Amplitude values may seem different than the original signal for the reason 
#       that this plot is showing one channel of the reconstructed audio signal signal 
#       overlayed with the original mono signal. 

