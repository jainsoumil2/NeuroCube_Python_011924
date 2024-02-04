# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 16:46:13 2021

@author: isnl
"""
from NeuroCube_functions import *
import time
import pyvisa 

#%%
def test_alpha_beta_currents(dev, my_Scope):
    neurodyn_sel = 1
    chip_init(dev, neurodyn_sel)
    
    set_current_source_selector_switch_all_neurodyns(dev, 2)                        # 1 - howland current source; 2 - external DAC 
    set_probe_on_expose_on(dev, 2**neurodyn_sel)
    set_neurodyn_outputs_mux(dev, 3)                                                # target_output = 1 -- gTapMUX; 2 -- EreverseTapMUX; 3 -- VmemBufMUX; 4 -- VmemProbeIn       
    
    write_external_DACs_neurodyn(dev, VmemProbeIn, 0.9, neurodyn_sel+1)             # set default voltage clamp value to 0.9v
    
    
    data_stim1 = load_matlab_data('down_sample1.mat')
    parms = load_matlab_data('labDemo.mat')
    
    
    blank = [[[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]],
    
             [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]],
    
             [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]]
    
    
    alpha_list = []
    beta_list = []
    Vmem_list = []
    #for sigmoid in range(7):
    sigmoid = 3
    for sigmoid_value in [0, 256, 512, 768, 1023]:
        parms['biasAlphaBeta'][0][0] = blank
        for alpha_beta in [0, 1]:
            for m_h_n in [0, 1, 2]:
                parms['biasAlphaBeta'][0][0][m_h_n][alpha_beta][sigmoid] = sigmoid_value
    
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
        
        for neuron in [0]:                                                      
            #for channel in [0, 32, 64]:
            for channel in [0]:                                                                            # m,h,n =[0,32,64]; needed for selecting m/n/h channel for IAlphaTapMUX, IBetaTapMUX but not for VmemProbeIn, VmemBufMUX       
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
                
                    
    np.savetxt('alpha_partial.csv', alpha_list, delimiter=',', fmt='%4s')
    np.savetxt('beta_partial.csv', beta_list, delimiter=',', fmt='%4s')
    np.savetxt('VmemBufMUX_partial.csv', beta_list, delimiter=',', fmt='%4s')


# %% visualize alpha beta currents
alpha_list = np.loadtxt('alpha_partial.csv', dtype=float)
beta_list = np.loadtxt('beta_partial.csv', dtype=float)
alpha_array = np.array(alpha_list)
beta_array = np.array(beta_list)

#sigmoid_alpha = np.reshape(alpha_array, (-1, 3, 21))
#sigmoid_beta = np.reshape(beta_array, (-1, 3, 21))
sigmoid_alpha = np.reshape(alpha_array, (-1, 21))
sigmoid_beta = np.reshape(beta_array, (-1, 21))
print('alpha :', sigmoid_alpha)
print('beta :',sigmoid_beta)


m = 0
h = 1
n = 2
ch_name = ['m', 'h', 'n']

Vmem = np.linspace(0.6, 1.2, 21, endpoint=True)
sigm_value = [0, 256, 512, 768, 1023]

for neuron in [0]:
    plt.close('all')
    fig = plt.figure()
    fig.patch.set_alpha(0.1)
    fig.subplots_adjust(hspace=0, wspace=0)
    
    #sigmoid_multi_alpha = sigmoid_alpha[neuron::4,:,:]
    #sigmoid_multi_beta = sigmoid_beta[neuron::4,:,:]
    
    #sliced_multi_alpha = np.reshape(sliced_multi_alpha, (-1, 21))
    #sliced_multi_beta = np.reshape(sliced_multi_beta, (-1, 21))
    
    sigmoid_multi_alpha = sigmoid_alpha
    sigmoid_multi_beta = sigmoid_beta
    
    #for channel in [m, h, n]:
    for channel in [m]:
        #sigmoid_single_alpha = sigmoid_multi_alpha[channel::3, :]
        sigmoid_single_alpha = sigmoid_multi_alpha
        #sigmoid_single_beta = sigmoid_multi_beta[channel::3, :]
        sigmoid_single_beta = sigmoid_multi_beta
        #for sigmoid_num in range(7):
        for sigmoid_num in [3]:
            #ax = fig.add_subplot(3, 7, 7 * channel + sigmoid_num + 1)
            ax = fig.add_subplot(1, 1, 1)
            ax.patch.set_facecolor('white')
            Font_Size = 12
            plt.ylabel('I ($nA$)', fontsize=Font_Size)
            plt.xlabel('Vmem $(V)$', fontsize=Font_Size)
    
            for sigmoid_value in range(5):
                #plt.plot(Vmem, sigmoid_single_alpha[sigmoid_num * 5 + sigmoid_value, :], '*-', linewidth=0.6,
                #         label=r'$\alpha$_' + str(sigm_value[sigmoid_value]))
                plt.plot(Vmem, sigmoid_single_alpha[sigmoid_value, :], '*-', linewidth=0.6,
                         label=r'$\alpha$_' + str(sigm_value[sigmoid_value]))
                #plt.plot(Vmem, sigmoid_single_beta[sigmoid_num * 5 + sigmoid_value, :], '*-', linewidth=0.6,
                #         label=r'$\beta$_' + str(sigm_value[sigmoid_value]))
                plt.plot(Vmem, sigmoid_single_beta[sigmoid_value, :], '*-', linewidth=0.6,
                         label=r'$\beta$_' + str(sigm_value[sigmoid_value]))
                #plt.ylim([-0.01, 0.19])
                #plt.yticks(np.arange(0.0, 0.2, step=0.02))
                plt.xlim([0.6, 1.2])
                plt.xticks([0.6, 0.9, 1.2])
                plt.text(0.42, 0.92, 'sigmoid' + str(sigmoid_num + 1) + ' of ' + ch_name[channel], fontsize=12,
                         color='black',transform=ax.transAxes)
            plt.legend(loc='center left', fontsize=Font_Size - 2, fancybox=False)
            
    fig.suptitle('Neuron '+str(neuron+1))
    plt.show()
    plt.savefig('figure neuron '+str(neuron+1)+' partial')
    

#%% Inflection point of sigmoids -- filtering noisy data and finding inflection point from zero-crossing of second derivative

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import statistics

plt.close('all')

for sigmoid_value in range(5):
    
    raw = sigmoid_alpha[sigmoid_value, :]
    standard_deviation = statistics.stdev(raw)
    standard_deviation = statistics.stdev(raw)
    print(standard_deviation)
    
    # smooth
    smooth = gaussian_filter1d(raw, 1)                # confirm how to estimate the standard deviation for Gaussian kernel
    
    # compute second derivative
    smooth_d2 = np.gradient(np.gradient(smooth))

    # find switching points
    infls = np.where(np.diff(np.sign(smooth_d2)))[0]

    plt.plot(raw, label='Noisy Data')
    plt.plot(smooth, label='Smoothed Data')
    plt.plot(smooth_d2 / np.max(smooth_d2), label='Second Derivative (scaled)')
    for i, infl in enumerate(infls, 1):
        plt.axvline(x=infl, color='k', label=f'Inflection Point {i}')
    
    print(infls*(0.6/20) + 0.6)
    plt.legend()
    plt.show()
    
#%%