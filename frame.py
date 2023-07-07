import numpy as np
import pandas as pd


class Frame:
    def __init__(self, mu, is_FR_one, BW):
        # PRB2.JPG at Google drive- Mydrive- Master Program- Thesis- PRB
        # First raw  shows Bandwidtht in MHz (channel)
        # the number of raw shows the miu
        #each number shows maximum number PRB at specified numerology

        self.FR1_dataframe = pd.read_excel(r'D:\Autonomous Systems\KTH\Thesis\Implementation\Data\Max.xlsx')
        # same file as the aformentioned but regarding to carrier frequency above 24 GHz
        self.FR2_dataframe = pd.read_excel(r'D:\Autonomous Systems\KTH\Thesis\Implementation\Data\Max2.xlsx')
        self.mu = mu
        # if FR is true, the carrier frequncy is below 6GHz otherwise above 24 GHz
        self.is_FR_one = is_FR_one
        self.BW = BW
        #lOOK AT tableI switched ethernet fronthaul architecture for cloud-radio access networks
        self._sample_rate = None
        # SCS in kHZ
        self._subcarrier_spacing = None
        #unit in ms

        self._slot_duration = None

        self._symbol_duration = None #microseconds
        self._slot_in_frame_count = None
        self._max_prb_count = None
    @property
    def sample_rate(self):
        if self._sample_rate == None:
            self._sample_rate = 1.536 * self.BW
        return self._sample_rate
    @property
    def subcarrier_spacing(self):
        if self._subcarrier_spacing == None:
            self._subcarrier_spacing = 15 * np.power(2, self.mu)
        return self._subcarrier_spacing
    @property
    def slot_duration(self):
        if self._slot_duration == None:
            self._slot_duration = 1 / np.power(2, self.mu)
        return self._slot_duration
    @property
    def slot_in_frame_count(self):
        if self._slot_in_frame_count == None:
            self._slot_in_frame_count = 10 * np.power(2, self.mu)
        return self._slot_in_frame_count
    @property
    def symbol_duration(self):
        if self._symbol_duration == None:
            self._symbol_duration = 66.67 / np.power(2, self.mu)
        return self._symbol_duration
    @property
    def max_prb_count(self): #gives the maximum number of PRB in each numorology
        if self._max_prb_count == None:
            if self.is_FR_one: #below 6GHZ
                self._max_prb_count = self.FR1_dataframe[self.BW][self.mu]
            else: #above 24 GHz
                self._max_prb_count = self.FR2_dataframe[self.BW][self.mu]
        return self._max_prb_count
    @property
    def mu(self):
        return self._mu
    @mu.setter
    def mu(self, mu):
        self._subcarrier_spacing = None
        self._slot_duration = None
        self._symbol_duration = None
        self._slot_in_frame_count = None
        self._max_prb_count = None
        self._mu = mu

    @property
    def is_FR_one(self):
        return self._is_FR_one
    @is_FR_one.setter
    def is_FR_one(self,is_FR_one):
        self._is_FR_one = is_FR_one

    @property
    def BW(self):
        return self._BW
    @BW.setter
    def BW(self,BW):
        if BW not in [5,10,15,20,25,30,40,50,60,70,80,90,100]:
            raise AttributeError("not valid bandwidth is selected")
        self._max_prb_count = None
        self._sample_rate = None
        self._BW = BW





# frame = Frame(0, True, 30)
#
# print(frame.slot_in_frame_count)

