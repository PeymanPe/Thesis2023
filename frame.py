import numpy as np
import pandas as pd


class Frame(object):
    def __init__(self, mu, isFR1, BW):
        # PRB2.JPG at Google drive- Mydrive- Master Program- Thesis- PRB
        # First raw  shows Bandwidtht in MHz (channel)
        # the number of raw shows the miu
        #each number shows maximum number PRB at specified numerology

        self.FR1_dataframe = pd.read_excel(r'D:\Autonomous Systems\KTH\Thesis\Implementation\Data\Max.xlsx')
        # same file as the aformentioned but regarding to carrier frequency above 24 GHz
        self.FR2_dataframe = pd.read_excel(r'D:\Autonomous Systems\KTH\Thesis\Implementation\Data\Max2.xlsx')
        self.mu = mu
        # if FR is true, the carrier frequncy is below 6GHz otherwise above 24 GHz
        self.isFR1 = isFR1
        self.BW = BW
        #lOOK AT tableI switched ethernet fronthaul architecture for cloud-radio access networks
        self.SampleRate = 1.536 * self.BW
        # SCS in kHZ
        self.subcarrier_spacing = 15 * np.power(2, mu)
        #unit in ms

        self.slot_duration = 1 / np.power(2, mu)

        self.symbol_duration = 66.67 / np.power(2, mu) #microseconds
        self.slot_in_frame_count = 10 * np.power(2, mu)
    def Maxnprb(self): #gives the maximum number of PRB in each numorology
        if self.isFR1: #below 6GHZ
            prb_max_count = self.FR1_dataframe[self.BW][self.mu]
        else: #above 24 GHz
            prb_max_count = self.FR2_dataframe[self.BW][self.mu]
        return prb_max_count

