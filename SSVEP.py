#author: John Naulty Jr.
#date: July 2014
#SSVEP class.

from psychopy import visual, core, event
import csv_collector
import serial

class SSVEP(object):
    #init sets the window(mywin), and the frequency of the flashing(frame_on, frame_off)
    #Frame duration in seconds = 1/monitorframerate(in Hz)
    #Thus the fastest frame rate could be 1 frame on 1 frame off
    #which equals 2/60 == 30Hz
    #Flash frequency = refreshrate/(frame_on+frame_off)

    def __init__(self, mywin= visual.Window([800, 600], fullscr=True, monitor='testMonitor',units='deg', color='black'),
                frame_on=5, frame_off=5, trialdur = 5.0, port='/dev/ttyACM0',
                fname='SSVEP.csv', numtrials=1, waitdur=2, usbtrig=False):

        self.mywin = mywin


        A = visual.TextStim(win=self.mywin, name='pattern1', units='norm', text='A', height=1.7, color=[1,1,1], font='Helvetica', bold=True)
        blank = visual.TextStim(win=self.mywin, name='pattern2', units='norm', text='', height=1.7, color=[1,1,1])

        self.pattern1 = A
        self.pattern2 = blank

        self.fixation = visual.GratingStim(win=self.mywin, size = 0.3, pos=[0,0], sf=0, rgb=-1)
        self.frame_on = frame_on
        self.frame_off = frame_off
        self.trialdur = trialdur
        self.fname = fname
        self.numtrials = numtrials
        self.waitdur = waitdur
        self.port = port

        self.usbtrig = usbtrig
        if self.usbtrig:
            ser = serial.Serial()
            ser.baudrate = 115200
            ser.port = 'COM4'
            ser.open()

            self.ser = ser
            self.code_stim_on = b'S'
            self.code_stim_off = b'T'
            self.code_trial_start = b'A'
            self.code_trial_end = b'B'



    def collecting(self):
        self.collector = csv_collector.CSVCollector(fname=self.fname, port= self.port)
        self.collector.start()

    def epoch(self, mark):
        self.collector.tag(mark)

    def stop(self):
        self.mywin.close()
        core.quit()


    def start(self):

        ###Testing framerate grabber###
        print(self.mywin.getActualFrameRate())
        self.Trialclock = core.Clock()
        self.freq = 60/(self.frame_on+self.frame_off)

        #start saving data from EEG device.
        #self.collecting()

        #possibly convert trialdur into frames given refresh rate (normally set at 60Hz)
        self.framerate = self.mywin.getActualFrameRate()
        #divison here makes it tricky
        self.trialframes = self.trialdur/60
        self.count = 0

        if self.usbtrig:
            self.ser.write(self.code_trial_start)

        while self.count<self.numtrials:

            #reset tagging
            self.should_tag = False
            #self.epoch(0)
            while self.Trialclock.getTime()<self.trialdur:

                #draws square and fixation on screen.
                self.fixation.setAutoDraw(True)
                self.pattern1.setAutoDraw(True)

                """
                ###Tagging the data with the calculated frequency###
                Attempting to only get 1 sample tagged, however, this is hard.
                """
                """alternative way to tag
                if self.should_tag == False:
                    #self.epoch(self.freq)
                    self.epoch(70)
                    self.mywin.flip()

                self.epoch(0)
                self.should_tag = True
                """
                #self.epoch(70)

                # usb trigger (frame on)
                if self.usbtrig:
                    self.ser.write(self.code_stim_on)

                for frameN in range(self.frame_on):
                    self.mywin.flip()

                #another way to change color with 1 pattern
                #self.pattern1.color *= -1
                self.pattern1.setAutoDraw(False)
                self.pattern2.setAutoDraw(True)

                # usb trigger (frame off)
                if self.usbtrig:
                    self.ser.write(self.code_stim_off)
                for frameN in range(self.frame_off):
                    self.mywin.flip()
                self.pattern2.setAutoDraw(False)

            #self.epoch(0)
            #clean black screen off
            self.mywin.flip()
            #wait certain time for next trial
            core.wait(self.waitdur)
            #reset clock for next trial
            self.Trialclock.reset()
            #count number of trials
            self.count+=1

            """
            ###Tagging the Data at end of stimulus###

    """
        if self.usbtrig:
            self.ser.write(self.code_trial_end)
        #self.collector.disconnect()
        #self.stop()




"""
Here are some test cases
Just run this program by itself if you don't want to use run.py

"""

if "__name__" == "__main__":
    stimuli75Hz = SSVEP(frame_on=4, frame_off=4)
    stimuli75Hz.start()

    stimuli12=SSVEP(frame_on=3, frame_off=2)
    stimuli12.start()

    stimuli20=SSVEP(frame_on=2, frame_off=1)
    stimuli20.start()
