####################################################
#%% Initialization
####################################################
# The following code for initializing and getting general information about the Opal Kelly was obtained from DESTester.py found in the samples of Opal Kelly samples folder (DES).
# FrontPanelSDK 5.2.3 was installed for Opal Kelly.
# Note - Initialization (class 'Initialize') does not work properly (Opal kelly is not recognised) if the Opal Kelly FrontPanel application is open.
'''
import os
abspath = os.path.abspath('C:/Users/isnl/OneDrive - UC San Diego/research/NeuroCube/NISoC_python/') ## String which contains absolute path to the script file
os.chdir(abspath) ## Setting up working directory
'''

from nc import *
from NeuroCube_functions_rev2 import *
import time
import pyvisa

# Utility functions
def range1(end, start=1):
    return range(start, end+1)


####################################################
#%% Initialize and set nisoc DACs
####################################################

# TODO: check with Akshay on using the new NiSoC
'''
init_DACs_nisoc(dev)

write_DACs_nisoc(dev, IVbP_OTA, 0.826)          #0.826, 0.800
write_DACs_nisoc(dev, Vinfinimp_bias, 1.278)    #1.278
write_DACs_nisoc(dev, Vclamp_p, 1.25)
write_DACs_nisoc(dev, Vclamp_n, 0.8)    
write_DACs_nisoc(dev, IVbNP_stim, 0.5)
write_DACs_nisoc(dev, IVbNN_stim, 0.5)
write_DACs_nisoc(dev, Vref_nisoc, 1.053)        #1.053, 1.13
'''

####################################################
#%% Set ports of gap junctions
####################################################
'''
Each neurodyn has four neurons. We can think of these as 4 quadrants.
28-Port IO Expander MAX7301 used for selecting gap junction resistors.
https://www.analog.com/media/en/technical-documentation/data-sheets/MAX7301.pdf
'''
PORT_CONFIG_P4_TO_P7    = 0x09
PORT_CONFIG_P8_TO_P11   = 0x0A
PORT_CONFIG_P12_TO_P15  = 0x0B
PORT_CONFIG_P16_TO_P19  = 0x0C
PORT_CONFIG_P20_TO_P23  = 0x0D
PORT_CONFIG_P16_TO_P19  = 0x0E
ACTIVE_LOW_HIGH = 0b01


# config 
# active high|low
# drive 0

for quadrant in range1(4):

    # disable shutdown mode, disable transition detection
    write_Gap_Junction(dev, quadrant, 0x0401)

    # configuration -- set P7, P6, P5, P4 as output ports
    write_Gap_Junction(dev, quadrant, 0x0955)
    
    # configuration -- set P11, P10, P9, P8 as output ports
    write_Gap_Junction(dev, quadrant, 0x0A55)

    # configuration -- set P15, P14, P13, P12 as output ports
    write_Gap_Junction(dev, quadrant, 0x0B55)
    
    # configuration -- set P19, P18, P17, P16 as output ports
    write_Gap_Junction(dev, quadrant, 0x0C55)
    
    # configuration -- set P23, P22, P21, P20 as output ports
    write_Gap_Junction(dev, quadrant, 0x0D55)
    
    # configuration -- set P27, P26, P25, P24 as output ports
    write_Gap_Junction(dev, quadrant, 0x0E55)
    
    # port 28 (neurodyn 1 dac's CSbar) outputs logic 1, ports 29-31 output logic 0
    write_Gap_Junction(dev, quadrant, 0x5C01)

    # ports 4-11 output logic 0
    write_Gap_Junction(dev, quadrant, 0x4400)
    # ports 12-19 output logic 0
    write_Gap_Junction(dev, quadrant, 0x4C00)
    # ports 20-27 output logic 0
    write_Gap_Junction(dev, quadrant, 0x5400)
    # configuration -- set P31, P30, P29, P28 as output ports
    write_Gap_Junction(dev, quadrant, 0x0F55)



####################################################
#%% Initialize and write all four neurodyn's external DACs
####################################################
def write_external_DACs_neurocube(dev, params, nd_to_write):
    '''
    DAC Channels
    Vref_neurodyn = 0
    vBiasN = 1
    vBiasP = 2
    Vb = 3
    IinVoltagePin = 4
    IinCurrentPin = 5
    IinRefPin = 6
    VmemProbeIn = 7
    '''

    for nd in nd_to_write:  # select each of 4 neurodyns

        # 2nd argument selects which out of the 4 neurodyn's dac to program; options -- 0, 1, 2, 3
        init_external_DACs_neurodyn(dev, nd)

        # last argument selects which out of the 4 neurodyn's dac to program; options -- 0, 1, 2, 3
        write_external_DACs_neurodyn(dev, Vref_neurodyn, params['Vref'][nd], nd)
        write_external_DACs_neurodyn(dev, vBiasN, params['vBiasN'][nd], nd)
        write_external_DACs_neurodyn(dev, vBiasP, params['vBiasP'][nd], nd)
        write_external_DACs_neurodyn(dev, Vb, params['Vb'][nd], nd)
        write_external_DACs_neurodyn(dev, IinVoltagePin,
                                     params['IinVoltagePin'][nd], nd)
        write_external_DACs_neurodyn(dev, IinCurrentPin,
                                     params['IinCurrentPin'][nd], nd)
        write_external_DACs_neurodyn(dev, IinRefPin, params['IinRefPin'][nd], nd)
        write_external_DACs_neurodyn(dev, VmemProbeIn, params['VmemProbeIn'][nd],
                                     nd)

        # Set neurodyn DAC MUXOUT to REF
        # 2nd argument: 0 -- disable, 1 -- enable; last argument selects which out of the 4 neurodyn's dac to program; options -- 0, 1, 2, 3
        external_DAC_mux_vref_neurodyn(dev, 1, nd)

# External DAC parameter table for all four NeuroDyns

external_DAC_params = {}
external_DAC_params['Vref'] = [0.9] * 4
external_DAC_params['vBiasN'] = [1.4] * 4
external_DAC_params['vBiasP'] = [1.7] * 4
external_DAC_params['Vb'] = [0.9] * 4
external_DAC_params['IinVoltagePin'] = [1.2, 1.2, 1.2, 1.16]
external_DAC_params['IinCurrentPin'] = [0.9, 0.6195, 0.6195, 0.6255]
external_DAC_params['IinRefPin'] = [0.9, 0.4405, 0.4405, 0.442]
external_DAC_params['VmemProbeIn'] = [0.9] * 4
# write_external_DACs_neurocube(dev, external_DAC_params, range1(4)) # write all four neurodyns' external DACs


####################################################
#%% Neurodyn main code
####################################################               
                                                                   
nd = 1  # options - 0, 1, 2, 3
#write_external_DACs_neurodyn(dev, Vb, 0.9, nd+1)                      # last argument selects which out of the 4 neurodyn's dac to program; options -- 1, 2, 3, 4
#write_external_DACs_neurodyn(dev, IinVoltagePin, 0.6877, nd+1)         # IinVoltagePin = 0.752 -- Ivoltage = 366.9.8nA, dac = 0.727 -- Imaster = 271.2nA
#write_external_DACs_neurodyn(dev, IinCurrentPin, 0.7063, nd+1)         # IinCurrentPin = 0.722 -- IMaster = 200.6nA, dac = 0.62 -- Imaster = 40.33nA, dac = 0.7575 -- Imaster = 400.2nA, dac = 1.2771 -- Imaster = 4.0004uA, dac = 0.7063 -- Imaster = 150nA
#write_external_DACs_neurodyn(dev, IinRefPin, 0.502, nd+1)              # IinRefPin = 0.672 -- IRef = 99.4 nA, dac = 0.443 -- Iref = 0.4nA, dac = 0.53 -- Iref = 4.08nA, dac = 0.622 -- Iref = 40.1nA, dac = 0.502 -- Iref = 2nA

external_DAC_params['Vref'][nd] = 0.901  # 0.9v
external_DAC_params['vBiasN'][nd] = 1.365  # 1.4v
external_DAC_params['vBiasP'][nd] = 1.694  # 1.7v
external_DAC_params['Vb'][nd] = 0.9012  # 0.9v
external_DAC_params['IinVoltagePin'][nd] = 1.154  # socket 1 - 1.154v -- 3uA => 0.3uA * 1Mohm = +/- 0.3V on Vref for DR (0.6 to 1.2)V
external_DAC_params['IinCurrentPin'][nd] = 0.6211  # socket 1 - 0.6211v -- 40nA => 40/10 nA Imaster (for both gmax and alpha|beta max) = 4nA (at DAC max of 1024) => 4 nA charges 4pF => 1ms to charge 1V
# sub-threshold: current doubles every 30mV 
external_DAC_params['IinRefPin'][nd] = 0.4422  # socket 1 - 0.4422v -- 0.4nA => 40 pA Iref (translinear operation of gating variables circuit)
external_DAC_params['VmemProbeIn'][nd] = 0.9  # 0.9v

write_external_DACs_neurocube(dev, external_DAC_params,[nd])  

chip_init(dev, nd)

set_current_source_selector_switch_all_neurodyns(dev, 1)                        # 1 - howland current source; 2 - external DAC 
#set_probe_on_expose_off(dev, 2**nd)
set_expose_off_probe_off_all_neurodyns(dev)
#set_expose_on_probe_off_all_neurodyns(dev) 
set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       
#set_dac_cal_off_switchrpin_off(dev)


data_stim1 = load_matlab_data('down_sample1.mat')
parms = load_matlab_data('labDemo.mat')

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
                  0, nd)


for quadrantSel in [0, 1, 2, 3]: # for synapse
    load_int_dacs(dev, parms['signAlphaBeta'],
                  parms['signgErev'],
                  parms['biasAlphaBeta'],
                  parms['biasgErev'],
                  quadrantSel,
                  1, nd)
    
neuron = 1
ifSynapse = 0
channelNum = 0
typ = 0                     # select alpha/beta rate, maximal conductance, reversal potential 
bumpNum = 0
addr = (neuron << 8) + (ifSynapse << 7) + (channelNum << 5) + (typ << 3) + bumpNum            # neuron 0, channel = 0 (m); m, h, n = [0,32,64]
set_internal_dacs_address(dev, addr, nd)

#bit = 1
#for i in range(100000):
#    parms['biasgErev'][0][0] = [[0, 1023], [0, 256], [1023, El + 50*bit]]                                     # Neuron 1 -- parms['biasgErev'][0][0][0][0] -- sodium maximal conductance, parms['biasgErev'][0][0][0][1] -- sodium maximal reversal potential, parms['biasgErev'][0][0][1][0] -- potassium maximal conductance, parms['biasgErev'][0][0][1][1] -- sodium reversal potential, parms['biasgErev'][0][0][2][0] -- leak maximal conductance, parms['biasgErev'][0][0][2][1] -- leak reverse potential 
#    load_int_dacs_signbit_leak_channels(dev, parms['signgErev'], parms['biasgErev'], 0, 0, neurodyn_sel)
#    time.sleep(0.1)
#    bit = -bit

