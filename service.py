import math
import pandas as pd
import numpy as np
from Constants import Constants


from numpy import random

def poisson_dist(x,y):
    return random.poisson(lam=1/x, size=y)



def data_generator(transfer_interval,first_instant,test_interval, slot_per_user):

    data_generated = np.zeros(test_interval)
    for i in range(test_interval):
        if (i == first_instant) :
            # data_generated[i] = 1
            data_generated[i:(slot_per_user+i)] = 1
        if (i > first_instant):
            if((i-first_instant) % transfer_interval == 0):
                data_generated[i:(slot_per_user+i)] = 1
    return data_generated




class Service:
    def __init__(self, user_count, prb_count):
        self.user_count = user_count
        self.prb_count = prb_count
        self._prb_per_user_count = None
    @property
    def prb_per_user_count(self):
        if self._prb_per_user_count == None:
            self._prb_per_user_count = math.floor(self.prb_count/self.user_count)
            #assume BW is uniformly distributed between users
        return self._prb_per_user_count
    @property
    def user_count(self):
        return self._user_count


    @user_count.setter
    def user_count(self, user_count):
        self._user_count = user_count


    @property
    def prb_count(self):
        return self._prb_count


    @prb_count.setter
    def prb_count(self, prb_count):
        self._prb_per_user_count = None
        self._prb_count = prb_count





#refer to service 5 in notebook
class Service_urllc(Service):
    def __init__(self, user_count, prb_count,test_interval,const):
        super().__init__(user_count, prb_count)
        #constant message size
        self.file_size = 1600 #20bytes
        self._target_transfer_interval_value = None
        self.user_count = user_count
        self.test_interval = test_interval #in milisoconds
        self._message_arival_time = None
        # self._prb_map = np.zero(self._test_interval)
        # self._prb_allocation_map = np.zero(self._test_interval)
        self._time_info = None
        self._slot_per_user = None
        self.const = const

    @property
    def slot_per_user(self):
        self._slot_per_user = math.ceil(self.file_size/(self._prb_per_user_count * 12 * self.const.modulation_index * self.const.nsymbol))
        return self._slot_per_user

    @property
    def time_info(self):
        if isinstance(self._time_info, pd.DataFrame):
            return self._time_info
        else:
            raise AttributeError("time info is not set, call target_transfer_interval_value")

    @property
    def message_arival_time(self):
        if isinstance(self._message_arival_time, pd.DataFrame):
            return self._message_arival_time
        if self._message_arival_time == None:
            # self._message_arival_time = self._target_transfer_interval_value.apply(lambda x: pd.Series(data_generator(x,self.test_interval)))
            self._message_arival_time = self._time_info.apply(lambda x: pd.Series(data_generator(x['target transfer interval'],x['arrival time'], self.test_interval, self._slot_per_user)), axis=1)
            self._message_arival_time.columns = list('t'+str(i) for i in np.arange(self._test_interval))
            return self._message_arival_time

    # @property
    # def prb_allocation_map(self):
    #     if isinstance(self._prb_allocation_map, pd.Series):
    #         return self._prb_allocation_map
    #     else:
    #         if self._prb_allocation_map == None:
    #             self._prb_allocation_map = self._message_arival_time.copy()
    #             for i in range(self._user_count):
    #                 for j in range(self._test_interval):
    #                     if(self._prb_allocation_map.iloc[i,j] == 1):
    #                         for k in range(self._slot_per_user):
    #                             if j+k< self._test_interval:
    #                                 self._prb_allocation_map.iloc[i, j+k]=1
    #
    #         return self._prb_allocation_map
    @property
    def target_transfer_interval_value(self):
        if isinstance(self._target_transfer_interval_value, pd.Series):
            return self._target_transfer_interval_value
        else:
            if self._target_transfer_interval_value == None:
                self._target_transfer_interval_value = pd.Series(np.random.randint(10, 20, size=self.user_count))
                self._time_info =pd.DataFrame(columns=['target transfer interval','arrival time'])
                self._time_info['target transfer interval'] = self._target_transfer_interval_value.copy()
                self._time_info['arrival time'] = self._target_transfer_interval_value.apply(lambda x: np.random.randint(0, x))
        return self._target_transfer_interval_value

    @property
    def user_count(self):
        return self._user_count


    @user_count.setter
    def user_count(self, user_count):
        if (user_count>20):
            raise AttributeError("user count for this service can be more that 20")
        elif (user_count<10):
            raise AttributeError("user count for this service can be less that 10")
        self._user_count = user_count
        self._target_transfer_interval_value = None
        self._message_arival_time = None
        self._time_info = None
        # self._prb_allocation_map = None

    @property
    def const(self):
        return self._const

    @const.setter
    def const(self, const):
        self._const = const

    @property
    def test_interval(self):
        return self._test_interval


    @test_interval.setter
    def test_interval(self, test_interval):
        self._test_interval = test_interval


class Service_embb(Service):
    def __init__(self, user_count, prb_count,test_interval,min_bitrate):
        super().__init__(user_count, prb_count)
        #constant message size
        self._file_size = None #20bytes
        self.E2E_delay_threshold = 10 # unit:milisecond
        self.min_bitrate = min_bitrate #unit in Mbit/s
        self.user_count = user_count
        self.test_interval = test_interval #in milisoconds


    @property
    def file_size(self):
        if self._file_size == None:
            self._file_size = pd.Series(100 *self.min_bitrate* np.random.randint(10, 14, size=self.user_count))
            return self._file_size
        else:
            return self._file_size
    @property
    def user_count(self):
        return self._user_count


    @user_count.setter
    def user_count(self, user_count):
        if (user_count>100): #suggested to choose less than 15
            raise AttributeError("user count for this service can be more that 100")
        self._user_count = user_count
        self._file_size = None

    @property
    def test_interval(self):
        return self._test_interval


    @test_interval.setter
    def test_interval(self, test_interval):
        self._test_interval = test_interval
    @property
    def min_bitrate(self):
        return self._min_bitrate


    @min_bitrate.setter
    def min_bitrate(self, min_bitrate):
        if (min_bitrate<10):
            raise AttributeError("bitrate should be choosen bigger than 10")
        self._min_bitrate = min_bitrate



# const = Constants()
# ser = Service_urllc(15,30,100,const)
# print(ser.target_transfer_interval_value)
#
#
# # print(ser.target_transfer_interval_value)
# #
# ser.prb_per_user_count
# print(ser.slot_per_user)
# k = ser.message_arival_time
# prb_map = np.zeros(100)
# for i in range(100):
#     prb_map[i] = k['t'+str(i)].sum()
#
# print(prb_map)
# print(k.to_string())
