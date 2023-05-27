import numpy as np
from frame import Frame
import math





# required bitrate for fronthaul
def MHbitRate(Nsc, Ts,const, SampleRate):
    if const.split == 9: #splitting at II_D (unit Mbps)
        MH = Nsc * 0.9 * 2 * const.Nbits * const.Nant * const.prb_usage / Ts
    elif const.split ==0: # splitting at E

        # fs=1/Ts
        fs = SampleRate
        # fs =1.536*BW
        MH = fs * 2 * const.Nbits * const.Nant
    elif const.split ==15:
        MH = 151
    return MH

def Ceq(NCPU,f,Ncores,Nipc):
    ceq1 = NCPU * f * Ncores * Nipc
    return ceq1


#return in ms unit
def Dtot(const, Nsc, frame, cj, cRUEq, cCCEq):

    Tslot = frame.slot_duration


    SampleRate = frame.sample_rate

    # switching delay (unit:microsecond)
    Dse = const.packet_size_bits / const.SwitchBitRate






    # required bitrate for fronthaul
    # Nsc = nprb * 12
    #sample duration time
    # Ts = Tslot/const.nsymbol
    ##to be more accurate (micro seconds)
    Ts = frame.symbol_duration
    MHbitRate1 = MHbitRate(Nsc, Ts, const, SampleRate)

    # MHbitRate1 = MHbitRate(Nsc, Ts, nn, split,Nant,nmod)
    # queuing delay
    EP = const.packet_size_bits/MHbitRate1
    L_phi = Nsc * const.nmod * 1.04
    ro = EP * L_phi/const.packet_size_bits
    kk = ro/(1-ro)
    # zz = math.log(kk)/math.log(math.e)

    # DD = max(0,kk*zz)

    # print(MHbitRate1)

    # Transmission delay (unit:microsecond)
    DMtx = const.Lf / MHbitRate1

    # print(DMtx)

    Nsc_user = math.floor(Nsc/const.user)

    nprb = Nsc/12



    Nslot = math.ceil(const.Lf*1000 / (Nsc_user * const.nmod * const.nsymbol))



    # equation 4 (unit:milisecond)
    DRtx = Nslot * Tslot

    #equation 23 (unit giga operation per radio subframe
    #we have 16 total number of CP and UP functions
    if const.split == 0: #splitting at E
        C_i_RU = 0
        C_i_CC_CP = np.sum(cj[:11])+cj[-2]
        C_i_CC_UP = np.sum(cj[11:-2])+cj[-1]
        f = 2.3 *1000
        Tss=(1/f)
        dRUpr = 0
        dCCpr = math.ceil(C_i_CC_CP * f*Tslot / cCCEq[0]) * (Tss) + math.ceil(C_i_CC_UP * f *Tslot/ cCCEq[1])* (Tss)


        n2 = 0
        n1 = 1

    elif const.split == 9: #spliting for II_D
        C_i_RU_CP = np.sum(cj[:11])
        C_i_CC_CP = cj[-2]
        C_i_CC_UP = np.sum(cj[11:-2])+cj[-1]

        n1 = 1
        n2 = 1
        # unit in kHz
        f = 2.3 *1000
        Tss=(1/f)


        dRUpr = 0
        dRUpr = math.ceil(C_i_RU_CP * f * Tslot/ cRUEq[0]) * (Tss)

        dCCpr = math.ceil(C_i_CC_CP * f * Tslot/ cCCEq[0]) * (Tss)
        dCCpr += math.ceil(C_i_CC_UP * f * Tslot/ cCCEq[1]) * (Tss)





    elif const.split == 11:
        C_i_RU_CP = np.sum(cj[:11])
        C_i_RU_UP = cj[11]
        C_i_CC_UP = np.sum(cj[-4:])
        n1 = 1
        n2 = 1
        # Equation 7 (unit miliseconds)

        dRUpr = C_i_RU_CP / cRUEq[0] + (C_i_RU_UP*const.user) / cRUEq[1]
        dCCpr = C_i_CC_UP / cCCEq[1]


    elif const.split == 16:
        C_i_RU = np.sum(cj)
        C_i_CC = 0
        n1 = 0
        n2 = 1
    else :
        C_i_RU = np.sum(cj[:const.split])
        C_i_CC = np.sum(cj[const.split:])
        n1 = 1
        n2 = 1




    # Equation 6 (unit miliseconds)
    Dpr = n1 * dCCpr + n2 * dRUpr

    # # equation 1 (unit milisecond)
    Dtot = DMtx  + const.Dp1 * 0.001 + DRtx  + Dpr + const.Nsw * (
                const.Dq * 0.001 + const.Df * 0.001 + Dse * 0.001) + \
           const.Dp2 * 0.001 + const.D_w

    # # equation 1 (unit milisecond)
    # Dtot = DMtx * 0.001 + const.Dp1 * 0.001 + DRtx + Dpr + const.Nsw * (const.Dq * 0.001 + const.Df * 0.001 + Dse * 0.001) + \
    #        const.Dp2 * 0.001 + const.D_w
    # equation 1 (unit milisecond) revised
    # Dtot =  DMtx * 0.001 +  const.Dp1 * 0.001 +  DRtx + Dpr * Nslot+  const.Nsw * (const.Dq * 0.001 + const.Df * 0.001 + Dse * 0.001) + \
    #          const.Dp2 * 0.001 + const.D_w

    return dRUpr, dCCpr, Dpr , Dtot, DRtx
    #revised processing equation
    # return dRUpr, dCCpr, Dpr * Nslot, Dtot, DRtx
    #Process delay simulation in process_Delay.py
    # return dCCpr, dRUpr, Dpr
