# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 19:47:27 2021

@author: isnl
"""
from NeuroCube_functions import *
 
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

#%% regress IGateVarTapMUX against alpha/(alpha+beta) v2

neurodyn_sel = 0
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

np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/gate_var.csv', gate_var_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/alpha.csv', alpha_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/beta.csv', beta_list, delimiter=',', fmt='%4s')
np.savetxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/gTap.csv', gTap_list, delimiter=',', fmt='%4s')

# %% plot regression of IGateVarTapMUX against Ialpha/(Ialpha+Ibeta)
gate_var_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/gate_var.csv', dtype=float)
alpha_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/alpha.csv', dtype=float)
beta_list = np.loadtxt('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/beta.csv', dtype=float)
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
            #z = np.polyfit(gate_steady_state[sigmoid_set, :], gate_single_var[sigmoid_set, :], 1)
            #p = np.poly1d(z)
            #xp = np.linspace(0, 1, 100)
            #plt.plot(xp, p(xp), '-', linewidth=0.6, label=r'set '+str(sigmoid_set+1)+'slope: '+str(z[0]))
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
    plt.savefig('characterization/gating variable kinetics/neurodyn 3/gating variable offset, slope; power coefficients for m, n, h/figure'+str(neuron+1)+' Igating variable vs measured SS gating varialble' )
