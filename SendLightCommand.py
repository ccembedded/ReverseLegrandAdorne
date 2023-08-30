import time
from rflib import RfCat as rfcat
from rflib import *

freq_list = [904861000, 910811000, 918869000, 922519000, 924873000]
channel_sequence = [2, 5, 4, 3, 5]
#channel_sequence = [2, 1, 4, 3, 1]
light_cmd = b'\x <header><address><function><power level><ramp rate><device type><crc><~crc>'
sync = 0xAA66

d = rfcat()

d.setMdmNumPreamble(preamble=MFMCFG1_NUM_PREAMBLE_4)
d.setMdmSyncWord(sync)
d.setMdmModulation(MOD_GFSK)
d.makePktFLEN(10)
d.setEnableMdmManchester(enable=True)

# Symbol rate bit is half of below since it is Manchester encoded
d.setMdmDRate(19200)
d.setMdmDeviatn(30500)

d.setMaxPower()

d.printRadioConfig()

for c in channel_sequence:
    print(f'Frequency: {freq_list[c-1]}')
    d.setModeIDLE()
    d.setFreq(freq_list[c-1])
    d.RFxmit(light_cmd)

d.setModeIDLE()
print('Exiting')

