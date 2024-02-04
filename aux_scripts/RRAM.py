#%% Initialize Opal Kelly

import os
path = "C:/Users/Soumil/OneDrive - UC San Diego/research/RRAM PCB/python"
#path = "C:/Users/jains/OneDrive - UC San Diego/research/RRAM PCB/python"
os.chdir(path)

from RRAM_functions import *
import time
import math
import pyvisa 

deviceCount = dev.xem.GetDeviceCount()
print(deviceCount)
#dev.xem.bitfile = "C:/Users/Soumil/OneDrive - UC San Diego/research/RRAM PCB/python/pcb_reset_common_clk.bit"   # Location of the bitfile
dev.xem.bitfile = path + "/pcb_reset_common_clk.bit"   # Location of the bitfile
dev.xem.OpenBySerial("")                                                                       # find connected xem7310
error = dev.xem.ConfigureFPGA(dev.xem.bitfile)                                                 # load bitfile
print("FPGA configuration error code:")
print(error)

dev.initDevice()

#%% Initialize switches, dacs and adcs


#switches
write_FPGA(dev, 0x05, 0x00000000)       # VP_BL_SEL
write_FPGA(dev, 0x06, 0x00000000)       # VN_BL_SEL
write_FPGA(dev, 0x07, 0x00000000)       # VREF_BL_SEL
write_FPGA(dev, 0x08, 0x00000000)       # ADC_BL_SEL
write_FPGA(dev, 0x09, 0x00000000)       # VP_WL_SEL
write_FPGA(dev, 0x0A, 0x00000000)       # VN_WL_SEL
write_FPGA(dev, 0x0B, 0x00000000)       # VREF_WL_SEL


# turn off vref switches from default ON condition
write_FPGA(dev, 0x16, 0x00000000)       


# DAC 
write_FPGA(dev, 0x0D, 0x00000000)       # LDACbDAC
write_FPGA(dev, 0x0E, 0xffffffff)       # CLRbDAC


# reset verilog FSM 
write_FPGA(dev, 0x00, 0x01)
time.sleep(1e-3)
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state))


print("initialization complete")


#%% Write to dacs


write_DAC(dev, VP_RRAM, 0.2)
write_DAC(dev, VN_RRAM, 0.0)
write_DAC(dev, VREF_RRAM, 0.0)
print ("dacs configured")


#%% Testing Default Vref connections to BL / WL


write_FPGA(dev, 0x16, 0x00000001)       # 0x01 - WL, BL Vref switches OFF; 0x00 - WL, BL Vref switches ON
write_FPGA(dev, 0x05, 0x0000FFFF)       # VP_BL_SEL
write_FPGA(dev, 0x09, 0x0000FFFF)       # VP_WL_SEL


#%% ADC0, setup
# Clear Brown out reset indicator in 0x00 (SYSTEM_STATUS) register


#ADC_SPI_write(dev, write_command, ADC_CSb, ADC_CLK, ADC_SDI0)
write_ADC0(dev, 0x080001) 
#ADC_SPI_read(dev, read_command, ADC_CSb, ADC_CLK, ADC_SDI0, ADC_SDO0,1)
read_ADC0(dev, 0x100000, 0)         #0 for reading from internal register, 1 for reading a channel


# Reset device (bit 0 in 0x01 register)
write_ADC0(dev, 0x080101)
read_ADC0(dev, 0x100000, 0)
#Clear Brown out reset indicator in 0x00 register
write_ADC0(dev, 0x080001)
read_ADC0(dev, 0x100000, 0)


# Set SEQ_MODE to Manual
write_ADC0(dev, 0x081000)


# Configure PIN_CFG reg for setting channels as analog inputs
write_ADC0(dev, 0x080500)
read_ADC0(dev, 0x100500, 0)


# Calibrate
write_ADC0(dev, 0x080102)
time.sleep(1e-3)


# Check if calibration is done
read_ADC0(dev, 0x100100, 0)


# Set SEQ_MODE to Manual
write_ADC0(dev, 0x081000)


# Set APPEND_STATUS[1:0] in 0x02 -- Displays CHID on SDO
write_ADC0(dev, 0x080210)


#%% Diagnostics, Bit-walk test mode, ADC0
write_ADC0(dev, 0x08BF96)         # set diagnostics_key register
read_ADC0(dev, 0x10BF00, 0)

write_ADC0(dev, 0x08C001)         # enable diagnostics
read_ADC0(dev, 0x10C000, 0)

write_ADC0(dev, 0x08C100)         # LSB
read_ADC0(dev, 0x10C100, 0)

write_ADC0(dev, 0x08C240)         # MSB
read_ADC0(dev, 0x10C200, 0)

# read voltage from a channel
write_ADC0(dev, 0x081104)         # Switch to the desired channel  
write_ADC0(dev, 0x000000)         # send dummy 24 clk cycles, acquire data from the desired channel
data_out = read_ADC0(dev, 0x000000, 1)         # convert and readout the desired channel  

data_out = int(data_out, 16)>>8
print((data_out/2**16)*3.3)

#%% Diagnostics, Fixed voltage test mode, verify 1.8v on AIN6, ADC0
write_ADC0(dev, 0x08BF96)        # set diagnostics_key register 
read_ADC0(dev, 0x10BF00, 0)

write_ADC0(dev, 0x08C010)        # enable diagnostics    
read_ADC0(dev, 0x10C000, 0)

# read voltage from CH6
write_ADC0(dev, 0x081106)        # Switch to the desired channel  
write_ADC0(dev, 0x000000)        # send dummy 24 clk cycles, acquire data from the desired channel
data_out = read_ADC0(dev, 0x000000, 1)         # convert and readout the desired channel   

data_out = int(data_out, 16)>>8
print((data_out/2**16)*3.3)

#%% Disable diagnostics, ADC0
write_ADC0(dev, 0x08C000)        # disable diagnostics
read_ADC0(dev, 0x10C000, 0)

write_ADC0(dev, 0x08BF00)        # set diagnostics_key register 
read_ADC0(dev, 0x10BF00, 0)

#%% Read a channel
write_FPGA(dev, 0x05, 0x00000001)       # VP_BL_SEL
write_FPGA(dev, 0x08, 0x00000001)       # ADC_BL_SEL
time.sleep(1e-3)

# read voltage from CH0
write_ADC0(dev, 0x081100)               # Switch to the desired channel  
write_ADC0(dev, 0x000000)               # send dummy 24 clk cycles, acquire data from the desired channel
data_out = read_ADC0(dev, 0x000000, 1)         # convert and readout the desired channel   

data_out = int(data_out, 16)>>8
print((data_out/2**16)*3.3)

#all_switches_off(dev)

#%% ADC1, setup
# Clear Brown out reset indicator in 0x00 (SYSTEM_STATUS) register
write_ADC1(dev, 0x080001)  
read_ADC1(dev, 0x100000, 0)


# Reset device (bit 0 in 0x01 register)
write_ADC1(dev, 0x080101)  
read_ADC1(dev, 0x100000, 0)


#Clear Brown out reset indicator in 0x00 register
write_ADC1(dev, 0x080001) 
read_ADC1(dev, 0x100000, 0)


# Set SEQ_MODE to Manual
write_ADC1(dev, 0x081000) 


# Configure PIN_CFG reg for setting channels as analog inputs
write_ADC1(dev, 0x080500) 
read_ADC1(dev, 0x100500, 0)


# Calibrate
write_ADC1(dev, 0x080102) 
time.sleep(1e-2)


# Check if calibration done
read_ADC1(dev, 0x100100, 0)


#Set SEQ_MODE to Manual
write_ADC1(dev, 0x081000) 


# Set APPEND_STATUS[1:0] in 0x02 -- Displays CHID on SDO
write_ADC1(dev, 0x080210)

           
#%% Diagnostics, Bit-walk test mode, ADC1
write_ADC1(dev, 0x08BF96)         # set diagnostics_key register
read_ADC1(dev, 0x10BF00, 0)

write_ADC1(dev, 0x08C001)         # enable diagnostics
read_ADC1(dev, 0x10C000, 0)

write_ADC1(dev, 0x08C100)         # LSB
read_ADC1(dev, 0x10C100, 0)

write_ADC1(dev, 0x08C240)         # MSB
read_ADC1(dev, 0x10C200, 0)

# read voltage from a channel
write_ADC1(dev, 0x081104)         # Switch to the desired channel  
write_ADC1(dev, 0x000000)         # send dummy 24 clk cycles, acquire data from the desired channel
data_out = read_ADC1(dev, 0x000000, 1)         # convert and readout the desired channel   

data_out = int(data_out, 16)>>8
print((data_out/2**16)*3.3)

#%% Diagnostics, Fixed voltage test mode, verify 1.8v on AIN6, ADC1
write_ADC1(dev, 0x08BF96)        # set diagnostics_key register 
read_ADC1(dev, 0x10BF00, 0)

write_ADC1(dev, 0x08C010)        # enable diagnostics    
read_ADC1(dev, 0x10C000, 0)

# read voltage from CH6
write_ADC1(dev, 0x081106)        # Switch to the desired channel  
write_ADC1(dev, 0x000000)        # send dummy 24 clk cycles, acquire data from the desired channel
data_out = read_ADC1(dev, 0x000000, 1)         # convert and readout the desired channel 

data_out = int(data_out, 16)>>8
print((data_out/2**16)*3.3)

#%% Disable diagnostics, ADC1
write_ADC1(dev, 0x08C000)        # disable diagnostics
read_ADC1(dev, 0x10C000, 0)

write_ADC1(dev, 0x08BF00)        # set diagnostics_key register 
read_ADC1(dev, 0x10BF00, 0)

#%% Read a channel

write_FPGA(dev, 0x07, 0x00002000)       # VREF_BL_SEL
write_FPGA(dev, 0x08, 0x00002000)       # ADC_BL_SEL
time.sleep(1e-3)

# read voltage from CH13
write_ADC1(dev, 0x081105)               # Switch to the desired channel  
write_ADC1(dev, 0x000000)               # send dummy 24 clk cycles, acquire data from the desired channel
data_out = read_ADC1(dev, 0x000000, 1)         # convert and readout the desired channel 

data_out = int(data_out, 16)>>8
print((data_out/2**16)*3.3)

all_switches_off(dev)

#%% test all ADC channels


all_switches_off(dev)


write_DAC(dev, VP_RRAM, 1)
write_DAC(dev, VN_RRAM, 0.4)
write_DAC(dev, VREF_RRAM, 0.7)


write_FPGA(dev, 0x05, 0x0000ffff)       # VP_BL_SEL
write_FPGA(dev, 0x06, 0x00000000)       # VN_BL_SEL
write_FPGA(dev, 0x07, 0x00000000)       # VREF_BL_SEL
write_FPGA(dev, 0x09, 0x0000ffff)       # VP_WL_SEL
write_FPGA(dev, 0x0A, 0x00000000)       # VN_WL_SEL


write_FPGA(dev, 0x07, 0x00000000)       # VREF_BL_SEL
write_FPGA(dev, 0x0B, 0x00000000)       # VREF_WL_SEL
write_FPGA(dev, 0x08, 0x0000ffff)       # ADC_BL_SEL


# ADC read - Ch0                 
write_ADC0(dev, 0x081100)  
write_ADC0(dev, 0x000000)               
Ch0 = read_ADC0(dev, 0x000000, 1)        
Ch0 = int(Ch0, 16)>>8
print('Ch0 ' + str((Ch0/2**16)*3.3) + '\n')


# ADC read - Ch1
write_ADC0(dev, 0x081101)  
write_ADC0(dev, 0x000000)               
Ch1 = read_ADC0(dev, 0x000000, 1)        
Ch1 = int(Ch1, 16)>>8
print('Ch1 ' + str((Ch1/2**16)*3.3) + '\n')


# ADC read - Ch2
write_ADC0(dev, 0x081102)  
write_ADC0(dev, 0x000000)               
Ch2 = read_ADC0(dev, 0x000000, 1)                       
Ch2 = int(Ch2, 16)>>8
print('Ch2 ' + str((Ch2/2**16)*3.3) + '\n')


# ADC read - Ch3
write_ADC0(dev, 0x081103)  
write_ADC0(dev, 0x000000)               
Ch3 = read_ADC0(dev, 0x000000, 1)        
Ch3 = int(Ch3, 16)>>8
print('Ch3 ' + str((Ch3/2**16)*3.3) + '\n')


# ADC read - Ch4
write_ADC0(dev, 0x081104)  
write_ADC0(dev, 0x000000)               
Ch4 = read_ADC0(dev, 0x000000, 1)        
Ch4 = int(Ch4, 16)>>8
print('Ch4 ' + str((Ch4/2**16)*3.3) + '\n')


# ADC read - Ch5
write_ADC0(dev, 0x081105)  
write_ADC0(dev, 0x000000)               
Ch5 = read_ADC0(dev, 0x000000, 1)        
Ch5 = int(Ch5, 16)>>8
print('Ch5 ' + str((Ch5/2**16)*3.3) + '\n')


# ADC read - Ch6
write_ADC0(dev, 0x081106)  
write_ADC0(dev, 0x000000)               
Ch6 = read_ADC0(dev, 0x000000, 1)        
Ch6 = int(Ch6, 16)>>8
print('Ch6 ' + str((Ch6/2**16)*3.3) + '\n')


# ADC read - Ch7
write_ADC0(dev, 0x081107)  
write_ADC0(dev, 0x000000)               
Ch7 = read_ADC0(dev, 0x000000, 1)        
Ch7 = int(Ch7, 16)>>8
print('Ch7 ' + str((Ch7/2**16)*3.3) + '\n')


# ADC read - Ch8
write_ADC1(dev, 0x081100)  
write_ADC1(dev, 0x000000)               
Ch8 = read_ADC1(dev, 0x000000, 1)        
Ch8 = int(Ch8, 16)>>8
print('Ch8 ' + str((Ch8/2**16)*3.3) + '\n')


# ADC read - Ch9
write_ADC1(dev, 0x081101)  
write_ADC1(dev, 0x000000)               
Ch9 = read_ADC1(dev, 0x000000, 1)        
Ch9 = int(Ch9, 16)>>8
print('Ch9 ' + str((Ch9/2**16)*3.3) + '\n')


# ADC read - Ch10
write_ADC1(dev, 0x081102)  
write_ADC1(dev, 0x000000)               
Ch10 = read_ADC1(dev, 0x000000, 1)    
Ch10 = int(Ch10, 16)>>8
print('Ch10 ' + str((Ch10/2**16)*3.3) + '\n')


# ADC read - Ch11
write_ADC1(dev, 0x081103)  
write_ADC1(dev, 0x000000)               
Ch11 = read_ADC1(dev, 0x000000, 1)    
Ch11 = int(Ch11, 16)>>8
print('Ch11 ' + str((Ch11/2**16)*3.3) + '\n')


# ADC read - Ch12
write_ADC1(dev, 0x081104)  
write_ADC1(dev, 0x000000)               
Ch12 = read_ADC1(dev, 0x000000, 1)    
Ch12 = int(Ch12, 16)>>8
print('Ch12 ' + str((Ch12/2**16)*3.3) + '\n')


# ADC read - Ch13
write_ADC1(dev, 0x081105)  
write_ADC1(dev, 0x000000)               
Ch13 = read_ADC1(dev, 0x000000, 1)    
Ch13 = int(Ch13, 16)>>8
print('Ch13 ' + str((Ch13/2**16)*3.3) + '\n')


# ADC read - Ch14
write_ADC1(dev, 0x081106)  
write_ADC1(dev, 0x000000)               
Ch14 = read_ADC1(dev, 0x000000, 1)    
Ch14 = int(Ch14, 16)>>8
print('Ch14 ' + str((Ch14/2**16)*3.3) + '\n')


# ADC read - Ch15
write_ADC1(dev, 0x081107)  
write_ADC1(dev, 0x000000)               
Ch15 = read_ADC1(dev, 0x000000, 1)    
Ch15 = int(Ch15, 16)>>8
print('Ch15 ' + str((Ch15/2**16)*3.3) + '\n')


all_switches_off(dev)


#%% FORMING/SET/RESET


# Reset verilog Finite State Machine 
write_FPGA(dev, 0x00, 0x01)
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state) + '\n')


all_switches_off(dev)
write_FPGA(dev, 0x17, 0x00)                     # de-assert READ trigger
write_DAC(dev, VP_RRAM, 1.6)
write_DAC(dev, VN_RRAM, 0.0)
write_DAC(dev, VREF_RRAM, 0.7)
 

WL_map = [5, 11, 14, 2, 1, 9, 10, 4, 7, 13, 16, 8, 3, 15, 12, 6]
BL_map = [8, 14, 9, 7, 4, 16, 13, 3, 12, 6, 11, 1, 10, 2, 15, 5]         


WL_to_reset = [9, 10, 11, 12, 13]
BL_to_reset = [2, 3, 4, 6]


WL_true = np.zeros(len(WL_to_reset))
BL_true = np.zeros(len(BL_to_reset))
WL_sw = np.zeros(len(WL_to_reset))
BL_sw = np.zeros(len(BL_to_reset))
WL_vref_sw = np.zeros(len(WL_to_reset))
BL_vref_sw = np.zeros(len(BL_to_reset))
vref_sw = np.zeros((len(WL_to_reset), len(BL_to_reset)))


for i in range (len(WL_to_reset)):
    WL_true[i] = WL_map.index(WL_to_reset[i])
    command = 0x0001
    WL_sw[i] = command<<int(WL_true[i])      
    WL_vref_sw[i] = 2**16 - 1 - int(WL_sw[i])
     
        
    print('WL_true: ' + str(WL_true[i]))
    print('switch command for WL: ' + str(hex(int(WL_sw[i]))))  
    
    
    for j in range (len(BL_to_reset)):
        BL_true[j] = BL_map.index(BL_to_reset[j])
        command = 0x0001
        BL_sw[j] = command<<int(BL_true[j])
        BL_vref_sw[j] =  (2**16 - 1 - int(BL_sw[j]))<<16
        
        
        BL_sw[j] = int(BL_sw[j])<<16
        vref_sw[i][j] = int(WL_vref_sw[i]) + int(BL_vref_sw[j])
      
             
        print('BL_true: ' + str(BL_true[j]))
        print('switch command for BL: ' + str(hex(int(BL_sw[j]))))
        print('switch command for vref: ' + str(hex(int(vref_sw[i][j]))) + '\n')
      
        
        #Change state -- RESET/SET/FORM
        write_FPGA(dev, 0x12, int(vref_sw[i][j]))                  # Vref switch select,   WL -- [15:0], BL -- [31:16]
        write_FPGA(dev, 0x13, int(BL_sw[j]))                       # Vp switch select,     WL -- [15:0], BL -- [31:16]
        write_FPGA(dev, 0x14, int(WL_sw[i]))                       # Vn switch select,     WL -- [15:0], BL -- [31:16] 
      
        
        done = 0
        write_FPGA(dev, 0x11, 25000000)                                # forming duration = #cycles*(40n); 2500 -- 100 us
        write_FPGA(dev, 0x10, 0x01)                                 # assert FORM trigger
        while True:
            done = read_FPGA(dev, 0x35)                             # read FORM done flag
            if done == 1:
                write_FPGA(dev, 0x10, 0x00)                         # de-assert FORM trigger
                print('reset done')
                break  
    print('\n')


#%% Capacitor Characterisation using transient measurements
 

all_switches_off(dev)
write_FPGA(dev, 0x00, 0x01)                     # Reset Finite State Machine in verilog
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state) + '\n')
write_FPGA(dev, 0x10, 0x00)                     # de-assert FORM trigger


vp = 0.5
vn = 0.2
vref = 0
write_DAC(dev, VP_RRAM, vp)
write_DAC(dev, VN_RRAM, vn)
write_DAC(dev, VREF_RRAM, vref)


positive_read_pulse        = 1
negative_read_pulse       = (1 - positive_read_pulse)
if (positive_read_pulse):
    write_FPGA(dev, 0x14, 0x00000000)               # Vn switch select, [15:0] for WL, [31:16] for BL
else:
    write_FPGA(dev, 0x13, 0x00000000)               # Vp switch select, [15:0] for WL, [31:16] for BL
  
    
N               = 50
R_true          = 10100000
C               = 100e-12
tau             = int((R_true*C)/(40e-9))
T               = np.logspace(np.log10(tau/5), np.log10(tau*4), num = 10)
T               = T.astype(int)
  

fr_array        = np.zeros((16,16,N))
g               = np.zeros((16,16))
R               = np.zeros((len(T),16,16))
av              = np.zeros((len(T),16,16))
g_tot           = np.zeros((16,1))
R_map           = np.zeros((len(T), 3))


l = 0
while (l<len(T)):
    
    
    write_FPGA(dev, 0x04, 0x03)                                 # reset fifo counter
    write_FPGA(dev, 0x04, 0x00)
  
    
    adc_data            = 0x081102
    adc_switch          = 0x00000004
    vp_WL_switch        = 0x00001000
    #vn_WL_switch        = 0x00001000
    vref_WL_switch      = 0xefff
    
    
    k = 12                                                      # WL loop
    #while k<16:       
    if (positive_read_pulse):
        write_FPGA(dev, 0x13, vp_WL_switch)                     # Vn switch select during read, [15:0] for WL, [31:16] for BL -- vp row ON
    else: 
        write_FPGA(dev, 0x14, vn_WL_switch)                     # Vn switch select during read, [15:0] for WL, [31:16] for BL -- vp row ON

    
    j = 2                                                       # BL loop
    #while j<16:     
    vref_BL_switch = ((~(adc_switch & (0x0000ffff))) & 0x0000ffff)<<16
    write_FPGA(dev, 0x12, vref_BL_switch + vref_WL_switch)     # Vref switch select during read
    #print('vref_switch = '+ str(hex(vref_BL_switch + vref_WL_switch)))
    
    
    #print('adc_data = ' + str(hex(adc_data)))
    write_FPGA(dev, 0x15, adc_switch)                           # select capacitor for ADC sampling
    #print('adc switch = '+ str(hex(adc_switch)) + '\n')
    
    i = 0
    while (i<N):
        done = 0
        if j<8:
            write_FPGA(dev, 0x1c, adc_data)                         # specify ADC0 channel to read from -- bits [7:0]
        else:
            write_FPGA(dev, 0x1f, adc_data)                         # specify ADC1 channel to read from -- bits [7:0]
        write_FPGA(dev, 0x0f, int(T[l]))                            # charging duration = #cycles*(10n)
        write_FPGA(dev, 0x17, 1)                                    # READ trigger flag asserted 
        while True:
            done = read_FPGA(dev, 0x36)
            if done == 1:
                write_FPGA(dev, 0x17, 0x00)                         # READ trigger deasserted
                adc0_Frame2 = read_FPGA(dev, 0x32)
                adc1_Frame2 = read_FPGA(dev, 0x34)
                adc0_Frame2 = adc0_Frame2>>8
                adc1_Frame2 = adc1_Frame2>>8
                if j<8:
                    fr_array[k][j][i] = 3.3*(adc0_Frame2/2**16)
                    # print('ADC0 Frame 2 output ' + str(3.3*(adc0_Frame2/2**16)))
                else:
                    fr_array[k][j][i] = 3.3*(adc1_Frame2/2**16)
                    # print('ADC1 Frame 2 output ' + str(3.3*(adc1_Frame2/2**16)))
                break
        i+=1
    
    
    if j<7:
        adc_data = adc_data + 1
    elif j==7:
        adc_data = 0x081100
    else: 
        adc_data = adc_data + 1    
    adc_switch = adc_switch << 1
    av[l][k][j] = np.mean(fr_array[k][j])
    delta_t = T[l]*40e-9
    print('delta_t: ' + str(delta_t))
    print('V_BL average: '+str(av[l][k][j]))
    R_map[l][0] = delta_t
    R_map[l][1] = av[l][k][j]
    
    if (positive_read_pulse):
        if ( av[l][k][j] < vref):
            av[l][k][j] = vref
            R[l][k][j] = 1e12
        else:
            R[l][k][j] = -(delta_t/C)*(1/np.log(1 - ( (av[l][k][j] - vref)/(vp - vref) )))
    else:
        if ( av[l][k][j] > vref):
            av[l][k][j] = vref
            R[l][k][j] = 1e12
        else:
            R[l][k][j] = -(delta_t/C)*(1/np.log(1 - ( (vref - av[l][k][j])/(vref - vn) )))
    print('R: '+str(R[l][k][j]))
    R_map[l][2] = R[l][k][j] 
    
    
    adc_data =  0x081100
    adc_switch = 0x00000001
  
    
    vref_WL_switch = vref_WL_switch<<1   
    vref_WL_switch = vref_WL_switch+1
    vref_WL_switch = vref_WL_switch & (0x0000ffff)
    
    
    #print('vp_WL_switch = '+ str(hex(vp_WL_switch)))
    #print('k = ' +str(k))
    print('\n')
    if (positive_read_pulse):
        vp_WL_switch= vp_WL_switch<<1
    else:
        vn_WL_switch= vn_WL_switch<<1
    #k+=1
    l+=1
    
df = pd.DataFrame(R_map, columns = ['delta_t', 'V_BL average', 'R'])
#df.to_excel(path + '/excel data/cap characterisation/WL'+str(k)+'/R_map_'+str(R_true)+'_WL'+str(k)+'_BL'+str(j)+'.xlsx')
df.to_excel(path+'/excel data/cap characterisation/WL'+str(k)+'/R_map_'+str(R_true)+'_WL'+str(k)+'_BL'+str(j)+'.xlsx')


#%% Plot transient measurements  


true_array = np.zeros((16,16))
WL_map = [5, 11, 14, 2, 1, 9, 10, 4, 7, 13, 16, 8, 3, 15, 12, 6]
BL_map = [8, 14, 9, 7, 4, 16, 13, 3, 12, 6, 11, 1, 10, 2, 15, 5]


l=0
for i in range(0,16):
    for j in range(0,16):
        #if BL_map[j] != 5: 
        if math.isnan(R[l][i][j]):   
            true_array[WL_map[i]-1][BL_map[j]-1] = 1e12
        else:
            true_array[WL_map[i]-1][BL_map[j]-1] = R[l][i][j]
        #else:
        #    true_array[WL_map[i]-1][BL_map[j]-1] = 5e11                     # Open BL
        
df = pd.DataFrame(true_array, columns = ['BL1', 'BL2', 'BL3', 'BL4', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL10', 'BL11', 'BL12', 'BL13', 'BL14', 'BL15', 'BL16'], 
                  index = ['WL1','WL2', 'WL3', 'WL4', 'WL5','WL6', 'WL7', 'WL8', 'WL9','WL10', 'WL11', 'WL12', 'WL13','WL14', 'WL15', 'WL16'])
#df.to_csv(path+'/excel data/array '+array+'/T_80nsec_vread_0.5v.csv')
plt.figure(figsize=(20, 20))
ax = plt.axes() 
p = plt.imshow(true_array, cmap='hot', norm=colors.LogNorm())
plt.colorbar(p)

#plt.hist(true_array.reshape(256,1), bins = np.logspace(start = np.log10(1e9), stop = np.log10(0.5e10), num = 100))
x = [i for i in range(0,16)]
x_map = [i for i in range(1,17)]
ax.set_xticks(x)
ax.set_xticklabels(x_map)
y = [i for i in range(0,16)]
y_map = [i for i in range(1,17)]
ax.set_yticks(y)
ax.set_yticklabels(y_map)
plt.show()
plt.xlabel('BL')
plt.ylabel('WL')
plt.title('resistance, Vread = ' + str(vp-vref) + ', Charging duration = ' + str(T[l]*40e-9) + 'sec')
#plt.savefig(path+'/plots/array '+array+'/T_80nsec_vread_0.5v.png')


#%% Scatter plot with discrete resistors


N               = 100		
C               = [1.99E-10, 2.01E-10, 1.90E-10, 1.93E-10, 1.96E-10, 1.99E-10, 1.93E-10, 1.93E-10,
                   1.99E-10, 1.97E-10, 1.93E-10, 1.96E-10, 1.96E-10, 2.02E-10, 1.97E-10, 1.11E-10]
R_true          = np.array([553, 993, 4662, 10.07e3, 46.67e3, 100.9e3, 479.4e3, 1.014e6, 4.826e6, 10.58e6],
                           dtype=float)
ADC_out         = np.zeros((len(R_true), 16, N))
ADC_out_av      = np.zeros((len(R_true), 16))
R_meas          = np.zeros((len(R_true), 16))


#%% Scatter plot with discrete resistors


all_switches_off(dev)
write_FPGA(dev, 0x00, 0x01)                                 # Reset Finite State Machine in verilog
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state) + '\n')
write_FPGA(dev, 0x10, 0x00)                                 # de-assert FORM trigger


vp = 1
vn = 0.0
vref = 0.0
write_DAC(dev, VP_RRAM, vp)
write_DAC(dev, VN_RRAM, vn)
write_DAC(dev, VREF_RRAM, vref)

                                                     
positive_read_pulse       = 1                               # Sensing using Vref + Vpulse scheme if set to 1
negative_read_pulse       = (1 - positive_read_pulse)       # Sensing using Vref - Vpulse scheme if set to 1

 
WL              = 1                                        # Programming WL0
BL              = 5                                        # Reading on BL0  
T               = ((4*R_true*C[BL])/40e-9).astype(int)     


write_FPGA(dev, 0x04, 0x03)                                 # reset fifo counter
write_FPGA(dev, 0x04, 0x00)
adc_data            = 0x081100 + BL%8
adc_switch          = 0x00000001 << BL
write_FPGA(dev, 0x15, adc_switch)                           # select capacitor for ADC sampling

if (positive_read_pulse):
    write_FPGA(dev, 0x14, 0x00000000)                       # Vn switch select
    vp_WL_switch    = 0x00000001 << WL
    write_FPGA(dev, 0x13, int(vp_WL_switch))                # Vp switch select
    print('vp_WL_switch: ' + str(hex(vp_WL_switch)))
    
else:    
    write_FPGA(dev, 0x13, 0x00000000)                       # Vp switch select
    vn_WL_switch    = 0x00000001 << WL
    write_FPGA(dev, 0x14, vn_WL_switch)                     # Vn switch select
    print('vn_WL_switch: ' + str(hex(vn_WL_switch)))


vref_WL         = 2**16 - 1 - (0x00000001 << WL)
vref_BL         = (2**16 - 1 - (0x00000001 << BL)) << 16
vref_switch     = vref_BL + vref_WL
write_FPGA(dev, 0x12, int(vref_switch))                     # Vref switch select   
print('vref_switch: ' + str(hex(vref_switch)))

    
l = 5                                                       # Resistor value
m = BL                                                      # BL 
i = 0
while (i<N):
    done = 0
    if BL<8:
        write_FPGA(dev, 0x1c, adc_data)                     # specify ADC0 channel to read from -- bits [7:0]
    else:
        write_FPGA(dev, 0x1f, adc_data)                     # specify ADC1 channel to read from -- bits [7:0]
    write_FPGA(dev, 0x0f, int(T[l]))                        # charging duration = #cycles*(40n)
    write_FPGA(dev, 0x17, 1)                                # read trigger asserted 
    while True:
        done = read_FPGA(dev, 0x36)
        if done == 1:
            write_FPGA(dev, 0x17, 0x00)                     # read trigger deasserted
            adc0_Frame2 = read_FPGA(dev, 0x32)
            adc1_Frame2 = read_FPGA(dev, 0x34)
            adc0_Frame2 = adc0_Frame2>>8
            adc1_Frame2 = adc1_Frame2>>8
            if BL<8:
                ADC_out[l][m][i] = 3.3*(adc0_Frame2/2**16)
            else:
                ADC_out[l][m][i] = 3.3*(adc1_Frame2/2**16)
            break
    i+=1


ADC_out_av[l][m] = np.mean(ADC_out[l][m])
delta_t = T[l]*40e-9
print('delta_t: ' + str(delta_t))
print('V_BL average: '+str(ADC_out_av[l][m]))


if (positive_read_pulse):
    if ( ADC_out_av[l][m] < vref):
        ADC_out_av[l][m] = vref
        R_meas[l][m]        = 1e12
    else:
        R_meas[l][m]        = -(delta_t/C[BL])*(1/np.log(1 - ( (ADC_out_av[l][m] - vref)/(vp - vref) )))
else:
    if ( ADC_out_av[l][m] > vref):
        ADC_out_av[l][m] = vref
        R_meas[l][m]        = 1e12
    else:
        R_meas[l][m]        = -(delta_t/C[BL])*(1/np.log(1 - ( (vref - ADC_out_av[l][m])/(vref - vn) )))
print('R: '+str(R_meas[l][m]))


#%% Save resistor test data   


df1 = pd.DataFrame(R_true)
df1.to_excel(path + '/excel data/discrete resistor test/R_true_WL'+str(WL)+'.xlsx')


df2 = pd.DataFrame(R_meas)
df2.to_excel(path + '/excel data/discrete resistor test/R_meas_WL'+str(WL)+'.xlsx')


del df1, df2


#%% Scatter plot with discrete resistors

R_true = pd.read_excel(path + '/excel data/discrete resistor test/R_true_WL'+str(WL)+'.xlsx', header = 0, index_col = 0).to_numpy()
R_meas = pd.read_excel(path + '/excel data/discrete resistor test/R_meas_WL'+str(WL)+'.xlsx', header = 0, index_col = 0).to_numpy()

# setting font sizeto 30
plt.rcParams.update({'font.size': 25})

fig, ax = plt.subplots(figsize = (15, 10))
x = np.logspace(np.log10(min(np.min(R_true), np.min(R_meas))), np.log10(max(np.max(R_true), np.max(R_meas))), 1000)
for i in range(16):
    ax.scatter(R_true, R_meas[:,i], 
               color = 'orange',
               linewidth = 6)
ax.plot(R_true, R_true,
        alpha=0.8,
        linewidth = 3)


# Set logarithmic scale on the both variables
ax.set_xscale("log")
ax.set_yscale("log")


plt.xlabel('True Resistance (ohms)')
plt.ylabel('Measured Resistance (ohms)')
plt.title('Measured vs True Resistance')
plt.grid(True, which='both')
plt.savefig(path+'/plots/discrete resistor test/WL'+str(WL)+'.png')
plt.show()


#%% Read operation --  transient measurements, measure total conductance in a BL


all_switches_off(dev)
write_FPGA(dev, 0x00, 0x01)                     # Reset verilog Finite State Machine 
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state))
write_FPGA(dev, 0x10, 0x00)                     # de-assert FORM trigger


vp      = 0.0
vn      = 0.0
vref    = 0.0
vread   = vp - vref
write_DAC(dev, VP_RRAM, vp)
write_DAC(dev, VN_RRAM, vn)
write_DAC(dev, VREF_RRAM, vref)


positive_read_pulse        = 1                              # Sensing using Vref + Vpulse scheme if set to 1
negative_read_pulse        = (1 - positive_read_pulse)      # Sensing using Vref - Vpulse scheme if set to 1


if (positive_read_pulse):
    write_FPGA(dev, 0x14, 0x00000000)                       # Vn switch select, [15:0] for WL, [31:16] for BL
else:
    write_FPGA(dev, 0x13, 0x00000000)                       # Vp switch select, [15:0] for WL, [31:16] for BL 
  
    
N               = 50
T               = np.linspace(2, 16000, 1000)
#T              = np.linspace(62500, 10000000, 1000)        # for measurements in Gohm range  
fr_array        = np.zeros((16,16,N))
g               = np.zeros((16,16))
R               = np.zeros((len(T),16,16))
av              = np.zeros((len(T),16,16))
g_tot           = np.ones((16,1))*1e-9
C               = [2.01E-10, 2.03E-10, 1.92E-10, 1.95E-10, 1.97E-10, 2.00E-10, 1.94E-10, 1.94E-10, 1.99E-10, 1.98E-10, 1.95E-10 ,1.97E-10, 1.95E-10, 2.00E-10, 1.96E-10, 1.10E-10]
        
        
write_FPGA(dev, 0x04, 0x03)                                 # reset fifo counter
write_FPGA(dev, 0x04, 0x00)


adc_data        = 0x081100
adc_switch      = 0x00000001
if (positive_read_pulse):   
    vp_WL_switch    = 0x0000ffff
else:
    vn_WL_switch    = 0x0000ffff
vref_WL         = 0x0
  
 
WL = 0                                                         
if (positive_read_pulse):
    write_FPGA(dev, 0x13, vp_WL_switch)                     # Vn switch select during read, [15:0] for WL, [31:16] for BL 
else: 
    write_FPGA(dev, 0x14, vn_WL_switch)                     # Vn switch select during read, [15:0] for WL, [31:16] for BL                                                      
for BL in range(5):    
   
    
    vref_BL             = (2**16 - 1 - adc_switch) << 16
    vref_switch         = vref_BL + vref_WL 
    write_FPGA(dev, 0x12, vref_switch)                      # Vref switch select during read
    print('vref_switch = '+ str(hex(vref_switch)))
    write_FPGA(dev, 0x15, adc_switch)                       # select capacitor for ADC sampling
    
    
    for l in range(len(T)):

        
        for i in range(N):
            done = 0
            if BL<8:
                write_FPGA(dev, 0x1c, adc_data)                 # specify ADC0 channel to read from -- bits [7:0]
            else:
                write_FPGA(dev, 0x1f, adc_data)                 # specify ADC1 channel to read from -- bits [7:0]
            write_FPGA(dev, 0x0f, int(T[l]))                    # charging duration = #cycles*(10n)
            write_FPGA(dev, 0x17, 0x01)                         # READ trigger flag asserted 
            while True:
                done = read_FPGA(dev, 0x36)
                if done == 1:
                    write_FPGA(dev, 0x17, 0x00)
                    #adc0_Frame1 = read_FPGA(dev, 0x31)
                    adc0_Frame2 = read_FPGA(dev, 0x32)
                    #adc1_Frame1 = read_FPGA(dev, 0x33)
                    adc1_Frame2 = read_FPGA(dev, 0x34)
                    #adc0_Frame1 = adc0_Frame1>>8
                    adc0_Frame2 = adc0_Frame2>>8
                    #adc1_Frame1 = adc1_Frame1>>8
                    adc1_Frame2 = adc1_Frame2>>8
                    if BL<8:
                        fr_array[WL][BL][i] = 3.3*(adc0_Frame2/2**16)
                        print('ADC0 Frame 2 output ' + str(3.3*(adc0_Frame2/2**16)))
                    else:
                        fr_array[WL][BL][i] = 3.3*(adc1_Frame2/2**16)
                        print('ADC1 Frame 2 output ' + str(3.3*(adc1_Frame2/2**16)))
                    break
        
            
        print('adc_data = ' + str(hex(adc_data)))
        av[l][WL][BL] = np.mean(fr_array[WL][BL])
        print('Vbl average: '+str(av[l][WL][BL]))
        
        
        delta_t = T[l]*40e-9
        print('delta_t: ' + str(delta_t))


        tau = C[BL]/delta_t
        if (positive_read_pulse):   
            if (av[l][WL][BL] >= ( vref + (vp - vref)*(1 - np.exp(-0.2)) )):
                g_tot[BL] = 0.2*tau
                print('sum of g in BL: ' + str(g_tot[BL]))
                print('BL index = ' + str(BL))
                print('\n')
                break
        else:
            if (av[l][WL][BL] <= ( vref - (vref - vn)*(1 - np.exp(-0.2)) )):
                g_tot[BL] = 0.2*tau
                print('sum of g in BL: ' + str(g_tot[BL]))
                print('BL index = ' + str(BL))
                print('\n')
                break
        
        
        # For Gohm measurement        
        #if (positive_read_pulse): 
        #   if (av[l][WL][BL] >= ( vref + (vp-vref)*(1 - np.exp(-0.1)) )):               
        #       g_tot[BL] = 0.1*(C/delta_t)
        #       print('sum of g in BL: ' + str(g_tot[BL]))
        #       print('BL index = ' + str(BL))
        #       print('\n')
        #       break
        #else:
        #   if (av[l][WL][BL] <= ( vref - (vref - vn)*(1 - np.exp(-0.1)) )):               
        #       g_tot[BL] = 0.1*(C/delta_t)
        #       print('sum of g in BL: ' + str(g_tot[BL]))
        #       print('BL index = ' + str(BL))
        #       print('\n')
        #       break
        print('\n')
    
        
    if BL<7:
        adc_data = adc_data + 1
    elif BL==7:
        adc_data = 0x081100
    else: 
        adc_data = adc_data + 1
        
        
    print('adc switch = '+ str(hex(adc_switch)) + '\n')
    adc_switch = adc_switch<<1  
    
    
print(g_tot)    


#%% Read operation, steady state or transient measurement accounting for total conductance in BL


all_switches_off(dev)
write_FPGA(dev, 0x00, 0x01)                                             # Reset verilog Finite State Machine 
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state))
write_FPGA(dev, 0x10, 0x00)                                             # de-assert FORM trigger


if (positive_read_pulse):
    write_FPGA(dev, 0x14, 0x00000000)                       # Vn switch select, [15:0] for WL, [31:16] for BL
else:
    write_FPGA(dev, 0x13, 0x00000000)                       # Vp switch select, [15:0] for WL, [31:16] for BL 


N               = 10
T               = [40000]                                               # for a steady state measurement
#T              = [500000000]                                           # for a steady state measurement in GOhm range, delta t = 20 sec
#T              = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]            # for a transient measurement


fr_array        = np.zeros((16,16,N))
av              = np.zeros((16,16))
g               = np.zeros((len(T),16,16))
R               = np.zeros((len(T),16,16))


C               = np.zeros((256,1))
# Define variable to load the dataframe
dataframe       = openpyxl.load_workbook(path+"/excel data/cap characterisation/cap characterisation w proxy.xlsx")
# Define variable to read sheet
dataframe1      = dataframe.active
j = 0    
# Iterate the loop to read the cell values
for row in range(1, 17):
    for col in dataframe1.iter_cols(2, dataframe1.max_column):
        C[j] = col[row].value
        j += 1
C               = np.reshape(C, (16, 16))             


for l in range(len(T)):
  
    
    write_FPGA(dev, 0x04, 0x03)                 # reset fifo counter
    write_FPGA(dev, 0x04, 0x00)
  
    
    adc_data = 0x081100
    adc_switch = 0x00000001
    if (positive_read_pulse):   
        vp_WL_switch    = 0x00000001
    else:
        vn_WL_switch    = 0x00000001
    vref_WL = 0xfffe
    
    
    for WL in range(16): 
        if (positive_read_pulse):
            write_FPGA(dev, 0x13, vp_WL_switch)                     # Vn switch select during read, [15:0] for WL, [31:16] for BL 
        else: 
            write_FPGA(dev, 0x14, vn_WL_switch)                     # Vn switch select during read, [15:0] for WL, [31:16] for BL 


        for BL in range(16):
           
            
            vref_BL             = (2**16 - 1 - adc_switch) << 16
            vref_switch         = vref_BL + vref_WL 
            write_FPGA(dev, 0x12, vref_switch)                      # Vref switch select during read
            print('vref_switch = '+ str(hex(vref_switch))) 
            write_FPGA(dev, 0x15, adc_switch)                       # select capacitor for ADC sampling
            
            
            for i in range(N):
                done = 0
                if BL<8:
                    write_FPGA(dev, 0x1c, adc_data)                 # specify ADC0 channel to read from -- bits [7:0]
                else:
                    write_FPGA(dev, 0x1f, adc_data)                 # specify ADC1 channel to read from -- bits [7:0]
                write_FPGA(dev, 0x0f, T[l])                         # charging duration = #cycles*(10n)
                write_FPGA(dev, 0x17, 0x01)                         # READ trigger flag asserted 
                while True:
                    done = read_FPGA(dev, 0x36)
                    if done == 1:
                        write_FPGA(dev, 0x17, 0x00)
                        #adc0_Frame1 = read_FPGA(dev, 0x31)
                        adc0_Frame2 = read_FPGA(dev, 0x32)
                        #adc1_Frame1 = read_FPGA(dev, 0x33)
                        adc1_Frame2 = read_FPGA(dev, 0x34)
                        #adc0_Frame1 = adc0_Frame1>>8
                        adc0_Frame2 = adc0_Frame2>>8
                        #adc1_Frame1 = adc1_Frame1>>8
                        adc1_Frame2 = adc1_Frame2>>8
                        if BL<8:
                            fr_array[WL][BL][i] = 3.3*(adc0_Frame2/2**16)
                        else:
                            fr_array[WL][BL][i] = 3.3*(adc1_Frame2/2**16)
                        #print('ADC0 Frame 2 output ' + str(3.3*(adc0_Frame2/2**16)))
                        #print('ADC1 Frame 2 output ' + str(3.3*(adc1_Frame2/2**16)))
                        break
            
            
            print('adc_data = ' + str(hex(adc_data)))
            if BL<7:
                adc_data = adc_data + 1
            elif BL==7:
                adc_data = 0x081100
            else: 
                adc_data = adc_data + 1
           
            
            print('adc switch = '+ str(hex(adc_switch)) + '\n')
            adc_switch = adc_switch<<1
            av[WL][BL] = np.mean(fr_array[WL][BL])
            
            
            delta_t = T[l]*40e-9
            if (positive_read_pulse):   
                g[l][WL][BL] = ( (av[WL][BL] - vref)/(vp - vref) ) * g_tot[BL]                    # steady state measurement 
                #g[l][WL][BL] = ( ( (av[WL][BL] - vref)/(vp - vref)) * g_tot[BL])/( 1 - np.exp(-(delta_t/C[WL][BL]) * g_tot[BL] ) )        # transient measurement
            else:
                g[l][WL][BL] = ( (vref - av[WL][BL])/(vref - vn) ) * g_tot[BL]                    # steady state measurement 
                #g[l][WL][BL] = ( ( (vref - av[WL][BL])/(vref - vn) * g_tot[BL] )/( 1 - np.exp(-(delta_t/C[WL][BL]) * g_tot[BL] ) )        # transient measurement
            R[l][WL][BL] = 1/g[l][WL][BL]
            
            
        adc_data =  0x081100
        adc_switch = 0x00000001
            
            
        vref_WL = vref_WL<<1   
        vref_WL = vref_WL+1
        vref_WL = vref_WL & (0x0000ffff)
        #print('vref_WL = '+ str(hex(vref_WL)))
        
        
        print('vp_WL_switch = '+ str(hex(vp_WL_switch)))
        print('WL = ' +str(WL))
        print('\n')
        if (positive_read_pulse):
            vp_WL_switch= vp_WL_switch<<1
        else:
            vn_WL_switch= vn_WL_switch<<1
    
print(g)
print(R)


#%% plot steady-state measurements


R_true = np.zeros((16,16))
g_true = np.zeros((16,16))
g_BL_true = np.zeros((16, 1))


WL_map = [5, 11, 14, 2, 1, 9, 10, 4, 7, 13, 16, 8, 3, 15, 12, 6]
BL_map = [8, 14, 9, 7, 4, 16, 13, 3, 12, 6, 11, 1, 10, 2, 15, 5]


l = 0
for i in range(0,16):
    for j in range(0,16):
       R_true[WL_map[i]-1][BL_map[j]-1] = R[l][i][j]
       g_true[WL_map[i]-1][BL_map[j]-1] = g[l][i][j]
for j in range(0, 16):
    g_BL_true[BL_map[j]-1] = g_tot[j] 


run = 1
datestamp = 230110
if (positive_read_pulse):
    polarity = 'plus'
else:
    polarity = 'minus'
    
array = '2.2 1'
df = pd.DataFrame(g[l],
                  columns = ['BL8', 'BL14', 'BL9', 'BL7', 'BL4', 'BL16', 'BL13','BL3', 'BL12', 'BL6', 'BL11', 'BL1', 'BL10', 'BL2', 'BL15', 'BL5'], 
                  index = ['WL8','WL14', 'WL9', 'WL7', 'WL4','WL16', 'WL13', 'WL3', 'WL12','WL6', 'WL11', 'WL1', 'WL10','WL2', 'WL15', 'WL5'])
#df.to_csv(path+'/excel data/array '+array+'/g_as_is_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_'+str(polarity)+'_pulse_run'+str(run)+'_'+str(datestamp)+'.csv')       
df = pd.DataFrame(R_true, 
                  columns = ['BL1', 'BL2', 'BL3', 'BL4', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL10', 'BL11', 'BL12', 'BL13', 'BL14', 'BL15', 'BL16'], 
                  index = ['WL1','WL2', 'WL3', 'WL4', 'WL5','WL6', 'WL7', 'WL8', 'WL9','WL10', 'WL11', 'WL12', 'WL13','WL14', 'WL15', 'WL16'])
#df.to_csv(path+'/excel data/array '+array+'/Res_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_'+str(polarity)+'_pulse_run'+str(run)+'_'+str(datestamp)+'.csv')
plt.close()


# setting font sizeto 30
plt.rcParams.update({'font.size': 35})


plt.figure(figsize=(20, 20))
ax = plt.axes() 
p = plt.imshow(R_true, cmap='hot', norm=colors.LogNorm())
plt.colorbar(p) 
x = [i for i in range(0,16)]
x_map = [i for i in range(1,17)]
ax.set_xticks(x)
ax.set_xticklabels(x_map)
y = [i for i in range(0,16)]
y_map = [i for i in range(1,17)]
ax.set_yticks(y)
ax.set_yticklabels(y_map)
#plt.show()
plt.xlabel('BL')
plt.ylabel('WL')
#plt.title('Resistance, Vread = ' + str(round(vread, 2)) + 'v, Read pulse polarity = ' + str(polarity) + ', \nCharging duration = '+ str(T[l]*40e-9))
plt.title('Resistance, Vread = ' + str(round(vread, 2)) + 'v, \nCharging duration = '+ str(T[l]*40e-9))
#plt.savefig(path+'/plots/array '+array+'/Res_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_'+str(polarity)+'_pulse_run'+str(run)+'_'+str(datestamp)+'.png')


#%% plot steady-state measurements for a subset of array


df = pd.read_csv(path+'/excel data/array '+array+'/Res_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_'+str(polarity)+'_pulse_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
WL1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
WL1 = WL1 - np.ones(len(WL1)).astype(int)
#BL = [1, 2, 3, 4, 6, 7, 9, 10, 11, 13, 14, 15, 16]
BL= [5]
BL = BL - np.ones(len(BL)).astype(int)


df1 = np.zeros((len(WL1), len(BL)))
for i in range(len(WL1)):
    for j in range(len(BL)):
        df1[i, j] = df[WL1[i], BL[j]]


'''
WL2 = [2, 4, 6, 13, 14, 16]
WL2 = WL2 - np.ones(len(WL2)).astype(int)
df2 = np.zeros((len(WL2), len(BL)))
for i in range(len(WL2)):
    for j in range(len(BL)):
        df2[i, j] = df[WL2[i], BL[j]]

del df


df = pd.read_csv(path+'/excel data/array '+array+'/Res_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_minus_pulse_run2_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df3 = np.zeros((len(WL1), len(BL)))
for i in range(len(WL1)):
    for j in range(len(BL)):
        df3[i, j] = df[WL1[i], BL[j]]

df4 = np.zeros((len(WL2), len(BL)))
for i in range(len(WL2)):
    for j in range(len(BL)):
        df4[i, j] = df[WL2[i], BL[j]]

del df
'''

polarity = 'plus'
# setting font sizeto 30
plt.rcParams.update({'font.size': 35})

plt.figure(figsize=(20, 20))
ax = plt.axes() 
x = [i for i in range(0,len(BL))]
ax.set_xticks(x)
ax.set_xticklabels(BL + np.ones(len(BL)).astype(int))
plt.xlabel('BL')
y1 = [i for i in range(0,len(WL1))]
ax.set_yticks(y1)
ax.set_yticklabels(WL1 + np.ones(len(WL1)).astype(int))
plt.ylabel('WL')
#plt.title('Resistance, Vref = 0.7v, read pulse polarity - '+str(polarity))
plt.title('Resistance, Vread = ' + str(round(vread, 2)) + 'v, \nCharging duration = '+ str(T[l]*40e-9))
p1 = plt.imshow(df1, cmap='hot', norm=colors.LogNorm())
plt.colorbar(p1)
plt.savefig(path+'/plots/array '+array+'/WL, BL choice for Double Differential Scheme, Low Res, vread_'+str(round(vread, 2))+'v_'+str(polarity)+' pulse, run'+str(run)+', '+str(datestamp)+'.png')
del ax


'''
plt.figure(figsize=(20, 20))
ax = plt.axes() 
ax.set_xticks(x)
ax.set_xticklabels(BL + np.ones(len(BL)).astype(int))
plt.xlabel('BL')
y2 = [i for i in range(0,len(WL2))]
ax.set_yticks(y2)
ax.set_yticklabels(WL2 + np.ones(len(WL2)).astype(int))
plt.ylabel('WL')
plt.title('Resistance, Vref = 0.7v, read pulse polarity - plus')
p2 = plt.imshow(df2, cmap='hot', norm=colors.LogNorm())
plt.colorbar(p2)
plt.savefig(path+'/plots/array '+array+'/WL, BL choice for Double Differential Scheme, High Res, '+str(polarity)+' pulse, run'+str(run)+', '+str(datestamp)+'.png')
del ax


polarity = 'minus'
plt.figure(figsize=(20, 20))
ax = plt.axes()
ax.set_xticks(x) 
ax.set_xticklabels(BL + np.ones(len(BL)).astype(int))
plt.xlabel('BL')
ax.set_yticks(y1)
ax.set_yticklabels(WL1 + np.ones(len(WL1)).astype(int))
plt.ylabel('WL')
plt.title('Resistance, Vref = 0.7v, read pulse polarity - minus')
p3 = plt.imshow(df3, cmap='hot', norm=colors.LogNorm())
plt.colorbar(p3)
plt.savefig(path+'/plots/array '+array+'/WL, BL choice for Double Differential Scheme, Low Res, '+str(polarity)+' pulse, run'+str(run)+', '+str(datestamp)+'.png')
del ax



plt.figure(figsize=(20, 20))
ax = plt.axes()
ax.set_xticks(x) 
ax.set_xticklabels(BL + np.ones(len(BL)).astype(int))
plt.xlabel('BL')
ax.set_yticks(y2)
ax.set_yticklabels(WL2 + np.ones(len(WL2)).astype(int))
plt.ylabel('WL')
plt.title('Resistance, Vref = 0.7v, read pulse polarity - minus')
p4 = plt.imshow(df4, cmap='hot', norm=colors.LogNorm())
plt.colorbar(p4)
plt.savefig(path+'/plots/array '+array+'/WL, BL choice for Double Differential Scheme, Hgih Res, '+str(polarity)+' pulse, run'+str(run)+', '+str(datestamp)+'.png')
del ax
'''


del BL 
del df1
'''
del df2
del df3
del df4
'''


#%% Histogram -- single cell measurements


#cutoff_ohms = 1e13
df = pd.DataFrame()
#df['single cell'] = pd.read_excel(path+'/excel data/array '+array+'/array_read.xlsx', header = None).stack().values
print(df)


# Histogram -- pcb measurement
#cutoff_ohms = 1e13
#df['crossbar_run1'] = pd.read_csv(path+'/excel data/array '+array+'/T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_run1_221102.csv', header = 0, index_col = 0).stack().values
#df['crossbar_run2'] = pd.read_csv(path+'/excel data/array '+array+'/T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_run2_221102.csv', header = 0, index_col = 0).stack().values
#df['crossbar_run3'] = pd.read_csv(path+'/excel data/array '+array+'/T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_run3_221102.csv', header = 0, index_col = 0).stack().values
#df['crossbar_run4'] = pd.read_csv(path+'/excel data/array '+array+'/T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_run4_221102.csv', header = 0, index_col = 0).stack().values
#df['crossbar_run5'] = pd.read_csv(path+'/excel data/array '+array+'/T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_run5_221102.csv', header = 0, index_col = 0).stack().values
#df['crossbar_run6'] = pd.read_csv(path+'/excel data/array '+array+'/T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_run6_221103.csv', header = 0, index_col = 0).stack().values
df['crossbar_run1'] = pd.read_csv(path + '/excel data/array '+array+'/Res_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_run1_221109.csv', header = 0, index_col = 0).stack().values
df['crossbar_run2'] = pd.read_csv(path+'/excel data/array '+array+'/Res_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_plus_pulse_run3_221110.csv', header = 0, index_col = 0).stack().values
df['crossbar_run3'] = pd.read_csv(path+'/excel data/array '+array+'/Res_T_1.6msec_ss_vread_'+str(round(vread, 2))+'v_minus_pulse_run4_221110.csv', header = 0, index_col = 0).stack().values
print(df)
#df['crossbar'] = df.stack().values
#flatten_df = flatten_df[flatten_df<cutoff_ohms] 


# setting font sizeto 30
plt.rcParams.update({'font.size': 35})


plt.figure(figsize=(20, 20))
ax = pd.DataFrame(df).plot.hist(bins=np.logspace(1, 13, num=150),
                                   logx = True,
                                   #ax=ax, 
                                   alpha = 0.8)
ax.set_xlabel('Resistance (ohms)')
ax.set_title('Resistance distribution of 16x16 RRAM crossbar')
#ax.get_legend().remove()
#ax.legend('single cell','crossbar')
plt.savefig(path+'/plots/array '+array+'/crossbar vref 0v, 0.7v and plus, minus read pulse polarity comparison '+str(datestamp)+'.png')


#%% Matrix-Vector Multiplication, non-differential encoding 


all_switches_off(dev)
write_FPGA(dev, 0x00, 0x01)                                             # Reset verilog Finite State Machine 
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state))
write_FPGA(dev, 0x10, 0x00)                                             # de-assert FORM trigger


vp              = 1.1
vn              = 0.3
vref            = 0.7
vread           = vp - vref
write_DAC(dev, VP_RRAM, vp)
write_DAC(dev, VN_RRAM, vn)
write_DAC(dev, VREF_RRAM, vref)


positive_read_pulse        = 0                                          # Sensing using Vref + Vpulse scheme if set to 1
negative_read_pulse        = (1 - positive_read_pulse)                  # Sensing using Vref - Vpulse scheme if set to 1


if (positive_read_pulse):
    write_FPGA(dev, 0x14, 0x00000000)                                   # Vn switch select, [15:0] for WL, [31:16] for BL
else:
    write_FPGA(dev, 0x13, 0x00000000)                                   # Vp switch select, [15:0] for WL, [31:16] for BL 


N               = 10
T               = [40000]  


WL_map = [5, 11, 14, 2, 1, 9, 10, 4, 7, 13, 16, 8, 3, 15, 12, 6]
BL_map = [8, 14, 9, 7, 4, 16, 13, 3, 12, 6, 11, 1, 10, 2, 15, 5]         


WL_pulse = [1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 15]                       # Specifying WLs to send input pulses to


WL_true = np.zeros(len(WL_pulse))
WL_init = np.zeros(len(WL_true))


for i in range(len(WL_pulse)):
    WL_true[i] = WL_map.index(WL_pulse[i])
    WL_init[i] = (0x0001)<<int(WL_true[i])  
WL_init      = WL_init.astype(int)

WL_seq       = WL_init.copy()

# Generate WL input combinations from WL_pulse set
for j in range(1, len(WL_init)):
    for i in range(len(WL_init) - j):
        sum = 0
        for k in range(j+1):
            sum = sum + WL_init[i+k]
        WL_seq = np.append(WL_seq, sum)
   
vref_WL_seqb    = WL_seq     
vref_WL_seq     = vref_WL_seqb*0
for  i in range(len(vref_WL_seqb)):
    vref_WL_seq[i] = 2**16 - 1 - vref_WL_seqb[i]        

                                                     
adc_data_seq    = [0x081105, 0x081104, 0x081107, 0x081101, 0x081103, 0x081100,                      # BL2, 4, 5, 6, 7, 8,
                   0x081102, 0x081102, 0x081106, 0x081101, 0x081105]                                # BL9, 11, 13, 14, 16          
adc_switch_seq  = [0x00002000, 0x00000010, 0x00008000, 0x00000200, 0x00000008, 0x00000001, 
                   0x00000004, 0x00000400, 0x00000040, 0x00000002, 0x00000020]                      # adc_switch_seq and adc_data_seq should be same length vectors
MVM_out         = np.zeros((len(WL_seq), len(adc_data_seq), N))
MVM_out_av      = np.zeros((len(WL_seq), len(adc_data_seq)))
MVM_true        = np.zeros((len(WL_seq), len(adc_data_seq)))


for l in range(len(T)):
    
    
    write_FPGA(dev, 0x04, 0x03)                                 # reset fifo counter
    write_FPGA(dev, 0x04, 0x00)
    
    
    for m in range(len(WL_seq)):
        
        
        if (positive_read_pulse):
            vp_WL_switch        = int(WL_seq[m])
            write_FPGA(dev, 0x13, vp_WL_switch)                             # Vp switch select during read, [15:0] for WL, [31:16] for BL
        else:
            vn_WL_switch        = WL_seq[m]
            write_FPGA(dev, 0x14, int(vn_WL_switch))                        # Vp switch select during read, [15:0] for WL, [31:16] for BL
        vref_WL_switch          = vref_WL_seq[m] 
        
        
        for n in range(len(adc_data_seq)):
           
            
            adc_data                = adc_data_seq[n]
            adc_switch              = adc_switch_seq[n]
            vref_BL_switch = ((~(adc_switch & (0x0000ffff))) & 0x0000ffff)<<16
            write_FPGA(dev, 0x12, int(vref_BL_switch + vref_WL_switch))     # Vref switch select during read
            print('vref_switch = '+ str(hex(vref_BL_switch + vref_WL_switch)))
           
            
            write_FPGA(dev, 0x15, adc_switch)                               # select capacitor for ADC sampling
            i = 0
            while (i<N):
                done = 0
                if int(np.log2(adc_switch_seq[n]))<8:
                    write_FPGA(dev, 0x1c, adc_data)                         # specify ADC0 channel to read from -- bits [7:0]
                else:
                    write_FPGA(dev, 0x1f, adc_data)                         # specify ADC1 channel to read from -- bits [7:0]
                write_FPGA(dev, 0x0f, T[l])                                 # charging duration = #cycles*(10n)
                write_FPGA(dev, 0x17, 0x01)                                 # READ trigger flag asserted 
                while True:
                    done = read_FPGA(dev, 0x36)
                    if done == 1:
                        write_FPGA(dev, 0x17, 0x00)
                        adc0_Frame2 = read_FPGA(dev, 0x32)
                        adc1_Frame2 = read_FPGA(dev, 0x34)
                        adc0_Frame2 = adc0_Frame2>>8
                        adc1_Frame2 = adc1_Frame2>>8
                        if int(np.log2(adc_switch_seq[n]))<8:
                            MVM_out[m][n][i] = 3.3*(adc0_Frame2/2**16)
                        else:
                            MVM_out[m][n][i] = 3.3*(adc1_Frame2/2**16)
                        break
                i+=1
            MVM_out_av[m][n] = np.mean(MVM_out[m][n])
            j = 0
            outer_product = 0
            X = WL_seq[m]
            while j<16:
                outer_product = outer_product + ((X & 0x01) * g[l][j][int(np.log2(adc_switch_seq[n]))])                             
                X = X >> 1
                j+=1
            if (positive_read_pulse):  
                MVM_true[m][n] = vref + (outer_product*(vp - vref)) / g_tot[int(np.log2(adc_switch_seq[n]))]
            else:
                MVM_true[m][n] = vref - (outer_product*(vref - vn)) / g_tot[int(np.log2(adc_switch_seq[n]))]
        
        
print('MVM out measured: \n' + str(MVM_out_av))
print('MVM true: \n' + str(MVM_true))


if (positive_read_pulse):
    polarity = 'plus'
else:
    polarity = 'minus'


df = pd.DataFrame(MVM_out_av, 
                  columns = ['BL2','BL4', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL11', 'BL13', 'BL14', 'BL16'])
                  #index = ['WL5', 'WL7', 'WL8','WL9', 'WL10', 'WL11', 'WL12', 'WL13', 
                  #         'WL5,7', 'WL7,8', 'WL8,9', 'WL9,10', 'WL10,11', 'WL11,12', 'WL12,13', 
                  #         'WL5, 7-8', 'WL7-9', 'WL8-10', 'WL9-11', 'WL10-12', 'WL11-13', 
                  #         'WL5, 7-9', 'WL7-10', 'WL8-11', 'WL9-12', 'WL10-13', 
                  #         'WL5,7-10', 'WL7-11', 'WL8-12', 'WL9-13', 
                  #         'WL5, 7-11', 'WL7-12', 'WL8-13', 
                  #         'WL5,7-12', 'WL7-13',
                  #         'WL5,7-13'])
df.to_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Non-Differential_Scheme_read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.csv')
df = pd.DataFrame(MVM_true, 
                  columns = ['BL2','BL4', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL11', 'BL13', 'BL14', 'BL16'])
                  #index = ['WL5', 'WL7', 'WL8','WL9', 'WL10', 'WL11', 'WL12', 'WL13', 
                  #         'WL5,7', 'WL7,8', 'WL8,9', 'WL9,10', 'WL10,11', 'WL11,12', 'WL12,13', 
                  #         'WL5, 7-8', 'WL7-9', 'WL8-10', 'WL9-11', 'WL10-12', 'WL11-13', 
                  #         'WL5, 7-9', 'WL7-10', 'WL8-11', 'WL9-12', 'WL10-13', 
                  #         'WL5, 7-10', 'WL7-11', 'WL8-12', 'WL9-13', 
                  #         'WL5, 7-11', 'WL7-12', 'WL8-13', 
                  #         'WL5,7-12', 'WL7-13',
                  #         'WL5,7-13'])
df.to_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Non-Differential_Scheme_read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.csv')
        
        
#%% Plot MVM, non-differential encoding
  

'''
x = np.linspace(0, len(MVM_true), len(MVM_true)) 
BL = [2, 4, 5, 6, 7, 8, 9, 11, 13, 14, 16]
for i in range(len(BL)):
    plt.figure(figsize=(20, 20))
    plt.scatter(x, MVM_true[:, i], 
                alpha = 0.7, 
                label = 'Expected MVM Output', 
                marker = '^')
    plt.scatter(x, MVM_out_av[:, i], 
                alpha = 0.7,
                label = 'Measured MVM Output',
                marker = 's')
    plt.ylabel('MVM Output (V)')
    plt.title('MVM Output - Measured vs Expected, BL' + str(BL[i]))
    plt.legend()
    plt.savefig(path + '/plots/array '+array+'/MVM/BL'+str(BL[i])+'_Read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.png')
    plt.show()         
'''


dim1 = np.shape(MVM_true)[0]
dim2 = np.shape(MVM_true)[1]


MVM_true_no_offset = np.zeros((dim1, dim2))                                     # Remove vref voltage offset from cxpected MVM
MVM_meas_no_offset = np.zeros((dim1, dim2))                                     # Remove vref voltage offset from measured MVM
for i in range(dim1):
    for j in range(dim2):
        MVM_true_no_offset[i][j] = MVM_true[i][j] - vref
        MVM_meas_no_offset[i][j] = MVM_out_av[i][j] - vref


from sklearn.metrics import mean_squared_error
import math
MSE = mean_squared_error(np.reshape(MVM_true_no_offset, (dim1*dim2, 1)), np.reshape(MVM_meas_no_offset, (dim1*dim2, 1)))
RMSE = math.sqrt(MSE)
print("Root Mean Square Error:\n")
print(RMSE)


# setting font sizeto 30
plt.rcParams.update({'font.size': 25})


if (positive_read_pulse):
    polarity = 'plus'
else:
    polarity = 'minus'
plt.figure(figsize=(15, 10))
x = np.linspace(min(np.min(MVM_true_no_offset), np.min(MVM_meas_no_offset)), max(np.max(MVM_true_no_offset), np.max(MVM_meas_no_offset)), 100)    
plt.scatter(np.reshape(MVM_true_no_offset, (dim1*dim2, 1)), np.reshape(MVM_meas_no_offset, (dim1*dim2, 1)), 
            alpha = 0.8,
            #label = 'Measured MVM Output',
            marker = 's',
            linewidth = 3)


plt.plot(x, x, 
         alpha = 0.8,
         #label = 'Ideal distribution',
         color = 'orange',
         linewidth = 3)


plt.ylabel('Measured MVM Output (V)')
plt.xlabel('Expected MVM Output (V)')
plt.title('MVM Output - Measured vs Expected')
plt.grid(True, which='both')
#plt.legend()
plt.savefig(path + '/plots/array '+array+'/MVM/MVM_Output_Read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.png')
plt.show()


#%% Combined plot for MVM for positive and negative polarity WL input pulses, non-differential encoding


run         = 1
datestamp   = 221117
polarity    = 'plus'
df1         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Non-Differential_Scheme_read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
dim1        = np.shape(df1)[0]
dim2        = np.shape(df1)[1]
df1         = np.reshape(df1, (dim1*dim2, 1))
df2         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Non-Differential_Scheme_read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df2         = np.reshape(df2, (dim1*dim2, 1))
 

polarity = 'minus'
df3         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Non-Differential_Scheme_read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df3         = np.reshape(df3, (dim1*dim2, 1))
df4         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Non-Differential_Scheme_read_pulse_polarity_'+str(polarity)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df4         = np.reshape(df4, (dim1*dim2, 1))


MVM_Expected = np.concatenate((df1, df3))
MVM_Measured = np.concatenate((df2, df4))
MVM_Expected_no_offset = np.zeros((len(MVM_Expected), 1))                       # Remove vref voltage offset from cxpected MVM
MVM_Measured_no_offset = np.zeros((len(MVM_Measured), 1))                       # Remove vref voltage offset from measured MVM


for i in range(len(MVM_Expected)):
    MVM_Expected_no_offset[i] = MVM_Expected[i] - vref
    MVM_Measured_no_offset[i] = MVM_Measured[i] - vref


df5 = pd.DataFrame(MVM_Expected_no_offset)
df5.to_excel(path + '/excel data/array '+array+'/MVM_out_Expected_Non-Differential_Scheme_combined_data_run'+str(run)+'_'+str(datestamp)+'.xlsx')
df6 = pd.DataFrame(MVM_Measured_no_offset)
df6.to_excel(path + '/excel data/array '+array+'/MVM_out_Measured_Non-Differential_Scheme_combined_data_run'+str(run)+'_'+str(datestamp)+'.xlsx')
        
      
        
from sklearn.metrics import mean_squared_error
import math
MSE = mean_squared_error(MVM_Expected_no_offset, MVM_Measured_no_offset)
RMSE = math.sqrt(MSE)
print("Root Mean Square Error:\n")
print(RMSE)


# setting font sizeto 30
plt.rcParams.update({'font.size': 30})
plt.figure(figsize=(15, 10))


plt.scatter(MVM_Expected_no_offset, MVM_Measured_no_offset, 
            alpha = 0.8,
            marker = 's',
            linewidth = 3)


x = np.linspace(min(np.min(MVM_Expected_no_offset), np.min(MVM_Measured_no_offset)), max(np.max(MVM_Expected_no_offset), np.max(MVM_Measured_no_offset)), 100)    
plt.plot(x, x, 
         alpha = 0.8,
         color = 'orange',
         linewidth = 3)


plt.ylabel('Measured MVM Output (V)')
plt.xlabel('Expected MVM Output (V)')
plt.title('MVM Output - Measured vs Expected \nNon-differential encoding')
plt.grid(True, which='both')
plt.savefig(path + '/plots/array '+array+'/MVM/MVM_Output_Non_Differential_Read_run'+str(run)+'_'+str(datestamp)+'.png')
plt.show()


#%% MVM, single differential encoding


all_switches_off(dev)
write_FPGA(dev, 0x00, 0x01)                                             # Reset verilog Finite State Machine 
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state))
write_FPGA(dev, 0x10, 0x00)                                             # de-assert FORM trigger


vp              = 1.1
vn              = 0.3
vref            = 0.7
vread           = vp - vref
write_DAC(dev, VP_RRAM, vp)
write_DAC(dev, VN_RRAM, vn)
write_DAC(dev, VREF_RRAM, vref)


write_FPGA(dev, 0x14, 0x00000000)                                                                   # Vn switch select, [15:0] for WL, [31:16] for BL
write_FPGA(dev, 0x13, 0x00000000)                                                                   # Vp switch select, [15:0] for WL, [31:16] for BL 


N               = 10
T               = [40000]                                                                           # for a steady state measurement
#T              = [500000000]                                                                       # for a steady state measurement in GOhm range, delta t = 20 sec


WL_map = [5, 11, 14, 2, 1, 9, 10, 4, 7, 13, 16, 8, 3, 15, 12, 6]
BL_map = [8, 14, 9, 7, 4, 16, 13, 3, 12, 6, 11, 1, 10, 2, 15, 5]         


MVM_out_type = 'negative'

if MVM_out_type == 'positive':
    vp_WL = [1, 3, 5, 7, 8, 9, 11, 15]
    vn_WL = [2, 4, 6, 10, 14, 13, 16, 12]
elif MVM_out_type == 'zero':
    vp_WL = [1, 2, 5, 6, 8, 14, 11, 16]
    vn_WL = [3, 4, 7, 10, 9, 13, 15, 12]
elif MVM_out_type == 'negative':
    vp_WL = [2, 4, 6, 10, 14, 13, 16, 12]
    vn_WL = [1, 3, 5, 7, 8, 9, 11, 15]
else:
    print("Invalid MVM output type!")
    
vp_WL_true = np.zeros(len(vp_WL))
vn_WL_true = np.zeros(len(vn_WL))
vp_WL_init = np.zeros(len(vp_WL_true))
vn_WL_init = np.zeros(len(vn_WL_true))


for i in range(len(vp_WL)):
    vp_WL_true[i] = WL_map.index(vp_WL[i])
    vp_WL_init[i] = (0x0001)<<int(vp_WL_true[i])  
vp_WL_init      = vp_WL_init.astype(int)

vp_WL_seq       = vp_WL_init.copy()
  
for j in range(1, len(vp_WL_init)):
    for i in range(len(vp_WL_init) - j):
        sum = 0
        for k in range(j+1):
            sum = sum + vp_WL_init[i+k]
        vp_WL_seq = np.append(vp_WL_seq, sum)
      
        
for i in range(len(vn_WL)):
    vn_WL_true[i] = WL_map.index(vn_WL[i])
    vn_WL_init[i] = (0x0001)<<int(vn_WL_true[i]) 
vn_WL_init      = vn_WL_init.astype(int)
    
vn_WL_seq       = vn_WL_init.copy()

for j in range(1, len(vn_WL_init)):
    for i in range(len(vn_WL_init) - j):
        sum = 0
        for k in range(j+1):
            sum = sum + vn_WL_init[i+k]
        vn_WL_seq = np.append(vn_WL_seq, sum)
        
        
vref_WL_seqb    = np.add(vp_WL_seq, vn_WL_seq)     
vref_WL_seq     = vref_WL_seqb*0
for  i in range(len(vref_WL_seqb)):
    vref_WL_seq[i] = 2**16 - 1 - vref_WL_seqb[i]
                                                                                                                                                                                           
                                                                                             
adc_data_seq    = [0x081105, 0x081107, 0x081101, 0x081103, 0x081100,                                # BL2, 5, 6, 7, 8,
                   0x081102, 0x081102, 0x081106, 0x081101, 0x081105]                                # BL9, 11, 13, 14, 16          

adc_switch_seq  = [0x00002000, 0x00008000, 0x00000200, 0x00000008, 0x00000001, 
                   0x00000004, 0x00000400, 0x00000040, 0x00000002, 0x00000020]                      


MVM_out_SD      = np.zeros((len(vp_WL_seq), len(adc_data_seq), N))
MVM_out_SD_av   = np.zeros((len(vp_WL_seq), len(adc_data_seq)))
MVM_true_SD     = np.zeros((len(vp_WL_seq), len(adc_data_seq)))


l = 0
while (l<len(T)):
    
    
    write_FPGA(dev, 0x04, 0x03)                             # reset fifo counter
    write_FPGA(dev, 0x04, 0x00)
    
    
    m = 0
    while (m<len(vref_WL_seq)):
        
        
        vp_WL_switch        = vp_WL_seq[m]
        write_FPGA(dev, 0x13, int(vp_WL_switch))                 # Vp switch select during read, [15:0] for WL, [31:16] for BL
        print('vp_WL_switch: '+str(hex(vp_WL_switch)))
        vn_WL_switch        = vn_WL_seq[m]
        write_FPGA(dev, 0x14, int(vn_WL_switch))                 # Vp switch select during read, [15:0] for WL, [31:16] for BL
        print('vn_WL_switch: '+str(hex(vn_WL_switch)))
        vref_WL_switch      = vref_WL_seq[m] 
        print('vref_WL_switch: '+str(hex(vref_WL_switch)))
        
        n = 0
        while (n<len(adc_data_seq)):
           
            
            adc_data                = adc_data_seq[n]
            adc_switch              = adc_switch_seq[n]
            vref_BL_switch = ((~(adc_switch & (0x0000ffff))) & 0x0000ffff)<<16
            print('vref_BL_switch: '+str(hex(vref_BL_switch)))
            write_FPGA(dev, 0x12, int(vref_BL_switch + vref_WL_switch))     # Vref switch select during read
            print('vref_switch = '+ str(hex(vref_BL_switch + vref_WL_switch)))
           
            
            write_FPGA(dev, 0x15, adc_switch)               # select capacitor for ADC sampling
            i = 0
            while (i<N):
                done = 0
                if int(np.log2(adc_switch_seq[n]))<8:
                    write_FPGA(dev, 0x1c, adc_data)                         # specify ADC0 channel to read from -- bits [7:0]
                else:
                    write_FPGA(dev, 0x1f, adc_data)                         # specify ADC1 channel to read from -- bits [7:0]
                write_FPGA(dev, 0x0f, T[l])                 # charging duration = #cycles*(10n)
                write_FPGA(dev, 0x17, 0x01)                 # READ trigger flag asserted 
                while True:
                    done = read_FPGA(dev, 0x36)
                    if done == 1:
                        write_FPGA(dev, 0x17, 0x00)
                        adc0_Frame2 = read_FPGA(dev, 0x32)
                        adc1_Frame2 = read_FPGA(dev, 0x34)
                        adc0_Frame2 = adc0_Frame2>>8
                        adc1_Frame2 = adc1_Frame2>>8
                        if int(np.log2(adc_switch_seq[n]))<8:
                            MVM_out_SD[m][n][i] = 3.3*(adc0_Frame2/2**16)
                        else:
                            MVM_out_SD[m][n][i] = 3.3*(adc1_Frame2/2**16)
                        #print('ADC0 Frame 2 output ' + str(3.3*(adc0_Frame2/2**16)))
                        #print('ADC1 Frame 2 output ' + str(3.3*(adc1_Frame2/2**16)))
                        break
                i+=1
            MVM_out_SD_av[m][n] = np.mean(MVM_out_SD[m][n])
            j = 0
            outer_product = 0
            plus = vp_WL_seq[m]
            minus = vn_WL_seq[m]
            #print('m: ' + str(m))
            #print('X: ' + str(hex(X)))
            while j<16:
                outer_product = outer_product + ((plus & 0x01) * g[l][j][int(np.log2(adc_switch_seq[n]))]) - ((minus & 0x01) * g[l][j][int(np.log2(adc_switch_seq[n]))])  
                #print('Outer Product: ' + str(outer_product))                           
                plus = plus >> 1
                minus = minus >> 1
                j+=1
            MVM_true_SD[m][n] = vref + (outer_product*(vp - vref)) / g_tot[int(np.log2(adc_switch_seq[n]))]
            print('\n')
            n += 1
        m += 1
    l += 1
        
        
print('MVM out measured: \n' + str(MVM_out_SD_av))
print('MVM true: \n' + str(MVM_true_SD))

df = pd.DataFrame(MVM_out_SD_av, 
                  columns = ['BL2', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL11', 'BL13', 'BL14', 'BL16'])
                  #index = ['WL5,7', 'WL8,9', 'WL10,11', 'WL12,13',  
                  #         'WL5, 7-9', 'WL8-11', 'WL10-13', 
                  #         'WL5, 7-11', 'WL8-13', 
                  #         'WL5,7-13'])
df.to_csv(path+'/excel data/array '+array+'/MVM_out_Measured_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv')
df = pd.DataFrame(MVM_true_SD, 
                  columns = ['BL2', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL11', 'BL13', 'BL14', 'BL16'])
                  #index = ['WL5,7', 'WL8,9', 'WL10,11', 'WL12,13',  
                  #         'WL5, 7-9', 'WL8-11', 'WL10-13', 
                  #         'WL5, 7-11', 'WL8-13', 
                  #         'WL5,7-13'])
df.to_csv(path+'/excel data/array '+array+'/MVM_out_Expected_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv')    
  

#%% Plot MVM, Single Differential encoding
  

'''
x = np.linspace(0, len(MVM_true_SD), len(MVM_true_SD)) 
BL = [2, 5, 6, 7, 8, 9, 11, 13, 14, 16]
for i in range(len(BL)):
    plt.figure(figsize=(20, 20))
    plt.scatter(x, MVM_true_SD[:, i], 
                alpha = 0.7, 
                label = 'Expected MVM Output', 
                marker = '^')
    plt.scatter(x, MVM_out_SD_av[:, i], 
                alpha = 0.7,
                label = 'Measured MVM Output',
                marker = 's')
    plt.ylabel('MVM Output (V)')
    plt.title('MVM Output - Measured vs Expected \nSingle Differential Read Scheme, BL' + str(BL[i]))
    plt.legend()
    plt.savefig(path + '/plots/array '+array+'/MVM/Single_differential_Read_scheme_BL'+str(BL[i])+'_run'+str(run)+'_'+str(datestamp)+'.png')
    plt.show()         
'''


dim1 = np.shape(MVM_true_SD)[0]
dim2 = np.shape(MVM_true_SD)[1]


MVM_true_SD_no_offset = np.zeros((dim1, dim2))                                     # Remove vref voltage offset from cxpected MVM
MVM_meas_SD_no_offset = np.zeros((dim1, dim2))                                     # Remove vref voltage offset from measured MVM
for i in range(dim1):
    for j in range(dim2):
        MVM_true_SD_no_offset[i][j] = MVM_true_SD[i][j] - vref
        MVM_meas_SD_no_offset[i][j] = MVM_out_SD_av[i][j] - vref


# setting font sizeto 30
plt.rcParams.update({'font.size': 25})
        
        
x = np.linspace(min(np.min(MVM_true_SD_no_offset), np.min(MVM_meas_SD_no_offset)), max(np.max(MVM_true_SD_no_offset), np.max(MVM_meas_SD_no_offset)), 100)    
plt.figure(figsize=(15, 10))
plt.scatter(np.reshape(MVM_true_SD_no_offset, (dim1*dim2, 1)), np.reshape(MVM_meas_SD_no_offset, (dim1*dim2, 1)), 
            alpha = 0.8,
            #label = 'Measured MVM Output',
            marker = 's',
            linewidth = 3)

plt.plot(x, x, 
         alpha = 0.8,
         #label = 'Ideal distribution',
         color = 'orange',
         linewidth = 3)


plt.ylabel('Measured MVM Output (V)')
plt.xlabel('Expected MVM Output (V)')
plt.title('MVM Output - Measured vs Expected \nSingle Differential Read Scheme')
plt.grid(True, which='both')
#plt.legend()
plt.savefig(path+'/plots/array '+array+'/MVM/MVM_Output_Single_Differential_Read_run'+str(run)+'_'+str(datestamp)+'.png')
plt.show()


from sklearn.metrics import mean_squared_error
import math
MSE_SD = mean_squared_error(np.reshape(MVM_true_SD_no_offset, (dim1*dim2, 1)), np.reshape(MVM_meas_SD_no_offset, (dim1*dim2, 1)))
RMSE_SD = math.sqrt(MSE_SD)
print("Root Mean Square Error, Single DIfferential Read Scheme:\n")
print(RMSE_SD)


#%% Combined plot for positive, zero, and negative MVM outputs, Single-differential encoding


run         = 1
datestamp   = 221117

MVM_out_type = 'positive'
df1         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
dim1        = np.shape(df1)[0]
dim2        = np.shape(df1)[1]
df1         = np.reshape(df1, (dim1*dim2, 1))
df2         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df2         = np.reshape(df2, (dim1*dim2, 1))
 

MVM_out_type = 'zero'
df3         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
dim1        = np.shape(df3)[0]
dim2        = np.shape(df3)[1]
df3         = np.reshape(df3, (dim1*dim2, 1))
df4         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df4         = np.reshape(df4, (dim1*dim2, 1))


MVM_out_type = 'negative'
df5         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
dim1        = np.shape(df5)[0]
dim2        = np.shape(df5)[1]
df5         = np.reshape(df5, (dim1*dim2, 1))
df6         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Single_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df6         = np.reshape(df6, (dim1*dim2, 1))


MVM_Expected_SD = np.concatenate((df1, df3, df5))
MVM_Measured_SD = np.concatenate((df2, df4, df6))
MVM_Expected_SD_no_offset = np.zeros((len(MVM_Expected_SD), 1))                       # Remove vref voltage offset from cxpected MVM
MVM_Measured_SD_no_offset = np.zeros((len(MVM_Measured_SD), 1))                       # Remove vref voltage offset from measured MVM


for i in range(len(MVM_Expected_SD)):
    MVM_Expected_SD_no_offset[i] = MVM_Expected_SD[i] - vref
    MVM_Measured_SD_no_offset[i] = MVM_Measured_SD[i] - vref


df7 = pd.DataFrame(MVM_Expected_SD_no_offset)
df7.to_excel(path + '/excel data/array '+array+'/MVM_out_Expected_Single_Differential_Scheme_combined_data_run'+str(run)+'_'+str(datestamp)+'.xlsx')
df8 = pd.DataFrame(MVM_Measured_SD_no_offset)
df8.to_excel(path + '/excel data/array '+array+'/MVM_out_Measured_Single_Differential_Scheme_combined_data_run'+str(run)+'_'+str(datestamp)+'.xlsx')
        
      
        
from sklearn.metrics import mean_squared_error
import math
MSE_SD = mean_squared_error(MVM_Expected_SD_no_offset, MVM_Measured_SD_no_offset)
RMSE_SD = math.sqrt(MSE_SD)
print("Root Mean Square Error:\n")
print(RMSE_SD)


# setting font sizeto 30
plt.rcParams.update({'font.size': 30})
plt.rcParams.update({'font.family': 'serif'})
plt.figure(figsize=(15, 10))


plt.scatter(MVM_Expected_SD_no_offset, MVM_Measured_SD_no_offset, 
            alpha = 0.8,
            marker = 's',
            linewidth = 3)


x = np.linspace(min(np.min(MVM_Expected_SD_no_offset), np.min(MVM_Measured_SD_no_offset)), max(np.max(MVM_Expected_SD_no_offset), np.max(MVM_Measured_SD_no_offset)), 100)    
plt.plot(x, x, 
         alpha = 0.8,
         color = 'orange',
         linewidth = 3)


plt.ylabel('Measured MVM Output (V)')
plt.xlabel('Expected MVM Output (V)')
plt.title('MVM Output - Measured vs Expected \nSingle-differential encoding')
plt.grid(True, which='both')
plt.savefig(path + '/plots/array '+array+'/MVM/MVM_Output_Single_Differential_Read_run'+str(run)+'_'+str(datestamp)+'.png')
plt.show()


#%% Combined scatter plot for NOn-Differential and Single-Differential encoding


# setting font sizeto 30
plt.rcParams.update({'font.size': 30})
plt.rcParams.update({'font.family': 'serif'})
plt.figure(figsize=(15, 10))


plt.scatter(MVM_Expected_no_offset, MVM_Measured_no_offset, 
            alpha = 0.8,
            marker = 's',
            linewidth = 3,
            label = 'Non-Differential encoding')


x = np.linspace(min(np.min(MVM_Expected_no_offset), np.min(MVM_Measured_no_offset)), max(np.max(MVM_Expected_no_offset), np.max(MVM_Measured_no_offset)), 100)    
plt.plot(x, x, 
         alpha = 0.8,
         color = 'orange',
         linewidth = 3)


plt.scatter(MVM_Expected_SD_no_offset, MVM_Measured_SD_no_offset, 
            alpha = 0.8,
            marker = 's',
            linewidth = 3, 
            label = 'Single-Differential encoding')


x = np.linspace(min(np.min(MVM_Expected_SD_no_offset), np.min(MVM_Measured_SD_no_offset)), max(np.max(MVM_Expected_SD_no_offset), np.max(MVM_Measured_SD_no_offset)), 100)    
plt.plot(x, x, 
         alpha = 0.8,
         color = 'orange',
         linewidth = 3)


plt.ylabel('Measured MVM Output (V)')
plt.xlabel('Expected MVM Output (V)')
plt.title('MVM Output - Measured vs Expected')
plt.grid(True, which='both')
plt.legend()
plt.savefig(path + '/plots/array '+array+'/MVM/MVM_Output_Non_vs_Single_Differential_Read_run'+str(run)+'_'+str(datestamp)+'.png')
plt.show()


#%% MVM, Double differential encoding


all_switches_off(dev)
write_FPGA(dev, 0x00, 0x01)                                             # Reset verilog Finite State Machine 
write_FPGA(dev, 0x00, 0x00)
state = read_FPGA(dev, 0x20)
print('state: ' + str(state))
write_FPGA(dev, 0x10, 0x00)                                             # de-assert FORM trigger


vp               = 1.1
vn               = 0.3
vref             = 0.7
write_DAC(dev, VP_RRAM, vp)
write_DAC(dev, VN_RRAM, vn)
write_DAC(dev, VREF_RRAM, vref)


write_FPGA(dev, 0x14, 0x00000000)                                                                   # Vn switch select, [15:0] for WL, [31:16] for BL
write_FPGA(dev, 0x13, 0x00000000)                                                                   # Vp switch select, [15:0] for WL, [31:16] for BL 


N                = 10
T                = [40000]                                                                           # for a steady state measurement
#T               = [500000000]                                                                       # for a steady state measurement in GOhm range, delta t = 20 sec


WL_map = [5, 11, 14, 2, 1, 9, 10, 4, 7, 13, 16, 8, 3, 15, 12, 6]
BL_map = [8, 14, 9, 7, 4, 16, 13, 3, 12, 6, 11, 1, 10, 2, 15, 5]         


MVM_out_type = 'negative'

if MVM_out_type == 'positive':
    vp_WL = [1, 3, 5, 7, 8, 9, 11, 15]
    vn_WL = [2, 4, 6, 10, 14, 13, 16, 12]
elif MVM_out_type == 'zero':
    vp_WL = [1, 2, 5, 6, 8, 14, 11, 16]
    vn_WL = [3, 4, 7, 10, 9, 13, 15, 12]
elif MVM_out_type == 'negative':
    vp_WL = [2, 4, 6, 10, 14, 13, 16, 12]
    vn_WL = [1, 3, 5, 7, 8, 9, 11, 15]
else:
    print("Invalid MVM output type!")
    
vp_WL_true = np.zeros(len(vp_WL))
vn_WL_true = np.zeros(len(vn_WL))
vp_WL_init = np.zeros(len(vp_WL_true))
vn_WL_init = np.zeros(len(vn_WL_true))


for i in range(len(vp_WL)):
    vp_WL_true[i] = WL_map.index(vp_WL[i])
    vp_WL_init[i] = (0x0001)<<int(vp_WL_true[i])  
vp_WL_init      = vp_WL_init.astype(int)

vp_WL_seq       = vp_WL_init.copy()
  
for j in range(1, len(vp_WL_init)):
    for i in range(len(vp_WL_init) - j):
        sum = 0
        for k in range(j+1):
            sum = sum + vp_WL_init[i+k]
        vp_WL_seq = np.append(vp_WL_seq, sum)
      
        
for i in range(len(vn_WL)):
    vn_WL_true[i] = WL_map.index(vn_WL[i])
    vn_WL_init[i] = (0x0001)<<int(vn_WL_true[i]) 
vn_WL_init      = vn_WL_init.astype(int)
    
vn_WL_seq       = vn_WL_init.copy()

for j in range(1, len(vn_WL_init)):
    for i in range(len(vn_WL_init) - j):
        sum = 0
        for k in range(j+1):
            sum = sum + vn_WL_init[i+k]
        vn_WL_seq = np.append(vn_WL_seq, sum)
        
        
vref_WL_seqb    = np.add(vp_WL_seq, vn_WL_seq)     
vref_WL_seq     = vref_WL_seqb*0
for  i in range(len(vref_WL_seqb)):
    vref_WL_seq[i] = 2**16 - 1 - vref_WL_seqb[i]
                                                           
                                                                                               
adc_ch_seq_plus  = [0x081105, 0x081101, 0x081102]           # BL2, 6, 11
                                                  
adc_ch_seq_minus = [0x081103, 0x081102, 0x081101]           # BL7, 9, 14

adc_sw_seq_plus  = [0x00002000, 0x00000200, 0x00000400]     # BL2, 6, 11     

adc_sw_seq_minus = [0x00000008, 0x00000004, 0x00000002]     # BL7, 9, 14

adc_switch_seq   = np.add(adc_sw_seq_plus, adc_sw_seq_minus)


vref_BL_seqb     = adc_switch_seq
vref_BL_seq      = np.int64(adc_switch_seq*0)               # intialize vref_BL_seq as the same length as adc_switch_seq

for  i in range(len(vref_BL_seqb)):
    vref_BL_seq[i] = 2**16 - 1 - vref_BL_seqb[i]
    vref_BL_seq[i] = vref_BL_seq[i] * (2**16)               # Left shift by 16 bits
    

MVM_out_DD_minus = np.zeros((len(vn_WL_seq), len(adc_ch_seq_minus), N))         
MVM_out_DD_plus  = np.zeros((len(vp_WL_seq), len(adc_ch_seq_plus), N))
MVM_out_DD_minus_av = np.zeros((len(vn_WL_seq), len(adc_ch_seq_minus)))         # MVM out data, BL-, from ADC0
MVM_out_DD_plus_av = np.zeros((len(vp_WL_seq), len(adc_ch_seq_plus)))           # MVM out data, BL+, from ADC1
MVM_out_DD_av    = np.zeros((len(vp_WL_seq), len(adc_ch_seq_plus)))         
MVM_true_DD      = np.zeros((len(vp_WL_seq), len(adc_ch_seq_plus)))


l = 0
while (l<len(T)):
    
    
    write_FPGA(dev, 0x04, 0x03)                             # reset fifo counter
    write_FPGA(dev, 0x04, 0x00)
    
    
    m = 0
    while (m<len(vref_WL_seq)):
        
        
        vp_WL_switch        = vp_WL_seq[m]
        write_FPGA(dev, 0x13, int(vp_WL_switch))                 # Vp switch select during read, [15:0] for WL, [31:16] for BL
        print('vp_WL_switch: '+str(vp_WL_switch))
        vn_WL_switch        = vn_WL_seq[m]
        write_FPGA(dev, 0x14, int(vn_WL_switch))                 # Vp switch select during read, [15:0] for WL, [31:16] for BL
        print('vn_WL_switch: '+str(vn_WL_switch))
        vref_WL_switch      = vref_WL_seq[m] 
        
        
        n = 0
        while (n<len(adc_ch_seq_plus)):
           
            
            adc0_data               = adc_ch_seq_minus[n]   # Assigning minus channels to ADC0
            adc1_data               = adc_ch_seq_plus[n]    # Assigning plus channels to ADC1
            adc_switch              = adc_switch_seq[n]
            vref_BL_switch          = vref_BL_seq[n]
            write_FPGA(dev, 0x12, int(vref_BL_switch + vref_WL_switch))     # Vref switch select during read
            print('vref_switch = '+ hex(int(vref_BL_switch + vref_WL_switch)))
            write_FPGA(dev, 0x15, int(adc_switch))          # select capacitor for ADC sampling
            
            
            i = 0
            while (i<N):
                done = 0
                write_FPGA(dev, 0x1c, adc0_data)            # specify ADC0 channel to read from -- bits [7:0]
                write_FPGA(dev, 0x1f, adc1_data)            # specify ADC1 channel to read from -- bits [7:0]
                write_FPGA(dev, 0x0f, T[l])                 # charging duration = #cycles*(10n)
                write_FPGA(dev, 0x17, 0x01)                 # READ trigger flag asserted 
                while True:
                    done = read_FPGA(dev, 0x36)
                    if done == 1:
                        write_FPGA(dev, 0x17, 0x00)
                        adc0_Frame2 = read_FPGA(dev, 0x32)
                        adc1_Frame2 = read_FPGA(dev, 0x34)
                        adc0_Frame2 = adc0_Frame2>>8
                        adc1_Frame2 = adc1_Frame2>>8
                        MVM_out_DD_minus[m][n][i] = 3.3*(adc0_Frame2/2**16)
                        MVM_out_DD_plus[m][n][i] = 3.3*(adc1_Frame2/2**16)
                        #print('ADC0 Frame 2 output ' + str(3.3*(adc0_Frame2/2**16)))
                        #print('ADC1 Frame 2 output ' + str(3.3*(adc1_Frame2/2**16)))
                        break
                i+=1
            MVM_out_DD_minus_av[m][n]   = np.mean(MVM_out_DD_minus[m][n])
            MVM_out_DD_plus_av[m][n]    = np.mean(MVM_out_DD_plus[m][n])
            MVM_out_DD_av[m][n]         = MVM_out_DD_plus_av[m][n] - MVM_out_DD_minus_av[m][n]
            
            
            j = 0
            outer_product_minus = 0
            outer_product_plus = 0
            plus = vp_WL_seq[m]
            minus = vn_WL_seq[m]
            #print('m: ' + str(m))
            #print('X: ' + str(hex(X)))
            while j<16:
                outer_product_minus = outer_product_minus + ((plus & 0x01) * g[l][j][int(np.log2(adc_sw_seq_minus[n]))]) - ((minus & 0x01) * g[l][j][int(np.log2(adc_sw_seq_minus[n]))])  
                outer_product_plus = outer_product_plus + ((plus & 0x01) * g[l][j][int(np.log2(adc_sw_seq_plus[n]))]) - ((minus & 0x01) * g[l][j][int(np.log2(adc_sw_seq_plus[n]))])                 
                #print('Outer Product: ' + str(outer_product))                           
                plus = plus >> 1
                minus = minus >> 1
                j+=1
            MVM_true_DD[m][n] = ((vp - vref) * outer_product_plus) / g_tot[int(np.log2(adc_sw_seq_plus[n]))] - ((vp - vref) * outer_product_minus) / g_tot[int(np.log2(adc_sw_seq_minus[n]))]
            print('\n')
            n += 1
        m += 1
    l += 1
        
        
print('MVM out measured: \n' + str(MVM_out_DD_av))
print('MVM true: \n' + str(MVM_true_DD))
df = pd.DataFrame(MVM_out_DD_av) 
'''columns = ['BL2', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL11', 'BL13', 'BL14', 'BL16'],
index = ['WL5,7', 'WL8,9', 'WL10,11', 'WL12,13',  
     'WL5, 7-9', 'WL8-11', 'WL10-13', 
     'WL5, 7-11', 'WL8-13', 
     'WL5,7-13'])'''
df.to_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv')
df = pd.DataFrame(MVM_true_DD) 
'''columns = ['BL2', 'BL5', 'BL6', 'BL7','BL8', 'BL9', 'BL11', 'BL13', 'BL14', 'BL16'],
index = ['WL5,7', 'WL8,9', 'WL10,11', 'WL12,13',  
         'WL5, 7-9', 'WL8-11', 'WL10-13', 
         'WL5, 7-11', 'WL8-13', 
         'WL5,7-13'])'''
df.to_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv')    

  
#%% Plot MVM, Double Differential encoding
 

'''
plt.close()
x = np.linspace(0, len(MVM_true_DD), len(MVM_true_DD)) 
BL_pair = ['BL2,7', 'BL6,9', 'BL11,14']
for i in range(len(BL_pair)):
    plt.figure(figsize=(20, 20))
    plt.scatter(x, MVM_true_DD[:, i], 
                alpha = 0.7, 
                label = 'Expected MVM Output', 
                marker = '^')
    plt.scatter(x, MVM_out_DD_av[:, i], 
                alpha = 0.7,
                label = 'Measured MVM Output',
                marker = 's')
    plt.ylabel('MVM Output (V)')
    plt.title('MVM Output - Measured vs Expected \nDouble Differential Read Scheme, ' + str(BL_pair[i]))
    plt.legend()
    #plt.savefig(path + '/plots/array '+array+'/MVM/Double_differential_Read_scheme_'+str(BL_pair[i])+'_run'+str(run)+'_'+str(datestamp)+'.png')
    plt.show()         
'''


dim1 = np.shape(MVM_true_DD)[0]
dim2 = np.shape(MVM_true_DD)[1]


# setting font sizeto 30
plt.rcParams.update({'font.size': 25})


x = np.linspace(min(np.min(MVM_true_DD), np.min(MVM_out_DD_av)), max(np.max(MVM_true_DD), np.max(MVM_out_DD_av)), 100)    
#x = np.linspace(-0.005, 0.005, 1000)
plt.figure(figsize=(15, 10))
plt.scatter(np.reshape(MVM_true_DD, (dim1*dim2, 1)), np.reshape(MVM_out_DD_av, (dim1*dim2, 1)), 
            alpha = 0.8,
            #label = 'Measured MVM Output',
            marker = 's',
            linewidth = 3)

plt.plot(x, x, 
         alpha = 0.8,
         #label = 'Ideal distribution',
         color = 'orange',
         linewidth = 3)

plt.ylabel('Measured MVM Output (V)')
plt.xlabel('Expected MVM Output (V)')
plt.title('MVM Output - Measured vs Expected \nDouble Differential Read Scheme')
plt.grid(True, which='both')
#plt.legend()
plt.savefig(path+'/plots/array '+array+'/MVM/MVM_Output_Double_Differential_Read_run'+str(run)+'_'+str(datestamp)+'.png')
plt.show()


from sklearn.metrics import mean_squared_error
import math
MSE_DD = mean_squared_error(np.reshape(MVM_true_DD, (dim1*dim2, 1)), np.reshape(MVM_out_DD_av, (dim1*dim2, 1)))
RMSE_DD = math.sqrt(MSE_DD)
print("Root Mean Square Error, Double Differential Read Scheme:\n")
print(RMSE_DD)
  

#%% Combined plot for positive, zero, and negative MVM outputs, Double-differential encoding


run         = 1
datestamp   = 221117
MVM_out_type = 'positive'
df1         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
dim1        = np.shape(df1)[0]
dim2        = np.shape(df1)[1]
df1         = np.reshape(df1, (dim1*dim2, 1))
df2         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df2         = np.reshape(df2, (dim1*dim2, 1))
 

MVM_out_type = 'zero'
df3         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
dim1        = np.shape(df3)[0]
dim2        = np.shape(df3)[1]
df3         = np.reshape(df3, (dim1*dim2, 1))
df4         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df4         = np.reshape(df4, (dim1*dim2, 1))


MVM_out_type = 'negative'
df5         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Expected_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
dim1        = np.shape(df5)[0]
dim2        = np.shape(df5)[1]
df5         = np.reshape(df5, (dim1*dim2, 1))
df6         = pd.read_csv(path + '/excel data/array '+array+'/MVM_out_Measured_Double_Differential_Scheme_'+str(MVM_out_type)+'_run'+str(run)+'_'+str(datestamp)+'.csv', header = 0, index_col = 0).to_numpy()
df6         = np.reshape(df6, (dim1*dim2, 1))


MVM_Expected_DD = np.concatenate((df1, df3, df5))
MVM_Measured_DD = np.concatenate((df2, df4, df6))


scaling_factor = 1
MVM_Expected_DD = scaling_factor*MVM_Expected_DD
MVM_Measured_DD = scaling_factor*MVM_Measured_DD
df7 = pd.DataFrame(MVM_Expected_DD)
df7.to_excel(path + '/excel data/array '+array+'/MVM_out_Expected_Double_Differential_Scheme_combined_data_run'+str(run)+'_'+str(datestamp)+'.xlsx')
df8 = pd.DataFrame(MVM_Measured_DD)
df8.to_excel(path + '/excel data/array '+array+'/MVM_out_Measured_Double_Differential_Scheme_combined_data_run'+str(run)+'_'+str(datestamp)+'.xlsx')  

    
from sklearn.metrics import mean_squared_error
import math
MSE_DD = mean_squared_error(MVM_Expected_DD, MVM_Measured_DD)
RMSE_DD = math.sqrt(MSE_DD)
print("Root Mean Square Error:\n")
print(RMSE_DD)


# setting font sizeto 30
plt.rcParams.update({'font.size': 30})
plt.rcParams.update({'font.family': 'serif'})
plt.figure(figsize=(17, 10))


plt.scatter(MVM_Expected_DD, MVM_Measured_DD, 
            alpha = 0.8,
            marker = 's',
            linewidth = 3)


x = np.linspace(min(np.min(MVM_Expected_DD), np.min(MVM_Measured_DD)), max(np.max(MVM_Expected_DD), np.max(MVM_Measured_DD)), 1000)    
plt.plot(x, x, 
         alpha = 0.8,
         color = 'orange',
         linewidth = 3)


plt.ylabel('Measured MVM Output (V)')
plt.xlabel('Expected MVM Output (V)')
plt.title('MVM Output - Measured vs Expected \nDouble-differential encoding')
plt.grid(True, which='both')
plt.savefig(path + '/plots/array '+array+'/MVM/MVM_Output_Double_Differential_Read_run'+str(run)+'_'+str(datestamp)+'.png')
plt.show()
