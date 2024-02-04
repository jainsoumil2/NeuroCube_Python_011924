#%% Initialization
# The following code for initializing and getting general information about the Opal Kelly was obtained from DESTester.py found in the samples of Opal Kelly samples folder (DES).
# FrontPanelSDK 5.2.3 was installed for Opal Kelly.
# Note - Initialization (class 'Initialize') does not work properly (Opal kelly is not recognised) if the Opal Kelly FrontPanel application is open.


import os

abspath = os.path.abspath(r"C:/Users/jains/OneDrive - UC San Diego/research/NeuroCube/Python/NeuroCube/") ## String which contains absolute path to the script file
os.chdir(abspath) ## Setting up working directory

from nc import *
from NeuroCube_functions import *
import time
import pyvisa 


# Main code
print("------ Main code ------")
#if not dev.InitializeDevice():   note: "if not ..." command just means "if False == ...", then do ...
if not dev.initDevice():
    # dev is instantiated in the beginningish nc.py (line 189) using the Initialize class (line 150-186 of nc.py)
    exit()


#%% initialize and set nisoc DACs ####################################################
init_DACs_nisoc(dev)

write_DACs_nisoc(dev, IVbP_OTA, 0.826)          #0.826, 0.800
write_DACs_nisoc(dev, Vinfinimp_bias, 1.278)    #1.278
write_DACs_nisoc(dev, Vclamp_p, 1.25)
write_DACs_nisoc(dev, Vclamp_n, 0.8)    
write_DACs_nisoc(dev, IVbNP_stim, 0.5)
write_DACs_nisoc(dev, IVbNN_stim, 0.5)
write_DACs_nisoc(dev, Vref_nisoc, 1.053)        #1.053, 1.13

# Set nisoc DAC MUXOUT to REF
DAC_mux_vref_nisoc(dev, 1)                      # 0 to disable, 1 to enable

# Set ports of gap junction row 1 ###################################

write_Gap_Junction(dev, 0x01, 0x0401)           # disable shutdown mode, disable transition detection

write_Gap_Junction(dev, 0x01, 0x0955)           # configuration -- set P7, P6, P5, P4 as output ports
write_Gap_Junction(dev, 0x01, 0x0A55)           # configuration -- set P11, P10, P9, P8 as output ports
write_Gap_Junction(dev, 0x01, 0x4400)           # ports 4-11 output logic 0 


write_Gap_Junction(dev, 0x01, 0x0B55)           # configuration -- set P15, P14, P13, P12 as output ports
write_Gap_Junction(dev, 0x01, 0x0C55)           # configuration -- set P19, P18, P17, P16 as output ports
write_Gap_Junction(dev, 0x01, 0x4C00)           # ports 12-19 output logic 0 


write_Gap_Junction(dev, 0x01, 0x0D55)           # configuration -- set P23, P22, P21, P20 as output ports
write_Gap_Junction(dev, 0x01, 0x0E55)           # configuration -- set P27, P26, P25, P24 as output ports
write_Gap_Junction(dev, 0x01, 0x5400)           # ports 20-27 output logic 0 


write_Gap_Junction(dev, 0x01, 0x0F55)           # configuration -- set P31, P30, P29, P28 as output ports
write_Gap_Junction(dev, 0x01, 0x5C01)           # port 28 (neurodyn 1 dac's CSbar) outputs logic 1, ports 29-31 output logic 0


# Set ports of gap junction row 2 ###################################

write_Gap_Junction(dev, 0x02, 0x0401)           # disable shutdown mode, disable transition detection

write_Gap_Junction(dev, 0x02, 0x0955)           # configuration -- set P7, P6, P5, P4 as output ports
write_Gap_Junction(dev, 0x02, 0x0A55)           # configuration -- set P11, P10, P9, P8 as output ports
write_Gap_Junction(dev, 0x02, 0x4400)           # ports 4-11 output logic 0 

write_Gap_Junction(dev, 0x02, 0x0B55)           # configuration -- set P15, P14, P13, P12 as output ports
write_Gap_Junction(dev, 0x02, 0x0C55)           # configuration -- set P19, P18, P17, P16 as output ports
write_Gap_Junction(dev, 0x02, 0x4C00)           # ports 12-19 output logic 0 

write_Gap_Junction(dev, 0x02, 0x0D55)           # configuration -- set P23, P22, P21, P20 as output ports
write_Gap_Junction(dev, 0x02, 0x0E55)           # configuration -- set P27, P26, P25, P24 as output ports
write_Gap_Junction(dev, 0x02, 0x5400)           # ports 20-27 output logic 0 

write_Gap_Junction(dev, 0x02, 0x0F55)           # configuration -- set P31, P30, P29, P28 as output ports
write_Gap_Junction(dev, 0x02, 0x5C01)           # port 28 outputs logic 1, ports 29-31 output logic 0


# Set ports of gap junction row 3 ###################################

write_Gap_Junction(dev, 0x03, 0x0401)           # disable shutdown mode, disable transition detection

write_Gap_Junction(dev, 0x03, 0x0955)           # configuration -- set P7, P6, P5, P4 as output ports
write_Gap_Junction(dev, 0x03, 0x0A55)           # configuration -- set P11, P10, P9, P8 as output ports
write_Gap_Junction(dev, 0x03, 0x4400)           # ports 4-11 output logic 0 

write_Gap_Junction(dev, 0x03, 0x0B55)           # configuration -- set P15, P14, P13, P12 as output ports
write_Gap_Junction(dev, 0x03, 0x0C55)           # configuration -- set P19, P18, P17, P16 as output ports
write_Gap_Junction(dev, 0x03, 0x4C00)           # ports 12-19 output logic 0 

write_Gap_Junction(dev, 0x03, 0x0D55)           # configuration -- set P23, P22, P21, P20 as output ports
write_Gap_Junction(dev, 0x03, 0x0E55)           # configuration -- set P27, P26, P25, P24 as output ports
write_Gap_Junction(dev, 0x03, 0x5400)           # ports 20-27 output logic 0 

write_Gap_Junction(dev, 0x03, 0x0F55)           # configuration -- set P31, P30, P29, P28 as output ports
write_Gap_Junction(dev, 0x03, 0x5C01)           # port 28 outputs logic 1, ports 29-31 output logic 0


#  Set ports of gap junction row 4 ###################################

write_Gap_Junction(dev, 0x04, 0x0401)           # disable shutdown mode, disable transition detection

write_Gap_Junction(dev, 0x04, 0x0955)           # configuration -- set P7, P6, P5, P4 as output ports
write_Gap_Junction(dev, 0x04, 0x0A55)           # configuration -- set P11, P10, P9, P8 as output ports
write_Gap_Junction(dev, 0x04, 0x4400)           # ports 4-11 output logic 0 

write_Gap_Junction(dev, 0x04, 0x0B55)           # configuration -- set P15, P14, P13, P12 as output ports
write_Gap_Junction(dev, 0x04, 0x0C55)           # configuration -- set P19, P18, P17, P16 as output ports
write_Gap_Junction(dev, 0x04, 0x4C00)           # ports 12-19 output logic 0 

write_Gap_Junction(dev, 0x04, 0x0D55)           # configuration -- set P23, P22, P21, P20 as output ports
write_Gap_Junction(dev, 0x04, 0x0E55)           # configuration -- set P27, P26, P25, P24 as output ports
write_Gap_Junction(dev, 0x04, 0x5400)           # ports 20-27 output logic 0 

write_Gap_Junction(dev, 0x04, 0x0F55)           # configuration -- set P31, P30, P29, P28 as output ports
write_Gap_Junction(dev, 0x04, 0x5C01)           # port 28 outputs logic 1, ports 29-31 output logic 0


# initialize and write neurodyn 1 dac ################################

init_external_DACs_neurodyn(dev, 1)                                # 2nd argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4

# DAC Channels
# Vref_neurodyn = 0
# vBiasN = 1
# vBiasP = 2
# Vb = 3
# IinVoltagePin = 4
# IinCurrentPin = 5
# IinRefPin = 6
# VmemProbeIn = 7

write_external_DACs_neurodyn(dev, Vref_neurodyn, 0.9, 1)           # last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4
write_external_DACs_neurodyn(dev, vBiasN, 1.4, 1)                     
write_external_DACs_neurodyn(dev, vBiasP, 1.7, 1)                  
write_external_DACs_neurodyn(dev, Vb, 0.9, 1)                      
write_external_DACs_neurodyn(dev, IinVoltagePin, 1.2, 1)           
write_external_DACs_neurodyn(dev, IinCurrentPin, 0.9, 1)           
write_external_DACs_neurodyn(dev, IinRefPin, 0.9, 1)               
write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, 1)             

# Set neurodyn DAC MUXOUT to REF
external_DAC_mux_vref_neurodyn(dev, 1, 1)                         # 2nd argument: 0 -- disable, 1 -- enable; last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4


# initialize and write neurodyn 2 dac ################################

init_external_DACs_neurodyn(dev, 2)                               # 2nd argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4

# DAC Channels
# Vref_neurodyn = 0
# vBiasN = 1
# vBiasP = 2
# Vb = 3
# IinVoltagePin = 4
# IinCurrentPin = 5
# IinRefPin = 6
# VmemProbeIn = 7

write_external_DACs_neurodyn(dev, Vref_neurodyn, 0.9, 2)            # last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4
write_external_DACs_neurodyn(dev, vBiasN, 1.4, 2)                     
write_external_DACs_neurodyn(dev, vBiasP, 1.7, 2)                  
write_external_DACs_neurodyn(dev, Vb, 0.9, 2)                      
write_external_DACs_neurodyn(dev, IinVoltagePin, 1.2, 2)            # dac = 0.752 - IVoltage = 270.8nA; dac = 1.2v - IVoltage = 3.059uA   
write_external_DACs_neurodyn(dev, IinCurrentPin, 0.6195, 2)         # dac = 0.722 - IMaster = 200.6nA; dac = 0.6195 - IMaster = 40nA   
write_external_DACs_neurodyn(dev, IinRefPin, 0.4405, 2)             # dac = 0.672 - IRef = 99.4 nA; dac = 0.4405 - IRef = 0.4nA 
write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, 2)             

# Set neurodyn DAC MUXOUT to REF
external_DAC_mux_vref_neurodyn(dev, 1, 2)                          # 2nd argument: 0 -- disable, 1 -- enable; last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4


# initialize and write neurodyn 3 dac ################################

init_external_DACs_neurodyn(dev, 3)                                # 2nd argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4

# DAC Channels
# Vref_neurodyn = 0
# vBiasN = 1
# vBiasP = 2
# Vb = 3
# IinVoltagePin = 4
# IinCurrentPin = 5
# IinRefPin = 6
# VmemProbeIn = 7

write_external_DACs_neurodyn(dev, Vref_neurodyn, 0.9, 3)           # last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4
write_external_DACs_neurodyn(dev, vBiasN, 1.4, 3)                     
write_external_DACs_neurodyn(dev, vBiasP, 1.7, 3)                  
write_external_DACs_neurodyn(dev, Vb, 0.9, 3)                      
write_external_DACs_neurodyn(dev, IinVoltagePin, 1.2, 3)           
write_external_DACs_neurodyn(dev, IinCurrentPin, 0.6195, 3)          
write_external_DACs_neurodyn(dev, IinRefPin, 0.4405, 3)            
write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, 3)             

# Set neurodyn DAC MUXOUT to REF
external_DAC_mux_vref_neurodyn(dev, 1, 3)                          # 2nd argument: 0 -- disable, 1 -- enable; last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4


# initialize and write neurodyn 4 dac ################################

init_external_DACs_neurodyn(dev, 4)                                # 2nd argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4

# DAC Channels
# Vref_neurodyn = 0
# vBiasN = 1
# vBiasP = 2
# Vb = 3
# IinVoltagePin = 4
# IinCurrentPin = 5
# IinRefPin = 6
# VmemProbeIn = 7

write_external_DACs_neurodyn(dev, Vref_neurodyn, 0.9, 4)           # last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4
write_external_DACs_neurodyn(dev, vBiasN, 1.4, 4)                    
write_external_DACs_neurodyn(dev, vBiasP, 1.7, 4)                  
write_external_DACs_neurodyn(dev, Vb, 0.9, 4)                      
write_external_DACs_neurodyn(dev, IinVoltagePin, 1.16, 4)          # dac = 1.16v - IVoltage = 3.019uA   
write_external_DACs_neurodyn(dev, IinCurrentPin, 0.6255, 4)        # dac = 0.6255v - IMaster = 40nA 
write_external_DACs_neurodyn(dev, IinRefPin, 0.442, 4)             # dac =  0.442v - IRef = 0.4nA  
write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, 4)             

# Set neurodyn DAC MUXOUT to REF
external_DAC_mux_vref_neurodyn(dev, 1, 4)                          # 2nd argument: 0 -- disable, 1 -- enable; last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4


#%% Characterizing Imaster currents -- obsolete

# SET Keithley for current measurements

rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')                             # by default, Keithley is set to measure currents and source voltage (0.000V) after reset which is what we want for current measurements
#my_K.write(':SENS:FUNC CURR')
#my_K.write(':SOUR:CURR:RANG 50E-6')           # can set a current range if required but the default uA is what we need
my_K.write(':SOUR:FUNC CURR')
my_K.write(':SOUR:CLE:AUTO ON')                # output will turn off after the measurement is completed
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')

neurodyn_sel = 1

Imaster = []

for dac_value in np.linspace(0.0, 1.80, 37, endpoint=True):
    #write_external_DACs_neurodyn(dev, IinCurrentPin, dac_value, neurodyn_sel) 
    write_external_DACs_neurodyn(dev, IinCurrentPin,0.9, neurodyn_sel) 
    time.sleep(0.01)
    sum = 0
    for i in range (20):
        reading = my_K.query('READ?')
        reading = reading.split(",")
        I = float(reading[1])
        time.sleep(0.01)
        sum = sum + I
    I_avg = round((sum/20)*1e6, 3)         # convert to uA and round to 3 decimals
    Imaster.append(I_avg)

print(Imaster)
    
#my_K.write(':OUTP OFF')
#my_K.close   

# %% Serial Data In(SDI)- Serial Data Out(SDO) ADC check ################

# write_FPGA_NC(dev, NC_DAC_V_data_addr, 0x00ff00ff)                  # 1111 xxxx xxxx xxxx xxxx xxxx -- no operation command; vout5 = IVbNN_stim_DAC ~ 1.2V
# write_FPGA_NC(dev, NC_DAC_target_addr, 1)                           # 1-- nisoc dac, 2-- neurodyn dac  
# time.sleep(10)
# write_FPGA_NC(dev, NC_DAC_flag_addr, 0x10)


# %% Test neurodyn internal dacs address write

setaddress_ND1(dev, 0x0300)
time.sleep(5)  # wait 5 seconds
setaddress_ND2(dev, 0x03ff)

# %% Test neurodyn internal dacs data write 

set_internal_dacs_data(dev, 0x0c53)
time.sleep(5)  # wait 5 seconds
set_internal_dacs_data(dev, 0x0c00)


# %% Test neurodyn internal dacs WR

set_WR_on(dev, 0) 
time.sleep(5)  # wait 5 seconds
set_WR_on(dev, 1)
time.sleep(5)  # wait 5 seconds
set_WR_on(dev, 2)
time.sleep(5)  # wait 5 seconds
set_WR_on(dev, 3)
time.sleep(5)   
set_WR_off(dev)

# %% Test neurodyn dac_cal and switchRpin_out control signals

set_dac_cal_off_switchrpin_off(dev)
time.sleep(5) 
set_dac_cal_on_switchrpin_off(dev)
time.sleep(5)  
set_dac_cal_off_switchrpin_on(dev)
time.sleep(5)  
set_dac_cal_on_switchrpin_on(dev)
time.sleep(5)   

# %% Test neurodyn probe and expose signals

set_probe_on_expose_off(dev, 0b1011)
time.sleep(5)
set_probe_on_expose_on(dev, 0b1100)
time.sleep(5)
set_expose_on_probe_off_all_neurodyns(dev)
time.sleep(5)
set_expose_off_probe_off_all_neurodyns
time.sleep(5)

# %% Neurodyn main code
                                                                   
neurodyn_sel = 1                                                               # options - 0, 1, 2, 3
#write_external_DACs_neurodyn(dev, Vb, 0.9, neurodyn_sel+1)                      # last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4
#write_external_DACs_neurodyn(dev, IinVoltagePin, 0.6877, neurodyn_sel+1)          # IinVoltagePin = 0.752 -- Ivoltage = 366.9.8nA, dac = 0.727 -- Imaster = 271.2nA   
#write_external_DACs_neurodyn(dev, IinCurrentPin, 0.7063, neurodyn_sel+1)          # IinCurrentPin = 0.722 -- IMaster = 200.6nA, dac = 0.62 -- Imaster = 40.33nA, dac = 0.7575 -- Imaster = 400.2nA, dac = 1.2771 -- Imaster = 4.0004uA, dac = 0.7063 -- Imaster = 150nA
#write_external_DACs_neurodyn(dev, IinRefPin, 0.502, neurodyn_sel+1)              # IinRefPin = 0.672 -- IRef = 99.4 nA, dac = 0.443 -- Iref = 0.4nA, dac = 0.53 -- Iref = 4.08nA, dac = 0.622 -- Iref = 40.1nA, dac = 0.502 -- Iref = 2nA

write_external_DACs_neurodyn(dev, Vref_neurodyn, 0.901, neurodyn_sel+1)    # 0.9v      
write_external_DACs_neurodyn(dev, vBiasN, 1.365, neurodyn_sel+1)           # 1.4v        
write_external_DACs_neurodyn(dev, vBiasP, 1.694, neurodyn_sel+1)           # 1.7v        
write_external_DACs_neurodyn(dev, Vb, 0.9012, neurodyn_sel+1)              # 0.9v     
write_external_DACs_neurodyn(dev, IinVoltagePin, 1.154, neurodyn_sel+1)    # socket 1 - 1.154v -- 3uA       
write_external_DACs_neurodyn(dev, IinCurrentPin, 0.6211, neurodyn_sel+1)   # socket 1 - 0.6211v -- 40nA        
write_external_DACs_neurodyn(dev, IinRefPin, 0.4422, neurodyn_sel+1)       # socket 1 - 0.4422v -- 0.4nA       
write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)        # 0.9v      

chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 1)                        # 1 - howland current source; 2 - external DAC 
#set_probe_on_expose_off(dev, 2**neurodyn_sel)
set_expose_off_probe_off_all_neurodyns(dev)
#set_expose_on_probe_off_all_neurodyns(dev) 
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       
#set_dac_cal_off_switchrpin_off(dev)


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')

rise_time_list = []
fall_time_list = []


startTime = time.time()

#Gert's from email thread - NeuroDyn spiking (bursting?, HCO?) parameters
parms['biasgErev'][0][0] = [[512, 1023], [1023, 1023], [32, 400]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
parms['signgErev'][0][0] = [[1, 1], [1, -1], [1, 1]]                                                # sign bits for the same as described in line 274
parms['biasgErev'][1][0] = [[512, 1023], [1023, 1023], [32, 400]]                                     # Neuron 2
parms['signgErev'][1][0] = [[1, 1], [1, -1], [1, 1]]
parms['biasgErev'][2][0] = [[512, 1023], [1023, 1023], [32, 400]]                                     # Neuron 3
parms['signgErev'][2][0] = [[1, 1], [1, -1], [1, 1]]
parms['biasgErev'][3][0] = [[512, 1023], [1023, 1023], [32, 400]]                                     # Neuron 4
parms['signgErev'][3][0] = [[1, 1], [1, -1], [1, 1]]

#Luka's quantized parameters
#parms['biasgErev'][0][0] = [[1023, 829], [307, 829], [3, 545]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
#parms['signgErev'][0][0] = [[1, 1], [1, -1], [1, -1]]                                                # sign bits for the same as described in line 274
#parms['biasgErev'][1][0] = parms['biasgErev'][0][0]                                     # Neuron 2
#parms['signgErev'][1][0] = parms['signgErev'][0][0]
#parms['biasgErev'][2][0] = parms['biasgErev'][0][0]                                     # Neuron 3
#parms['signgErev'][2][0] = parms['signgErev'][0][0]
#parms['biasgErev'][3][0] = parms['biasgErev'][0][0]                                     # Neuron 4
#parms['signgErev'][3][0] = parms['signgErev'][0][0]

#Soumil's experiment
#dac = 4
#sigm_value_plus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                      # sigmoid DAC values for the monotonically increasing sigmoids 
#sigm_value_minus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                     # sigmoid DAC values for the monotonically decreasing sigmoids

#parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
#parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
#parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
#parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
#parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
#parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta

#Gert's from email thread - NeuroDyn spiking (bursting?, HCO?) parameters
parms['biasAlphaBeta'][0][0][0][0][:] = [0, 0, 0, 256, 0, 0, 0]           # m alpha
parms['biasAlphaBeta'][0][0][0][1][:] = [0, 0, 0, 256, 0, 0, 0]           # m beta
parms['biasAlphaBeta'][0][0][1][0][:] = [0, 0, 0, 32, 0, 0, 0]            # h alpha
parms['biasAlphaBeta'][0][0][1][1][:] = [0, 0, 0, 32, 0, 0, 0]            # h beta
parms['biasAlphaBeta'][0][0][2][0][:] = [0, 0, 0, 32, 0, 0, 0]            # n alpha
parms['biasAlphaBeta'][0][0][2][1][:] = [0, 0, 0, 32, 0, 0, 0]            # n beta

#Luka's quantized parameters
#parms['biasAlphaBeta'][0][0][0][0][:] = [0, 1, 11, 23, 0 , 0, 870]          # m alpha
#parms['biasAlphaBeta'][0][0][0][1][:] = [190, 4, 6, 0, 0, 0, 0]             # m beta
#parms['biasAlphaBeta'][0][0][1][0][:] = [3, 0, 0, 0, 0, 0, 0]               # h alpha
#parms['biasAlphaBeta'][0][0][1][1][:] = [0, 0, 6, 3, 0, 0, 0]               # h beta
#parms['biasAlphaBeta'][0][0][2][0][:] = [0, 0, 2, 2, 3, 0, 0]               # n alpha
#parms['biasAlphaBeta'][0][0][2][1][:] = [15, 0, 0, 0, 0, 0, 0]              # n beta

parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]                 # Neuron 2
parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]                 # Neuron 3
parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]                 # Neuron 4


parms['signAlphaBeta'][0][0] = [[1, -1], [-1, 1], [1, -1]]                  # Neuron 1
parms['signAlphaBeta'][1][0] = parms['signAlphaBeta'][0][0]                 # Neuron 2
parms['signAlphaBeta'][2][0] = parms['signAlphaBeta'][0][0]                 # Neuron 3
parms['signAlphaBeta'][3][0] = parms['signAlphaBeta'][0][0]                 # Neuron 4
       
# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]
    
for quadrantSel in [0, 1, 2, 3]:  # for soma
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  0, neurodyn_sel)


for quadrantSel in [0, 1, 2, 3]: 
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  1, neurodyn_sel)
    
neuron = 1
ifSynapse = 0
channelNum = 0
typ = 0                     # select alpha/beta rate, maximal conductance, reversal potential 
bumpNum = 0
addr = (neuron << 8) + (ifSynapse << 7) + (channelNum << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
set_internal_dacs_address(dev, addr, neurodyn_sel)

#bit = 1
#for i in range(100000):
#    parms['biasgErev'][0][0] = [[0, 1023], [0, 256], [1023, El + 50*bit]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
#    load_int_dacs_signbit_leak_channels(dev, parms['signgErev'], parms['biasgErev'], 0, 0, neurodyn_sel)
#    time.sleep(0.1)
#    bit = -bit
    
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
    my_Scope.write(':CHANnel'+str(channel+1)+':RANGe 1.6V')     #Sets the full scale vertical range in mV or V. The range value is 8 times the volts per division.
    #my_Scope.write(':CHANnel1:DISPlay OFF')


    #my_Scope.write(':WAVEFORM:UNSigned ON')
    #my_Scope.write(':DIGitize CHANnel'+str(channel))

    #my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(channel))
    #avg = my_Scope.query(':MEASure:VAVerage?');
    #print("The average voltage is", avg)

#%% Record alpha beta currents
 
neurodyn_sel = 0
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_on(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')

# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]

for quadrantSel in [0, 1, 2, 3]:  # for synapse
       load_int_dacs(dev, parms['signAlphaBeta'],
                     parms['signgErev'],
                     parms['biasAlphaBeta'],
                     parms['biasgErev'],
                     quadrantSel,
                     1, neurodyn_sel)
        

blank = [[[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]],

         [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]],

         [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]]


alpha_list = []
beta_list = []
Vmem_list = []

startTime = time.time()

for sigmoid in range(7):
    for sigmoid_value in [0, 256, 512, 768, 1023]:
        parms['biasAlphaBeta'][0][0] = blank
        for alpha_beta in [0, 1]:
            for m_h_n in [0, 1, 2]:
                parms['biasAlphaBeta'][0][0][m_h_n][alpha_beta][sigmoid] = sigmoid_value                     #set a sigmoid from S1-S7 for all gating variables and their opening closing rates 
    
        parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
        parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
        parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]
    
        for quadrantSel in [0, 1, 2, 3]:  # for soma
            load_int_dacs(dev, parms['signAlphaBeta'],
                          parms['signgErev'],
                          parms['biasAlphaBeta'],
                          parms['biasgErev'],
                          quadrantSel,
                          0, neurodyn_sel)
    
    
        ifSynapse = 0                            
        typ = 0         # not needed for VmemProbeIn, VmemBufMUX or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX
        bumpNum = 0     # not needed for VmemProbeIn, VmemBufMUX or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX
        
        for neuron in [2]:                                                      
            for channel in [0, 32, 64]:                                                                    # m,h,n =[0,32,64]; needed for selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX but not for VmemProbeIn, VmemBufMUX       
                addr = (neuron << 8) + (ifSynapse << 7) + (channel << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
                set_internal_dacs_address(dev, addr, neurodyn_sel)                                         # set internal dacs address to select neuron for voltage clamping through vmemprobein, for VmemBufMUX, and gating variable m/n/h for IalphaTapMUX, IBetaTapMUX output 
                    
                for vclamp in np.linspace(0.60, 1.20, 21, endpoint=True):  # sweep VmemProbeIn
                    write_external_DACs_neurodyn(dev, VmemProbeIn, vclamp, neurodyn_sel+1)
                    time.sleep(0.01)  # wait until stable
        
                    print('sigmoid' + str(sigmoid) + ': ' + str(sigmoid_value) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
                    
                    for scope_ch in [2, 3, 4]:
                        my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(scope_ch))
                        avg = my_Scope.query(':MEASure:VAVerage?')                          # recording average over 1 sec as scope range is set to 1 sec in ':TIMebase:RANGe 1E0' command
                        if scope_ch==2:
                            alpha_list.append((float(avg)/1.53)*1000)                              # switchRpin is on. IAlphaTapMUX current tap converted to voltage, across a 1.53M resistor whose one terminal is set to gnd and other comes out from IAlphaTapMUX pinon NeuroDyn chip
                            print("Average IAlphaTapMUX is", (float(avg)/1.53)*1000,'nA')       
                        elif scope_ch==3:
                            beta_list.append((float(avg)/1.53)*1000)                               # switchRpin is on. IBetaTapMUX current tap converted to voltage, across a 1.53M resistor whose one terminal is set to gnd and other comes out from IBetaTapMUX pinon NeuroDyn chip
                            print("Average IBetaTapMUX is", (float(avg)/1.53)*1000,'nA') 
                        elif scope_ch == 4:
                            Vmem_list.append(float(avg))
                            print("Measured membrane voltage clamp from VmemBufMUX", avg)
        #except:
        #        print('There is a error at:')
        #        print('sigmoid' + str(sigmoid) + ': ' + str(sigmoid_value) + ', VmemProbeIn:' + str(
        #            vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel) + ', alpha_beta')
                
executionTime = (time.time() - startTime)
print(executionTime)

np.savetxt('characterization/alpha beta currents/neurodyn 3/alpha.csv', alpha_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/alpha beta currents/neurodyn 3/beta.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/alpha beta currents/neurodyn 3/VmemBufMUX.csv', Vmem_list, delimiter=',', fmt='%4s')

#%% visualize alpha beta currents
import numpy as np
import matplotlib.pyplot as plt

alpha_list = np.loadtxt('characterization/alpha beta currents/neurodyn 3/alpha.csv', dtype=float)
beta_list = np.loadtxt('characterization/alpha beta currents/neurodyn 3/beta.csv', dtype=float)
alpha_array = np.array(alpha_list)
beta_array = np.array(beta_list)

#sigmoid_alpha = np.reshape(alpha_array, (-1, 3, 21))
#sigmoid_beta = np.reshape(beta_array, (-1, 3, 21))
sigmoid_alpha = np.reshape(alpha_array, (-1, 21))
sigmoid_beta = np.reshape(beta_array, (-1, 21))

m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

Vmem = np.linspace(0.6, 1.2, 21, endpoint=True)
sigm_value = [0, 256, 512, 768, 1023]

plt.close('all')
for neuron in [1]:

    fig = plt.figure()
    fig.patch.set_alpha(0.1)
    fig.subplots_adjust(hspace=0, wspace=0)
    
    #sigmoid_multi_alpha = sigmoid_alpha[neuron::4,:,:]
    #sigmoid_multi_beta = sigmoid_beta[neuron::4,:,:]
    
    #sigmoid_multi_alpha = np.reshape(sigmoid_multi_alpha, (-1, 21))
    #sigmoid_multi_beta = np.reshape(sigmoid_multi_beta, (-1, 21))
    
    for channel in [m, h, n]:
        #sigmoid_single_alpha = sigmoid_multi_alpha[channel::3, :]
        #sigmoid_single_beta = sigmoid_multi_beta[channel::3, :]
        sigmoid_single_alpha = sigmoid_alpha
        sigmoid_single_beta = sigmoid_beta
        
        for sigmoid_num in range(7):
            ax = fig.add_subplot(3, 7, 7 * channel + sigmoid_num + 1)
            ax.patch.set_facecolor('white')
            Font_Size = 12
            plt.ylabel('I ($nA$)', fontsize=Font_Size)
            plt.xlabel('Vmem $(V)$', fontsize=Font_Size)
    
            for sigmoid_value in range(5):
                plt.plot(Vmem, sigmoid_single_alpha[sigmoid_num * 5 + sigmoid_value, :], '*-', linewidth=0.6,
                         label=r'$\alpha$_' + str(sigm_value[sigmoid_value]))
                plt.plot(Vmem, sigmoid_single_beta[sigmoid_num * 5 + sigmoid_value, :], '*-', linewidth=0.6,
                         label=r'$\beta$_' + str(sigm_value[sigmoid_value]))
                #plt.ylim([-0.01, 0.19])
                #plt.yticks(np.arange(0.0, 0.2, step=0.02))
                plt.xlim([0.6, 1.2])
                plt.xticks([0.6, 0.9, 1.2])
                plt.text(0.32, 0.9, 'sigmoid' + str(sigmoid_num + 1) + ' of ' + ch_name[channel], fontsize=12,
                         color='black',transform=ax.transAxes)
            plt.legend(loc='center left', fontsize=Font_Size - 2, fancybox=False, prop={'size':7})
            
    fig.suptitle('Neuron '+str(neuron+1))
    plt.show()
    plt.savefig('characterization/alpha beta currents/neurodyn 3/figure'+str(neuron+1))
    

#%% record alpha beta currents with Teddy's parameters

neurodyn_sel = 0
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_on(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')


alpha_list = []
beta_list = []
Vmem_list = []

       
parms['biasAlphaBeta'][0][0] = [[[0, 0, 0, 0, 512, 512, 512],                         # parms['biasAlphaBeta'][0][0][0][0][:] -- alpha_m
                                     [512, 512, 512, 0, 0, 0, 0]],                    # parms['biasAlphaBeta'][0][0][0][1][:] -- beta_m

                                    [[128, 128, 0, 0, 0, 0, 0],                                 # parms['biasAlphaBeta'][0][0][1][0][:] -- alpha_h
                                     [0, 0, 0, 0, 0, 128, 128]],                                # parms['biasAlphaBeta'][0][0][1][1][:] -- beta_h

                                    [[0, 0, 0, 0, 0, 64, 64],                                 # parms['biasAlphaBeta'][0][0][2][0][:] = alpha_n
                                     [64, 64, 0, 0, 0, 0, 0]]]                               # parms['biasAlphaBeta'][0][0][2][1][:] = beta_n
parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]

for quadrantSel in [0, 1, 2, 3]:  # for soma
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  0, neurodyn_sel)

# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]

for quadrantSel in [0, 1, 2, 3]:  # for synapse
       load_int_dacs(dev, parms['signAlphaBeta'],
                     parms['signgErev'],
                     parms['biasAlphaBeta'],
                     parms['biasgErev'],
                     quadrantSel,
                     1, neurodyn_sel)
        
       
ifSynapse = 0                            
typ = 0         # not needed for VmemProbeIn, VmemBufMUX or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX
bumpNum = 0     # not needed for VmemProbeIn, VmemBufMUX or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX

for neuron in [0, 1, 2, 3]:                                                      
    for channel in [0, 32, 64]:                                                                    # m,h,n =[0,32,64]; needed for selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX but not for VmemProbeIn, VmemBufMUX       
        addr = (neuron << 8) + (ifSynapse << 7) + (channel << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
        set_internal_dacs_address(dev, addr, neurodyn_sel)                                         # set internal dacs address to select neuron for voltage clamping through vmemprobein, for VmemBufMUX, and gating variable m/n/h for IalphaTapMUX, IBetaTapMUX output 
            
        for vclamp in np.linspace(0.60, 1.20, 21, endpoint=True):  # sweep VmemProbeIn
            write_external_DACs_neurodyn(dev, VmemProbeIn, vclamp, neurodyn_sel+1)
            time.sleep(0.01)  # wait until stable
            print(' VmemProbeIn:' + str(vclamp)+ ', neuron' + str(neuron) + ', channel' +str(channel))
            #print('sigmoid' + str(sigmoid) + ': ' + str(sigmoid_value) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
            
            for scope_ch in [2, 3, 4]:
                my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(scope_ch))
                avg = my_Scope.query(':MEASure:VAVerage?')                          # recording average over 1 sec as scope range is set to 1 sec in ':TIMebase:RANGe 1E0' command
                if scope_ch==2:
                    alpha_list.append((float(avg)/1.53)*1000)                              # switchRpin is on. IAlphaTapMUX current tap converted to voltage, across a 1.53M resistor whose one terminal is set to gnd and other comes out from IAlphaTapMUX pinon NeuroDyn chip
                    print("Average IAlphaTapMUX is", (float(avg)/1.53)*1000,'nA')       
                elif scope_ch==3:
                    beta_list.append((float(avg)/1.53)*1000)                               # switchRpin is on. IBetaTapMUX current tap converted to voltage, across a 1.53M resistor whose one terminal is set to gnd and other comes out from IBetaTapMUX pinon NeuroDyn chip
                    print("Average IBetaTapMUX is", (float(avg)/1.53)*1000,'nA') 
                elif scope_ch == 4:
                    Vmem_list.append(float(avg))
                    print("Measured membrane voltage clamp from VmemBufMUX", avg)
#except:
#        print('There is a error at:')
#        print('sigmoid' + str(sigmoid) + ': ' + str(sigmoid_value) + ', VmemProbeIn:' + str(
#            vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel) + ', alpha_beta')
        
                
np.savetxt('characterization/alpha beta currents/neurodyn 3 w Teddys sigmoid dac values/alpha_teddy_parameters.csv', alpha_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/alpha beta currents/neurodyn 3 w Teddys sigmoid dac values/beta_teddy_parameters.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/alpha beta currents/neurodyn 3 w Teddys sigmoid dac values/VmemBufMUX_teddy_paramters.csv', Vmem_list, delimiter=',', fmt='%4s')


#%% visualize alpha beta currents from Teddy's parameters

alpha_list = np.loadtxt('characterization/alpha beta currents/neurodyn 38 w Teddys sigmoid dac values/alpha_teddy_parameters.csv', dtype=float)
beta_list = np.loadtxt('characterization/alpha beta currents/neurodyn 38 w Teddys sigmoid dac values/beta_teddy_parameters.csv', dtype=float)
alpha_array = np.array(alpha_list)
beta_array = np.array(beta_list)

sigmoid_alpha = np.reshape(alpha_array, (-1, 3, 21))
sigmoid_beta = np.reshape(beta_array, (-1, 3, 21))

m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

Vmem = np.linspace(0.6, 1.2, 21, endpoint=True)
Cg = 5e-12
Vt = 26e-3

plt.close('all')
for neuron in [0, 1, 2, 3]:

    fig = plt.figure()
    fig.patch.set_alpha(0.1)
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    
    sigmoid_multi_alpha = sigmoid_alpha[neuron::4,:,:]
    sigmoid_multi_beta = sigmoid_beta[neuron::4,:,:]
    
    sigmoid_multi_alpha = np.reshape(sigmoid_multi_alpha, (-1, 21))
    sigmoid_multi_beta = np.reshape(sigmoid_multi_beta, (-1, 21))
    
    print('sigmoid_multi_alpha: ')
    print(sigmoid_multi_alpha)
    print('sigmoid_multi_beta: ')
    print(sigmoid_multi_beta)
    for channel in [m, h, n]:

        ax = fig.add_subplot(1,3, channel+1) 
        ax.patch.set_facecolor('white')
        Font_Size = 12
        plt.ylabel('Rate ($1/msec$)', fontsize=Font_Size)
        plt.xlabel('Vmem $(V)$', fontsize=Font_Size)
        
        plt.plot(Vmem, sigmoid_multi_alpha[channel,:]*(1e-12/(Cg*Vt)), '.-', linewidth=0.6, label = r'$\alpha$_'+ch_name[channel])
        plt.plot(Vmem, sigmoid_multi_beta[channel,:]*(1e-12/(Cg*Vt)), '*-', linewidth=0.6, label = r'$\beta$_'+ch_name[channel])
        #plt.ylim([-0.01, 0.19])
        #plt.yticks(np.arange(0.0, 0.2, step=0.02))
        plt.xlim([0.6, 1.2])
        plt.xticks([0.6, 0.9, 1.2])
        plt.text(0.32, 0.9, r'$\alpha$_$\beta$'+' of ' +ch_name[channel], fontsize=12, color='black',transform=ax.transAxes)
        plt.legend(loc='center left', fontsize=Font_Size - 2, fancybox=False, prop={'size':7})
            
    fig.suptitle('Neuron '+str(neuron+1))
    plt.show()
    plt.savefig('characterization/alpha beta currents/neurodyn 38 w Teddys sigmoid dac values/figure'+str(neuron+1))
 

#%% gating variable kinetics translinear circuit capacitance Cg; should be ~5pF

neurodyn_sel = 1
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_on(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 1)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')


sigm_value_plus_sign_bit = [0, 0, 0, 255, 255, 255, 255]                     # sigmoid DAC values for the monotonically increasing sigmoids 
sigm_value_minus_sign_bit = [255, 255, 255, 255, 0, 0, 0]                    # sigmoid DAC values for the monotonically decreasing sigmoids

rise_time_list = []
fall_time_list = []
alpha_list = []
beta_list = []
gTap_list = []
read_count_list = []

my_Scope.write(':TIMebase:RANGe 50E-3')         # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.
#my_Scope.write(':TRIGger:MODE EDGE') 
#my_Scope.query(':TRIGger:MODE?') 
#my_Scope.write(':TRIGger:EDGE:SLOPe POSITIVE')
#my_Scope.query(':TRIGger:EDGE:SLOPe?') 
#my_Scope.write(':TRIGger:EDGE:SOURce CHANnel1')
#my_Scope.query(':TRIGger:EDGE:SOURce?') 
#my_Scope.timeout = 60000
#my_Scope.read_termination = '\r'
#my_Scope.write_termination = '\r'
#my_Scope.query('*IDN?')

# SYNAPSE PARAMETERS

# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]

for quadrantSel in [0, 1, 2, 3]:  # for synapse
       load_int_dacs(dev, parms['signAlphaBeta'],
                     parms['signgErev'],
                     parms['biasAlphaBeta'],
                     parms['biasgErev'],
                     quadrantSel,
                     1, neurodyn_sel)
        
m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

startTime = time.time()

bit = 1
while sigm_value_plus_sign_bit[0]<1023 and sigm_value_minus_sign_bit[6]< 1023:
    if bit == 1:
        for i in [0, 1, 2]:
            sigm_value_plus_sign_bit[i] = sigm_value_plus_sign_bit[i] + 256
        for i in [4, 5, 6]:
            sigm_value_minus_sign_bit[i] = sigm_value_minus_sign_bit[i] + 256
    elif bit == -1:
        for i in [3, 4, 5, 6]:
            sigm_value_plus_sign_bit[i] = sigm_value_plus_sign_bit[i] + 256
        for i in [0, 1, 2, 3]:
            sigm_value_minus_sign_bit[i] = sigm_value_minus_sign_bit[i] + 256
    
    parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
    parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
    parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
    parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
    parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
    parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta
    
    parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
    parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
    parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]
    
    for quadrantSel in [0, 1, 2, 3]:  # for soma
        load_int_dacs(dev, parms['signAlphaBeta'],
                      parms['signgErev'],
                      parms['biasAlphaBeta'],
                      parms['biasgErev'],
                      quadrantSel,
                      0, neurodyn_sel)
    
    
    ifSynapse = 0                            
    typ = 0         # not needed for VmemProbeIn or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX
    bumpNum = 0     # not needed for VmemProbeIn or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX
    
    for neuron in [0, 1, 2, 3]:                                                      
        for channel in [0, 32, 64]:                             # m,h,n =[0,32,64]; needed for selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX but not for VmemProbeIn       
            
            readings_count = 1
            addr = (neuron << 8) + (ifSynapse << 7) + (channel << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
            set_internal_dacs_address(dev, addr, neurodyn_sel)                                         # set internal dacs address to select neuron for voltage clamping through vmemprobein, for VmemBufMUX, and gating variable m/n/h for IalphaTapMUX, IBetaTapMUX output 
            
            bit_clamp = 1
            j = 1
            cnt = 1
        
            while j<=1000:  
    
                if cnt == 100:
                    cnt = 1
                    
                    for scope_ch in [1, 2, 3, 4]:
                        my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(scope_ch))
                        readings_count= readings_count+1
                        
                        if scope_ch == 1:          # IGateVarTapMUX
                            #if bit_clamp == 1:
                            rise_time = my_Scope.query(':MEASure:RISetime?')
                            rise_time_list.append((float(rise_time))*1e6)
                            print("rise time on ", ch_name[int(channel/32)]," is", (float(rise_time))*1e6,'usec')  
                            #else:
                            fall_time = my_Scope.query(':MEASure:FALLtime?') 
                            fall_time_list.append((float(fall_time))*1e6)
                            print("fall time on ", ch_name[int(channel/32)]," is", (float(fall_time))*1e6,'usec') 
           
                        elif scope_ch==2:         # IAlphaTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            alpha_list.append((float(avg)/1.53)*1000)                              # switchRpin is on.
                            print("IAlphaTapMUX is", (float(avg)/1.53)*1000,'nA')  
                                
                        elif scope_ch==3:         # IBetaTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            beta_list.append((float(avg)/1.53)*1000)                               # switchRpin is on.
                            print("IBetaTapMUX is", (float(avg)/1.53)*1000,'nA') 
                        
                        elif scope_ch == 4:       # gTapMUX
                                avg = my_Scope.query(':MEASure:VAVerage?')                          # switchRpin is on.
                                gTap_list.append((float(avg)/1.53)*1000)
                                print("gTapMUX is ", (float(avg)/1.53)*1000,'nA')  
                                                                  
                vclamp = 0.9 + bit_clamp*0.3                                                     # square pulse on VmemProbeIn
                write_external_DACs_neurodyn(dev, VmemProbeIn, vclamp, neurodyn_sel+1)
                time.sleep(0.005)  # wait until stable
                
                print('sigmoid plus: ' + str(sigm_value_plus_sign_bit) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
                print('sigmoid minus: ' + str(sigm_value_minus_sign_bit) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
                
                 
                bit_clamp = -bit_clamp
                cnt = cnt + 1
                
                j = j + 1
            read_count_list.append(float(readings_count))
    bit = -bit

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/rise_time.csv', rise_time_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/fall_time.csv', fall_time_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/alpha.csv', alpha_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/beta.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/gTap.csv', gTap_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/readings_count.csv', read_count_list, delimiter=',', fmt='%4s')
#np.savetxt('characterization/gating variable kinetics/gTap.csv', gTap_list, delimiter=',', fmt='%4s')
#np.savetxt('characterization/gating variable kinetics/readings_count.csv', read_count_list, delimiter=',', fmt='%4s')

#%% gating variable kinetics translinear circuit capacitance Cg -- mini version

neurodyn_sel = 1
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_on(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')


sigm_value_plus_sign_bit = [0, 0, 0, 255, 255, 255, 255]                     # sigmoid DAC values for the monotonically increasing sigmoids 
sigm_value_minus_sign_bit = [255, 255, 255, 255, 0, 0, 0]                    # sigmoid DAC values for the monotonically decreasing sigmoids

parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta

parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]

for quadrantSel in [0, 1, 2, 3]:  # for soma
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  0, neurodyn_sel)
    
# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]

for quadrantSel in [0, 1, 2, 3]: 
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  1, neurodyn_sel)


rise_time_list = []
fall_time_list = []
alpha_list = []
beta_list = []
Vmem_list = []

my_Scope.write(':TIMebase:RANGe 50E-3')         # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.

addr = (0 << 8) + (0 << 7) + (0 << 5) + (0 << 3) + 0            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
set_internal_dacs_address(dev, addr, neurodyn_sel)

bit_clamp = 1
j = 1
cnt_1sec = 1
startTime = time.time()
while j<=1000:                                                                      # square pulse on VmemProbeIn
    
    if cnt_1sec == 100:
        cnt_1sec = 1
        
        for scope_ch in [1, 2, 3, 4]:
            my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(scope_ch))
            if scope_ch == 1:
                #if bit_clamp == 1:
                rise_time = my_Scope.query(':MEASure:RISetime?')
                rise_time_list.append((float(rise_time))*1e6)
                print("rise time on ", ch_name[channel]," is", (float(rise_time))*1000,'usec')  
                #else:
                fall_time = my_Scope.query(':MEASure:FALLtime?') 
                fall_time_list.append((float(fall_time))*1e6)
                print("fall time on ", ch_name[channel]," is", (float(fall_time))*1000,'usec') 
            elif scope_ch==2:  # IAlphaTapMUX
                avg = my_Scope.query(':MEASure:VAVerage?')
                alpha_list.append((float(avg)/1.53)*1000)                              # switchRpin is on.
                print("IAlphaTapMUX is", (float(avg)/1.53)*1000,'nA')  
                    
            elif scope_ch==3:  # IBetaTapMUX
                avg = my_Scope.query(':MEASure:VAVerage?')
                beta_list.append((float(avg)/1.53)*1000)                               # switchRpin is on.
                print("IBetaTapMUX is", (float(avg)/1.53)*1000,'nA') 
            
            elif scope_ch == 4:  # VmemBufMUX
                    avg = my_Scope.query(':MEASure:VAVerage?')
                    Vmem_list.append(float(avg))
                    print("Measured membrane voltage clamp from VmemBufMUX", avg)
                    
    vclamp = 0.9 + bit_clamp*0.9
    write_external_DACs_neurodyn(dev, VmemProbeIn, vclamp, neurodyn_sel+1)
    time.sleep(0.005)  # wait until stable
    
    print('VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
    print('VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
    
    bit_clamp = -bit_clamp
    cnt_1sec = cnt_1sec + 1
      
    j = j+1

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/rise_time.csv', rise_time_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/fall_time.csv', fall_time_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/alpha.csv', alpha_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/beta.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/VmemBufMUX.csv', Vmem_list, delimiter=',', fmt='%4s')

#%% gating variable kinetics translinear circuit, achievable time constants assuming Cg = 5pF (mini version)

write_external_DACs_neurodyn(dev, IinCurrentPin, 0.9, 2)         # 0.67v - 175.2nA, last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4     
write_external_DACs_neurodyn(dev, IinRefPin, 0.6, 2)             # 0.79v - 1.421uA, last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4



neurodyn_sel = 0
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_off(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       
set_dac_cal_off_switchrpin_off(dev)

write_external_DACs_neurodyn(dev, VmemProbeIn, 0, neurodyn_sel+1)             # set default voltage clamp value to 0.9v

data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')

rise_time_list = []
fall_time_list = []


#Set scope
my_Scope.timeout = 15000                        # set scope timeout to 15 sec
my_Scope.write(':WAVEFORM:SOURCE CHANnel'+str(1))   # IGateVarTapMUX
my_Scope.query(':WAVEFORM:SOURce?')
my_Scope.write(':CHANnel'+str(4)+':RANGe 0.2V')


# Trigger settings
my_Scope.write(':TRIG:MODE EDGE')
my_Scope.write(':TRIG:SWEEP AUTO')
my_Scope.write(':TRIG:EDGE:COUP DC')
my_Scope.write(':TRIG:SLOP POS')
my_Scope.write(':TRIG:EDGE:SOUR CHAN1') # assume keithley on channel1


# SET Keithley for voltage source
rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')     # Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC VOLT')
my_K.write(':SOUR:VOLT:RANG 5')
my_K.write(':SOUR:VOLT:LEV 0.9')
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')

startTime = time.time()

dac = 64
sigm_value_plus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                     # sigmoid DAC values for the monotonically increasing sigmoids 
sigm_value_minus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                     # sigmoid DAC values for the monotonically decreasing sigmoids
bit = 1

#my_Scope.write(':TIMebase:RANGe ', str(384E-2/(np.log2(dac) + 1)))    #18e-2       # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.
my_Scope.write(':TIMebase:RANGe ', str(96E-2/(np.log2(dac) + 1)))    #18e-2       # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.


parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta

parms['signAlphaBeta'][0][0] = [[bit, -bit], [bit, -bit], [bit, -bit]]
            
parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]

parms['signAlphaBeta'][1][0] = parms['signAlphaBeta'][0][0]
parms['signAlphaBeta'][2][0] = parms['signAlphaBeta'][0][0]
parms['signAlphaBeta'][3][0] = parms['signAlphaBeta'][0][0]
       
# SYNAPSE PARAMETERS

# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]

for quadrantSel in [0, 1, 2, 3]:  # for soma
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  0, neurodyn_sel)

for quadrantSel in [0, 1, 2, 3]:  # for synapse
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  1, neurodyn_sel)
    
# Neuron 0, Im
addr = (3 << 8) + (0 << 7) + (0 << 5) + (0 << 3) + 0            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
set_internal_dacs_address(dev, addr, neurodyn_sel)

## sending current pulses over keithley

volt = 0.9
sign = 1

try:
    while(True):
    #for i in range(2000):
        my_K.write(':SOUR:VOLT:LEV '+str(0.9 + sign*volt))  
        sign = -sign
        time.sleep(0.48/(np.log2(dac) + 1))
except KeyboardInterrupt:
    my_K.write(':SOUR:VOLT:LEV 0.9')
    print('Voltage clamped to 0.9v.')

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

#%%
my_K.write(':OUTP OFF')
my_K.close 

#%% plot gating variable time constants -- dac value vs rise time -- Imaster = 175.2nA, Iref = 1.421uA -- manual data acquisition

dac = [4, 8, 16, 32, 64, 128, 256, 512, 1023]
x = np.zeros((4,9))
x = [[11, 5.03, 2.22, 1.23 ,0.98, 0.788, 0.64, 0.56, 0.7],
     [12, 5, 2.2, 1.31, 0.8, 0.6, 0.404, 0.305, 0.317],
     [8, 3.7, 1.76, 0.9, 0.8, 0.5, 0.3, 0.217, 0.238],
     [10.9, 5.88, 2.001, 1.3, 0.8, 0.5, 0.33, 0.224, 0.23],
     [10, 5, 2, 1.1, 0.755, 0.5, 0.33, 0.227, 0.214],
     [11, 5.5, 2.01, 1.1, 0.7, 0.5, 0.3, 0.2, 0.2],
     [7, 3.5, 1.85, 1, 0.65, 0.5, 0.3, 0.2, 0.18]]


ch_name = ['m','h','n']
channel = 0

fig = plt.figure()
fig.patch.set_alpha(0.1)
fig.subplots_adjust(hspace=0, wspace=0)
    
ax = fig.add_subplot(1, 1, 1)
ax.patch.set_facecolor('white')
Font_Size = 12
plt.ylabel('Rise time($msec$)', fontsize=Font_Size)
plt.xlabel('log2(DAC value)', fontsize=Font_Size)

plt.plot(np.log2(dac), x[0], '*-', linewidth=0.6, label=r'sigmoid 1')
plt.plot(np.log2(dac), x[1], '*-', linewidth=0.6, label=r'sigmoid 2')
plt.plot(np.log2(dac), x[2], '*-', linewidth=0.6, label=r'sigmoid 3')
plt.plot(np.log2(dac), x[3], '*-', linewidth=0.6, label=r'sigmoid 4')
plt.plot(np.log2(dac), x[4], '*-', linewidth=0.6, label=r'sigmoid 5')
plt.plot(np.log2(dac), x[5], '*-', linewidth=0.6, label=r'sigmoid 6')
plt.plot(np.log2(dac), x[6], '*-', linewidth=0.6, label=r'sigmoid 7')
#plt.plot(gate_steady_state[sigmoid_set, :], gate_single_var[sigmoid_set, :])
#plt.ylim([-0.01, 0.19])
#plt.yticks(np.arange(0.0, 0.2, step=0.02))
#plt.xlim([0, 0.2])
#plt.xticks([0.6, 0.9, 1.2])
#plt.text(0.32, 0.9, fontsize=12,
         #color='black',transform=ax.transAxes)
plt.legend(loc='center right', fontsize=Font_Size - 2, fancybox=False, prop={'size':7})

fig.suptitle('Gating variable time constants')
plt.show()
#plt.savefig('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/figure '+str(neuron+1))

#%% gating variable kinetics translinear circuit, achievable time constants assuming Cg = 5pF (complete version for characterising all neurons on a neurodyn)

neurodyn_sel = 0
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_off(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

#write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')

rise_time_list = []
fall_time_list = []


#Set scope
my_Scope.timeout = 15000                        # set scope timeout to 15 sec
my_Scope.write(':WAVEFORM:SOURCE CHANnel'+str(1))   # IGateVarTapMUX
my_Scope.query(':WAVEFORM:SOURce?')
my_Scope.write(':CHANnel'+str(1)+':RANGe 0.4V')

# Trigger settings
my_Scope.write(':TRIG:MODE EDGE')
my_Scope.write(':TRIG:SWEEP AUTO')
my_Scope.write(':TRIG:EDGE:COUP DC')
my_Scope.write(':TRIG:SLOP POS')
my_Scope.write(':TRIG:EDGE:SOUR CHAN1') # assume keithley on channel1


# set Keithley
rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC VOLT')
my_K.write(':SOUR:VOLT:RANG 5')
my_K.write(':SOUR:VOLT:LEV 0.9')
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')

# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]

for quadrantSel in [0, 1, 2, 3]: 
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  1, neurodyn_sel)
    
blank = [[[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]],

         [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]],

         [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]]

ch_list = ['m','h','n','r1','r2','r3']

rise_time_avg_list = []
fall_time_avg_list = []

sign = 1
startTime = time.time()

for i in range(2):
    for sigmoid in range(7):
        for sigmoid_value in [16, 32, 64, 128, 256, 512, 1023]:
            parms['biasAlphaBeta'][0][0] = blank
            for alpha_beta in [0, 1]:
                for m_h_n in [0, 1, 2]:
                    parms['biasAlphaBeta'][0][0][m_h_n][alpha_beta][sigmoid] = sigmoid_value                     #set a sigmoid from S1-S7 for all gating variables and their opening closing rates 
                    parms['signAlphaBeta'][0][0] = [[sign, -sign], [sign, -sign], [sign, -sign]]
    
                        
            parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
            parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
            parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]
        
            parms['signAlphaBeta'][1][0] = parms['signAlphaBeta'][0][0]
            parms['signAlphaBeta'][2][0] = parms['signAlphaBeta'][0][0]
            parms['signAlphaBeta'][3][0] = parms['signAlphaBeta'][0][0]
            
            for quadrantSel in [0, 1, 2, 3]:  # for soma
                load_int_dacs(dev, parms['signAlphaBeta'],
                              parms['signgErev'],
                              parms['biasAlphaBeta'],
                              parms['biasgErev'],
                              quadrantSel,
                              0, neurodyn_sel)
        
            my_Scope.write(':TIMebase:RANGe ', str(18E-2/(np.log2(sigmoid_value/16) + 1)))           # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.

            ifSynapse = 0                            
            typ = 0         # not needed for VmemProbeIn, VmemBufMUX or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX
            bumpNum = 0     # not needed for VmemProbeIn, VmemBufMUX or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX
            
            for neuron in [1]:  
            #for neuron in [0, 1, 2, 3]:
                for ifSynapse in [0]:   
                # for ifSynapse in [0, 1]:                                                 
                    for channel in [0, 32, 64]:    # m,h,n =[0,32,64]; needed for selecting m/n/h/r11/r12/r13 channel for IAlphaTapMUX, IBetaTapMUX but not for VmemProbeIn, VmemBufMUX       
                    
                        addr = (neuron << 8) + (ifSynapse << 7) + (channel << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
                        set_internal_dacs_address(dev, addr, neurodyn_sel)                                         # set internal dacs address to select neuron for voltage clamping through vmemprobein, for VmemBufMUX, and gating variable m/n/h for IalphaTapMUX, IBetaTapMUX output 
                        print('sigmoid: ', str(sigmoid), 'sigmoid value: ', str(sigmoid_value), 'sign: ', str(sign), 'neuron: ', str(neuron), 'channel: ', ch_list[int(channel/32)+ifSynapse*3])
                         ## sending current pulses over keithley
                        
                        ## sending current pulses over keithley
                        rise_time_list = []
                        #fall_time_list = []
                        
                        volt = 0.9
                        clamp_sign = 1
                        try:
                            for i in range(1000):
                                my_K.write(':SOUR:VOLT:LEV '+str(0.87 + clamp_sign*volt))  
                                my_Scope.write(':SINGLE') # set scope to look for single trigger
                                rise_time = my_Scope.query(':MEASure:RISetime?')
                                rise_time_list.append(rise_time)                        # enteries saved in msec
                                #fall_time = my_Scope.query(':MEASure:FALLtime?') 
                                #print("rise time on is ", (float(rise_time))*1e3,'msec')
                                #print("fall time on is ", (float(fall_time))*1e3,'msec') 
                                sign = -sign
                                time.sleep(0.03/(np.log2(sigmoid_value/16) + 1))
                        except KeyboardInterrupt:
                            my_K.write(':SOUR:VOLT:LEV 0.9')
                            print('Voltage clamped to 0.9v.')
                            
                        rise_time_list = np.array(rise_time_list)
                        rise_time_list = rise_time_list.astype(float)
                        
                        for i in range(len(rise_time_list)):
                            if rise_time_list[i] > (.04/(np.log2(sigmoid_value/16) + 1)):                   # remove all enteries above 5x times     
                                rise_time_list[i] = 0
                                
                            
                        rise_time_list = [i for i in rise_time_list if i != 0]
                        rise_time_avg_list.append(np.average(rise_time_list))                        
                        
                        #volt = 0.9
                        #sign_clamp = 1
                        #cnt = 1
                        #try:
                        #    for j in range(100):
                        #        my_K.write(':SOUR:VOLT:LEV '+str(0.87 + sign_clamp*volt))  
                        #        sign_clamp = -sign_clamp
                        #        time.sleep(0.01)
                        #        cnt = cnt+1
                        #        if cnt == 10:
                        #            cnt = 1
                        #            if sign_clamp == 1:
                        #                rise_time = my_Scope.query(':MEASure:RISetime?')
                        #                rise_time_list.append((float(rise_time))*1e6)
                        #                print("rise time on is ", (float(rise_time))*1e6,'usec')
                        #            else:
                        #                fall_time = my_Scope.query(':MEASure:FALLtime?') 
                        #               fall_time_list.append((float(fall_time))*1e6)
                        #                print("fall time on is ", (float(fall_time))*1e6,'usec') 
                
                        #except KeyboardInterrupt:
                        #    my_K.write(':SOUR:VOLT:LEV 0.9')
                        #    print('Voltage clamped to 0.9v.')

sign  = -sign
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))


np.savetxt('characterization/gating variable kinetics/neurodyn 11/translinear circuit capacitance Cg/rise_time_avg_list.csv', rise_time_list, delimiter=',', fmt='%4s')
#np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/fall_time.csv', fall_time_list, delimiter=',', fmt='%4s')
#np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/alpha.csv', alpha_list, delimiter=',', fmt='%4s')
#np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/beta.csv', beta_list, delimiter=',', fmt='%4s')
#np.savetxt('characterization/gating variable kinetics/neurodyn 38/translinear circuit capacitance Cg/VmemBufMUX.csv', Vmem_list, delimiter=',', fmt='%4s')

#%%
my_K.write(':OUTP OFF')
my_K.close

#%% observing ion channel currents from gTap (mini)

write_external_DACs_neurodyn(dev, IinCurrentPin, 0.67, 2)         # 0.67v - 175.2nA, last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4     
write_external_DACs_neurodyn(dev, IinRefPin, 0.7, 2)             # 0.79v - 1.421uA, last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4



neurodyn_sel = 1
chip_init(dev, neurodyn_sel)

set_dac_cal_off_switchrpin_off(dev)                         # measure ITaps as currents -- switchRpin off
set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_off(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 1)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')

rise_time_list = []
fall_time_list = []


#Set scope
my_Scope.timeout = 15000                        # set scope timeout to 15 sec
my_Scope.write(':WAVEFORM:SOURCE CHANnel'+str(1))   # IGateVarTapMUX
my_Scope.query(':WAVEFORM:SOURce?')
my_Scope.write(':CHANnel'+str(1)+':RANGe 0.2V')


# Trigger settings
my_Scope.write(':TRIG:MODE EDGE')
my_Scope.write(':TRIG:SWEEP AUTO')
my_Scope.write(':TRIG:EDGE:COUP DC')
my_Scope.write(':TRIG:SLOP POS')
my_Scope.write(':TRIG:EDGE:SOUR CHAN1') # assume keithley on channel1


# SET Keithley for voltage source
rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC VOLT')
my_K.write(':SOUR:VOLT:RANG 5')
my_K.write(':SOUR:VOLT:LEV 0.9')
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')

startTime = time.time()

dac = 8
sigm_value_plus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                     # sigmoid DAC values for the monotonically increasing sigmoids 
sigm_value_minus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                     # sigmoid DAC values for the monotonically decreasing sigmoids
bit = 1

#my_Scope.write(':TIMebase:RANGe ', str(384E-2/(np.log2(dac) + 1)))    #18e-2       # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.
my_Scope.write(':TIMebase:RANGe ', str(96E-2/(np.log2(dac) + 1)))    #18e-2       # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.


parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta

parms['signAlphaBeta'][0][0] = [[bit, -bit], [-bit, bit], [bit, -bit]]
            
parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]

parms['signAlphaBeta'][1][0] = parms['signAlphaBeta'][0][0]
parms['signAlphaBeta'][2][0] = parms['signAlphaBeta'][0][0]
parms['signAlphaBeta'][3][0] = parms['signAlphaBeta'][0][0]
        
# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1,
                                              1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]

neuron = 1

parms['biasgErev'][neuron][0] = [[128, 1023], [1023, 256], [10, 10]]                         # parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
parms['signgErev'][neuron][0] = [[1, 1], [1, -1], [1, 1]]                                    # sign bits for same as above indices
     
for quadrantSel in [0, 1, 2, 3]:  # for soma
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  0, neurodyn_sel)
    
for quadrantSel in [0, 1, 2, 3]:  # for soma
load_int_dacs(dev, parms['signAlphaBeta'],
              parms['signgErev'],
              parms['biasAlphaBeta'],
              parms['biasgErev'],
              quadrantSel,
              1, neurodyn_sel)

addr = (neuron << 8) + (0 << 7) + (0 << 5) + (0 << 3) + 0            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
set_internal_dacs_address(dev, addr, neurodyn_sel)

## sending current pulses over keithley


import threading

def volt_pulse():
    volt = 0.9
    sign = 1
    try:
        while(True):
        #for i in range(2000):
            my_K.write(':SOUR:VOLT:LEV '+str(0.87 + sign*volt))  
            #my_Scope.write(':SINGLE') # set scope to look for single trigger
            #rise_time = my_Scope.query(':MEASure:RISetime?')
            #rise_time_list.append(rise_time)                        # enteries saved in msec
            #fall_time = my_Scope.query(':MEASure:FALLtime?') 
            #print("rise time on is ", (float(rise_time))*1e3,'msec')
            #print("fall time on is ", (float(fall_time))*1e3,'msec') 
            sign = -sign
            time.sleep(0.48/(np.log2(dac) + 1))
    except KeyboardInterrupt:
        my_K.write(':SOUR:VOLT:LEV 0.9')
        print('Voltage clamped to 0.9v.')
        
x = threading.Thread(target=volt_pulse, daemon=True)
x.setDaemon(True)
print(x.isDaemon())
x.start()

answer = input("Do you wish to exit?")

 
#rise_time_list = np.array(rise_time_list)
#rise_time_list = rise_time_list.astype(float)

#for i in range(len(rise_time_list)):
#    if rise_time_list[i] > (.04/(np.log2(dac/16) + 1)):                   # remove all enteries above expected 5x    
#        rise_time_list[i] = 0
        
    
#rise_time_list = [i for i in rise_time_list if i != 0]
#rise_time_avg = np.average(rise_time_list)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
 
#%% regress IGateVarTapMUX against alpha/(alpha+beta)

neurodyn_sel = 0
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_on(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 1)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')


sigm_value_plus_sign_bit = [0, 0, 0, 255, 255, 255, 255]                     # sigmoid DAC values for the monotonically increasing sigmoids 
sigm_value_minus_sign_bit = [255, 255, 255, 255, 0, 0, 0]                    # sigmoid DAC values for the monotonically decreasing sigmoids

gate_var_list = []
alpha_list = []
beta_list = []
gTap_list = []

my_Scope.write(':TIMebase:RANGe 50E-3')         # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.
#my_Scope.write(':TRIGger:MODE EDGE') 
#my_Scope.query(':TRIGger:MODE?') 
#my_Scope.write(':TRIGger:EDGE:SLOPe POSITIVE')
#my_Scope.query(':TRIGger:EDGE:SLOPe?') 
#my_Scope.write(':TRIGger:EDGE:SOURce CHANnel1')
#my_Scope.query(':TRIGger:EDGE:SOURce?') 
#my_Scope.timeout = 60000
#my_Scope.read_termination = '\r'
#my_Scope.write_termination = '\r'
#my_Scope.query('*IDN?')

m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

startTime = time.time()

bit = 1
while sigm_value_plus_sign_bit[0]<=1023 and sigm_value_minus_sign_bit[6]<= 1023:
    
    parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
    parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
    parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
    parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
    parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
    parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta
    
    parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
    parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
    parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]
    
    for quadrantSel in [0, 1, 2, 3]:  # for soma
        load_int_dacs(dev, parms['signAlphaBeta'],
                      parms['signgErev'],
                      parms['biasAlphaBeta'],
                      parms['biasgErev'],
                      quadrantSel,
                      0, neurodyn_sel)
    
    
    ifSynapse = 0                            
    typ = 0         # not needed for VmemProbeIn or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX
    bumpNum = 0     # not needed for VmemProbeIn or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX
    
    for neuron in [0, 1, 2, 3]:                                                      
        for channel in [0, 32, 64]:                             # m,h,n =[0,32,64]; needed for selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX but not for VmemProbeIn       
            addr = (neuron << 8) + (ifSynapse << 7) + (channel << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
            set_internal_dacs_address(dev, addr, neurodyn_sel)                                         # set internal dacs address to select neuron for voltage clamping through vmemprobein, for VmemBufMUX, and gating variable m/n/h for IalphaTapMUX, IBetaTapMUX output 
        
            for vclamp in np.linspace(0.60, 1.20, 21, endpoint=True):  # sweep VmemProbeIn
                write_external_DACs_neurodyn(dev, VmemProbeIn, vclamp, neurodyn_sel+1)
                
                time.sleep(0.005)  # wait until stable
        
                print('sigmoid plus: ' + str(sigm_value_plus_sign_bit) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
                print('sigmoid minus: ' + str(sigm_value_minus_sign_bit) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
                
                for scope_ch in [1, 2, 3, 4]:
                        my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(scope_ch))
                       
                        if scope_ch == 1:          # IGateVarTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            gate_var_list.append((float(avg)/1.53)*1000)                           # switchRpin is on.
                            print("IGateVarTapMUX is", (float(avg)/1.53)*1000,'nA')  
           
                        elif scope_ch==2:         # IAlphaTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            alpha_list.append((float(avg)/1.53)*1000)                              # switchRpin is on.
                            print("IAlphaTapMUX is", (float(avg)/1.53)*1000,'nA')  
                                
                        elif scope_ch==3:         # IBetaTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            beta_list.append((float(avg)/1.53)*1000)                               # switchRpin is on.
                            print("IBetaTapMUX is", (float(avg)/1.53)*1000,'nA') 
                        
                        elif scope_ch == 4:       # gTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')                             # switchRpin is on.
                            gTap_list.append((float(avg)/1.53)*1000)
                            print("gTapMUX is ", (float(avg)/1.53)*1000,'nA')
    
    
    if sigm_value_plus_sign_bit[0]==0 and sigm_value_minus_sign_bit[6]==0:
        for i in [0, 1, 2]:
            sigm_value_plus_sign_bit[i] = sigm_value_plus_sign_bit[i] + 255
        for i in [4, 5, 6]:
            sigm_value_minus_sign_bit[i] = sigm_value_minus_sign_bit[i] + 255                
    elif bit == 1:
        for i in [3, 4, 5, 6]:
            sigm_value_plus_sign_bit[i] = sigm_value_plus_sign_bit[i] + 256
        for i in [0, 1, 2, 3]:
            sigm_value_minus_sign_bit[i] = sigm_value_minus_sign_bit[i] + 256
        
    elif bit == -1:
        for i in [0, 1, 2]:
            sigm_value_plus_sign_bit[i] = sigm_value_plus_sign_bit[i] + 256
        for i in [4, 5, 6]:
            sigm_value_minus_sign_bit[i] = sigm_value_minus_sign_bit[i] + 256
    bit = -bit

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/gate_var.csv', gate_var_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/alpha.csv', alpha_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/beta.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/gTap.csv', gTap_list, delimiter=',', fmt='%4s')

#%% regress IGateVarTapMUX against alpha/(alpha+beta) v2

neurodyn_sel = 1
chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
set_probe_on_expose_on(dev, 2**neurodyn_sel)
set_neurodyn_outputs_mux(dev, 1)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')


sigm_value_plus_sign_bit = [255, 255, 255, 255, 255, 255, 255]                     # sigmoid DAC values for the monotonically increasing sigmoids 
sigm_value_minus_sign_bit = [255, 255, 255, 255, 255, 255, 255]                    # sigmoid DAC values for the monotonically decreasing sigmoids

gate_var_list = []
alpha_list = []
beta_list = []
gTap_list = []

my_Scope.write(':TIMebase:RANGe 50E-3')         # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.
#my_Scope.write(':TRIGger:MODE EDGE') 
#my_Scope.query(':TRIGger:MODE?') 
#my_Scope.write(':TRIGger:EDGE:SLOPe POSITIVE')
#my_Scope.query(':TRIGger:EDGE:SLOPe?') 
#my_Scope.write(':TRIGger:EDGE:SOURce CHANnel1')
#my_Scope.query(':TRIGger:EDGE:SOURce?') 
#my_Scope.timeout = 60000
#my_Scope.read_termination = '\r'
#my_Scope.write_termination = '\r'
#my_Scope.query('*IDN?')

m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

startTime = time.time()

while sigm_value_plus_sign_bit[0]<=1023 and sigm_value_minus_sign_bit[0]<= 1023:
    
    parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
    parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
    parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
    parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
    parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
    parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta
    
    parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]
    parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]
    parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]
    
    for quadrantSel in [0, 1, 2, 3]:  # for soma
        load_int_dacs(dev, parms['signAlphaBeta'],
                      parms['signgErev'],
                      parms['biasAlphaBeta'],
                      parms['biasgErev'],
                      quadrantSel,
                      0, neurodyn_sel)
    
    
    ifSynapse = 0                            
    typ = 0         # not needed for VmemProbeIn or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX
    bumpNum = 0     # not needed for VmemProbeIn or selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX
    
    for neuron in [0, 1, 2, 3]:                                                      
        for channel in [0, 32, 64]:                             # m,h,n =[0,32,64]; needed for selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX, gTapMUX but not for VmemProbeIn       
            addr = (neuron << 8) + (ifSynapse << 7) + (channel << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
            set_internal_dacs_address(dev, addr, neurodyn_sel)                                         # set internal dacs address to select neuron for voltage clamping through vmemprobein, for VmemBufMUX, and gating variable m/n/h for IalphaTapMUX, IBetaTapMUX output 
        
            for vclamp in np.linspace(0.60, 1.20, 21, endpoint=True):  # sweep VmemProbeIn
                write_external_DACs_neurodyn(dev, VmemProbeIn, vclamp, neurodyn_sel+1)
                
                time.sleep(0.005)  # wait until stable
        
                print('sigmoid plus: ' + str(sigm_value_plus_sign_bit) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
                print('sigmoid minus: ' + str(sigm_value_minus_sign_bit) + ', VmemProbeIn:' + str(vclamp) + ', neuron' + str(neuron) + ', channel' + str(channel)) 
                
                for scope_ch in [1, 2, 3, 4]:
                        my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(scope_ch))
                       
                        if scope_ch == 1:          # IGateVarTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            gate_var_list.append((float(avg)/1.53)*1000)                           # switchRpin is on.
                            print("IGateVarTapMUX is", (float(avg)/1.53)*1000,'nA')  
           
                        elif scope_ch==2:         # IAlphaTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            alpha_list.append((float(avg)/1.53)*1000)                              # switchRpin is on.
                            print("IAlphaTapMUX is", (float(avg)/1.53)*1000,'nA')  
                                
                        elif scope_ch==3:         # IBetaTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')
                            beta_list.append((float(avg)/1.53)*1000)                               # switchRpin is on.
                            print("IBetaTapMUX is", (float(avg)/1.53)*1000,'nA') 
                        
                        elif scope_ch == 4:       # gTapMUX
                            avg = my_Scope.query(':MEASure:VAVerage?')                             # switchRpin is on.
                            gTap_list.append((float(avg)/1.53)*1000)
                            print("gTapMUX is ", (float(avg)/1.53)*1000,'nA')
    
    
    for i in range(7):
        sigm_value_plus_sign_bit[i] = sigm_value_plus_sign_bit[i] + 256
        sigm_value_minus_sign_bit[i] = sigm_value_minus_sign_bit[i] + 256


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

np.savetxt('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/gate_var_Iref_0.85v.csv', gate_var_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/gate_var_Iref_0.85v.csv', gate_var_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/alpha.csv', alpha_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/alpha.csv', gate_var_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/beta.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/beta.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/gTap_Iref_0.85v.csv', gTap_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/gTap_Iref_0.85v.csv', beta_list, delimiter=',', fmt='%4s')


# %% plot regression of IGateVarTapMUX against Ialpha/(Ialpha+Ibeta)
gate_var_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/gate_var_Iref_0.85v.csv', dtype=float)
alpha_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/alpha.csv', dtype=float)
beta_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/beta.csv', dtype=float)


gate_var_array = np.array(gate_var_list)
alpha_array = np.array(alpha_list)
beta_array = np.array(beta_list)

gate_var = np.reshape(gate_var_array, (-1, 3, 21))
sigmoid_alpha = np.reshape(alpha_array, (-1, 3, 21))
sigmoid_beta = np.reshape(beta_array, (-1, 3, 21))

m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

Vmem = np.linspace(0.6, 1.2, 21, endpoint=True)

plt.close('all')
for neuron in [0, 1, 2, 3]:

    fig = plt.figure()
    fig.patch.set_alpha(0.1)
    fig.subplots_adjust(hspace=0, wspace=0)
    
    gate_multi_var = gate_var[neuron::4,:,:]
    sigmoid_multi_alpha = sigmoid_alpha[neuron::4,:,:]
    sigmoid_multi_beta = sigmoid_beta[neuron::4,:,:]
    
    gate_multi_var = np.reshape(gate_multi_var, (-1, 21))
    sigmoid_multi_alpha = np.reshape(sigmoid_multi_alpha, (-1, 21))
    sigmoid_multi_beta = np.reshape(sigmoid_multi_beta, (-1, 21))
    
    for channel in [m, h, n]:
        gate_single_var = gate_multi_var[channel::3, :]
        sigmoid_single_alpha = sigmoid_multi_alpha[channel::3, :]
        sigmoid_single_beta = sigmoid_multi_beta[channel::3, :]

        gate_steady_state = np.divide(sigmoid_single_alpha, np.add(sigmoid_single_alpha, sigmoid_single_beta))
        
        ax = fig.add_subplot(3, 1, channel + 1)
        ax.patch.set_facecolor('white')
        Font_Size = 12
        plt.ylabel('I ($nA$)', fontsize=Font_Size)
        plt.xlabel('Ialpha/(Ialpha+IBeta)', fontsize=Font_Size)
    
        for sigmoid_set in range(4):
            z = np.polyfit(gate_steady_state[sigmoid_set, :], gate_single_var[sigmoid_set, :], 1)
            p = np.poly1d(z)
            xp = np.linspace(0, 1, 100)
            plt.plot(xp, p(xp), '-', linewidth=0.6, label=r'set '+str(sigmoid_set+1)+'slope: '+str(z[0]))
            plt.plot(gate_steady_state[sigmoid_set, :], gate_single_var[sigmoid_set, :], '*-', linewidth=0.6, label=r'set '+str(sigmoid_set+1))
            #plt.plot(gate_steady_state[sigmoid_set, :], gate_single_var[sigmoid_set, :])
            #plt.ylim([-0.01, 0.19])
            #plt.yticks(np.arange(0.0, 0.2, step=0.02))
            plt.xlim([0, 1])
            #plt.xticks([0.6, 0.9, 1.2])
            plt.text(0.32, 0.9, ch_name[channel], fontsize=12,
                     color='black',transform=ax.transAxes)
        plt.legend(loc='center left', fontsize=Font_Size - 2, fancybox=False, prop={'size':7})
        
    fig.suptitle('Neuron '+str(neuron+1) +': Measured steady-state gating variable current vs measured Ialpha/Ialpha+Ibeta')
    plt.show()
    plt.savefig('characterization/gating variable kinetics/neurodyn 38/gating variable offset, slope/figure'+str(neuron+1)+' Regressing Igating variable vs measured SS gating variable_850mv_Iref_dac' )

# %% plot regression of log(gTapMUX) vs log(gating variables)
gTap_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/gTap_Iref_0.85v.csv', dtype=float)
gate_var_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/gate_var_Iref_0.85v.csv', dtype=float)

gTap_array = np.array(gTap_list)
gate_var_array = np.array(gate_var_list)

gTap = np.reshape(gTap_array, (-1, 3, 21))
gate_var = np.reshape(gate_var_array, (-1, 3, 21))

m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

Vmem = np.linspace(0.6, 1.2, 21, endpoint=True)

plt.close('all')
for neuron in [0, 1, 2, 3]:

    fig = plt.figure()
    fig.patch.set_alpha(0.1)
    fig.subplots_adjust(hspace=0, wspace=0)
    
    gTap_multi = gTap[neuron::4,:,:]
    gate_multi_var = gate_var[neuron::4,:,:]
    
    gTap_multi = np.reshape(gTap_multi, (-1, 21))
    gate_multi_var = np.reshape(gate_multi_var, (-1, 21))
    
    #for channel in [m, h, n]:
    gTap_Na = gTap_multi[0::3,:]                # gTap_Na contains Na currents for different sigmoid sets (and across the voltage range 0.6 - 1.2v)
    gTap_K = gTap_multi[1::3,:]
    gate_var_m = gate_multi_var[0::3, :]
    gate_var_h = gate_multi_var[1::3, :]
    gate_var_n = gate_multi_var[2::3, :]

    
    #log_gate_var_K= np.log(gate_var_n+20)
    #log_gTap_K = np.log(gTap_K+ 20)
    for channel in [m, h, n]:
        ax = fig.add_subplot(3, 1, channel+1)
        ax.patch.set_facecolor('white')
        Font_Size = 12
        plt.ylabel('I ($nA$)', fontsize=Font_Size)
        plt.xlabel('Vmem', fontsize=Font_Size)
        
        for sigmoid_set in range(4):
            #plt.plot(log_gate_var_K[sigmoid_set, :], log_gTap_K[sigmoid_set, :], '*-', linewidth=0.6, label=r'set '+str(sigmoid_set+1))
            if channel ==0:
                plt.plot(Vmem, gate_var_m[sigmoid_set, :], '*-', linewidth=0.6, label=r'Im, set '+str(sigmoid_set+1))
                plt.plot(Vmem, gTap_Na[sigmoid_set, :], '*-', linewidth=0.6, label=r'INa, set '+str(sigmoid_set+1))
            elif channel==1:
                plt.plot(Vmem, gate_var_h[sigmoid_set, :], '*-', linewidth=0.6, label=r'Ih, set '+str(sigmoid_set+1))
            elif channel==2:
                plt.plot(Vmem, gate_var_n[sigmoid_set, :], '*-', linewidth=0.6, label=r'In, set '+str(sigmoid_set+1))
                plt.plot(Vmem, gTap_K[sigmoid_set, :], '*-', linewidth=0.6, label=r'IK, set '+str(sigmoid_set+1))
            #plt.plot(gate_steady_state[sigmoid_set, :], gate_single_var[sigmoid_set, :])
            #plt.ylim([-0.01, 0.19])
            #plt.yticks(np.arange(0.0, 0.2, step=0.02))
            #plt.xlim([0, 0.2])
            #plt.xticks([0.6, 0.9, 1.2])
            plt.text(0.32, 0.9, ch_name[channel], fontsize=12,
                     color='black',transform=ax.transAxes)
            plt.legend(loc='center left', fontsize=Font_Size - 2, fancybox=False, prop={'size':7})
        
    fig.suptitle('Neuron '+str(neuron+1))
    plt.show()
    plt.savefig('characterization/gating variable kinetics/neurodyn 38/power coefficients for n, m, h/figure '+str(neuron+1))
                
    
#%% DIC -- clamp Vmem @El and perturb ENa, EK, El -- measure changes in Vmem

neurodyn_sel = 3                                                                 # options - 0, 1, 2, 3
#write_external_DACs_neurodyn(dev, Vb, 0.9, neurodyn_sel+1)                      # last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4
#write_external_DACs_neurodyn(dev, IinVoltagePin, 0.6877, neurodyn_sel+1)          # IinVoltagePin = 0.752 -- Ivoltage = 366.9.8nA, dac = 0.727 -- Imaster = 271.2nA   
#write_external_DACs_neurodyn(dev, IinCurrentPin, 0.7063, neurodyn_sel+1)          # IinCurrentPin = 0.722 -- IMaster = 200.6nA, dac = 0.62 -- Imaster = 40.33nA, dac = 0.7575 -- Imaster = 400.2nA, dac = 1.2771 -- Imaster = 4.0004uA, dac = 0.7063 -- Imaster = 150nA
#write_external_DACs_neurodyn(dev, IinRefPin, 0.502, neurodyn_sel+1)              # IinRefPin = 0.672 -- IRef = 99.4 nA, dac = 0.443 -- Iref = 0.4nA, dac = 0.53 -- Iref = 4.08nA, dac = 0.622 -- Iref = 40.1nA, dac = 0.502 -- Iref = 2nA

write_external_DACs_neurodyn(dev, Vref_neurodyn, 0.901, neurodyn_sel+1)    # 0.9v      
write_external_DACs_neurodyn(dev, vBiasN, 1.365, neurodyn_sel+1)           # 1.4v        
write_external_DACs_neurodyn(dev, vBiasP, 1.694, neurodyn_sel+1)           # 1.7v        
write_external_DACs_neurodyn(dev, Vb, 0.9012, neurodyn_sel+1)              # 0.9v     
write_external_DACs_neurodyn(dev, IinVoltagePin, 1.152, neurodyn_sel+1)    # socket 1 - 1.152v -- 3uA       
write_external_DACs_neurodyn(dev, IinCurrentPin, 0.9074, neurodyn_sel+1)   # socket 1 - 0.6211v -- 40nA        
write_external_DACs_neurodyn(dev, IinRefPin, 0.5714, neurodyn_sel+1)       # socket 1 - 0.4422v -- 0.4nA       
write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)        # 0.9v      

chip_init(dev, neurodyn_sel)

set_current_source_selector_switch_all_neurodyns(dev, 1)                        # 1 - howland current source; 2 - external DAC 
#set_probe_on_expose_off(dev, 2**neurodyn_sel)
set_expose_off_probe_off_all_neurodyns(dev)
#set_expose_on_probe_off_all_neurodyns(dev) 
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       
#set_dac_cal_off_switchrpin_off(dev)


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')

rise_time_list = []
fall_time_list = []


startTime = time.time()

#Gert's parameters from email thread - NeuroDyn spiking (bursting?, HCO?) parameters
parms['biasgErev'][0][0] = [[1023, 829], [420, 829], [3, 545]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
parms['signgErev'][0][0] = [[1, 1], [1, -1], [1, -1]]                                                # sign bits for the same as described in line 274
parms['biasgErev'][1][0] = [[1023, 829], [420, 829], [3, 545]]                                     # Neuron 2
parms['signgErev'][1][0] = [[1, 1], [1, -1], [1, -1]]
parms['biasgErev'][2][0] = [[1023, 829], [420, 829], [3, 545]]                                     # Neuron 3
parms['signgErev'][2][0] = [[1, 1], [1, -1], [1, -1]]
parms['biasgErev'][3][0] = [[1023, 829], [420, 829], [3, 545]]                                     # Neuron 4
parms['signgErev'][3][0] = [[1, 1], [1, -1], [1, -1]]


#Soumil's experiment
#dac = 4
#sigm_value_plus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                      # sigmoid DAC values for the monotonically increasing sigmoids 
#sigm_value_minus_sign_bit = [0, 0, 0, dac, 0, 0, 0]                     # sigmoid DAC values for the monotonically decreasing sigmoids

#parms['biasAlphaBeta'][0][0][0][0][:] = sigm_value_plus_sign_bit         # m alpha
#parms['biasAlphaBeta'][0][0][0][1][:] = sigm_value_minus_sign_bit        # m beta
#parms['biasAlphaBeta'][0][0][1][0][:] = sigm_value_minus_sign_bit        # h alpha
#parms['biasAlphaBeta'][0][0][1][1][:] = sigm_value_plus_sign_bit         # h beta
#parms['biasAlphaBeta'][0][0][2][0][:] = sigm_value_plus_sign_bit         # n alpha
#parms['biasAlphaBeta'][0][0][2][1][:] = sigm_value_minus_sign_bit        # n beta

#Gert's from email thread - NeuroDyn spiking (bursting?, HCO?) parameters
parms['biasAlphaBeta'][0][0][0][0][:] = [0, 1, 12, 27, 0, 0, 1023]           # m alpha
parms['biasAlphaBeta'][0][0][0][1][:] = [223, 5, 7, 0, 0, 0, 1]           # m beta
parms['biasAlphaBeta'][0][0][1][0][:] = [2, 1, 0, 0, 0, 0, 0]            # h alpha
parms['biasAlphaBeta'][0][0][1][1][:] = [0, 0, 5, 5, 0, 0, 0]            # h beta
parms['biasAlphaBeta'][0][0][2][0][:] = [0, 0, 4, 2, 2, 2, 2]            # n alpha
parms['biasAlphaBeta'][0][0][2][1][:] = [1, 0, 0, 0, 0, 0, 1]            # n beta

parms['biasAlphaBeta'][1][0] = parms['biasAlphaBeta'][0][0]                 # Neuron 2
parms['biasAlphaBeta'][2][0] = parms['biasAlphaBeta'][0][0]                 # Neuron 3
parms['biasAlphaBeta'][3][0] = parms['biasAlphaBeta'][0][0]                 # Neuron 4


parms['signAlphaBeta'][0][0] = [[1, -1], [-1, 1], [1, -1]]                  # Neuron 1
parms['signAlphaBeta'][1][0] = parms['signAlphaBeta'][0][0]                 # Neuron 2
parms['signAlphaBeta'][2][0] = parms['signAlphaBeta'][0][0]                 # Neuron 3
parms['signAlphaBeta'][3][0] = parms['signAlphaBeta'][0][0]                 # Neuron 4
       
# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

parms['biasgErev'][0][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][0][1] = [[0, 256], [40, 256], [0, 256]]          # Neuron 3's membrane potential (Vpost) does not have a very strong effect on neuron 1's membrane potential (Vpre) (smaller gsyn)
parms['biasgErev'][1][1] = [[0, 256], [0, 256], [0, 256]]
parms['biasgErev'][2][1] = [[0, 256], [0, 256], [0, 256]]
# parms['biasgErev'][2][1] = [[100, 256], [0, 256], [0, 256]]         # Neuron 1's membrane potential (Vpost) has a strong effect on neuron 3's membrane potential (Vpre) (bigger gsyn)
parms['biasgErev'][3][1] = [[0, 800], [0, 800], [0, 256]]

parms['signgErev'][0][1] = [[1, 1], [1, -1], [1, 1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 1 (Vpost) from neuron 3 (Vpre)
parms['signgErev'][1][1] = [[1, 1], [1, 1], [1, 1]]
parms['signgErev'][2][1] = [[1, -1], [1, 1], [1, 1]]  # sign = -1 for Erev for an INHIBITORY synapse on neuron 3 (Vpost) from neuron 1 (Vpre)
parms['signgErev'][3][1] = parms['signgErev'][1][1]

parms['biasAlphaBeta'][0][1] = [[[  0,   0,   0,   20,   0, 0, 0],
                                 [  200,   10,  5,   0,   0,   0,   0]],

                                [[  0,   0,   0,   20,   0,  0, 0],
                                 [  200,   10,   5,   0,   0,   0,   0]],

                                [[  0,   10,   20,   40,   80,  120, 240],
                                 [  1000,   1000,   1000,   0,   0,   0,   0]]]

parms['signAlphaBeta'][0][1] = [[1, -1], [1, -1], [1, -1]]

parms['biasAlphaBeta'][1][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][2][1] = parms['biasAlphaBeta'][0][1]
parms['biasAlphaBeta'][3][1] = parms['biasAlphaBeta'][0][1]

parms['signAlphaBeta'][1][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][2][1] = parms['signAlphaBeta'][0][1]
parms['signAlphaBeta'][3][1] = parms['signAlphaBeta'][0][1]
    
for quadrantSel in [0, 1, 2, 3]:  # for soma
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  0, neurodyn_sel)


for quadrantSel in [0, 1, 2, 3]: 
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  1, neurodyn_sel)
    
neuron = 1
ifSynapse = 0
channelNum = 1
typ = 0                     # select alpha/beta rate, maximal conductance, reversal potential 
bumpNum = 0
addr = (neuron << 8) + (ifSynapse << 7) + (channelNum << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
set_internal_dacs_address(dev, addr, neurodyn_sel)

#%%
#bit = 1
#for i in range(100000):
#    Erev = 1023
#    #if Erev>=0:
#    parms['biasgErev'][neuron][0] = [[0, 1023], [0, 1023], [1023, Erev]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
#    parms['signgErev'][neuron][0] = [[1, 1], [1, -1], [1, bit]]        
    #else:
    #    parms['biasgErev'][neuron][0] = [[0, 1023], [0, 256], [1023, -Erev]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
    #    parms['signgErev'][neuron][0] = [[1, 1], [1, -1], [1, -1]]  
#    load_int_dacs_signbit_leak_channels(dev, parms['signgErev'], parms['biasgErev'], neuron, 0, neurodyn_sel)
#    time.sleep(0.01)
#    bit = -bit

#set_probe_on_expose_off(dev, 2**neurodyn_sel)
#try:
#    bit = 1
#    for i in range(100000):
#        volt = 0.9 + bit*0.9
#        write_external_DACs_neurodyn(dev, VmemProbeIn, volt, neurodyn_sel+1)              
#        time.sleep(0.01)
#        bit = -bit
#except KeyboardInterrupt:
#    write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)        # 0.9v   
#    print('VmemProbeIn set to 0.9v for neuron', neuron)

# SET Keithley for voltage source
rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')     # Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC CURR')
my_K.write(':SOUR:VOLT:RANG 5')
my_K.write(':SOUR:VOLT:LEV 0.0')
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')
   
#volt = 0.9
#sign = 1

set_probe_on_expose_off(dev, 2**neurodyn_sel)

#try:
#    while(True):
    #for i in range(2000):
#        my_K.write(':SOUR:VOLT:LEV '+str(0.9 + sign*volt))  
#        sign = -sign
#        time.sleep(0.01)
#except KeyboardInterrupt:
#    my_K.write(':SOUR:VOLT:LEV 0.9')
#    print('Voltage clamped to 0.9v.')


import threading

def volt_pulse():
    sign = 1
    volt = 0.9
    try:
        while(True):
            my_K.write(':SOUR:VOLT:LEV '+str(0.9 + sign*volt))  
            sign = -sign
            time.sleep(0.01)
    except KeyboardInterrupt:
        my_K.write(':SOUR:VOLT:LEV 0.9')
        print('Voltage clamped to 0.9v.')

x = threading.Thread(target=volt_pulse, daemon=True)
print(x.isDaemon())
x.start()

answer = input("Do you wish to exit?")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

#%% send a sine current waveform over keithley -- to force a neuron to burst with a frequency ~1/10*spiking frequency 
rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC CURR')
#my_K.write(':SOUR:CURR:MODE FIX')
my_K.write(':SOUR:CURR:RANG 500E-9')
my_K.write(':SOUR:CURR:LEV 0E-9')
my_K.write(':SENS:VOLT:PROT 2')
my_K.write(':SENS:FUNC "VOLT"')
my_K.write(':SENS:VOLT:RANG 5')
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')

set_probe_on_expose_off(dev, 2**neurodyn_sel)

I_strength = 1e-9        # 1nA
I_freq = 5                 # 5Hz  -- spiking frequency ~60Hz known beforehand. I_freq sets frequency of stimulation waveform and hence the bursting frequency
samp_freq = 20*I_freq
T = 60                    # duration of stimulation in seconds     
N = T*I_freq              # number of cycles over which stimulation lasts

t = np.linspace(0, T, int(T*samp_freq))
I = I_strength*np.sin(2*np.pi*I_freq*t)

plt.figure()
plt.plot(t, I*1e9)
plt.xlabel('t [s]')
plt.ylabel('I [nA]')
plt.xlim(0,1)
plt.title('Stimulation current')
plt.grid()
plt.show()

try:
    for i in range(int(T*samp_freq)):
        my_K.write(':SOUR:CURR:LEV '+str(I[i]))  
        time.sleep(1/samp_freq)
except KeyboardInterrupt:
    my_K.write(':SOUR:CURR:LEV 0E-9')
    print('Current injection stopped. Injected current set to 0nA.')

my_K.write(':SOUR:CURR:LEV 0E-9')
print('Current injection stopped. Injected current set to 0nA.')
my_K.write(':OUTP OFF')

set_expose_off_probe_off_all_neurodyns(dev)

#%% SET Keithley for current source 

rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC CURR')
#my_K.write(':SOUR:CURR:MODE FIX')
#%%
my_K.write(':SOUR:CURR:RANG 500E-9')
my_K.write(':SOUR:CURR:LEV 0E-9')
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')
#%% SET Keithley for voltage source

rm = pyvisa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC VOLT')
#%%
my_K.write(':SOUR:VOLT:RANG 5')
my_K.write(':SOUR:VOLT:LEV 0.0')
#my_K.write(':SENS:FUNC "CURR"')     # measure current - dosen't work
my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')

#%% sending voltage pulses over keithley

volt = 0.9
sign = 1
try:
    while True:
        my_K.write(':SOUR:VOLT:LEV '+str(0.9 + sign*volt))  
        sign = -sign
        time.sleep(0.001)
except KeyboardInterrupt:
    my_K.write(':SOUR:VOLT:LEV 0.9')
    print('Voltage clamped to 0.9v.')
    
#%%
my_K.write(':OUTP OFF')
my_K.close     
 
#%% Set Agilent scope for measurements

rm = pyvisa.ResourceManager()
rm.close

my_Scope = rm.open_resource('TCPIP0::172.16.25.245::inst0::INSTR')# Agilent scope

my_Scope.write('*RST')
my_Scope.write(':TIMEBASE:MODE MAIN')
#my_Scope.write(':ACQUIRE:TYPE NORM')
my_Scope.write(':ACQUIRE:TYPE HRES')
my_Scope.write(':WAV:POINTS:MODE RAW')
my_Scope.write(':WAV:POINTS MAXimum')
my_Scope.write(':TIMebase:RANGe 1E0')         # The :TIMebase:RANGe command sets the full- scale horizontal time in seconds for the main window. The range is 10 times the current time- per- division setting.
my_Scope.query(':TIMebase:RANge?')          
channel = 4 
my_Scope.write(':WAVEFORM:SOURCE CHANnel'+str(channel))
my_Scope.query(':WAVEFORM:SOURce?')
my_Scope.write(':CHANnel'+str(channel)+':RANGe 4V')     #Sets the full scale vertical range in mV or V. The range value is 8 times the volts per division.
#my_Scope.write(':CHANnel1:DISPlay OFF')
#%%
my_Scope.write(':WAVEFORM:UNSigned ON')
my_Scope.write(':DIGitize CHANnel'+str(channel))

#%%
my_Scope.write(':MEASURE:SOURCE CHANNEL'+str(channel))
vpp = my_Scope.query(':MEASURE:VPP?');
print("The peak to peak voltage is", vpp)
max = my_Scope.query(':MEASure:VMAX?')
print("The max voltage is", max)
min = my_Scope.query(':MEASure:VMIN?')
print("The min voltage is", min)
#rise_time = my_Scope.query(':MEASure: RISetime?')
#print('The risetime is', rise_time)
#fall_time = my_Scope.query(':MEASure: FALLtime?')
#print('The risetime is', fall_time)

#%% obsolete
operationComplete = int(my_Scope.query('*OPC?'))
print(operationComplete)
while not operationComplete:
    operationComplete = double(my_Scope.query('*OPC?'));


# Get the data back as a WORD (i.e., INT16), other options are ASCII and BYTE
my_Scope.write(':WAVEFORM:FORMAT WORD')
# Set the byte order on the instrument as well
my_Scope.write(':WAVEFORM:BYTEORDER LSBFirst')
# Get the preamble block
preambleBlock = my_Scope.query(':WAVEFORM:PREAMBLE?')

#%% obsolete
my_Scope.write(':WAV:DATA?');

waveform.RawData = my_Scope.binblockread('uint16'); 
my_Scope.read();
#%% set conversion mode 
full_conv = True;
f83k = False;

#%%  Main Clock Configuration and Output 

if full_conv:
    # fconv addr 1
    write_FPGA(dev,0x10,int('0000000000000001', 2))
    # CLK delay time fconv: 0 ns; (rsl) 2,750ns
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time fconv: 250ns
    #write_FPGA(dev,0x12,int('0000000000011001', 2))
    # CLK low time fconv: 500ns
    write_FPGA(dev,0x12,int('0000000000110010', 2))
    # CLK high time fconv: 250ns
    #write_FPGA(dev,0x13,int('0000000000011001', 2)) 
    # CLK high time fconv: 250ns
    write_FPGA(dev,0x13,int('0000000000110010', 2)) 
    # CLK delay sign CLK1M6
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('fconv configured.')
else:
    # fconv addr 1
    write_FPGA(dev,0x10,int('0000000000000001', 2))
    # CLK delay time fconv: 0 ns; (rsl) 2,750ns
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time fconv: 3,400ns
    #write_FPGA(dev,0x12,int('0000000101010100', 2))
    # CLK low time fconv: 3,700ns
    write_FPGA(dev,0x12,int('0000000101110010', 2))
    # CLK high time fconv: 3,400ns
    #write_FPGA(dev,0x13,int('0000000101010100', 2))  
    # CLK high time fconv: 3,700ns
    write_FPGA(dev,0x13,int('0000000101110010', 2))  
    # CLK delay sign CLK1M6
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('fconv configured.')

if full_conv:
    # rsl addr 2
    write_FPGA(dev,0x10,int('0000000000000010', 2))
    # CLK delay time rsl: 0ns
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    if f83k:
        # CLK low time rsl: 10,000ns
        write_FPGA(dev,0x12,int('0000001111101000', 2))
    else:
        # CLK low time rsl: 24,000ns
        write_FPGA(dev,0x12,int('0000100101100000', 2))
    # CLK high time rsl: 16,000ns
    write_FPGA(dev,0x13,int('0000011001000000', 2))  
    # CLK delay sign rsl
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('rsl configured.')
else:
    # rsl addr 2
    write_FPGA(dev,0x10,int('0000000000000010', 2))
#    # CLK delay time rsl: 0ns
#    write_FPGA(dev,0x11,int('0000000000000000', 2))
#    # CLK low time rsl: 129,200ns fconv + 2,000ns + 3,400ns = 134,600 for 1bit
#    write_FPGA(dev,0x12,int('0011010010010100', 2))
#    # CLK low time rsl: 30,000ns
#    #write_FPGA(dev,0x12,int('0000101110111000', 2))
#    # CLK high time rsl: 2,000ns
#    write_FPGA(dev,0x13,int('0000000011001000', 2))  
#    # CLK delay sign rsl
#    write_FPGA(dev,0x14,int('0000000000000000', 2))
#    time.sleep(0.01)
#    print 'rsl configured.'
    # CLK delay time conv: 2,300ns
    #write_FPGA(dev,0x11,int('0000000011100110', 2))
    # CLK delay time conv: 0ns
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    #write_FPGA(dev,0x11,int('0000000000000000', 2))
    ## CLK low time conv: 129,200 1bit
    #write_FPGA(dev,0x12,int('0011001001111000', 2))  
    # CLK low time conv: 132,500 1bit
    #write_FPGA(dev,0x12,int('0011001111000010', 2))
    # CLK low time conv: 265,000ns 1bit
    write_FPGA(dev,0x12,int('0110011110000100', 2))
    # CLK low time conv: 7,890ns
    #write_FPGA(dev,0x12,int('0000001100010101', 2))
    # CLK high time conv: 5,100ns for 1bit 
    #write_FPGA(dev,0x13,int('0000000111111110', 2))
    # CLK high time conv: 1,800ns for 1bit 
    write_FPGA(dev,0x13,int('0000000010110100', 2))
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print('conv configured.')

#default
## rstota addr 3
#write_FPGA(dev,0x10,int('0000000000000011', 2))
## CLK delay time rstota: -19,000 ns
#write_FPGA(dev,0x11,int('0000011101101100', 2))
## CLK low time rstota: 10,000 ns 
## ideally 1000 ns
#write_FPGA(dev,0x12,int('0000000001100100', 2)) 
## CLK high time rstota: 23,000ns
#write_FPGA(dev,0x13,int('0000100011111100', 2)) 
## CLK delay sign rstota
#write_FPGA(dev,0x14,int('0000000000000001', 2))
#time.sleep(0.01)
#print 'rstota configured.'

# rstota addr 3
write_FPGA(dev,0x10,int('0000000000000011', 2))
# CLK delay time rstota: 2,000 ns
#write_FPGA(dev,0x11,int('0000000011001000', 2))
# CLK delay time rstota: 0 ns
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time rstota: 50,000 ns
write_FPGA(dev,0x12,int('0001001110001000', 2)) 
# CLK high time rstota: 10 s
#write_FPGA(dev,0x13,int('00111011100110101100101000000000', 2)) 
# CLK high time rstota: 10,000ns
write_FPGA(dev,0x13,int('0000001111101000', 2)) 
# CLK delay sign rstota
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('rstota configured.')

if full_conv:
    # conv addr 4
    write_FPGA(dev,0x10,int('0000000000000100', 2))
    # CLK delay time conv: 2,300ns
    #write_FPGA(dev,0x11,int('0000000011100110', 2))
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time conv: 2,630ns
    #write_FPGA(dev,0x12,int('0000000100000111', 2))
    # CLK low time conv: 7,890ns
    write_FPGA(dev,0x12,int('0000001100010101', 2))
    # CLK high time conv: 9,370ns
    #write_FPGA(dev,0x13,int('0000001110101001', 2))  
    # CLK high time conv: 18,560
    write_FPGA(dev,0x13,int('0000011101000000', 2))  
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('conv configured.')
else:
    # conv addr 4
    write_FPGA(dev,0x10,int('0000000000000100', 2))
    # CLK delay time conv: 2,300ns
    write_FPGA(dev,0x11,int('0000000011100110', 2))
    #write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time conv: 5,100ns for 1bit 
    #write_FPGA(dev,0x12,int('0000000111111110', 2))
    # CLK low time conv: 104,600 ns
    write_FPGA(dev,0x12,int('0010100011011100', 2))
    # CLK high time conv: 162,200 1bit
    write_FPGA(dev,0x13,int('0011111101011100', 2))  
    # CLK high time conv: 259,400 ns 1bit
    #write_FPGA(dev,0x13,int('0110010101010100', 2))  
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000001', 2))
    time.sleep(0.01)
    print ('conv configured.')

if full_conv:
    # done addr 5
    write_FPGA(dev,0x10,int('0000000000000101', 2))
    # CLK delay time done: 0 ns (rsl) 11,125ns
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time done: 5,000 ns 
    write_FPGA(dev,0x12,int('0000000111110100', 2))
    # CLK high time conv: 500 ns
    write_FPGA(dev,0x13,int('0000000000110010', 2))  
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('done configured.')
else:
    # done addr 5
    write_FPGA(dev,0x10,int('0000000000000101', 2))
    # CLK delay time done: 8,200 ns 
    write_FPGA(dev,0x11,int('0000001100110100', 2))
    # CLK delay time done: 0 ns 
    #write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time done: 10,000 ns 
    #write_FPGA(dev,0x12,int('0000001111101000', 2))
    # CLK low time done: 45,000 ns 
    write_FPGA(dev,0x12,int('0001000110010100', 2))
    # CLK high time conv: 500 ns
    #write_FPGA(dev,0x13,int('0000000000110010', 2))  
    # CLK high time conv: 16,030 ns
    write_FPGA(dev,0x13,int('0000011001000011', 2))  
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000001', 2))
    time.sleep(0.01)
    print ('done configured.')

if full_conv:
    # str addr 6
    write_FPGA(dev,0x10,int('0000000000000110', 2))
    # CLK delay time str: 49 ns (rsl) 11,625ns
    write_FPGA(dev,0x11,int('0000000000110001', 2))
    # CLK low time str: 11,500ns 
    write_FPGA(dev,0x12,int('0000010001111110', 2))
    # CLK high time str: 500ns  # lower to 370 ns
    #write_FPGA(dev,0x13,int('0000000000110010', 2))  
    # CLK high time str: 870 ns
    write_FPGA(dev,0x13,int('0000000001010111', 2)) 
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000001', 2))
    time.sleep(0.01)
    print ('str configured.')
else:
    # str addr 6
    write_FPGA(dev,0x10,int('0000000000000110', 2))
    # CLK delay time str: 100 ns 
    #write_FPGA(dev,0x11,int('0000000000001010', 2))
    # CLK delay time str: 200 ns 
    #write_FPGA(dev,0x11,int('0000000000010100', 2))
    # CLK delay time str: 1000ns  
    ##write_FPGA(dev,0x11,int('0000000001100100', 2)) 
    # CLK delay time str: 0 ns 
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time str: 11,500ns 
    write_FPGA(dev,0x12,int('0000001010111100', 2))
    # CLK high time str: 1000ns  
    #write_FPGA(dev,0x13,int('0000000001100100', 2)) 
    # CLK high time str: 500ns  # lower to 370 ns
    write_FPGA(dev,0x13,int('0000000000110010', 2))  
    #write_FPGA(dev,0x13,int('0000000000100101', 2)) 
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('str configured.')
    
if full_conv:
    # read_data addr 7
    write_FPGA(dev,0x10,int('0000000000000111', 2))
    # CLK delay time read_data: 240 ns (rsl) 12,250ns
    #write_FPGA(dev,0x11,int('0000000000011000', 2))
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time read_data: 800 ns 
    write_FPGA(dev,0x12,int('0000000001010000', 2))
    # CLK high time read_data: 100ns
    write_FPGA(dev,0x13,int('0000000000001010', 2))
    # CLK high time read_data: 500ns
    #write_FPGA(dev,0x13,int('0000000000110010', 2))
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('read_data configured.')
else:
    # read_data addr 7
    write_FPGA(dev,0x10,int('0000000000000111', 2))
    # CLK delay time read_data: 240 ns (rsl) 12,250ns
    #write_FPGA(dev,0x11,int('0000000000011000', 2))
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time read_data: 800 ns + 40,000ns for 1bit 
    write_FPGA(dev,0x12,int('0000111111110000', 2))
    # CLK high time read_data: 100ns
    write_FPGA(dev,0x13,int('0000000000001010', 2))  
    # CLK delay sign conv
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('read_data configured.')

# CDS addr 8
write_FPGA(dev,0x10,int('0000000000001000', 2))
# CLK delay time CDS: 0 ns (rsl) 2,450ns
write_FPGA(dev,0x11,int('0000000000000000', 2))
if f83k:
    # CLK low time CDS: 12,100ns 
    write_FPGA(dev,0x12,int('0000010010111010', 2))
    # CLK high time CDS: 11,900
    write_FPGA(dev,0x13,int('0000010010100110', 2))  
else:
    # CLK low time CDS: 12,100ns 
    write_FPGA(dev,0x12,int('0000010010111010', 2))
    # CLK high time CDS: 40,000 ns
    write_FPGA(dev,0x13,int('0000111110100000', 2))  
# CLK delay sign conv
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('CDS configured.')

# re addr 9
write_FPGA(dev,0x10,int('0000000000001001', 2))
# CLK delay time re: 0 ns (rsl) 12,000 ns
write_FPGA(dev,0x11,int('0000000000000000', 2))
if f83k:
    # CLK low time re: 11,110 ns
    write_FPGA(dev,0x12,int('0000010001010111', 2))
else:
    # CLK low time re: 38,000ns
    write_FPGA(dev,0x12,int('0000111011011000', 2))
# CLK high time re: 890 ns
write_FPGA(dev,0x13,int('0000000001011001', 2))  
# CLK delay sign re
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('re configured.')
    
# write_config addr 10
write_FPGA(dev,0x10,int('0000000000001010', 2))
# CLK delay time write_config: 47,815 ns
#write_FPGA(dev,0x11,int('0001001010101101', 2))
# CLK delay time write_config: 2,000 ns
write_FPGA(dev,0x11,int('0000000011001000', 2))
# CLK low time write_config: 1,335 ns
write_FPGA(dev,0x12,int('0000000010000101', 2))
# CLK high time write_config: 20 ns
write_FPGA(dev,0x13,int('0000000000010100', 2))  
# CLK delay sign write_config
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('write_config configured.')

# arst addr 11
write_FPGA(dev,0x10,int('0000000000001011', 2))
# CLK delay time arst: 20ns (rsl) 47,815 ns
#write_FPGA(dev,0x11,int('0000000000000010', 2))
# CLK delay time arst: 300ns 
write_FPGA(dev,0x11,int('0000000000011110', 2))
#write_FPGA(dev,0x11,int('0000000000000000', 2))
if f83k:
    # CLK low time arst: 210 ns
    write_FPGA(dev,0x12,int('0000000011010010', 2))
else:
    # CLK low time arst: 38,000ns
    write_FPGA(dev,0x12,int('0000111011011000', 2))
# CLK high time arst: 1,000 ns
write_FPGA(dev,0x13,int('0000000001100100', 2))  
# CLK delay sign arst
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('arst configured.')

# ainc addr 12
write_FPGA(dev,0x10,int('0000000000001100', 2))
# CLK delay time ainc: 0 ns (rsl) .. ns
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time ainc: 210 ns
#write_FPGA(dev,0x12,int('0000000000010101', 2))
# CLK low time ainc: 38,000ns
write_FPGA(dev,0x12,int('0000111011011000', 2))
# CLK high time ainc: 1,000 ns
write_FPGA(dev,0x13,int('0000000001100100', 2))  
# CLK delay sign ainc
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('ainc configured.')

if full_conv:
    # shift addr 13 #total period 17 * 400ns = 6,800ns
    write_FPGA(dev,0x10,int('0000000000001101', 2))
    # CLK delay time shift: 0 ns (rsl) 12,256 ns
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time shift: 50 ns 10 MHz
    #write_FPGA(dev,0x12,int('0000000000000101', 2))
    # CLK low time shift: 500 ns 1 MHz
    write_FPGA(dev,0x12,int('0000000000110010', 2))
    # CLK low time shift: 200 ns 2.5 MHz
    #write_FPGA(dev,0x12,int('0000000000010100', 2))
    # CLK high time shift: 50 ns 10 MHz
    #write_FPGA(dev,0x13,int('0000000000000101', 2))  
    # CLK high time shift: 500 ns 1 MHz
    write_FPGA(dev,0x13,int('0000000000110010', 2))
    # CLK high time shift: 200 ns 2.5 MHz
    #write_FPGA(dev,0x13,int('0000000000010100', 2))
    # CLK delay sign shift
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('shift configured.')
else:
    # shift addr 13 #total period 17 * 400ns = 6,800ns
    write_FPGA(dev,0x10,int('0000000000001101', 2))
    # CLK delay time shift: 0 ns (rsl) 12,256 ns
    write_FPGA(dev,0x11,int('0000000000000000', 2))
    # CLK low time shift: 50 ns 10 MHz
    #write_FPGA(dev,0x12,int('0000000000000101', 2))
    # CLK low time shift: 500 ns 1 MHz
    #write_FPGA(dev,0x12,int('0000000000110010', 2))
    # CLK low time shift: 250 ns 2 MHz
    #write_FPGA(dev,0x12,int('0000000000011001', 2))
    # CLK low time shift: 200 ns 2.5 MHz
    write_FPGA(dev,0x12,int('0000000000010100', 2))
    # CLK high time shift: 50 ns 10 MHz
    #write_FPGA(dev,0x13,int('0000000000000101', 2))  
    # CLK high time shift: 500 ns 1 MHz
    #write_FPGA(dev,0x13,int('0000000000110010', 2))
    # CLK high time shift: 250 ns 2 MHz
    #write_FPGA(dev,0x13,int('0000000000011001', 2))
    # CLK high time shift: 200 ns 2.5 MHz
    write_FPGA(dev,0x13,int('0000000000010100', 2))
    # CLK delay sign shift
    write_FPGA(dev,0x14,int('0000000000000000', 2))
    time.sleep(0.01)
    print ('shift configured.')

# FIFO_WR addr 14
write_FPGA(dev,0x10,int('0000000000001110', 2))
# CLK delay time FIFO_WR: 0 ns (rsl) 12,256 ns
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time FIFO_WR: 5000 ns
write_FPGA(dev,0x12,int('0000000111110100', 2))
# CLK high time FIFO_WR: 5000 ns
write_FPGA(dev,0x13,int('0000000111110100', 2))  
# CLK delay sign FIFO_WR
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('FIFO_WR configured.')

# test_spi_clk addr 15
write_FPGA(dev,0x10,int('0000000000001111', 2))
# CLK delay time test_spi_clk 0 ns 
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time test_spi_clk 500 ns 1MHz
write_FPGA(dev,0x12,int('0000000000110010', 2))
# CLK high time test_spi_clk: 500 ns
write_FPGA(dev,0x13,int('0000000000110010', 2))  
# CLK delay sign test_spi_clk
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('test_spi_clk configured.')

# test_spi_in addr 16
write_FPGA(dev,0x10,int('0000000000010000', 2))
# CLK delay time test_spi_in 0 ns 
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time test_spi_in 29,500 ns  16.949 kHz
write_FPGA(dev,0x12,int('0000101110000110', 2))
# CLK high time test_spi_in 29,500 ns
write_FPGA(dev,0x13,int('0000101110000100', 2))  
# CLK delay sign test_spi_in
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('test_spi_in configured.')

# Ag addr 17
write_FPGA(dev,0x10,int('0000000000010001', 2))
# CLK delay time Ag 0 ns 
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time Ag 29,500 ns  16.949 kHz
write_FPGA(dev,0x12,int('0000101110000110', 2))
# CLK high time Ag 29,500 ns
write_FPGA(dev,0x13,int('0000000000000000', 2))  
# CLK delay sign Ag
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('Ag configured.')

# Pg addr 18
write_FPGA(dev,0x10,int('0000000000010010', 2))
# CLK delay time Pg 0 ns 
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time Pg 29,500 ns  16.949 kHz
write_FPGA(dev,0x12,int('0000101110000110', 2))
# CLK high time Pg 29,500 ns
write_FPGA(dev,0x13,int('0000000000000000', 2))  
# CLK delay sign Pg
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('Pg configured.')

# Probe addr 19
write_FPGA(dev,0x10,int('0000000000010011', 2))
# CLK delay time Probe 0 ns 
write_FPGA(dev,0x11,int('0000000000000000', 2))
# CLK low time Probe 83,333,366 ns  6 Hz
write_FPGA(dev,0x12,int('011111110010100000110110', 2))
# CLK high time Probe 83,333,300 ns  6 Hz
write_FPGA(dev,0x13,int('011111110010011111110100', 2))  
# CLK delay sign Probe
write_FPGA(dev,0x14,int('0000000000000000', 2))
time.sleep(0.01)
print ('Probe configured.')

#%%  brute force spi write configure global  15:0
#write_FPGA(dev,0x07,int('1001111000000101', 2)) # default configuration, CC
#write_FPGA(dev,0x07,int('1111111000000101', 2)) # CC, RST 0 HIGH and RST 1 HIGH 
#write_FPGA(dev,0x07,int('1110000000000101', 2)) # new default, CC, full conv, 0 gain, no BW limit, RSTs 1, SAR Ctrls 0
#write_FPGA(dev,0x07,int('1110000000111101', 2)) # CC, full conv, full gain, no BW limit, RSTs 1, SAR Ctrls 0
if full_conv:
    write_FPGA(dev,0x07,int('1110000111111101', 2)) # CC, full conv, 60 gain, 2.1pF, full BW limit, RSTs 1, SAR Ctrls 0
    
    # bits[3:5]   total capacitance - Cf+Cg (VC)            gain capacitance, Cg (CC)   total feedback cap, Cfeff (CC)    Gain = 1 + Cg/Cfeff
    # 111         35fF                                      (48+9+2)*35fF = 2.065pF     35fF                              60 
    # 110         105fF                                     (48+9)*35fF = 1.995fF       (2+1)*35fF = 105fF                20
    # 101         350fF                                     (48+2)*35fF = 1.75pF        (9+1)*35fF = 350fF                6
    # 100         420fF                                     48*35fF = 1.68pF            (9+2+1)*35fF = 420fF              5
    # 011         1.715pF                                   (9+2)*35fF = 385fF          (48+1)*35fF = 1.715pF             1.22
    # 010         1.785pF                                   9*35fF = 315fF              (48+2+1)*35fF = 1.785pF           1.18 
    # 001         2.03pF                                    2*35fF = 70fF               (48+9+1)*35fF = 2.03pF            1.03
    # 000         2.1pF                                     0*35fF = 0                  (48+9+2+1)*35fF = 2.1pF           1
else:
    print ('single bit chip config')
    write_FPGA(dev,0x07,int('1110000111010001', 2)) # CC, 1-bit, 0 gain, full BW limit, RSTs 1, SAR Ctrls 0
#write_FPGA(dev,0x07,int('1001111000000100', 2))# default except VC
#write_FPGA(dev,0x07,int('1001111000111101', 2)) # no BW limit; full gain
#write_FPGA(dev,0x07,int('1001111111111100', 2)) # BW limited configuration; gain !
#write_FPGA(dev,0x07,int('0010000001111001', 2))
#write_FPGA(dev,0x07,int('0101010101010101', 2)) #this one just works
#write_FPGA(dev,0x07,int('0010010010010010', 2))  #this one breaks
#write_FPGA(dev,0x07,int('1000100000000001', 2))
#write_FPGA(dev,0x07,int('1001001001001001', 2))
#write_FPGA(dev,0x07,int('00000101000001010010010010010010', 2)) #100 ns period
#write_FPGA(dev,0x07,int('00110010 00110010 0101010101010101', 2)) #1000 ns period
#write_FPGA(dev,0x07,int('01001100010011000101010101010101', 2)) #1000 ns period
print ('bf spi write global configuration configured.')

#  brute force spi write enable
write_FPGA(dev,0x06,int('0000000000000001', 2))
print ('bf spi write_enable configured.')
time.sleep(0.3)
#%  brute force spi write disable
write_FPGA(dev,0x06,int('0000000000000000', 2))
print ('bf spi write dis-enable configured.')

#%%  brute force spi write configure local
write_FPGA(dev,0x07,int('0000000000011000', 2))  # [0] Al, [1] Pl, [2:5] strt_indx
print ('bf spi write local configuration configured.')

#  brute force spi write enable
write_FPGA(dev,0x06,int('0000000000000001', 2))
print ('bf spi write_enable configured.')
time.sleep(0.3)
#%  brute force spi write disable
write_FPGA(dev,0x06,int('0000000000000000', 2))
print ('bf spi write dis-enable configured.')
    
#%% channels_to_use configuration 

# address reset
# D_channels_to_use [6:2] 11111 = 31
write_FPGA(dev,0x02,int('0000000000000000', 2))
time.sleep(0.000001)
write_FPGA(dev,0x02,int('0000000000000001', 2))
#time.sleep(0.00000001)
write_FPGA(dev,0x02,int('0000000000000000', 2))
time.sleep(0.000001)
print ('Address Reset Pulse Sent')
#%%
write_FPGA(dev,0x02,int('0000000000111100', 2))
time.sleep(0.000001)
write_FPGA(dev,0x02,int('0000000000111110', 2))
time.sleep(0.000001)
write_FPGA(dev,0x02,int('0000000000111100', 2))
time.sleep(0.000001)

#%% initialize and set DACs
init_DACs(dev)
    #write_FPGA(dev,0x04,0)#calibration on/off=1/0
    
time.sleep(0.500)
# Keithley Current Measurement Test 210419
write_DACs(dev,IVbNP_stim,0.9);
write_DACs(dev,IVbNN_stim,0.9); 

#write_DACs(dev,Vinfinimp_bias,0.8);

#write_DACs(dev,IVbP_OTA,0.6);
write_DACs(dev,Vclamp_p,0.7);
write_DACs(dev,Vclamp_n,0.5);

#%% initialize and set dacs neurocube

write_DACs_nisoc(dev, Vref_nisoc, 1.053)        #1.053
write_DACs_nisoc(dev, IVbP_OTA, 0.851)          #0.821
write_DACs_nisoc(dev, Vinfinimp_bias, 1.278)    #1.278
write_DACs_nisoc(dev, Vclamp_p, 1.2)
write_DACs_nisoc(dev, Vclamp_n, 0.8)    
write_DACs_nisoc(dev, IVbNP_stim, 0.3)
write_DACs_nisoc(dev, IVbNN_stim, 0.3)
    
#%%  twfcontrol
#python reset, just set to 0
write_FPGA(dev,0x01,int('0000000000000000', 2))

if full_conv:    
    write_FPGA(dev,0x00,int('0000000000000100', 2))
    print ('[0] 0-Full/1-SingleConv, [2] RSTOTA enabled, [3] DS mode OFF.')
    time.sleep(2)
    write_FPGA(dev,0x00,int('0000000000001010', 2))
    print ('[0] 0-Full/1-SingleConv, [1] 0_CC/1_VC, [2] RSTOTA disabled, [3] DS mode OFF,',
    '[4] CDS Master Force, [5] use canned spi, [6] dual canned, [7] Ag, [8] Pg, [10] probe sig, [11] 0 Str_freeze')
else:                                   
    write_FPGA(dev,0x00,int('0000001000000101', 2))
    print ('[0] 0-Full/1-SingleConv, [1] 0_CC/1_VC, [2] RSTOTA enabled, [3] DS mode OFF.')
    time.sleep(2)
    write_FPGA(dev,0x00,int('0000001000000001', 2))
    print ('[0] 0-Full/1-SingleConv, [1] 0_CC/1_VC, [2] RSTOTA disabled, [3] DS mode OFF, [5] use canned spi, [6] dual canned, [7] Ag, [8] Pg, [9] 1then12bit mode')

#%% the second write configuration for 1bit then 12bit mode which sets 12bit
write_FPGA(dev,0x05,int('1110000111000101', 2))
print ('2nd global write configured for full conv for 1then12bit mode.')
#%% Enable clocks
write_FPGA(dev,0x03,int('0000000000000001', 2))
print ('Clocks output enabled.')

#%% Disable clocks
write_FPGA(dev,0x03,int('0000000000000000', 2))
print ('Clocks output disabled.')

#%% Continuous capture with FIFO Prog_Full flag

savepath="C:/Users/isnl/OneDrive - UC San Diego/research/NeuroCube/NISoC_python/plots/"
filename=savepath+time.strftime("%Y%m%d-%H%M%S")+ "_QFP8_NeuroCube_lab_pluggedin_gain_60_BW111_current_clamp_ND18_neuron10_Ch15"+".h5" 

#filename=savepath+time.strftime("%Y%m%d-%H%M%S")+ "CC_gate_current_measurement_"+"Keithley_on_Ch0_AL_1_PL_1_Vsrc_0.7v"+".h5" 
Data_Read_USB(dev=dev,filename=filename,recordingtime=1);  

# load usb saved data and plot
#prefile = '20210611-121723_QFP4_Ch0_Battery_Bear_sanity_gain60_noCDS_60secs_3M_20';
#filename = prefile + ".h5"

start_time = time.time()    
f = tables.open_file(filename, "r")
datain=f.root.data.read()
f.close()
data_check = datain
datain=datain.astype(np.int16)

# convert the loaded integer USB data to decimal 

data_dict={}

if full_conv:   
    datain_dec = np.zeros(len(datain));
    res_io = np.zeros(len(datain));
    cds_flag = np.zeros(len(datain));
    rstota_flag = np.zeros(len(datain));
    ainc_count = np.zeros(len(datain));
    test_count = np.zeros(len(datain));
    for i in range(0,len(datain)):
        temp_str0 = "{0:b}".format(datain[i,0]);
        if len(temp_str0) < 8:
            numfill = 8 - len(temp_str0);
            for j in range(numfill):
                temp_str0 = '0' + temp_str0;
        #bitstring.append(temp_str0);
        temp_str0d = temp_str0[:4][::-1];
        temp_str1 = "{0:b}".format(datain[i,1]);
        if len(temp_str1) < 8:
            numfill = 8 - len(temp_str1);
            for j in range(numfill):
                temp_str1 = '0' + temp_str1;
        temp_str1 = temp_str1[::-1];
        datain_dec[i] = int(temp_str0d+temp_str1,2)
        res_io[i] = int(temp_str0[4:][::-1],2);
        
        temp_str2 = "{0:b}".format(datain[i,2]);
        if len(temp_str2) < 8:
            numfill = 8 - len(temp_str2);
            for j in range(numfill):
                temp_str2 = '0' + temp_str2;
        #temp_str2 = temp_str2[::-1];
        cds_flag[i] = int(temp_str2[-2],2);
        rstota_flag[i] = int(temp_str2[-1],2);
        ainc_count[i] = int(temp_str2[-8:-2],2);
        
        temp_str3 = "{0:b}".format(datain[i,3]);
        if len(temp_str3) < 8:
            numfill = 8 - len(temp_str3);
            for j in range(numfill):
                temp_str3 = '0' + temp_str3;
        test_count[i] = int(temp_str3[-6:],2);
        
    data_dict[0] = datain_dec; 
    print ('Full Conv, USB to Decemial conversion complete')    
    
else:   
    datain_dec = np.zeros(len(datain));
    compbits = np.zeros(len(datain));
    for i in range(0,len(datain)):
        temp_str0 = "{0:b}".format(datain[i,0]);
        if len(temp_str0) < 8:
            numfill = 8 - len(temp_str0);
            for j in range(numfill):
                temp_str0 = '0' + temp_str0;
        #bitstring.append(temp_str0);
        temp_str0d = temp_str0[:4][::-1];
        temp_str1 = "{0:b}".format(datain[i,1]);
        if len(temp_str1) < 8:
            numfill = 8 - len(temp_str1);
            for j in range(numfill):
                temp_str1 = '0' + temp_str1;
        temp_str1 = temp_str1[::-1];
        compbits[i] = int(temp_str1[-2:-1],2);
    
    data_dict[0] = compbits; 
    print ('1-bit Conv, USB to Decemial conversion complete')
        
# plot

plt.ion()
if full_conv:
    fig, ax1 = plt.subplots();
    #ax1.plot(datain_dec)
    #ax2 = ax1.twinx();
    #ax2.plot(res_io, '.r')
    toplot = [];
    for i in range(0,len(data_dict)):
        toplot = np.append(toplot, data_dict[i]);
    ax1.plot((toplot*(1.2/4096))+0.3)
    #ax1.plot(cds_flag)
    ax1.set_xlim([1,25000])
    #ax1.set_ylim([0, 4095])
    ax1.set_ylim([0.3, 1.5])
    fig.suptitle('ch15, HGain[2:0]=111 -- gain = 60')
    #plt.savefig('plots/vclamp = '+str(0.5))
    
    print(np.max(datain_dec))
    print(np.min(datain_dec))
  
else:
    fig, ax1 = plt.subplots();
    ax1.plot(compbits)
    ax1.set_xlim([650,780])
    ax1.set_ylim([-1, 2])

#%% save USB load converted decimal data to csv
#with open("20210611-115930_QFP4_Ch1_Battery_Bear_sanity_gain60_noCDS_60secs_flatcnt_9.csv", "a") as f:
#with open(prefile +".csv", "a") as f:
with open(filename[:-3] +".csv", "a") as f:
    writer = csv.writer(f)
    #writer.writerow(datain_dec)
    writer.writerow(data_dict[0])
    
#%% generate cds_dataset/calculate integrated current

# if CDS_mode:
    
# if VC_mode:
#%% data capture and conversion from FIFO.

#%% 1-bit load 
filename = "210519_QFP4_Ch1_VrefShorted_1bit_1.csv"
with open(filename, 'rb') as f:
    onebit = csv.reader(f)
    print ('csv being read ...')
    for row in onebit:
        compbitload = map(int,map(float,row))   #convert csv loaded data which is string to float to int
        
#%% 1-bit algorithm 
from gates_ap import *
# main dir loop
done_check = 0;
RST = 0;
RSTb = not RST; 
fconv_cnt = 0;
surpress = 0;
res_pre = 0;
res_pre_log = [];
sign_changed = 0;
sign_changed_bar = 1;
prev_dir = 0;
res_dir = [];
stayb = [];
dir = [];
sign_changed_log = [];

R = [0, 0, 0, 0];                   # ** How to set the starting radix? Should it match what's set on the chip register? Yes, e.g. [0010] = 4
RB = [1, 1, 1, 1];
R_log = [];
gater_clk = 0;
r_count = 0;
r_count_log = [];

GTB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
cnt_clk = 0;
d_count = 0;
d_count_log = [];
addval = 0;

ndirc = 0; # ndir loop count 

# main loop scans through saved comp_bit outputs. 
# ndir here is the actual comp_bit, not the index or count (ndirc)
# think of each loop here as an fconv clock cycle
for ndir in compbitload:
    # need to put RST flag captured here
    fconv_cnt = fconv_cnt + 1;
    # assuming rst following every 19th fconv      # ** Is an assumed RSL RST sufficient?
    if fconv_cnt > 19:
        fconv_cnt = 0;
        RST = 1;
        RSTb = not RST;
    else: 
        RST = 0;
        RSTb = not RST;
        
    if RST == 1:  # added reset conditions, needs to match (incl. dffsrpq, etc)
        #print 'RST'
        sign_changed_bar = 1;
        sign_changed = not sign_changed_bar;
        #sign_changed_log.append(int(sign_changed));
            
        #ndir = 0;
        prev_dir = 0;
        
        d_count_log.append(d_count)     # 12-bit output (IO_Data)
        #d_count = 0;                    # should only be reset to 2048 during config register write
    # reset during reset_data
    #d_count_log.append(d_count)     # 12-bit output (IO_Data)
    #d_count = 0;                
    
 
    # direction control
    res_pre = OR(surpress, XNOR(ndir,prev_dir)) 
    prev_dir = ndir;
    res_pre_log.append(res_pre);
    
    if (NAND(res_pre, sign_changed_bar) == 1):
        sign_changed_bar = 0;
        sign_changed = not sign_changed_bar;
     
    elif (NAND(res_pre, sign_changed_bar) == 0):
        if (RSTb == 1):
            sign_changed_bar = not NAND(res_pre, sign_changed_bar);
            sign_changed = not sign_changed_bar;
    sign_changed_log.append(int(sign_changed));
                
    res_dir.append(NOR(res_pre, sign_changed_bar));
    stayb.append(int(AND(NAND(res_pre, sign_changed), not surpress))); 
    dir.append(ndir); 

    # Res_center_preload: res_clk_gater_preload
    #gater_clk = AND(AND(stayb[ndirc] ,NAND(not res_dir[ndirc],AND(R[2],R[3]))), NAND(res_dir[ndirc] ,AND(AND(not R[1],not R[2]), not R[3])))
    I30 = AND(R[2],R[3]);                           # ** Review these logic blocks with Preston; not sure how to implement R table here
    I21 = NAND(not res_dir[ndirc],I30);
    I2 = AND(AND(RB[1],RB[2]),RB[3]);
    I19 = NAND(res_dir[ndirc], I2);
    gater_clk = AND(AND(stayb[ndirc],I21),I19);
    res_dirb = not res_dir[ndirc];
    
    if gater_clk:
        #print [gater_clk, len(res_dir), ndirc, res_dir[ndirc]]
        if res_dir[ndirc]:
            #print res_dir[ndirc]
            r_count = r_count + 1; 
        elif res_dir[ndirc] == 0: 
            r_count = r_count - 1;
        
        if r_count > 11:
            r_count = 0;
        elif r_count < 0:
            r_count = 0; 
        r_count_log.append(r_count)
            
        for r in range(len(R[:])):
            bintmp = "{0:b}".format(r_count);
            if len(bintmp) < 4:
                numfill = 4 - len(bintmp);
                for j in range(numfill):
                    bintmp = '0' + bintmp;
            R[r] = int(bintmp[-(1+r)])
        for p in range(len(R)): RB[p] = not R[p]; 
        R_log.append(R);
        
        
    # c_btou_decoder11, Radix to GTB mask
    GTB = decodeGTB(R);                             # ** The decoder table in Jun's cbtou_11 schematic doesn't match, so made GTB function
        
    # c_btou_decoder11, GTB 1s are locked bits 
#    if R[:] == [0, 1, 0, 0]: 
#        for g in range(len(GTB)): GTB[g] = 0;
#    elif R[:] == [1, 1, 0, 0]: 
#        for g in range(len(GTB)): GTB[g] = 0;
#        GTB[0] = 1;
#    elif R[:] == [1, 0, 1, 1]: 
#        for g in range(len(GTB)): GTB[g] = 1;
#        GTB[11] = 0;
#    elif R[:] == [0, 1, 1, 1]: 
#        for g in range(len(GTB)): GTB[g] = 0;
    
    # cnt_clk_gen
    
    #cnt_clk = AND(NAND(dir[ndirc],AND(GTB[0],done_check)), 1);
    cnt_clk = 1;
    addval = 0;
    
    #DAC ctrl, check this because it only happens during done check, fconv increment dcount everytime
    if cnt_clk:  
        #print GTB                                               # ** Still not sure why d_count increments when cnt_clk not high
        #for i in range(len(GTB)):
        #    if GTB[i] == 1:
        #        break;
        #addval = 2**(i);
        #print r_count                                        # ** The GTB mask supposedly locks when 1, is my method correct?
        addval = 2**(r_count);
        if ndir:
            d_count = d_count + addval;
            print (d_count)
        else:
            d_count = d_count - addval; 
    
    ndirc = ndirc + 1; 

#%% GTB Decoder Func

def decodeGTB(R):
    bR = [0, 0, 0, 0];
    GTB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    for i in range(len(R)): bR[i] = not R[i];
    GTB[0] = AND(bR[3], AND(bR[2],bR[1])); 
    GTB[1] = AND(bR[3], AND(bR[2],OR(bR[1],bR[0]))); #check cadence 
    GTB[2] = AND(bR[3],bR[2]);
    GTB[3] = AND(bR[3],OR(bR[2],AND(bR[1],bR[0])));
    GTB[4] = AND(bR[3],OR(bR[2],bR[1]));
    GTB[5] = AND(bR[3],NAND(R[2], AND(R[1],R[0])));
    GTB[6] = not R[3];
    GTB[7] = NAND(R[3],NAND(bR[2],AND(R[1],R[0])));
    GTB[8] = NAND(R[3],OR(R[2],R[1]));
    GTB[9] = NAND(R[3],OR(R[2], AND(R[1],R[0])));
    GTB[10] = NAND(R[3],R[2]);
    GTB = list(map(int, GTB));
    return GTB

#%% Radix Func

def radixCount(stayb, res_dir, r_count):
    if stayb:
        r_count = r_count + 1;
        
#%% Plot
plt.figure();
plt.plot(dir);

#%% Direct Signal Into NISoC, varying the frequency and amplitude 
# initialize and set DACs

savepath="C:/Users/a1pau/Desktop/VLSI2020_Demo/sweep/"
rec_len = 30; # seconds

srt_V = 0.0;
end_V = 1.2;
step_V = 0.01;
amps = np.arange(srt_V,end_V+step_V,step_V);
#srt_f = 1;
#end_f = 12500;
a1 = 10.**(np.arange(0, 4));
a2 = np.arange(1,11,1);
freqs = np.outer(a1, a2).flatten();

time_step = 30;
start_time = '180600'

while(1):
    if (time.strftime("%H%M%S") == start_time):
        for k in amps:
            for i in freqs: 
                
                write_FPGA(dev,0x00,int('0000000000001100', 2))
                #print '[0] 0-Full/1-SingleConv, [2] RSTOTA enabled, [3] DS mode OFF.'
                time.sleep(1)
                write_FPGA(dev,0x00,int('0000000000001000', 2))
                
                while int(time.strftime("%Y%m%d-%H%M%S")[-2:])%time_step != 0: pass
                #print 'after while'    
                print (i)
                # Acquire data from NISoC 
                filename=savepath+time.strftime("%Y%m%d-%H%M%S")+ "_QFP4_Ch0_"+"amp_"+str(k)+"_freq_"+str(i)+".h5" 
                Data_Read_USB(dev=dev,filename=filename,recordingtime=rec_len);
            
        break


# Disable clocks
write_FPGA(dev,0x03,int('0000000000000000', 2))
print ('Clocks output disabled.')
    