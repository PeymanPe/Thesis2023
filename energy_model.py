from service import Service_urllc
import math
from Constants import Constants
import matplotlib.pyplot as plt
from frame import Frame
import numpy as np

power_transmission_per_subcarier = 0.39

power_DU_central_cloud_min = 10
power_DU_central_cloud_max = 1000
power_cooling_central_cloud = 5
power_switching_static = 5
ro_switching = 0.000001

power_DU_RU_min = 5
power_DU_RU_max = 200

services_count = 3


# equal allocated number of subcarriers per user
def service_energy_calculater(service,frame,const):
    energy_RU = 0
    energy_central_cloud = 0
    prb_allocatiom_map = service.message_arival_time
    # print(service.target_transfer_interval_value)
    for i in range(service.test_interval):
        utility_factor_central_cloud = 0
        total_file_size = 0
        power_switching = (power_switching_static/services_count + ro_switching * total_file_size) * frame.slot_duration
        power_DU_central_cloud = power_DU_central_cloud_min + (power_DU_central_cloud_max-power_DU_central_cloud_min)*\
                                 utility_factor_central_cloud
        energy_central_cloud += (power_DU_central_cloud + power_cooling_central_cloud + power_switching) * frame.slot_duration
        for j in range(const.ru_count):
            utility_factor_RU = 0
            power_DU_RU = power_DU_RU_min + (power_DU_RU_max - power_DU_RU_min) * \
                                     utility_factor_RU

            active_users_count = prb_allocatiom_map['t'+str(i)].sum()
            print(service.prb_per_user_count)
            print(active_users_count)
            energy_RU += (active_users_count * service.prb_per_user_count * power_transmission_per_subcarier + power_DU_RU) * frame.slot_duration
    total_energy = energy_RU + energy_central_cloud


    return total_energy

numerology=0
bandwidth =20
const = Constants()

frame = Frame(numerology, True, bandwidth)
test_duration=100
subcarrier_count = frame.max_prb_count*8
user_count=15
ser = Service_urllc(user_count,subcarrier_count,test_duration,const)
print(ser.target_transfer_interval_value)
ser.prb_per_user_count
print(ser.slot_per_user)

print(service_energy_calculater(ser,frame,const))