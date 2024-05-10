
#author:John Naulty
#date: july 2014
#SSVEP Example with Psychopy and OpenBCI
#stimuli frequency = 60/(frame_on+frame_off)


from SSVEP import *
#from InputBox import InputBox
import csv_collector

# expinfos = InputBox()
# filename = expinfos.file()
# print expinfos.port_name()
# port_addr = expinfos.port_name()
# print filename
# flash_dur = expinfos.stim_duration()
# trialnums = expinfos.stim_trials()
# waitduration = expinfos.waitduration()
# print port_addr
# print type(port_addr)

stim = SSVEP(frame_on=3, frame_off=3, numtrials=1, trialdur=30, usbtrig=True)
for i in range(5):
	# 30 seconds @ 10 Hz, no wait
	stim.frame_on 	= 3
	stim.frame_off 	= 3
	stim.waitdur 	= 0 # post-trial wait time in seconds
	stim.start()

	# 30 seconds @ 15 Hz, 10 second wait
	stim.frame_on 	= 2
	stim.frame_off 	= 2
	stim.waitdur 	= 10 # post-trial wait time in seconds
	stim.start()

stim.stop()
