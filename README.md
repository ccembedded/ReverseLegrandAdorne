# Background
Due to the Adorne RF switches being discontinued by Legrand and wanting to be able to expand my lighting system in the future, I decided to reverse engineer the RF portion.

# Hardware
The RF portion of the system uses the TI CC1110 chip.

# RF Info
As per the FCC test reports

Operating frequencies: 904.861-924.873 MHz
<br>
Modulation: FSK Synchronous Manchester Encoded
<br>
Channels: 5

Three of the channels are listed in the report
<br>
Low: 904.861 MHz
<br>
Mid: 918.869 MHz
<br>
High: 924.873 MHz

Channel seperation is also listed in the report which can be used to calculate the rest of the frequencies.
<br>
1: 904.861 MHz
<br>
2: 910.811 MHz
<br>
3: 918.869 MHz
<br>
4: 922.519 MHz
<br>
5: 924.873 MHz

# Process
Recorded an RF transmission using gqrx and an RTL-SDR.  The transmission was decoded using inspecturm.  Several more transmissions were captured from different switches to verify decoding was correct.  Used RfCat and a TI CC1111 dongle to capture all transmissions from the lighting system.  Tried to send a light on/off command using RfCat on only 924.873 MHz, but this did not work to control the switches.

As per SP-adorneGuideFo-AD.pdf


![Alt text](images/guide.png))

I don't see anything in the TI CC1110 datasheet that would allow it to transmit on multiple frequencies simultaneously so I tried transmitting the same light on/off command with RfCat on each channel sequentially.  This also did not work to control the light switches.  Either the settings on the TI CC1111 are wrong or there is a frequency hopping sequence.

The RTL-SDR did not have enough bandwidth to look at all channels simultaneously so I picked up a HackRF One.  Recorded the signal with gqrx, center frequency = 914.850 MHz.

![Alt text](images/pattern_channel.png))

I had to remove the scale so channel 5 would be visible.  With scales turned on

![Alt text](images/pattern_scales.png))

This is the pattern that seems to repeat.  There are some other patterns that are a little different, but that could be from interference.  Channel 1 and channel 5 transmitting at the same time seems weird.


# To do
- Check CC1110 manual again to see if there is a way to transmit on channel 1 and channel 5 simultaneously.
- Decode some of the different patterns to verify if they are valid or caused by interference.
- Try transmitting channel sequence 2, 5, 4, 3, 5 and 2, 1, 4, 3, 1 with RfCat.

