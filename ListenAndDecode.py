from rflib import RfCat as rfcat
from rflib import *
from binascii import hexlify

# table from crccalc.com
crc_table = [
    0x00, 0x5e, 0xbc, 0xe2, 0x61, 0x3f, 0xdd, 0x83,
    0xc2, 0x9c, 0x7e, 0x20, 0xa3, 0xfd, 0x1f, 0x41,
    0x9d, 0xc3, 0x21, 0x7f, 0xfc, 0xa2, 0x40, 0x1e,
    0x5f, 0x01, 0xe3, 0xbd, 0x3e, 0x60, 0x82, 0xdc,
    0x23, 0x7d, 0x9f, 0xc1, 0x42, 0x1c, 0xfe, 0xa0,
    0xe1, 0xbf, 0x5d, 0x03, 0x80, 0xde, 0x3c, 0x62,
    0xbe, 0xe0, 0x02, 0x5c, 0xdf, 0x81, 0x63, 0x3d,
    0x7c, 0x22, 0xc0, 0x9e, 0x1d, 0x43, 0xa1, 0xff,
    0x46, 0x18, 0xfa, 0xa4, 0x27, 0x79, 0x9b, 0xc5,
    0x84, 0xda, 0x38, 0x66, 0xe5, 0xbb, 0x59, 0x07,
    0xdb, 0x85, 0x67, 0x39, 0xba, 0xe4, 0x06, 0x58,
    0x19, 0x47, 0xa5, 0xfb, 0x78, 0x26, 0xc4, 0x9a,
    0x65, 0x3b, 0xd9, 0x87, 0x04, 0x5a, 0xb8, 0xe6,
    0xa7, 0xf9, 0x1b, 0x45, 0xc6, 0x98, 0x7a, 0x24,
    0xf8, 0xa6, 0x44, 0x1a, 0x99, 0xc7, 0x25, 0x7b,
    0x3a, 0x64, 0x86, 0xd8, 0x5b, 0x05, 0xe7, 0xb9,
    0x8c, 0xd2, 0x30, 0x6e, 0xed, 0xb3, 0x51, 0x0f,
    0x4e, 0x10, 0xf2, 0xac, 0x2f, 0x71, 0x93, 0xcd,
    0x11, 0x4f, 0xad, 0xf3, 0x70, 0x2e, 0xcc, 0x92,
    0xd3, 0x8d, 0x6f, 0x31, 0xb2, 0xec, 0x0e, 0x50,
    0xaf, 0xf1, 0x13, 0x4d, 0xce, 0x90, 0x72, 0x2c,
    0x6d, 0x33, 0xd1, 0x8f, 0x0c, 0x52, 0xb0, 0xee,
    0x32, 0x6c, 0x8e, 0xd0, 0x53, 0x0d, 0xef, 0xb1,
    0xf0, 0xae, 0x4c, 0x12, 0x91, 0xcf, 0x2d, 0x73,
    0xca, 0x94, 0x76, 0x28, 0xab, 0xf5, 0x17, 0x49,
    0x08, 0x56, 0xb4, 0xea, 0x69, 0x37, 0xd5, 0x8b,
    0x57, 0x09, 0xeb, 0xb5, 0x36, 0x68, 0x8a, 0xd4,
    0x95, 0xcb, 0x29, 0x77, 0xf4, 0xaa, 0x48, 0x16,
    0xe9, 0xb7, 0x55, 0x0b, 0x88, 0xd6, 0x34, 0x6a,
    0x2b, 0x75, 0x97, 0xc9, 0x4a, 0x14, 0xf6, 0xa8,
    0x74, 0x2a, 0xc8, 0x96, 0x15, 0x4b, 0xa9, 0xf7,
    0xb6, 0xe8, 0x0a, 0x54, 0xd7, 0x89, 0x6b, 0x35
]

def computeCrc(message):
    crc = 0

    for b in message:
        crc = crc_table[crc ^ b]

    return crc

def isCrcValid(message, crc, ncrc = -1):
    computed_crc = 0
    valid_crc = False

    computed_crc = computeCrc(message)
    #print(f'MESSAGE: {hex(message)}')
    #print(f'CRC: {hex(crc)}  NCRC: {hex(ncrc)}  COMPUTED CRC: {hex(computed_crc)}')

    if ncrc >= 0:
        if crc == computed_crc and ncrc == (computed_crc ^ 0xff):
            valid_crc = True
        else:
            valid_crc = False
    else:
        if crc == computed_crc:
            valid_crc = True
        else:
            valid_crc = False

    return valid_crc


TOPDOG_F1 = 0x0
TOPDOG_CADIR = 0x4
TOPDOG_F2 = 0x6

BROADCAST = 0x0
ANON_MULTICAST = 0x1
UNICAST = 0x2
MULTICAST = 0x3

SHORT_RANDOM_TIME = 0x0
LONG_RANDOM_TIME = 0x1

HEADER_FAMILY_TYPE = 0x0
HEADER_ADDRESS_MODE = 0x1
HEADER_RETX_DELAY = 0x2
HEADER_TTL = 0x3


family_dict = {
    TOPDOG_F1 : "TopDog F1",
    TOPDOG_CADIR : "TopDog CADIR",
    TOPDOG_F2 : "TopDog F2"
}

address_type_dict = {
    BROADCAST : "Broadcast",
    ANON_MULTICAST  : "Anonymous Multicast",
    UNICAST : "Unicast",
    MULTICAST : "Multicast"
}

retx_delay_dict = {
    SHORT_RANDOM_TIME : "Short Random Time",
    LONG_RANDOM_TIME : "Long Random Time"
}

def getHeaderData(header):
    family_type = 0
    address_mode = 0
    retx_delay = 0
    ttl = 0
    data = list()

    family_type = (header & 0xe0) >> 5
    address_mode = (header & 0x18) >> 3
    retx_delay = (header & 0x4) >> 2
    ttl = (header & 0x3)
    data.append(family_type)
    data.append(address_mode)
    data.append(retx_delay)
    data.append(ttl)

    return data


def isHeaderValid(header_data):
    family_type = 0
    address_mode = 0
    retx_delay = 0
    ttl = 0
    valid_header = False

    valid_families = [TOPDOG_F1, TOPDOG_CADIR, TOPDOG_F2] # F1, CADIR, F2
    valid_addr_mode = [BROADCAST, ANON_MULTICAST, UNICAST, MULTICAST] # broadcast, anon_multicast, unicast, multicast
    valid_delay = [SHORT_RANDOM_TIME, LONG_RANDOM_TIME]
    valid_ttl = [0x0, 0x1, 0x2, 0x3]

    family_type = header_data[HEADER_FAMILY_TYPE]
    address_mode = header_data[HEADER_ADDRESS_MODE]
    retx_delay = header_data[HEADER_RETX_DELAY]
    ttl = header_data[HEADER_TTL]

    if family_type in valid_families:
        if address_mode in valid_addr_mode:
            if retx_delay in valid_delay:
                if ttl in valid_ttl:
                    valid_header = True
    return valid_header

def printHeaderData(header_data):
    family_type = header_data[HEADER_FAMILY_TYPE]
    address_mode = header_data[HEADER_ADDRESS_MODE]
    retx_delay = header_data[HEADER_RETX_DELAY]
    ttl = header_data[HEADER_TTL]

    print(f'Family: {family_dict[family_type]} {hex(family_type)}\nAddress Mode: {address_type_dict[address_mode]} {hex(address_mode)}\nReTx Delay: {retx_delay_dict[retx_delay]} {hex(retx_delay)}\nTTL: {hex(ttl)}')


RAMP = 0x05
BINDING_REPLY = 0x0f
OPEN_BINDING = 0x3013
CLOSE_BINDING = 0x3014

COMMAND_START_BYTE = 0x4

command_dict = {
    RAMP : "Ramp",
    BINDING_REPLY : "Binding Reply",
    OPEN_BINDING : "Open Binding",
    CLOSE_BINDING : "Close Binding"
}

def getCommand(frame):
    COMMAND_SIZE_MASK = 0xc0
    ONE_BYTE = 0x0
    TWO_BYTES = 0x1
    FOUR_BYTES = 0x2
    SIX_BYTES = 0x3

    command = frame[COMMAND_START_BYTE]
    # Command size includes the number of command bytes
    command_size = (command & COMMAND_SIZE_MASK) >> 6
    if command_size == ONE_BYTE:
        command_size = 1
    elif command_size == TWO_BYTES:
        command_size = 2
    elif command_size == FOUR_BYTES:
        command_size = 4
    elif command_size == SIX_BYTES:
        command_size = 6
    #else:
        # error

    command &= frame[COMMAND_START_BYTE] & (COMMAND_SIZE_MASK ^ 0xff)
    if command >= 0x30:
        command = command << 8
        command |= frame[COMMAND_START_BYTE + 1]

    return command, command_size


def printGroupAddress(building, house, group):
    print(f'Building ID: {hex(building)}\nHouse ID: {hex(house)}\nGroup ID: {hex(group)}')

def printRoomAddress(building, house, room, preset):
    print(f'Building ID: {hex(building)}\nHouse ID: {hex(house)}\nRoom ID: {hex(room)}\nPreset: {hex(preset)}')



def decodeFrame(frame):
    buildingID = 0
    houseID = 0
    groupID = 0
    roomID = 0
    preset = 0
    command = 0
    mac_address = 0
    crc = 0
    ncrc = 0
    power_level = 0
    ramp_rate = 0
    device_type = 0
    header = frame[0]
    header_data = list()
    valid_crc = False
    crc_index = 0

    header_data = getHeaderData(header)

    printHeaderData(header_data)

    command, command_size = getCommand(frame)

    address_type = header_data[HEADER_ADDRESS_MODE]
    family_type = header_data[HEADER_FAMILY_TYPE]


    crc_index = COMMAND_START_BYTE + command_size
    if address_type == MULTICAST:
        # Source MAC address at end of COMMAND_START + size
        crc_index += 3
    if family_type == TOPDOG_F2 or family_type == TOPDOG_CADIR:
        crc = frame[crc_index]
        ncrc = frame[crc_index + 1]
        valid_crc = isCrcValid(frame[0:crc_index], crc, ncrc)
    else:
        crc = frame[crc_index]
        valid_crc = isCrcValid(frame[0:crc_index], crc)

    if valid_crc == True:
        print("CRC: Valid")
    else:
        print("CRC: Invalid")

    ROOM_GROUP_MASK = 0x10
    GROUP = 0
    ROOM = 1
    room_group = frame[2] & ROOM_GROUP_MASK

    # Destination address
    if address_type == MULTICAST or address_type == ANON_MULTICAST:
        if(room_group == GROUP):
            # Group ID
            buildingID = (frame[1] & 0xe0) >> 5
            houseID = (frame[1] & 0x1f) << 3
            houseID |= (frame[2] & 0xe0) >> 5
            groupID = (frame[2] & 0x0f) << 8
            groupID |= frame[3]
            printGroupAddress(buildingID, houseID, groupID)
        else:
            # Room ID
            buildingID = (frame[1] & 0xe0) >> 5
            houseID = (frame[1] & 0x1f) << 3
            houseID |= (frame[2] & 0xe0) >> 5
            roomID = (frame[2] & 0x0f) << 3
            roomID |= (frame[3] & 0xe0)
            preset = frame[3] & 0x1f
            printRoomAddress(buildingID, houseID, roomID, preset)

    # Source address
    if address_type == MULTICAST:
        mac_address = 0
        for i in range(3):
            index = COMMAND_START_BYTE + command_size + i
            shift = 16 - (8 * i)
            mac_address |= frame[index] << shift

    print(f'Command: {command_dict[command]} {hex(command)}')

    if command == RAMP:
        power_level = frame[5]
        ramp_rate = frame[6]
        device_type = frame[7]

        print(f'\nCommand Data:')
        print(f'Power Level: {hex(power_level)}\nRamp Rate: {hex(ramp_rate)}\nDevice Type: {hex(device_type)}')

    elif command == BINDING_REPLY:
        device_type = frame[5]
        
        data_build_id = (frame[6] & 0xe0) >> 5
        data_room_group = (frame[6] & 0x10) >> 4

        if data_room_group == GROUP:
            data_group_id = (frame[6] & 0x0f) << 8
            data_group_id |= frame[7]
        else:
            data_room_id = (frame[6] & 0x0f) << 3
            data_room_id |= (frame[7] & 0xe0)
            data_preset = (frame[7] & 0x01) << 4
            data_preset |= frame[7] & 0x0f

        data_house_id = frame[8]

        print(f'\nCommand Data:')
        if data_room_group == GROUP:
            printGroupAddress(data_build_id, data_house_id, data_group_id)
        else:
            printRoomAddress(data_build_id, data_house_id, data_room_id, data_preset)

        print(f'\nSource Address:')
        print(f'MAC: {hex(mac_address)}')

    elif command == OPEN_BINDING or command == CLOSE_BINDING:
        print(f'\nSource Address:')
        print(f'MAC: {hex(mac_address)}')






frames = []
prev_val = 0
val = 0x85
sync = 0xAA66

d = rfcat()
last_cfg = d.getRadioConfig()
#d.setModeIDLE()
d.setEnableMdmManchester(enable=True)

d.setFreq(918860000)
#d.setFreq(924870000)

d.setMdmNumPreamble(preamble=MFMCFG1_NUM_PREAMBLE_4)
d.setMdmSyncWord(sync)
d.setMdmModulation(MOD_GFSK)



#d.setMdmChanBW(62500)
#d.setMdmChanBW(75000)
#d.setMdmDRate(19171)
d.setMdmDRate(19200)
#d.setMdmSyncMode(SYNCM_16_of_16)
d.setMdmSyncMode(SYNCM_CARRIER_16_of_16)
d.makePktFLEN(16)
#d.makePktFLEN(RF_MAX_TX_BLOCK)
#d.setMdmDeviatn(30000)
# works between 10000 and 40000
d.setMdmDeviatn(30000)
d.calculatePktChanBW()

d.printRadioConfig()
#d.discover(SyncWordMatchList=sync, length=16, Search=val)



while not keystop():
    try:
        f,t = d.RFrecv()
        fhex = hexlify(f).decode()
        print(fhex)
        print(t)
        # if frame is repeated twice
        # good chance it is a frame we want
        header = f[0]
        header_data = getHeaderData(header)
        header_valid = isHeaderValid(header_data)
        if prev_val == fhex or header_valid is True:
            decodeFrame(f)
            if f not in frames:
                # Add frame if only if we haven't already added
                frames.append(f)
                print("Frame Added\n")

        prev_val = fhex
    except ChipconUsbTimeoutException:
        pass

d.setModeIDLE()

for f in frames:
    print(hexlify(f).decode())
    decodeFrame(f)
    print("\n")

d.setRadioConfig(last_cfg)

print('Exiting')
