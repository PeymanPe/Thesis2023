import numpy as np
import pandas as pd
from Delay_Model import Ceq


class Constants:
    def __init__(self):
        # packet size (unit: Bytes)
        self.packetSize_byte = 1500
        # ethernet packet in bits
        self.packet_size_bits = self.packetSize_byte * 8
        # # modulation index =4 16-QAM
        # self.nmod = 4
        #number of bits per sample(20,16,8)
        self.Nbits = 16
        # Switch bit rate (unit: Mbps)
        self.SwitchBitRate = 800
        # number of symbols per slot
        self.nsymbol = 14 #14
        # number of resources elements per PRB
        self.nre = 12 * self.nsymbol
        # splitting II_D
        self.split = 9
        # splitting E
        #self.split = 0
        # 4 RU
        #number of antennas per radio unit
        self.Nant = 1
        # perctage of usage of resource blocks
        # self.nn = 1
        self.prb_usage = 1
        # number of bits per symble 16-QAM
        self.nmod = 4
        #
        # Number of CPUs per Cloud Server
        self.cpu_count = 2
        # Base processor frequency
        self.f = 2.3
        # Number of cores per CPU
        self.core_per_cpu_count = 18
        # Number of instructions per CPU cycle
        self.Nipc = 16

        # C_i values is calculated here based on specified senario

        df = pd.read_excel(r'D:\Autonomous Systems\KTH\Thesis\New simulation\Data\table2ref.xlsx')
        dff = df.values
        pd.DataFrame(dff).to_numpy()
        self.dff = dff
        # Table V values (SISO, 20MHz, 6 BPS/HZ, 64-QAM
        self.refvalue = np.array([20, 6, 1, 6, 1])
        # GOPs capacity at each processing unit
        self.ceq_CC = Ceq(self.cpu_count, self.f, self.core_per_cpu_count, self.Nipc)
        self.ceq_RU = 300
        # Number of users
        self.user = 5
        # number of radio units
        self.ru = 4
        # file size(each user) 0.5kB
        self.Lf = 5 * 8 #0.5
        # assumption 20Mhz channel miu=0 , FR1
        self.miu = 0
        #channel BW
        self.BW = 20
        #Switch bit rate (unit: Mbps)
        self.SwitchBitRate = 800
        #number of switches in series between central cloud and edge cloud
        self.Nsw = 1
        # #queuing delay for simplicity we assume it is constant (unit micro  seconds)
        self.Dq = 10
        #fabric delay (unit in micro second)
        self.Df = 5


        # slice instatioan delay delay (unit in ms)
        self.D_w = 0.5
        #proppagation delay (unit in micro seconds)
        self.Dp1 = 5 #fronhaul
        self.Dp2 = 1  #RAN NR
        # DRtx = 1

