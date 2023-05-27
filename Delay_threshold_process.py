import numpy as np
import math
import matplotlib.pyplot as plt
from frame import Frame
from Delay_Model import Dtot
from Constants import Constants
import pandas as pd



def DelayChangeBW(p, n_subcar, C_percent,const):
    # number of radio units
    ru = const.ru
    BW = (n_subcar * p.subcarrier_spacing) / 1000
    n_subcar_user = math.floor(n_subcar / const.user)
    BW_user = (n_subcar_user * p.subcarrier_spacing) / 1000

    actualvalue = np.array([BW, const.nmod, 1, 6, 1])

    actToRef = actualvalue / const.refvalue

    actualvalue_user = np.array([BW_user, const.nmod, 1, 6, 1])
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
            else:
                cjj[i] *= pow(actToRefUser[j], dff2[i, j])
    cj *= cjj
    # GOPs capacity allocated for CP and UP (first eleement for CP and the second for UP)
    if const.split == 9:
        # frac_CC = (np.sum(cj[-5:])*user*ru)/(np.sum(cj[-5:])*user*ru+cj[-6])
        frac_CC = 0.5
        ceq_CC2 = np.array([1 - frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([1, 0]) * const.ceq_RU * C_percent

    elif const.split == 11:
        frac_RU = (cj[-5] * const.user) / (cj[-5] * const.user + np.sum(cj[:-5]))
        ceq_RU2 = np.array([1 - frac_RU, frac_RU]) * const.ceq_RU
        ceq_CC2 = np.array([0, 1]) * const.ceq_CC * C_percent


    dd = Dtot(const, n_subcar, p, cj, ceq_RU2, ceq_CC2)

    return dd[2], dd[-1]





const = Constants()

#threshold computing


mu2 =np.array([0,1,2])

# what percent of DUs allocated for a service
C_percent = 0.1
x1 = np.linspace(0.1, 1, num=10)
C_percent = np.linspace(0.01, 0.8, num=100)



C_percent_list=[]
DU_list =[]

y2 = np.empty([len(x1),len(mu2)])

for k in range(len(mu2)):
# for k in range(len(user))
    for i in range(len(x1)):
        y3=0
        for j in range(len(C_percent)):

            p = Frame(k, True, 20)
            # p = Frame(1, True, 20)
            n_subcar_max = 12 * p.max_prb_count

            ll2 = DelayChangeBW(p, math.floor(x1[i] * n_subcar_max), C_percent[j], const)
            # oc1[i,j,k] = ll2[2]
            # oc2[i,j,k] = ll2[-1]
            if (ll2[0]>ll2[1]) and (y3< C_percent[j]):
                y3 = C_percent[j]

            del p
        y2[i,k]=y3







x2=np.array(["{:.0%}".format(i) for i in x1])
yy1=np.array(["{:.0%}".format(i) for i in y2[:,0]])
yy2=np.array(["{:.0%}".format(i) for i in y2[:,1]])
yy3=np.array(["{:.0%}".format(i) for i in y2[:,2]])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


ax.plot(x2, y2[:,0], 'o-r')
ax.plot(x2, y2[:,1], 'o-g')
ax.plot(x2, y2[:,2], 'o-b')



ax.set_title(
    "Minimum percentage for processing with different numerology in a slice with 5 users")

ax.set(xlabel='Percentage of channel BW allocated for a slice', ylabel='minimum required Virtual machine reserve')
ax.legend(('miu=0', 'miu=1', 'miu=2'), loc='upper right', shadow=True)

minor_ticks = np.arange(0, 0.8, 0.01)
major_ticks = np.arange(0, 0.8, 0.04)
ax.set_yticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)


ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

plt.show()