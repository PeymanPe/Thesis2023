import math
import pandas as pd
import numpy as np


class Service:
    def __init__(self, user_count, subcarier_count):
        self.user_count = user_count
        self.subcarier_count = subcarier_count
        self._subcarier_user = None
    @property
    def subcarier_user(self):
        if self._subcarier_user == None:
            self._subcarier_user = math.floor(self.subcarier_count/self.user_count)
        return self._subcarier_user
    @property
    def user_count(self):
        return self._user_count


    @user_count.setter
    def user_count(self, user_count):
        self._user_count = user_count


    @property
    def subcarier_count(self):
        return self._subcarier_count


    @subcarier_count.setter
    def subcarier_count(self, subcarier_count):
        self._subcarier_count_per_user = None
        self._subcarier_count = subcarier_count





#refer to service 5 in notebook
class Service_urllc(Service):
    def __init__(self, user_count, subcarier_count,test_interval):
        super().__init__(user_count, subcarier_count)
        #constant message size
        self.file_size = 80
        self._target_transfer_interval_value = None
        self.user_count = user_count
        self.test_interval = test_interval


    @property
    def target_transfer_interval_value(self):
        if self._target_transfer_interval_value == None:
            self._target_transfer_interval_value = pd.Series(np.random.randint(10, 20, size=super().user_count))
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


    @property
    def test_interval(self):
        return self._test_interval


    @test_interval.setter
    def test_interval(self, test_interval):
        self._test_interval = test_interval




vv = Service(3, 201)
vv.user_count =4

print(vv.subcarier_user)

ser = Service_urllc(15,200,2)
print(ser.target_transfer_interval_value)
