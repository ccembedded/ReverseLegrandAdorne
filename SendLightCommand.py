import time
from rflib import RfCat as rfcat
from rflib import *

freq_list = [904861000, 910811000, 918869000, 922519000, 924873000]
light_cmd = b'\x'
sync = 0xAA66

d = rfcat()

d.setMdmNumPreamble(preamble=MFMCFG1_NUM_PREAMBLE_4)
d.setMdmSyncMode(SYNCM_CARRIER_16_of_16)
d.setMdmSyncWord(sync)
d.setMdmModulation(MOD_GFSK)
d.makePktFLEN(10)
d.setEnableMdmManchester(enable=True)

# Symbol rate bit is half of below since it is Manchester encoded
d.setMdmDRate(19200)
d.setMdmDeviatn(30500)

d.setMaxPower()
d.setEnableMdmDCFilter(True)

d.calculatePktChanBW()
d.printRadioConfig()

for f in freq_list:
    print(f'Frequency: {f}')
    d.setModeIDLE()
    d.setFreq(f)
    d.calculatePktChanBW()
    d.RFxmit(light_cmd)

d.setModeIDLE()
print('Exiting')

