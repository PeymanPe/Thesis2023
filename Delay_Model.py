import numpy as np
from frame import Frame
import math





# required bitrate for fronthaul unit: Mbps
def Fronthaul_bit_rate_calculater(Nsc, frame,const,bitwidth):
    SampleRate = frame.sample_rate
    Ts = frame.symbol_duration
    if const.split == 'IID': #splitting at II_D (unit Mbps)
        # fronthaul_bitrate = Nsc * 0.9 * 2 * const.bits_per_sample * const.antennas_per_ru * const.prb_usage / Ts
        fronthaul_bitrate = Nsc * frame.slot_in_subframe_count * frame.symbol_per_slot *bitwidth*1000
    elif const.split == 'E': # splitting at E

        # fs=1/Ts
        fs = SampleRate
        # fs =1.536*BW
        fronthaul_bitrate = fs * 2 * const.bits_per_sample * const.antennas_per_ru
    elif const.split ==15:
        fronthaul_bitrate = 151
    return fronthaul_bitrate




#return in ms unit
def Total_Delay_Calculator(const, Nsc, frame, cj, cRUEq, cCCEq):

    Tslot = frame.slot_duration


    SampleRate = frame.sample_rate

    # switching delay (unit:microsecond)
    Dse = const.packet_size_bits / const.switch_bit_rate
    if(const.modulation_compression == False):
        bitwidth = 32
    else:
        if(const.modulation_index == 8):
            bitwidth=8
        elif(const.modulation_index == 6):
            bitwidth =6
        elif(const.modulation_index == 4):
            bitwidth = 4




    # required bitrate for fronthaul
    # Nsc = nprb * 12
    #sample duration time
    # Ts = Tslot/const.nsymbol
    ##to be more accurate (micro seconds)
    Ts = frame.symbol_duration

    # MHbitRate1 = Fronthaul_bit_rate_calculater(Nsc, Ts, const, SampleRate)
    MHbitRate1 = Fronthaul_bit_rate_calculater(Nsc, frame, const,bitwidth)

    # MHbitRate1 = MHbitRate(Nsc, Ts, nn, split,Nant,nmod)
    # queuing delay
    EP = const.packet_size_bits/MHbitRate1
    L_phi = Nsc * const.modulation_index * 1.04
    ro = EP * L_phi/const.packet_size_bits
    kk = ro/(1-ro)
    # zz = math.log(kk)/math.log(math.e)

    # DD = max(0,kk*zz)

    # print(MHbitRate1)



    # print(DMtx)

    Nsc_user = math.floor(Nsc/const.user_count)

    nprb = Nsc/12



    Nslot = math.ceil(const.file_size*1000 / (Nsc_user * const.modulation_index * const.nsymbol))



    # equation 4 (unit:milisecond)
    DRtx = Nslot * Tslot
    # Transmission delay (unit:microsecond)
    file_size_per_subframe = math.ceil(const.file_size *frame.slot_in_subframe_count / Nslot )
    # print(math.ceil(file_size_per_slot / (MHbitRate1*frame.symbol_duration))*frame.symbol_duration*0.001)
    DMtx = math.ceil(file_size_per_subframe / (MHbitRate1*frame.symbol_duration))*frame.symbol_duration*0.001
    #equation 23 (unit giga operation per radio subframe
    #we have 16 total number of CP and UP functions
    if const.split == 'E': #splitting at E
        C_i_RU = 0
        C_i_CC_CP = np.sum(cj[:11])+cj[-2]
        C_i_CC_UP = np.sum(cj[11:-2])+cj[-1]
        f = 2.3 *1000
        Tss=(1/f)
        dRUpr = 0
        dCCpr = math.ceil(C_i_CC_CP * f*Tslot*frame.slot_in_subframe_count / cCCEq[0]) * (Tss) + math.ceil(C_i_CC_UP * f *Tslot*frame.slot_in_subframe_count/ cCCEq[1])* (Tss)


        n2 = 0
        n1 = 1

    elif const.split == 'IID': #spliting for II_D
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





    elif const.split == 'ID':
        C_i_RU_CP = np.sum(cj[:11])
        C_i_RU_UP = cj[11]
        C_i_CC_UP = np.sum(cj[-4:])
        n1 = 1
        n2 = 1
        # Equation 7 (unit miliseconds)

        dRUpr = C_i_RU_CP / cRUEq[0] + (C_i_RU_UP*const.user_count) / cRUEq[1]
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
    Delay_process = n1 * dCCpr + n2 * dRUpr
    print(Delay_process)

    # # equation 1 (unit milisecond)
    Delay_total = DMtx  + const.propagation_delay_fronthaul * 0.001 + DRtx  + Delay_process + const.switch_count * (
                const.queue_delay * 0.001 + const.delay_fabric * 0.001 + Dse * 0.001) + \
           const.propagation_delay_RAN * 0.001 + const.slice_instantiation_delay
    Delay_fronthaul= const.propagation_delay_fronthaul* 0.001 + DMtx + const.switch_count * (
                const.queue_delay * 0.001 + const.delay_fabric * 0.001 + Dse * 0.001)

    # # equation 1 (unit milisecond)
    # Dtot = DMtx * 0.001 + const.Dp1 * 0.001 + DRtx + Dpr + const.Nsw * (const.Dq * 0.001 + const.Df * 0.001 + Dse * 0.001) + \
    #        const.Dp2 * 0.001 + const.D_w
    # equation 1 (unit milisecond) revised
    # Dtot =  DMtx * 0.001 +  const.Dp1 * 0.001 +  DRtx + Dpr * Nslot+  const.Nsw * (const.Dq * 0.001 + const.Df * 0.001 + Dse * 0.001) + \
    #          const.Dp2 * 0.001 + const.D_w

    return dRUpr, dCCpr, Delay_process , Delay_total, DRtx, Delay_fronthaul
    #revised processing equation
    # return dRUpr, dCCpr, Dpr * Nslot, Dtot, DRtx
    #Process delay simulation in process_Delay.py
    # return dCCpr, dRUpr, Dpr
