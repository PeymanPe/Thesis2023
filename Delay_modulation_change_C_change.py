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
    if const.split == 'IID':
        # frac_CC = (np.sum(cj[-5:])*user*ru)/(np.sum(cj[-5:])*user*ru+cj[-6])
        frac_CC = 0.5
        ceq_CC2 = np.array([1 - frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([1, 0]) * const.ceq_RU * C_percent

    elif const.split == 11:
        frac_RU = (cj[-5] * const.user_count) / (cj[-5] * const.user_count + np.sum(cj[:-5]))
        ceq_RU2 = np.array([1 - frac_RU, frac_RU]) * const.ceq_RU
        ceq_CC2 = np.array([0, 1]) * const.ceq_CC * C_percent
    elif const.split == 'E':
        frac_CC = ((np.sum(cj[11:-2])+cj[-1]) * const.user_count * const.ru_count) / ((np.sum(cj[11:-2])+cj[-1]) * const.user_count * const.ru_count + (np.sum(cj[:11])+cj[-2])) * const.ru_count
        ceq_CC2 = np.array([1 - frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([0, 0]) * const.ceq_RU * C_percent

    total_delay = Total_Delay_Calculator(const, n_subcar, frame, cj, ceq_RU2, ceq_CC2)[3]
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


C_percent = 0.1
# x1 = np.arange(5, n_subcar_max)
# x1 = np.arange(50, n_subcar_max, 20)
x1 = np.linspace(0.05, 0.5, num=30)
x2=np.array(["{:.0%}".format(i) for i in x1])

y1 = np.empty([len(x1), 4])
for i in range(len(x1)):
    y1[i, 0] = DelayChangeBW(frame, n_subcar, x1[i], const,2)
    y1[i, 1] = DelayChangeBW(frame, n_subcar, x1[i], const, 4)
    y1[i, 2] = DelayChangeBW(frame, n_subcar, x1[i], const, 6)
    y1[i, 3] = DelayChangeBW(frame, n_subcar, x1[i], const, 8)
    # y1[i, :] = DelayChangeBW(p, math.floor(n_subcar_max/2), x1[i], Lf)[:-1]
    # print(x1[i])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(x2, y1[:, 0], 'o-r')
ax.plot(x2, y1[:, 1], 'o-g')
ax.plot(x2, y1[:, 2], 'o-c')
ax.plot(x2, y1[:, 3], 'o-b')
# ax.axhline(y=1, color='r', linestyle='-')
# ax.text(3.5, 1.25, 'processing time threshold', fontsize=8, color='r')

ax.set_title(
    "Delay components with varying allocated digital units for a slice, miu=0 File size=5 KB with slice\n containing 5 users and slice BW is half of channel BW and fully loaded ")

ax.set(xlabel='Virtual machine limit(percentage) for the slice', ylabel='Total delay (ms)')
ax.legend(('QPSK', '16QAM', '64QAM','256QAM'), loc='upper right', shadow=True)

minor_ticks = np.arange(0, 9, 0.1)
major_ticks = np.arange(0, 9, 0.5)

# minor_ticks2 = np.arange(x2[0], x2[-1], x2[1]-x2[0])
# major_ticks2 = np.arange(x2[0], x2[-1], x2[3]-x2[0])

ax.set_yticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)

# ax.set_xticks(minor_ticks2, minor=True)
# ax.set_xticks(major_ticks2)

# ax.grid(which='both')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)
plt.setp(plt.gca(),ylim=(5,9))
plt.xlim([0, 29])

plt.show()