import math
import pandas as pd
import numpy as np


from numpy import random

def poisson_dist(x,y):
    return random.poisson(lam=1/x, size=y)



def data_generator(transfer_interval,first_instant,test_interval):

    data_generated = np.zeros(test_interval)
    for i in range(test_interval):
        if (i == first_instant) :
            data_generated[i] = 1
        if (i > first_instant):
            if((i-first_instant) % transfer_interval == 0):
                data_generated[i] = 1
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
    def __init__(self, user_count, prb_count,test_interval):
        super().__init__(user_count, prb_count)
        #constant message size
        self.file_size = 160 #20bytes
        self._target_transfer_interval_value = None
        self.user_count = user_count
        self.test_interval = test_interval #in milisoconds
        self._message_arival_time = None
        self._time_info = None
        self._slot_per_user = None

    @property
    def slot_per_user(self):
        self._slot_per_user = math.floor(self.file_size/1)
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
            self._message_arival_time = self._time_info.apply(lambda x: pd.Series(data_generator(x['target transfer interval'],x['arrival time'], self.test_interval)), axis=1)
            self._message_arival_time.columns = list('t'+str(i) for i in np.arange(100))
            return self._message_arival_time


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


#
# vv = Service(3, 201)
# vv.user_count =4
# #
# print(vv.subcarier_user)
#
ser = Service_urllc(15,200,100)
print(ser.target_transfer_interval_value)
ser.user_count= 500

# print(ser.target_transfer_interval_value)
#
k = ser.message_arival_time
print(k.to_string())
# print(ser.message_arival_time)
# for i in range(15):
#     print(k.loc[i].to_string())
# # print(pd.DataFrame(np.zeros((ser.user_count, ser.test_interval)), columns=list(np.arange(100))))
# print(ser.time_info)