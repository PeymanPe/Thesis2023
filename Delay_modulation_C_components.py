import numpy as np
import math
from Constants import Constants
import matplotlib.pyplot as plt
from frame import Frame
from Delay_Model import Total_Delay_Calculator




def DelayChangeBW(frame, n_subcar, C_percent, const, modulation_idx):

    BW = (n_subcar * frame.subcarrier_spacing) / 1000
    n_subcar_user = math.floor(n_subcar / const.user_count)
    BW_user = (n_subcar_user * frame.subcarrier_spacing) / 1000

    actualvalue = np.array([BW, modulation_idx, const.antennas_per_ru, 6, 1])

    actToRef = actualvalue / const.refvalue

    actualvalue_user = np.array([BW_user, modulation_idx, const.antennas_per_ru, 6, 1])

    actToRefUser = actualvalue_user / const.refvalue

    dff2 = const.dff[:, 1:]

    # cj = dff[:, 0]
    cj2 = const.dff[:, 0]
    cj = np.copy(cj2)
    # print(cj)
    cjj = np.ones(16)
    # print(cjj)

    for i in range(16):
        for j in range(5):
            if i < 11:
                cjj[i] *= pow(actToRef[j], dff2[i, j])
            elif i !=15:
                cjj[i] *= pow(actToRefUser[j], dff2[i, j])
            else:
                cjj[i] *= pow(actToRef[j], dff2[i, j])
    cj *= cjj
    # GOPs capacity allocated for CP and UP (first eleement for CP and the second for UP)
    if const.split == 'IID':
        # frac_CC = (np.sum(cj[-5:])*user*ru)/(np.sum(cj[-5:])*user*ru+cj[-6])
        frac_CC = 0.5
        ceq_CC2 = np.array([1 - frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([1, 0]) * const.ceq_RU * C_percent

    elif const.split == 'ID':
        frac_RU = (cj[-5] * const.user_count) / (cj[-5] * const.user_count + np.sum(cj[:-5]))
        ceq_RU2 = np.array([1 - frac_RU, frac_RU]) * const.ceq_RU
        ceq_CC2 = np.array([0, 1]) * const.ceq_CC * C_percent
    elif const.split == 'E':
        frac_CC = ((np.sum(cj[11:-2])+cj[-1]) * const.user_count * const.ru_count) / ((np.sum(cj[11:-2])+cj[-1]) * const.user_count * const.ru_count + (np.sum(cj[:11])+cj[-2])) * const.ru_count
        ceq_CC2 = np.array([1 - frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([0, 0]) * const.ceq_RU * C_percent

    total_delay = Total_Delay_Calculator(const, n_subcar, frame, cj, ceq_RU2, ceq_CC2)
    # Dtot(Lf, packetsize, SwitchBitRate, Nsc, nre, nmod, Tslot, cj, cRUEq, cCCEq, split, Nant, nn, nsymbol, user)
    return total_delay
    # dd[0], dd[1], dd[2], dd[3], dd[4], cj



const= Constants()
numerology=0
bandwidth =20
frame = Frame(numerology, True, bandwidth)
# frame = Frame(const.mu, True, const.BW)


# we have 12 subcarrier per prb so 50% BW
n_subcar = 6 * frame.max_prb_count


C_percent = 0.3



delay = np.empty([3, 6])


const.modulation_index = 4
delay[0, :] = DelayChangeBW(frame, n_subcar, C_percent, const, const.modulation_index)
const.modulation_index = 6
delay[1, :] = DelayChangeBW(frame, n_subcar, C_percent, const, const.modulation_index)
const.modulation_index = 8
delay[2, :] = DelayChangeBW(frame, n_subcar, C_percent, const, const.modulation_index)

x= ['16QAM', '64QAM','256QAM']

p1 =plt.bar(x, delay[:,4], color='r',width=0.2)
p2 =plt.bar(x, delay[:,2], bottom=delay[:,4], color='b',width=0.2)
p3 =plt.bar(x, delay[:,-1], bottom=delay[:,4]+delay[:,2], color='g',width=0.2)
plt.ylabel('Delay in (ms)')
plt.title('Delay componenets with varying modulation indexesfor a slice, miu=0 File size=5 KB with slice\n containing 5 users and slice BW is half of channel BW and fully loaded 30% computional power is used')
plt.legend((p1[0], p2[0], p3[0]), ('Delay in RAN', 'Processing Delay', 'Delay in fronthaul'))
plt.show()