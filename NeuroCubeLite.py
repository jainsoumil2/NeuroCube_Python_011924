####################################################
#%% Initialization
####################################################
'''
The following code for initializing and getting general information about Opal Kelly was obtained from DESTester.py found in the samples of Opal Kelly samples folder (DES).
FrontPanelSDK 5.2.11 was installed (that is, files were copied into the repo) for Opal Kelly.
Note - Initialization (class 'Initialize') does not work (USB trouble) if the Opal Kelly FrontPanel application is open.


~~Key Datasheets~~
Gap Junction Mux (I/O Expander)
    MAX 7301
        https://www.analog.com/media/en/technical-documentation/data-sheets/MAX7301.pdf

External DAC: 
    LTC 2666
        https://www.analog.com/media/en/technical-documentation/data-sheets/ltc2666.pdf
'''

# helper functions
import sys
sys.path.append("okFiles/Mac//")
from NeuroCube_functions_rev2 import *
import time
import pyvisa

from numpy import sign as sign

# Utility functions
def range1(end, start=1):
    return range(start, end+1)


####################################################
# initialize neurocube device (dev)
####################################################
from nc import *

# Path to bitfile   
# BIT_FILE_PATH = r"/Users/Abhinav/NeuroCube/BIT_FILES/nisoc_main.bit"
BIT_FILE_PATH = r"C:/Users/jains/OneDrive - UC San Diego/research/NeuroCube/Python/NeuroCube/BIT_FILES/nisoc_main.bit"

# Load bitfile to opal kelly
LOAD_BIT_FILE = False
if LOAD_BIT_FILE:
    dev.loadBitFile(BIT_FILE_PATH) # skip loading bitfile (rely on flash)

# reset the device
RESET_DEVICE = True
if RESET_DEVICE:
    dev.initDevice() 


#%%#################################################
### Initialize and set nisoc DACs
####################################################

# TODO: check with Akshay on using the new NiSoC

if 0: # skip using NiSoC for now
    init_DACs_nisoc(dev)

    write_DACs_nisoc(dev, IVbP_OTA, 0.826)          #0.826, 0.800
    write_DACs_nisoc(dev, Vinfinimp_bias, 1.278)    #1.268
    write_DACs_nisoc(dev, Vclamp_p, 1.25)           #1.24
    write_DACs_nisoc(dev, Vclamp_n, 0.8)            #0.794
    write_DACs_nisoc(dev, IVbNP_stim, 0.5)          #0.497
    write_DACs_nisoc(dev, IVbNN_stim, 0.5)          #0.497
    write_DACs_nisoc(dev, Vref_nisoc, 1.053)        #1.044


####################################################
#%% Set ports of gap junctions
####################################################
'''
Each neurodyn has four neurons. We can think of these as 4 quadrants.
28-Port IO Expander MAX7301 used for selecting gap junction resistors.
'''

# configuring the gap junction switches is a three step process:
# 1. disable MAX7301 shutdown
# 2. config all ports as active high|low outputs
# 3. set each port to drive 0 (or 1 for P28 CS)

# Command addresses for accessing different ports (in groups of 4)
PORT_CONFIG_P4_TO_P7    = 0x09
PORT_CONFIG_P8_TO_P11   = 0x0A
PORT_CONFIG_P12_TO_P15  = 0x0B
PORT_CONFIG_P16_TO_P19  = 0x0C
PORT_CONFIG_P20_TO_P23  = 0x0D
PORT_CONFIG_P24_TO_P27  = 0x0E
PORT_CONFIG_P28_TO_P31  = 0x0F

# Data word for setting active outputs on these ports
ACTIVE_L_H = 0b01
FOUR_PORT_ACTIVE_L_H  = ACTIVE_L_H << 0
FOUR_PORT_ACTIVE_L_H |= ACTIVE_L_H << 2
FOUR_PORT_ACTIVE_L_H |= ACTIVE_L_H << 4
FOUR_PORT_ACTIVE_L_H |= ACTIVE_L_H << 6

# Now perform the port configuration and high|low settings
for quadrant in range1(4):

    # disable shutdown mode, disable transition detection
    write_Gap_Junction(dev, quadrant, 0x0401)

<<<<<<< HEAD
    # configuration -- set P7, P6, P5, P4 as output ports
    write_Gap_Junction(dev, quadrant, 0x0955)
=======
    # configuration -- set ports P4 through P31 as active outputs
    for PORT_CONFIG_PINS in [
                                PORT_CONFIG_P4_TO_P7, 
                                PORT_CONFIG_P8_TO_P11,
                                PORT_CONFIG_P12_TO_P15,
                                PORT_CONFIG_P16_TO_P19,
                                PORT_CONFIG_P20_TO_P23,
                                PORT_CONFIG_P24_TO_P27
                            ]:
        write_Gap_Junction(dev, quadrant, PORT_CONFIG_PINS << 8 | FOUR_PORT_ACTIVE_L_H)
>>>>>>> 0c2d8b006a2ec693fddac461f173a51c6cca5e76
    
    # ports 4-11 output logic 0
    write_Gap_Junction(dev, quadrant, 0x4400)
    # ports 12-19 output logic 0
    write_Gap_Junction(dev, quadrant, 0x4C00)
    # ports 20-27 output logic 0
    write_Gap_Junction(dev, quadrant, 0x5400)
    # port 28 (neurodyn 1 dac's CSbar) outputs logic 1, ports 29-31 output logic 0
    write_Gap_Junction(dev, quadrant, 0x5C01)
    

####################################################
#%% Initialize and write all four neurodyn's external DACs
####################################################

# External DAC parameter table for all four NeuroDyns
external_DAC_params = {}
external_DAC_params['Vref']             = [""]*4    # [0.9] * 4
external_DAC_params['vBiasN']           = [""]*4    # [1.4] * 4
external_DAC_params['vBiasP']           = [""]*4    # [1.7] * 4
external_DAC_params['Vb']               = [""]*4    # [0.9] * 4
external_DAC_params['IinVoltagePin']    = [""]*4    # [1.2, 1.2, 1.2, 1.16]
external_DAC_params['IinCurrentPin']    = [""]*4    # [0.9, 0.6195, 0.6195, 0.6255]
external_DAC_params['IinRefPin']        = [""]*4    # [0.9, 0.4405, 0.4405, 0.442]
external_DAC_params['VmemProbeIn']      = [""]*4    # [0.9] * 4


####################################################
#%% Neurodyn main code
####################################################               

# Select a neurodyn chip to write to   

nd = 1  # options - 0, 1, 2, 3       

# Provide ext DAC voltages
external_DAC_params['Vref'][nd]             = 0.901     # 0.893v measured
external_DAC_params['vBiasN'][nd]           = 1.365     # 1.385v measured
external_DAC_params['vBiasP'][nd]           = 1.694     # 1.656v measured
external_DAC_params['Vb'][nd]               = 0.9012    # 0.895v measured

# socket 1 - 1.154v -- 3uA => 0.3uA * 1Mohm = +/- 0.3V on Vref for DR (0.6 to 1.2)V
external_DAC_params['IinVoltagePin'][nd]    = 1.154     # 0.145v measured

# socket 1 - 0.6211v -- 40nA => 40/10 nA Imaster (for both gmax and alpha|beta max) 
# = 4nA (at DAC max of 1024) => 4 nA charges 4pF => 1ms to charge 1V
external_DAC_params['IinCurrentPin'][nd]    = 0.6211    # 0.616v measured
# note: in sub-threshold, current doubles every 30mV

# socket 1 - 0.4422v -- 0.4nA => 40 pA Iref 
# (translinear operation of gating variables circuit)
external_DAC_params['IinRefPin'][nd]        = 0.4422    # 0.437v measured
external_DAC_params['VmemProbeIn'][nd]      = 0.9       # 0.893v measured

# Write external DACs
write_external_DACs_neurocube(dev, external_DAC_params, nd)  
# this function does not set the DAC's test MUX

# Does this reset gap junctions, or just assert CS for nd?
chip_init(dev, nd)

# 1 - howland current source; 2 - external DAC 
CURRENT_SOURCE_HOWLAND = 1
CURRENT_SOURCE_EXT_DAC = 2
set_current_source_selector_switch_all_neurodyns(dev, CURRENT_SOURCE_HOWLAND) 

####################################################
# Configure probe/expose for measuring output voltages
####################################################
# We can use "expose" to bring out unbuffered voltages to the NiSoC header, and 
# then jump these over to the four buffer inputs.
#set_probe_on_expose_off(dev, 2**nd)
set_expose_off_probe_off_all_neurodyns(dev)
#set_expose_on_probe_off_all_neurodyns(dev) 

# target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn
OUTPUT_MUX_GTAPMUX = 1
OUTPUT_MUX_EREVERSETAPMUX = 2
OUTPUT_MUX_VMEMBUFMUX = 3       # buffered VMem
OUTPUT_MUX_VMEMPROBEIN = 4      # externally drive a voltage into Vmem
set_neurodyn_outputs_mux(dev, OUTPUT_MUX_VMEMBUFMUX)                              
#set_dac_cal_off_switchrpin_off(dev)

# Load stim data (currently unused)
data_stim1 = load_matlab_data('down_sample1.mat')

# Load internal DAC values from MATLAB data structure
parms = load_matlab_data('labDemo.mat')
# parms['biasgErev'][neuron0][0][0][0] -- sodium maximal conductance, 
# parms['biasgErev'][neuron0][0][0][1] -- sodium maximal reversal potential, 
# parms['biasgErev'][neuron0][0][1][0] -- potassium maximal conductance, 
# parms['biasgErev'][neuron0][0][1][1] -- sodium reversal potential, 
# parms['biasgErev'][neuron0][0][2][0] -- leak maximal conductance, 
# parms['biasgErev'][neuron0][0][2][1] -- leak reverse potential 

# Override loaded parameters as needed:
g_Na = 512
E_Na = 1023
g_K = 1023
E_K = -1023
g_L = 32
E_L = 400

m_α = [0, 0, 0, 256, 0, 0, 0]
m_β = [0, 0, 0, 256, 0, 0, 0]
h_α = [0, 0, 0, 32, 0, 0, 0]
h_β = [0, 0, 0, 32, 0, 0, 0]
n_α = [0, 0, 0, 32, 0, 0, 0]
n_β = [0, 0, 0, 32, 0, 0, 0]
# sign_Iα

#Gert's from email thread - NeuroDyn spiking (bursting?, HCO?) parameters
for neuron in range(4):
    parms['biasgErev'][neuron][0] = [[abs(g_Na), abs(E_Na)], 
                                     [abs(g_K), abs(E_K)], 
                                     [abs(g_L), abs(E_L)]] 
    # note, sign is only used for Erev (redundant for g)
    parms['signgErev'][neuron][0] = [[sign(g_Na), sign(E_Na)], 
                                     [sign(g_K), sign(E_K)], 
                                     [sign(g_L), sign(E_L)]]

    parms['biasAlphaBeta'][neuron][0][0][0][:] = m_α
    parms['biasAlphaBeta'][neuron][0][0][1][:] = m_β
    parms['biasAlphaBeta'][neuron][0][1][0][:] = h_α
    parms['biasAlphaBeta'][neuron][0][1][1][:] = h_β
    parms['biasAlphaBeta'][neuron][0][2][0][:] = n_α
    parms['biasAlphaBeta'][neuron][0][2][1][:] = n_β

    parms['signAlphaBeta'][neuron][0] = [[1, -1], [-1, 1], [1, -1]] # are these fixed?
       
# SYNAPSE PARAMETERS
# SETTING MUTUAL INHIBITORY SYNAPSES BETWEEN NEURON 1 AND NEURON 3 FOR ANTI-PHASE OSCILLATIONS -- required for HCO (Bursting neurons are also required for a HCO)

# Each neuron can synapse to three other neurons
# => we have three synapses per neuron
g_syn = [0, 0, 0]
E_syn = [256, 256, 256]

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

# Program internal DACs
startTime = time.time()
for quadrantSel in [0, 1, 2, 3]:  # for soma
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  0, nd)


for quadrantSel in [0, 1, 2, 3]: # for synapse
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  1, nd)

# Now reselect neuron1 to output Vmem to MUX
neuron = 0 # 0 and 2 are happy
ifSynapse = 0
channelNum = 0
typ = 0                     # select alpha/beta rate, maximal conductance, reversal potential 
bumpNum = 0
addr = (neuron << 8) + (ifSynapse << 7) + (channelNum << 5) + (typ << 3) + bumpNum            
# neuron 0, channel = 0 (m); m, h, n = [0,32,64]
set_internal_dacs_address(dev, addr, nd)


#bit = 1
#for i in range(100000):
#    parms['biasgErev'][0][0] = [[0, 1023], [0, 256], [1023, El + 50*bit]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
#    load_int_dacs_signbit_leak_channels(dev, parms['signgErev'], parms['biasgErev'], 0, 0, neurodyn_sel)
#    time.sleep(0.1)
#    bit = -bit