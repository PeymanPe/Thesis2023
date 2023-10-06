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

def processing_gops_calculator(modulation_idx,frame,service):

    cj2 = const.dff[:, 0]
    cj = np.copy(cj2)
    BW_service = service.prb_count * frame.subcarrier_spacing * 12 * 0.001
    actualvalue = np.array([BW_service, modulation_idx, const.antennas_per_ru, 6, 1])
    actToRef = actualvalue / const.refvalue
    dff2 = const.dff[:, 1:]
    cjj = np.ones(16)
    BW_user = service.prb_per_user_count* frame.subcarrier_spacing * 12 * 0.001
    actualvalue_user = np.array([BW_user, modulation_idx, const.antennas_per_ru, 6, 1])
    actToRefUser = actualvalue_user / const.refvalue


    for i in range(16):
        for j in range(5):
            if i < 11:
                cjj[i] *= pow(actToRef[j], dff2[i, j])
            elif i !=15:
                cjj[i] *= pow(actToRefUser[j], dff2[i, j])
            else:
                cjj[i] *= pow(actToRef[j], dff2[i, j])
    cj *= cjj

    C_i_RU_CP = np.sum(cj[:11])
    C_i_RU_UP = 0
    C_i_CC_CP = cj[-2]
    C_i_CC_UP = np.sum(cj[11:-2]) + cj[-1]

    return C_i_RU_CP,C_i_RU_UP,C_i_CC_CP,C_i_CC_UP


# equal allocated number of subcarriers per user
def service_energy_calculater(service,frame,const,provided_processing):
    energy_RU = 0
    energy_central_cloud = 0
    prb_allocatiom_map = service.message_arival_time
    required_procsess = processing_gops_calculator(const.modulation_index,frame,service)
    # print(service.target_transfer_interval_value)
    for i in range(service.test_interval):

        total_file_size = 0
        total_active_user_in_a_service = 0

        for j in range(const.ru_count):
            utility_factor_RU =  required_procsess[0]/provided_processing[0]
            power_DU_RU = power_DU_RU_min + (power_DU_RU_max - power_DU_RU_min) * utility_factor_RU

            active_users_count = prb_allocatiom_map['t'+str(i)].sum()
            total_active_user_in_a_service += active_users_count
            print(service.prb_per_user_count)
            print(active_users_count)
            energy_RU += (active_users_count * service.prb_per_user_count * power_transmission_per_subcarier + power_DU_RU) * frame.slot_duration

        total_file_size = total_active_user_in_a_service * service.prb_per_user_count * const.modulation_index * const.nsymbol
        power_switching = (
                                      power_switching_static / services_count + ro_switching * total_file_size) * frame.slot_duration


        utility_factor_central_cloud = (required_procsess[2] + total_active_user_in_a_service * required_procsess[3]) / (
                provided_processing[2] + provided_processing[2] * service.user_count)
        power_DU_central_cloud = power_DU_central_cloud_min + (power_DU_central_cloud_max-power_DU_central_cloud_min)*\
                                 utility_factor_central_cloud
        energy_central_cloud += (power_DU_central_cloud + power_cooling_central_cloud + power_switching) * frame.slot_duration
    total_energy = energy_RU + energy_central_cloud


    return np.array([total_energy , energy_central_cloud , energy_RU, power_DU_central_cloud,power_switching])

numerology=0
bandwidth =20
const = Constants()

frame = Frame(numerology, True, bandwidth)
test_duration=100
prb_count = math.ceil(frame.max_prb_count * 0.7)
user_count=15
ser = Service_urllc(user_count,prb_count,test_duration,const)
print(ser.target_transfer_interval_value)
ser.prb_per_user_count
print(ser.slot_per_user)

provided_processing_cloud = 2000
provided_processing_cloud_percentage = 0.5
provided_processing_cloud_cp = provided_processing_cloud * provided_processing_cloud_percentage

provided_processing_cloud_up = provided_processing_cloud * (1 - provided_processing_cloud_percentage)/ser.user_count
provided_processing = np.array([300,0, 1000,])
print(service_energy_calculater(ser,frame,const,provided_processing))


