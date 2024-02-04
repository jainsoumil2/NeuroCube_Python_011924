# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 13:35:06 2021

@author: isnl
"""

#%% initialize oscilloscope
# SET Agilent scope for measurements

rm = pyvisa.ResourceManager()
rm.close

#my_Scope = rm.open_resource('TCPIP0::172.16.25.245::inst0::INSTR')# Agilent scope
#my_Scope = rm.open_resource('TCPIP0::a-d6034a-003719::INSTR ')
my_Scope = rm.open_resource('USB0::0x0957::0x1734::MY44003718::0::INSTR')   # Agilent scope
#my_Scope = rm.open_resource('GPIB0::7::INSTR')# Agilent Scope

my_Scope.write('*RST')
my_Scope.write(':TIMEBASE:MODE MAIN')
#my_Scope.write(':ACQUIRE:TYPE NORM')
my_Scope.write(':ACQUIRE:TYPE HRES')
my_Scope.write(':WAV:POINTS:MODE RAW')
my_Scope.write(':WAV:POINTS MAXimum')
my_Scope.write(':TIMebase:RANGe 1E0')         # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.
my_Scope.query(':TIMebase:RANge?')   


for channel in range(4):                   # ch2 on scope wired to IalphaTapMUX, ch3 on scope wired to IbetaTapMUX, ch4 wired to VmemBufMUX 
    my_Scope.write(':WAVEFORM:SOURCE CHANnel'+str(channel+1))
    my_Scope.query(':WAVEFORM:SOURce?')
    my_Scope.write(':CHANnel'+str(channel+1)+':RANGe 4V')     #Sets the full scale vertical range in mV or V. The range value is 8 times the volts per division.
    #my_Scope.write(':CHANnel1:DISPlay OFF')


    #my_Scope.write(':WAVEFORM:UNSigned ON')
    #my_Scope.write(':DIGitize CHANnel'+str(channel))

    #my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(channel))
    #avg = my_Scope.query(':MEASure:VAVerage?');
    #print("The average voltage is", avg)
    
    
volt = 0.9
sign_clamp = 1
cnt = 1
try:
    for j in range(100):
        my_K.write(':SOUR:VOLT:LEV '+str(0.87 + sign_clamp*volt))  
        sign_clamp = -sign_clamp
        time.sleep(0.01)
        cnt = cnt+1
        if cnt == 10:
            cnt = 1
            if sign_clamp == 1:
                rise_time = my_Scope.query(':MEASure:RISetime?')
                rise_time_list.append((float(rise_time))*1e6)
                print("rise time on is ", (float(rise_time))*1e6,'usec')
            else:
                fall_time = my_Scope.query(':MEASure:FALLtime?') 
                fall_time_list.append((float(fall_time))*1e6)
                print("fall time on is ", (float(fall_time))*1e6,'usec') 

except KeyboardInterrupt:
    my_K.write(':SOUR:VOLT:LEV 0.9')
    print('Voltage clamped to 0.9v.')