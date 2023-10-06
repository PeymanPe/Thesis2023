# import dataclasses

import numpy as np
import pandas as pd

def Ceq(NCPU,f,Ncores,Nipc):
    ceq1 = NCPU * f * Ncores * Nipc
    return ceq1

class Constants:
    def __init__(self):
        # packet size (unit: Bytes)
        self.packetSize_byte = 1500
        # ethernet packet in bits
        self.packet_size_bits = self.packetSize_byte * 8
        # # modulation index =4 16-QAM
        # self.nmod = 4
        #number of bits per sample(20,16,8)
        self.bits_per_sample = 16
        # Switch bit rate (unit: Mbps)
        self.SwitchBitRate = 800
        # number of symbols per slot
        self.nsymbol = 14 #14
        # number of resources elements per PRB
        self.nre = 12 * self.nsymbol
        # splitting II_D
        self.split = 'IID'
        # self.split = 9
        # splitting E
        #self.split = 0
        # 4 RU
        #number of antennas per radio unit
        self.antennas_per_ru = 1
        # perctage of usage of resource blocks
        # self.nn = 1
        self.prb_usage = 1
        # number of bits per symble 16-QAM
        self.modulation_index = 4
        #
        # Number of CPUs per Cloud Server
        self.cpu_count = 2
        # Base processor frequency
        self.processor_freq = 2.3
        # Number of cores per CPU
        self.core_per_cpu_count = 18
        # Number of instructions per CPU cycle
        self.instructions_per_cycle = 16

        self.modulation_compression = False

        # C_i values is calculated here based on specified senario

        df = pd.read_excel('compute_ref_values.xlsx')
        dff = df.values
        pd.DataFrame(dff).to_numpy()
        self.dff = dff
        # Table V values (SISO, 20MHz, 6 BPS/HZ, 64-QAM
        self.refvalue = np.array([20, 6, 1, 6, 1])
        # GOPs capacity at each processing unit
        self.ceq_CC = Ceq(self.cpu_count, self.processor_freq, self.core_per_cpu_count, self.instructions_per_cycle)
        self.ceq_RU = 300
        # Number of users
        self.user_count = 5
        # number of radio units
        self.ru_count = 1
        # self.ru_count = 4
        # file size(each user) 0.5kB
        self.file_size = 5 * 8 #0.5
        # assumption 20Mhz channel miu=0 , FR1
        self.mu = 0
        #channel BW
        self.BW = 20
        #Switch bit rate (unit: Mbps)
        self.switch_bit_rate = 800
        #number of switches in series between central cloud and edge cloud
        self.switch_count = 1
        # #queuing delay for simplicity we assume it is constant (unit micro  seconds)
        self.queue_delay = 10
        #fabric delay (unit in micro second)
        self.delay_fabric = 5


        # slice instatioan delay delay (unit in ms)
        self.slice_instantiation_delay = 0.5
        #proppagation delay (unit in micro seconds)
        self.propagation_delay_fronthaul = 5 #fronhaul
        self.propagation_delay_RAN = 1  #RAN NR
        # DRtx = 1


#
# @dataclasses
# class Constants:
#
#     # packet size (unit: Bytes) ethernet (Max size)
#     packetSize_byte = 1500
#     # ethernet packet in bits
#     packet_size_bits = packetSize_byte * 8
#     # # modulation index =4 16-QAM
#     # self.nmod = 4
#     #number of bits per sample(20,16,8) Switched Ethernet Fronthaul
#     #Architecture for Cloud-Radio Access Networks
#     bits_per_sample = 16
#     # Switch bit rate (unit: Mbps)
#     SwitchBitRate = 800
#     # number of symbols per slot
#     nsymbol = 14 #14
#     # number of resources elements per PRB
#     nre = 12 * nsymbol
#     # splitting II_D
#     split = 9
#     # splitting E
#     #self.split = 0
#     # 4 RU
#     #number of antennas per radio unit
#     antennas_per_ru = 1
#     # perctage of usage of resource blocks
#     prb_usage = 1
#     # number of bits per symble 16-QAM
#     nmod = 4
#     #
#     # Number of CPUs per Cloud Server
#     cpu_count = 2
#     # Base processor frequency
#     f = 2.3
#     # Number of cores per CPU
#     core_per_cpu_count = 18
#     # Number of instructions per CPU cycle
#     instructions_per_cycle = 16
#
#     # C_i values is calculated here based on specified senario
#
#     df = pd.read_excel(r'D:\Autonomous Systems\KTH\Thesis\New simulation\Data\table2ref.xlsx')
#     dff = df.values
#     pd.DataFrame(dff).to_numpy()
#
#     # Table V values (SISO, 20MHz, 6 BPS/HZ, 64-QAM
#     refvalue = np.array([20, 6, 1, 6, 1])
#     # GOPs capacity at each processing unit
#     ceq_CC = Ceq(cpu_count, f, core_per_cpu_count, instructions_per_cycle)
#     ceq_RU = 300
#     # Number of users
#     user_count = 5
#     # number of radio units
#     ru_count = 4
#     # file size(each user) 0.5kB
#     file_size = 5 * 8 #0.5
#     # assumption 20Mhz channel miu=0 , FR1
#     mu = 0
#     #channel BW
#     BW = 20
#     #Switch bit rate (unit: Mbps)
#     SwitchBitRate = 800
#     #number of switches in series between central cloud and edge cloud
#     switch_count = 1
#     # #queuing delay for simplicity we assume it is constant (unit micro  seconds)
#     Dq = 10
#     #fabric delay (unit in micro second)
#     Df = 5
#
#
#     # slice instatioan delay delay (unit in ms)
#     D_w = 0.5
#    #proppagation delay (unit in micro seconds)
#     Dp1 = 5 #fronhaul
#     Dp2 = 1  #RAN NR
#         # DRtx = 1