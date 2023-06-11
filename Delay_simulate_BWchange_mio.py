import numpy as np
import math
import matplotlib.pyplot as plt
from frame import Frame

from Delay_Model import Dtot
from Constants import Constants




def DelayChangeBW(p, n_subcar,const):
    # number of radio units

    BW = (n_subcar * p.subcarrier_spacing)/1000
    n_subcar_user = math.floor(n_subcar/const.user_count)
    BW_user = (n_subcar_user * p.subcarrier_spacing)/1000



    actualvalue = np.array([BW, const.nmod, 2, 6, 1])

    actToRef = actualvalue / const.refvalue

    actualvalue_user = np.array([BW_user, const.nmod, 2, 6, 1])
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
        ceq_CC2 = np.array([1-frac_CC, frac_CC]) * const.ceq_CC
        ceq_RU2 = np.array([1, 0])*const.ceq_RU
    elif const.split == 11:
        frac_RU = (cj[-5]*const.user_count)/(cj[-5] * const.user_count + np.sum(cj[:-5]))
        ceq_RU2 = np.array([1-frac_RU, frac_RU]) * const.ceq_RU
        ceq_CC2 = np.array([0, 1]) * const.ceq_CC

    # dd = Dtot(Lf, packetsize, SwitchBitRate, n_subcar, nre, nmod, p.Tslot, cj, ceq_RU2, ceq_CC2, split, Nant, nn, nsymbol,
    #           user,ru)
    dd = Dtot(const, n_subcar, p, cj,ceq_RU2, ceq_CC2)

    return dd[0], dd[1], dd[2], dd[3], dd[4], cj





const= Constants()

#percentage of BW allocation for a service
sp=1


x2 =np.linspace(0.1, 1, num=20)
y2 = np.empty([len(x2),3])


for i in range(3):
    for j in range(len(x2)):
        p = Frame(i, True, 20)
        x3= x2[j] * 12 * p.max_prb_count
        y2[j,i]= DelayChangeBW(p,x3,const)[3]




plt.plot(x2,y2[:,0], 'o-r')
plt.plot(x2,y2[:,1], 'o-g')
plt.plot(x2,y2[:,2], 'o-c')
plt.title('Delay components with varying allocated bandwidth for various numerologies')
plt.xlabel("number of subcarriers")
plt.ylabel("Total delay")
plt.legend(('miu=0', 'miu=1','miu=2'), loc='upper right', shadow=True)

plt.grid()
plt.show()