import numpy as np
import math
import matplotlib.pyplot as plt
from frame import Frame
from Delay_Model import Dtot
from Constants import Constants



def DelayChangeBW(p, n_subcar, C_percent, const):

    BW = (n_subcar * p.subcarrier_spacing) / 1000 #unit in MHz
    n_subcar_user = math.floor(n_subcar / const.user_count)
    BW_user = (n_subcar_user * p.subcarrier_spacing) / 1000 #unit in MHz

    actualvalue = np.array([BW, const.nmod, const.antennas_per_ru, 6, 1])

    actToRef = actualvalue / const.refvalue

    actualvalue_user = np.array([BW_user, const.nmod, const.antennas_per_ru, 6, 1])
    # actToRefUser = actToRef.copy()
    # we assume we allocate equally to each user
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
    if const.split == 9: #split II_D
        # frac_CC = (np.sum(cj[-5:])*user*ru)/(np.sum(cj[-5:])*user*ru+cj[-6])
        frac_CC = 0.5
        ceq_CC2 = np.array([1 - frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([1, 0]) * const.ceq_RU * C_percent

    elif const.split == 11:
        frac_RU = (cj[-5] * const.user_count) / (cj[-5] * const.user_count + np.sum(cj[:-5]))
        ceq_RU2 = np.array([1 - frac_RU, frac_RU]) * const.ceq_RU
        ceq_CC2 = np.array([0, 1]) * const.ceq_CC * C_percent
    elif const.split == 0:
        frac_CC = ((np.sum(cj[11:-2])+cj[-1]) * const.user_count * const.ru_count) / ((np.sum(cj[11:-2])+cj[-1]) * const.user * const.ru + (np.sum(cj[:11])+cj[-2]))* const.ru
        ceq_CC2 = np.array([1 - frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([0, 0]) * const.ceq_RU * C_percent

    dd = Dtot(const, n_subcar, p, cj, ceq_RU2, ceq_CC2)
    # Dtot(Lf, packetsize, SwitchBitRate, Nsc, nre, nmod, Tslot, cj, cRUEq, cCCEq, split, Nant, nn, nsymbol, user)
    return dd[0], dd[1], dd[2], dd[3], dd[4], cj





const= Constants()
frame = Frame(const.mu, True, const.BW)


n_subcar_max = 12 * frame.max_prb_count

# what percent of DUs allocated for a service
C_percent = 1

x1 = np.arange(50, n_subcar_max, 50)
x3 =x1.copy()
x3=x3/n_subcar_max
x2=np.array(["{:.0%}".format(i) for i in x3])

y1 = np.empty([len(x1), 5])
for i in range(len(x1)):
    y1[i, :] = DelayChangeBW(frame, x1[i], C_percent, const)[:-1]
    # print(x1[i])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(x2, y1[:, 3], 'o-r') #total delay
ax.plot(x2, y1[:, 2], 'o-g') #processing delay
ax.plot(x2, y1[:, 4], 'o-c') #transmission delay in RAN

ax.axhline(y=frame.slot_duration, color='r', linestyle='-') #It shows when processing delay is greater than delay in RAN
ax.text(0.1, frame.slot_duration*1.1, 'processing time threshold', fontsize=8, color='r')

ax.set_title(
    "Delay components with varying allocated bandwidth, miu=0, channel BW =20MHz File size=0.5 KB  with slice containing 5 users \n when 100% of total computing capacity is allocated ")

ax.set(xlabel='Percentage of channel BW allocated for a slice', ylabel='Total delay (ms)')
ax.legend(('total delay', 'processing delay at 1st time slot', 'Delay in RAN'), loc='upper right', shadow=True)

minor_ticks = np.arange(0, 10*frame.slot_duration, 0.5)
major_ticks = np.arange(0, 10*frame.slot_duration, 1)
ax.set_yticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)

# ax.grid(which='both')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

plt.show()