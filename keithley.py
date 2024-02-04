
import time
import pyvisa
print(pyvisa.__version__)

# pip3 install pyvisa pyvisa-py

'''
Driver installation
- NI-488.2 Version 21.5
	https://www.ni.com/en-us/support/downloads/drivers/download.ni-488-2.html#441749
'''

'''
class keithley():
	def __init__(self, GPIB_ADDR='GPIB0::25::INSTR', rm = []):
		# open a resource manager if none was provided
		if rm == []:
			rm = pyvisa.ResourceManager()
			self = rm.open_resource(GPIB_ADDR)
'''

# SET Keithley for voltage source

'''
import os
os.environ["LD_LIBRARY_PATH"] = '/Library/Frameworks/NI4882.framework/NI4882'
rm = pyvisa.ResourceManager('/Library/Frameworks/NI4882.framework/NI4882')
'''

# rm = pyvisa.ResourceManager() #'/Library/Frameworks/VISA.framework/VISA')
rm = pyvisa.ResourceManager()
print(rm.list_resources())

for resource in rm.list_resources():
    if not 'Bose' in resource:
        print(resource)

print(rm.visalib)
# print(dir(rm))

GPIB_ADDR = 'GPIB0::25::INSTR'
Ksrc = rm.open_resource(GPIB_ADDR)
ID = Ksrc.query('*IDN?')
print("Connected to", ID)

# Ksrc.write(':SOUR:DEL .001')
# Ksrc.write(':OUTP ON')

Ip = 100e-12
I = [Ip, -Ip]
T = 200e-3
I_range = Ip*10

Ksrc.write('*RST')  # Restore GPIB defaults (source V, measure I).
Ksrc.write(':SOUR:FUNC CURR')
Ksrc.write(':SOUR:CURR:RANG ' + str(I_range))
Ksrc.write(':SOUR:CURR:LEV 0E-3')
Ksrc.write(':SENS:VOLT:PROT 3.3')
Ksrc.write(':SENS:FUNC "VOLT"')
Ksrc.write(':SENS:VOLT:RANG 5')
Ksrc.write(':OUTP ON')
#Ksrc.write(':OUTP OFF')

try:
    while(True):
        Ksrc.write(':SOUR:CURR:LEV '+str(I[0]))
        time.sleep(T)
        Ksrc.write(':SOUR:CURR:LEV '+str(I[1]))
        time.sleep(T)
except KeyboardInterrupt:
    Ksrc.write(':SOUR:CURR:LEV 0E-9')
    Ksrc.write(':OUTP OFF')
    print('Current injection stopped. Injected current set to 0nA.')

#Ksrc.write(':SENS:CURR:PROT 50e-3')

# Ksrc.write(':SOUR:CURR:LEV 5e-4') # Set bias level to 0V.
# Ksrc.write(':SENS:FUNC "VOLT"')
# Ksrc.write(':SOUR:DEL 0.1') # Set delay to 100ms.
# Ksrc.write(':SOUR:SWE:RANG BEST') # Select best source ranging.
# Ksrc.write(':SOUR:VOLT:MODE LIST') # Select the list source mode.
# Ksrc.write(':SOUR:LIST:VOLT 1, 0, 1, 0, 1, 0') # Specify source list (1V, 0V, 1V, 0V, 1V and 0V).
#Ksrc.write(':TRIG:COUN 6')
# print(Ksrc.query(':SOUR:LIST:CURR:POIN?'))
# Ksrc.write(':TRIG:COUN 4') # Set trigger count to 6.
# Ksrc.write(':OUTP ON') # ON Turn output on.
# Ksrc.write(':READ?') # Trigger sweep and acquire data.
# Ksrc.write(':INIT')
'''
# rm.close


#startTime = time.time()
'''
