from rflib import RfCat as rfcat
from rflib import *
from binascii import hexlify

def tryDecodingHeader(header):
    family_type = 0
    address_mode = 0
    retx_delay = 0
    ttl = 0
    
    valid_families = [0x1, 0x4, 0x6] # F1, CADIR, F2
    valid_addr_mode = [0x0, 0x1, 0x2, 0x3] # broadcast, anon_multicast, unicast, multicast
    valid_delay = [0x0, 0x1]
    valid_ttl = [0x0, 0x1, 0x2, 0x3]

    family_type = (header & 0xe0) >> 5
    address_mode = (header & 0x18) >> 3
    retx_delay = (header & 0x4) >> 2
    ttl = (header & 0x3)

    if family_type in valid_families:
        if address_mode in valid_addr_mode:
            if retx_delay in valid_delay:
                if ttl in valid_ttl:
                    print("VALID HEADER")
                    print(f'Family: {hex(family_type)}  Address Mode: {hex(address_mode)}  ReTx Delay: {hex(retx_delay)}  TTL: {hex(ttl)}')
                    return True


def tryDecodingFrame(frame):
    buildingID = 0
    houseID = 0
    groupID = 0
    roomID = 0
    preset = 0
    command = 0
    crc = 0
    ncrc = 0
    power_level = 0
    ramp_rate = 0
    device_type = 0
    header = frame[0]

    tryDecodingHeader(header)

    if(frame[0] == 0xCA):
        if(frame[2] & 0x10 == 0):
            # Group ID
            buildingID = (frame[1] & 0xe0) >> 5
            houseID = (frame[1] & 0x1f) << 3
            houseID |= (frame[2] & 0xe0) >> 5
            groupID = (frame[2] & 0x0f) << 16
            groupID |= frame[3]

        command = frame[4]
        if(command == 0x85):
            # need to add computing the crc
            # for now check that crc == ~(~crc)
            crc = frame[8]
            ncrc = frame[9]
            test_crc = ncrc ^ 0xFF
            if(crc == test_crc):
                print("CRC GOOD")

            power_level = frame[5]
            ramp_rate = frame[6]
            device_type = frame[7]

            print(f'Building ID: {hex(buildingID)}  House ID: {hex(houseID)}  Group ID: {hex(groupID)}')
            print(f'Command: {hex(command)}  Power Level: {hex(power_level)}  Ramp Rate: {hex(ramp_rate)}  Device Type: {hex(device_type)}')
    #else:
        # RoomID
    #    buildingID = (frame[1] & 0xe0) >> 5
    #    houseID = (frame[1] & 0x1f) << 3
    #    houseID |= (frame[2] & 0xe0) >> 5

        # from the LCM source code roomID seems to only take the 3 upper bits
        # and 3 lower bits?
        # address diagram shows houseID is 7 bits?
        # below is as per diagram
    #    roomID = (frame[2] & 0x0f) << 3
    #    roomID |= (frame[3] & 0xe0) >> 4
    #    preset = (frame[3] & 0x1f)
    #    command = frame[4] # not sure if this is actually a command
        # still not completely sure what this command is
        # seems to be a broadcast from each switch
    #    if(command == 0xcf):
    #        hID = 0
    #        crc = frame[13]
    #        ncrc = frame[14]
    #        test_crc = ncrc ^ 0xFF
    #        if(crc == test_crc):
    #            print("CRC GOOD")

            # everything I've managed to decode so far
    #        device_type = frame[5]

            # for some reason group ID has the lower 3 bits of houseID (byte 1 and 2 of address in BuildRamp())
            # or this could be buildID | groupID since byte 8 is houseID?
    #        groupID = frame[6] << 16
    #        groupID |= frame[7]
    #        hID = frame[8]

            # no idea what byte 9 to 12 is
            # from the watt stopper patent this might be the source MAC address

frames = []
prev_val = 0
val = 0x85
sync = 0xAA66

d = rfcat()
last_cfg = d.getRadioConfig()

d.setEnableMdmManchester(enable=True)
d.setFreq(924873000)
d.setMdmNumPreamble(preamble=MFMCFG1_NUM_PREAMBLE_4)
d.setMdmSyncWord(sync)
d.setMdmModulation(MOD_GFSK)
d.setMdmDRate(19200)
d.setMdmSyncMode(SYNCM_CARRIER_16_of_16)
d.makePktFLEN(16)
# works between 10000 and 40000
d.setMdmDeviatn(30000)
d.calculatePktChanBW()

d.printRadioConfig()


while not keystop():
    try:
        y,t = d.RFrecv()
        yhex = hexlify(y).decode()
        print(yhex)
        # If frame is repeated twice there good chance it is a frame we want
        header = y[0]
        if((prev_val == yhex) or (tryDecodingHeader(header))):
            if(y not in frames):
                # Add frame only if it hasen't already been added
                frames.append(y)
                print("Frame Added\n")

        prev_val = yhex
    except ChipconUsbTimeoutException:
        pass

d.setModeIDLE()

for f in frames:
    print(hexlify(f).decode())
    tryDecodingFrame(f)
    print("\n")


d.setRadioConfig(last_cfg)

print('Exiting')





