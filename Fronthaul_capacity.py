from Delay_Model import Fronthaul_bit_rate_calculater
import numpy as np
import math
import matplotlib.pyplot as plt
from Constants import Constants
from frame import Frame


const= Constants()
bandwidth =20
numerology=0
frame = Frame(numerology, True, bandwidth)


n_subcar_max = 12 * frame.max_prb_count

print(frame.slot_in_subframe_count)



C_percent = 0.3



delay = np.zeros(4)



bitwidth = 32
delay[0] = Fronthaul_bit_rate_calculater(n_subcar_max, frame,const,bitwidth)/1000000
bitwidth = 8
delay[1] = Fronthaul_bit_rate_calculater(n_subcar_max, frame,const,bitwidth)/1000000
bitwidth = 6
delay[2] = Fronthaul_bit_rate_calculater(n_subcar_max, frame,const,bitwidth)/1000000
bitwidth = 4
delay[3] = Fronthaul_bit_rate_calculater(n_subcar_max, frame,const,bitwidth)/1000000
print(delay)
x= ['No compression', '256QAM','64QAM','16QAM']
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, delay, color='r')
major_ticks = np.arange(0, 601, 50)
ax.set_yticks(major_ticks)
# ax.grid(which='minor', alpha=0.1)
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

# plt.grid()
plt.ylabel('Fronthaul capcity Mbps')
plt.title('Calculated required fronthaul capacity for 20Mhz channel and numerology 0')
# plt.legend((p1[0], p2[0], p3[0]), ('Delay in RAN', 'Processing Delay', 'Delay in fronthaul'))
plt.show()