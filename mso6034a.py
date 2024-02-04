'''
If rm.list_resources() doesn't see the scope, check the I/O settings on the scope:
	- Make sure USB/LAN is connected
	- Utility / I/O / Control: set this to match the cable used (USB in this case)

If trouble persists, maybe we could look in pyvisa's backend?
	pyvisa can use different backends, including NI-VISA, Keysight VISA, etc:
	It might not be necessary to configure the backend, but just in case:
		https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html
	(this also includes a link to installing NI-VISA)

Keysight has some programming examples in python available:
	https://www.keysight.com/us/en/support/MSO6034A/mixed-signal-oscilloscope-300-mhz-4-analog-16-digital-channels.html?&cc=US&lc=eng#drivers
	(These just use the default backend, so Keysight VISA shouldn't be necessary)

The programmer's guide is here:
	https://www.keysight.com/us/en/assets/9018-08107/programming-guides/9018-08107.pdf?success=true
'''

import pyvisa

# Select a VISA backend if needed
rm = pyvisa.ResourceManager()
#rm = pyvisa.ResourceManager('@py')

# List all availabke connections
for resource in rm.list_resources():
	#if not 'Bose' in resource:
	print(resource)

# Connect to MSO6034A
INSTR_ADDR = 'USB0::0x0957::0x1734::MY44003833::INSTR' # might need to update this address

scope = rm.open_resource(INSTR_ADDR)
ID = scope.query('*IDN?')
print("Connected to", ID)


####################################
# User settings
####################################
ch = 3 # select the channel used

# Display
OFFSET_V = .8
VDIV_V = 0.100
V_RANGE_V = VDIV_V * 8
T_RANGE_s = 0.1 # will get split into 10 divisions

# Trigger
TRIG_LEVEL_V = 1

####################################
# Display settings
####################################
# Turn the channel display ON
scope.write(f":CHANnel{ch}:DISPlay ON")

# Verify its ON
chDisp = scope.query(f":CHANnel{ch}:DISPlay?")
print(f'Is ch{ch} displayed? {chDisp}')

# Set vertical (voltage) range and offset
scope.write(f":CHANNEL{ch}:RANGE {V_RANGE_V} V")
scope.write(f":CHANNEL{ch}:OFFSET {OFFSET_V} V")

# Set horizontal (time) divisions
scope.write(f":TIMEBASE:RANGE {T_RANGE_s}")


####################################
# Probe settings
####################################
# Set to be Hi-Z
scope.write(f":CHANNEL{ch}:IMP ONEMEG")

# DC coupling
scope.write(f":CHANNEL{ch}:COUP DC")


####################################
# Acquisition settings
####################################
# Set to be hires
scope.write(f":ACQ:TYPE HRES") # does averaging


####################################
# Trigger settings
####################################
# Edge trigger on selected channel
scope.write(f":TRIG:MODE EDGE")
scope.write(f":TRIG:EDGE:SOURCE {ch}")
scope.write(f":TRIG:EDGE:LEVEL {TRIG_LEVEL_V} V")


####################################
# Measurements
####################################
Vmax = scope.query(f":MEAS:VMAX? CHANNEL{ch}")
Vmin = scope.query(f":MEAS:VMIN? CHANNEL{ch}")
Vpp = scope.query(f":MEAS:VPP? CHANNEL{ch}")
trise = scope.query(f":MEAS:RISETIME? CHANNEL{ch}")
tfall = scope.query(f":MEAS:FALLTIME? CHANNEL{ch}")
print('Vmax', Vmax)
print('Vmin', Vmin)
print('Vpp', Vpp)
print('tr', trise)
print('tf', tfall)

# Set time/voltage scales
# Set trigger
# Set measurements
# Acquire data
# Save screenshot