# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:44:16 2021

@author: isnl
"""

# visualize alpha beta currents
import numpy as np
import matplotlib.pyplot as plt

alpha_list = np.loadtxt('alpha.csv', dtype=float)
beta_list = np.loadtxt('beta.csv', dtype=float)
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
    