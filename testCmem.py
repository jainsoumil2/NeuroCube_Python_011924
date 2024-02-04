import sys
sys.path.append("okFiles/Win//")
from nc import *
from NeuroCube_functions import *
import time
import pyvisa 


    

# gating variable kinetics translinear circuit capacitance Cg -- mini version

neurodyn_sel = 2   #THIS IS NEURODYN 3                                         
set_dac_cal_off_switchrpin_on(dev)
set_expose_off_probe_off_all_neurodyns(dev) 
#set_probe_on_expose_off(dev, 0b0100)  # turn probe off for neurodyn 3
clear_all_int_dacs(dev, neurodyn_sel)                                        # options -- 0, 1, 2, 3
# set_current_source_selector_switch_all_neurodyns(dev, 2)      
# set_probe_on_expose_off(dev, 2**neurodyn_sel)  # 1 - howland current source; 2 - external DAC 
# set_probe_on_expose_on(dev, 2**neurodyn_sel) 

# set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       

write_external_DACs_neurodyn(dev, VmemProbeIn, 0.8, neurodyn_sel+1)             # set default voltage clamp value to 0.9v
