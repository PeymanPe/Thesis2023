import numpy as np
import math
from Constants import Constants
import matplotlib.pyplot as plt
from frame import Frame
from energy_model import service_energy_calculater
from service import Service_urllc


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

provided_processing_ru = 300
provided_processing_cloud = 2000
provided_processing_cloud_percentage = 0.5
provided_processing_cloud_cp = provided_processing_cloud * provided_processing_cloud_percentage

provided_processing_cloud_up = provided_processing_cloud * (1 - provided_processing_cloud_percentage)/ser.user_count
provided_processing = np.array([provided_processing_ru,0, provided_processing_cloud_cp,provided_processing_cloud_up])
print(service_energy_calculater(ser,frame,const,provided_processing))



energy = np.empty([3, 5])
Energy_process_cc = np.zeros(3)
Energy_cooling_cc = np.zeros(3)
Energy_switching  = np.zeros(3)
Energy_ran  = np.zeros(3)
Energy_process_ru  = np.zeros(3)
const.modulation_compression = True

const.modulation_index = 4

Energy_process_cc[0] = service_energy_calculater(ser,frame,const,provided_processing)[3]
Energy_cooling_cc[0] = service_energy_calculater(ser,frame,const,provided_processing)[4]
Energy_switching[0] = service_energy_calculater(ser,frame,const,provided_processing)[5]
Energy_ran[0] = service_energy_calculater(ser,frame,const,provided_processing)[6].sum()
Energy_process_ru[0] = service_energy_calculater(ser,frame,const,provided_processing)[7].sum()
const.modulation_index = 6

Energy_process_cc[1] = service_energy_calculater(ser,frame,const,provided_processing)[3]
Energy_cooling_cc[1] = service_energy_calculater(ser,frame,const,provided_processing)[4]
Energy_switching[1] = service_energy_calculater(ser,frame,const,provided_processing)[5]
Energy_ran[1] = service_energy_calculater(ser,frame,const,provided_processing)[6].sum()
Energy_process_ru[1] = service_energy_calculater(ser,frame,const,provided_processing)[7].sum()
const.modulation_index = 8

Energy_process_cc[2] = service_energy_calculater(ser,frame,const,provided_processing)[3]
Energy_cooling_cc[2] = service_energy_calculater(ser,frame,const,provided_processing)[4]
Energy_switching[2] = service_energy_calculater(ser,frame,const,provided_processing)[5]
Energy_ran[2] = service_energy_calculater(ser,frame,const,provided_processing)[6].sum()
Energy_process_ru[2] = service_energy_calculater(ser,frame,const,provided_processing)[7].sum()

x= ['16QAM', '64QAM','256QAM']

p1 =plt.bar(x, Energy_process_cc, color='r',width=0.2)
p2 =plt.bar(x, Energy_cooling_cc, bottom=Energy_process_cc, color='b',width=0.2)
p3 =plt.bar(x, Energy_switching, bottom=Energy_cooling_cc+Energy_process_cc, color='g',width=0.2)
p4 =plt.bar(x, Energy_ran, bottom=Energy_cooling_cc+Energy_process_cc+Energy_switching, color='c',width=0.2)
p5 =plt.bar(x, Energy_process_ru, bottom=Energy_cooling_cc+Energy_process_cc+Energy_switching+Energy_ran, color='m',width=0.2)
plt.ylabel('Energy in (J)')
plt.title('')
plt.legend((p1[0], p2[0], p3[0],p4[0],p5[0]), ('Energy for processing at CC', 'Energy for cooling at CC', 'Energy consumed for switching','Energy at RAN','Energy for processing at ru'))
plt.show()