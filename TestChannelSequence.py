import time
from rflib import RfCat as rfcat
from rflib import *
import socket
import json
from itertools import combinations


def getLightPower():
    # LCM message
    m = {"ID": 12345, "Service": "ReportZoneProperties", "ZID": 1}

    msg = json.dumps(m)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('<LCM address>', 2112))

    data = s.recv(1024)

    s.sendall(bytes(msg, encoding="utf-8"))
    s.sendall(bytes('\0', encoding="utf-8"))

    data = s.recv(1024)

    # Remove null byte
    data = data[:-1]

    status = data.decode('utf-8')

    status_json = json.loads(status)

    property_list = status_json['PropertyList']
    light_power = property_list['Power']

    s.close()

    return light_power


freq_list = [904861000, 910811000, 918869000, 922519000, 924873000]

channel_sequence = [2, 5, 4, 3, 5]
#channel_sequence = [2, 1, 4, 3, 1]

channel_sequence_comb = list()
for n in range(len(channel_sequence) + 1):
    channel_sequence_comb += list(combinations(channel_sequence, n))

# Light
light_cmd_off = b'\x <header><address><function><power level><ramp rate><device type><crc><~crc>'
light_cmd_on = b'\x <header><address><function><power level><ramp rate><device type><crc><~crc>'

sync = 0xAA66
d = rfcat()

d.setMdmNumPreamble(preamble=MFMCFG1_NUM_PREAMBLE_4)
d.setMdmSyncWord(sync)
d.setMdmModulation(MOD_GFSK)
d.makePktFLEN(10)
d.setEnableMdmManchester(enable=True)

#Symbol rate bit is half of below since it is Manchester encoded
d.setMdmDRate(19200)

d.setMdmDeviatn(30500)
d.setMaxPower()
d.printRadioConfig()


ON = 1
OFF = 0
expected_light_state = OFF

pass_list = list()
fail_list = list()

for seq in channel_sequence_comb:
    light_power = getLightPower()

    print(light_power)
    if light_power == True:
        # Light is currently ON set to OFF
        expected_light_state = OFF
        light_cmd = light_cmd_off
    else:
        # Light is currently OFF set to ON
        expected_light_state = ON
        light_cmd = light_cmd_on

    for c in seq:
        d.setModeIDLE()
        d.setFreq(freq_list[c-1])
        d.RFxmit(light_cmd)

    light_power = getLightPower()

    if light_power == True:
        # Light is ON
        if expected_light_state == ON:
            pass_list.append(seq)
        else:
            fail_list.append(seq)
    else:
        # Light is OFF
        if expected_light_state == OFF:
            pass_list.append(seq)
        else:
            fail_list.append(seq)

    # Prevent LCM from giving us an error
    time.sleep(1)

d.setModeIDLE()

print("Channel Sequences that work:")
print(pass_list)

print("\nChannel Sequences that fail:")
print(fail_list)

print('Exiting')





