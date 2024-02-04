# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 2021

@author: Soumil
"""

import csv
import operator
import os
import string
# import ok
import sys
import time
from operator import itemgetter  # for sorting the array by column

import matplotlib.pyplot as plt
import numpy as np
import ok
import os
import pandas as pd
import scipy as sp
import scipy.io
import serial
import struct
import tables
import pyvisa as visa
import math
from matplotlib.figure import Figure
from scipy.integrate import quad
from scipy.signal import butter, lfilter, freqz

AVDD_neurodyn = 3.3
VREF = 1.8

# acronym NC used below stands for NeuroCube

NC_DAC_V_data_addr = 0x19  # opal kelly's wire in endpoint address for writing data for dacs on neurocube
NC_DAC_target_addr = 0x1A  # opal kelly's wire in endpoint address for sending information about to whether to write to neurodyns' or nisoc's dacs
NC_DAC_flag_addr = 0x1B  # opal kelly's wire in endpoint address for flag which indicates the period during which data is to be written to neurocube dacs
NC_vdac_done_addr = 0x21  # opal kelly's wire in endpoint address for flag which indicates when the data has been written to neurocube dacs

GJ_V_data_addr = 0x1C
GJ_row_number = 0x1D
GJ_flag_addr = 0x1E
GJ_done_addr = 0x25

#DAC Channels - neurodyn
Vref_neurodyn = 0
vBiasN = 1
vBiasP = 2
Vb = 3
IinVoltagePin = 4
IinCurrentPin = 5
IinRefPin = 6
VmemProbeIn = 7

#DAC Channels - nisoc
IVbP_OTA = 0;
Vinfinimp_bias = 1;
Vclamp_p = 2;
Vclamp_n = 3;
IVbNP_stim = 4; 
IVbNN_stim = 5; 
Vref_nisoc = 6;

def set_internal_dacs_address(dev, address, neurodynSel):
    # set neurodyn internal dacs address (a0 - a9)

    if neurodynSel == 0:                                   # neurodyn 1
        dev.xem.SetWireInValue(0x17, address, 0xffffffff)
        dev.xem.UpdateWireIns()
        #print('Neurodyn 1 internal dacs address updated to ' + str(bin(address)))     
    
    elif neurodynSel == 1:                                 # neurodyn 2
        LSB = address % (2 ** 8)
        MSB = address - LSB
        MSB_shift_left_2bits = MSB << 2
        address_mod = MSB_shift_left_2bits + LSB

        dev.xem.SetWireInValue(0x17, address_mod, 0xffffffff)
        dev.xem.UpdateWireIns()
        #print('Neurodyn 2 internal dacs address updated to ' + str(bin(address)))
    
    elif neurodynSel == 2:                                 # neurodyn 3
        LSB = address % (2 ** 8)
        MSB = address - LSB
        MSB_shift_left_4bits = MSB << 4
        address_mod = MSB_shift_left_4bits + LSB

        dev.xem.SetWireInValue(0x17, address_mod, 0xffffffff)
        dev.xem.UpdateWireIns()
        #print('Neurodyn 3 internal dacs address updated to ' + str(bin(address)))
    
    elif neurodynSel == 3:                                 # neurodyn 4
        LSB = address % (2 ** 8)
        MSB = address - LSB
        MSB_shift_left_6bits = MSB << 6
        address_mod = MSB_shift_left_6bits + LSB

        dev.xem.SetWireInValue(0x17, address_mod, 0xffffffff)
        dev.xem.UpdateWireIns()
        #print('Neurodyn 4 internal dacs address updated to ' + str(bin(address)))


def set_internal_dacs_data(dev, data):
    # set neurodyn internal dacs data (d0 - d11)

    dev.xem.SetWireInValue(0x18, int(data), 0xffffffff)
    dev.xem.UpdateWireIns()
    #print('Neurodyn internal dacs data updated to ' + str(bin(data)))


def set_probe_on_expose_off(dev, target_neurodyn):
    # Probe on a specific neurodyn/ a subset of neurodyns

    # target_neurodyn can be 0bxyzw, x = 1 to probe neurodyn 4; y = 1 to probe neurodyn 3; z = 1 to probe neurodyn 2; w = 1 for neurodyn 1
    # example, target_neurodyn = 0x1101 will allow us to probe a specific neuron on neurodyn 4, 3 and 1. NOTE: The address of the neuron to be probed has to be set separately. It can be done by calling the desired 'set_internal_dacs_address_NDx' function after calling this set_probe_on function.

    dev.xem.SetWireInValue(0x15, target_neurodyn, 0xffffffff)
    dev.xem.UpdateWireIns()
    print('probe turned on and expose is off')


def set_probe_on_expose_on(dev, target_neurodyn):
    # Probe on a specific neurodyn/ a subset of neurodyns

    # target_neurodyn can be 0bxyzw, x = 1 to probe neurodyn 4; y = 1 to probe neurodyn 3; z = 1 to probe neurodyn 2; w = 1 for neurodyn 1
    # example, target_neurodyn = 0x1101 will allow us to probe some neuron on neurodyn 4, 3 and 1. NOTE: The address of the neuron to be probed has to be set separately. It can be done by calling the desired 'set_internal_dacs_address_NDx' function after calling this set_probe_on function.

    control_signal = (1 << 4) + target_neurodyn
    dev.xem.SetWireInValue(0x15, control_signal, 0xffffffff)
    dev.xem.UpdateWireIns()
    print('probe turned on and expose is off')


def set_expose_on_probe_off_all_neurodyns(dev):
    dev.xem.SetWireInValue(0x15, 0b10000, 0xffffffff)
    dev.xem.UpdateWireIns()


def set_expose_off_probe_off_all_neurodyns(dev):
    dev.xem.SetWireInValue(0x15, 0b00000, 0xffffffff)
    dev.xem.UpdateWireIns()


def set_WR_on(dev, target_neurodyn):  # turn on internal neurodyn dacs write
    dev.xem.SetWireInValue(0x0a, 2 ** target_neurodyn,
                           0xffffffff)  # 0b0001 -- neurodyn 1; 0b0010 -- neurodyn 2; 0b0100 -- neurodyn 3; 0b1000 -- neurodyn 4
    dev.xem.UpdateWireIns()


def set_WR_off(dev):  # turn off internal neurodyn dacs write
    dev.xem.SetWireInValue(0x0a, 0x00, 0xffffffff)
    dev.xem.UpdateWireIns()


def set_dac_cal_off_switchrpin_on(dev):
    dev.xem.SetWireInValue(0x0c, 0b10, 0xffffffff)
    dev.xem.UpdateWireIns()


def set_dac_cal_on_switchrpin_on(dev):
    dev.xem.SetWireInValue(0x0c, 0b11, 0xffffffff)
    dev.xem.UpdateWireIns()


def set_dac_cal_on_switchrpin_off(dev):
    dev.xem.SetWireInValue(0x0c, 0b01, 0xffffffff)
    dev.xem.UpdateWireIns()


def set_dac_cal_off_switchrpin_off(dev):
    dev.xem.SetWireInValue(0x0c, 0b00, 0xffffffff)
    dev.xem.UpdateWireIns()


def set_neurodyn_outputs_mux(dev, target_output):
    # function for selecting one of the following four outputs from neurodyn to channels on NISoC (neurodyn 1 -- CH7 on NISoC; neurodyn 2 -- CH15; neurodyn 3 -- CH23; neurodyn 4 -- CH31) using the 4 TMUX1104DGSR chips (one for each neurodyn) on the pcb
    # target_output = 1 -- gTapMUX
    # target_output = 2 -- EreverseTapMUX
    # target_output = 3 -- VmemBufMUX
    # target_output = 4 -- VmemProbeIn

    if target_output == 1:
        dev.xem.SetWireInValue(0x0d, 0b00, 0xffffffff)
        print('gTapMUX is sent to the corresponding neurodyn channel on NISoC')
    elif target_output == 2:
        dev.xem.SetWireInValue(0x0d, 0b01, 0xffffffff)
        print('EreverseTapMUX is sent to the corresponding neurodyn channel on NISoC')
    elif target_output == 3:
        dev.xem.SetWireInValue(0x0d, 0b10, 0xffffffff)
        print('VmemBufMUX is sent to the corresponding neurodyn channel on NISoC')
    elif target_output == 4:
        dev.xem.SetWireInValue(0x0d, 0b11, 0xffffffff)
        print('VmemProbeIn is sent to the corresponding neurodyn channel on NISoC')
    dev.xem.UpdateWireIns()


def set_neurodyn_current_source_selector_switch(dev, source_sel, neurodyn_sel):
    # function for selecting the current source as either the howland current source or from external DAC intended for neurodyn (voltage clamp?)
    # source select = 1 -- howland current source
    # source select = 2 -- external DAC
    
    if source_sel == 1:
        if neurodyn_sel == 0:                               # neurodyn 1
            dev.xem.SetWireInValue(0x16, 0b00000001, 0xffffffff)
            print('howland current source selected for neurodyn 1')
        elif neurodyn_sel == 1:                             # neurodyn 2
            dev.xem.SetWireInValue(0x16, 0b00000010, 0xffffffff)
            print('howland current source selected for neurodyn 2')
        elif neurodyn_sel == 2:                             # neurodyn 3
            dev.xem.SetWireInValue(0x16, 0b00000100, 0xffffffff)
            print('howland current source selected for neurodyn 3')
        elif neurodyn_sel == 3:                             # neurodyn 4
            dev.xem.SetWireInValue(0x16, 0b00001000, 0xffffffff)
            print('howland current source selected for neurodyn 4')
    elif source_sel == 2:
        if neurodyn_sel == 0:                               # neurodyn 1
            dev.xem.SetWireInValue(0x16, 0b00010000, 0xffffffff)
            print('External dac selected for voltage clamping neurodyn 1')
        elif neurodyn_sel == 1:                             # neurodyn 2
            dev.xem.SetWireInValue(0x16, 0b00100000, 0xffffffff)
            print('External dac selected for voltage clamping neurodyn 2')
        elif neurodyn_sel == 2:                             # neurodyn 3
            dev.xem.SetWireInValue(0x16, 0b01000000, 0xffffffff)
            print('External dac selected for voltage clamping neurodyn 3')
        elif neurodyn_sel == 3:                             # neurodyn 4
            dev.xem.SetWireInValue(0x16, 0b10000000, 0xffffffff)
            print('External dac selected for voltage clamping neurodyn 4')
    
def set_current_source_selector_switch_all_neurodyns(dev, source_sel):
    # function for selecting the current source as either the howland current source or from external DAC intended for neurodyn (voltage clamp?)
    # source select = 1 -- howland current source
    # source select = 2 -- external DAC
    
    if source_sel == 1:
        dev.xem.SetWireInValue(0x16, 0b00001111, 0xffffffff)
        print('howland current source selected for all neurodyns')
    elif source_sel == 2:
        dev.xem.SetWireInValue(0x16, 0b11110000, 0xffffffff)
        print('External dac selected for voltage clamping all neurodyns')

def write_FPGA_NC(dev, addr, value):
    dev.xem.SetWireInValue(addr, value, 0xffffffff)
    dev.xem.UpdateWireIns()


def read_FPGA_NC(dev, addr):
    dev.xem.UpdateWireOuts()
    return dev.xem.GetWireOutValue(addr)


# %  Functions Definition
# DAC configuration
# start configure DAC
# Config Reference: 0111 0000 0000 0000 0000 0001
# Write Span:   1110 0111 0000 0000 0000 0000
# Write Span_alt:   1110 0001 0000 0000 0000 0000
def init_DACs_nisoc(dev):
    tmptime = time.time()
    write_FPGA_NC(dev, NC_DAC_V_data_addr, 0x700001)
    write_FPGA_NC(dev, NC_DAC_target_addr, 1)  # target = 1 -- nisoc, 2 -- neurodyns
    write_FPGA_NC(dev, NC_DAC_flag_addr, 0x06)
    while True:
        done = read_FPGA_NC(dev, NC_vdac_done_addr)
        if done == 1:
            write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
            time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period.10 usec will be a wait of 5 clock cycles.
            write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
            #print("DAC reference is configured")
            break
        if (time.time() - tmptime) > 10:
           print("G Check USB connnection or Re-connect USB !")
           break

    time.sleep(1)

    write_FPGA_NC(dev, NC_DAC_V_data_addr, 0xE10000)
    write_FPGA_NC(dev, NC_DAC_target_addr, 1)  # target = 1 -- nisoc, 2 -- neurodyns
    write_FPGA_NC(dev, NC_DAC_flag_addr, 0x06)
    while True:
        done = read_FPGA_NC(dev, NC_vdac_done_addr)
        if done == 1:
            write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
            time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period.10 usec will be a wait of 5 clock cycles.
            write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
            #print("DAC Span is configured")
            break
        if (time.time() - tmptime) > 10:
            print("H Check USB connnection or Re-connect USB !")
            break


def calc_dac_values_NC(targetV):
    """
    functional description - calculates the DAC digital value to achieve the
    target output voltage
    """
    global VREF
    return np.round(targetV / (VREF * 2.0) * 2 ** 16).astype('int')


def write_DACs_nisoc(dev, ch, value):
    """
    functional description:
    writes I/V DACs
    """
    if 0 <= ch <= 15:
        done = 0
        # V_I=ch/8
        addr = ch % 8
        data = calc_dac_values_NC(value)
        command = int(0x300000 + (addr * 0x10000) + data)

        write_FPGA_NC(dev, NC_DAC_V_data_addr, command)
        write_FPGA_NC(dev, NC_DAC_target_addr, 1)  # target = 1 -- nisoc, 2 -- neurodyns
        write_FPGA_NC(dev, NC_DAC_flag_addr, 0x02)  # 0x02 will select V DAC

        while True:
            #  print "loop"
            done = read_FPGA_NC(dev, NC_vdac_done_addr)
            if done == 1:
                write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
                time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period.10 usec will be a wait of 5 clock cycles.
                write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
                #print("DAC" + str(ch) + " is updated")
                break
    else:
        print("Dac Channel 'ch' is wrong!")


def DAC_mux_vref_nisoc(dev, enable):
    """
    function will instruct DACs to output REF value on MUXOUT pin
    """
    #print(enable)
    ref_command = 0xB00019  # 1011 0000 0000 0000 0001 1001
    off_command = 0xB00000  # 1011 0000 0000 0000 0000 0000
    if enable:
        write_FPGA_NC(dev, NC_DAC_V_data_addr, ref_command)
        write_FPGA_NC(dev, NC_DAC_target_addr, 1)  # target = 1 -- nisoc, 2 -- neurodyns
    else:
        write_FPGA_NC(dev, NC_DAC_V_data_addr, off_command)
        write_FPGA_NC(dev, NC_DAC_target_addr, 1)  # target = 1 -- nisoc, 2 -- neurodyns
    write_FPGA_NC(dev, NC_DAC_flag_addr, 0x02)  # 0x02 will select V DAC
    # print "step1"
    while True:
        #print("loop")
        done = read_FPGA_NC(dev, NC_vdac_done_addr)
        if done == 1:
            write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
            time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period.10 usec will be a wait of 5 clock cycles.
            write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
            if enable:
                #print("DAC MUXOUT configured to REF")
                None
            else:
                print("DAC MUXOUT configured to HiZ off")
            break


def write_external_DACs_neurocube(dev, params, nd_to_write):
    ''' 
    Helper function to write external DACs for all nd chips listed in nd_to_write.
    Note, external DAC settings are shared for all four neurons on a ND chip, however, different ND chips in NeuroCube are driven by independent DACs.
    params is just a dictionary with each voltage settings specified for each of four neurons in a neurodyn

    Channel mapping as defined in nc.py:
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

    if not nd_to_write == list: # if a single nd index was provided as input
        nd_to_write = [nd_to_write] # make it into a list for running the loop below

    for nd in nd_to_write:  # select the nd chip to write external DACs for (from 0 to 3)
        print("Write external DACs for nd{}...".format(nd))

        # 2nd argument selects which out of the 4 neurodyn's dac to program; options -- 0, 1, 2, 3
        init_external_DACs_neurodyn(dev, nd)

        # last argument selects which out of the 4 neurodyn's dac to program; options -- 0, 1, 2, 3
        write_external_DACs_neurodyn(dev, Vref_neurodyn, params['Vref'][nd], nd)
        write_external_DACs_neurodyn(dev, vBiasN, params['vBiasN'][nd], nd)
        write_external_DACs_neurodyn(dev, vBiasP, params['vBiasP'][nd], nd)
        write_external_DACs_neurodyn(dev, Vb, params['Vb'][nd], nd)
        write_external_DACs_neurodyn(dev, IinVoltagePin, params['IinVoltagePin'][nd], nd)
        write_external_DACs_neurodyn(dev, IinCurrentPin, params['IinCurrentPin'][nd], nd)
        write_external_DACs_neurodyn(dev, IinRefPin, params['IinRefPin'][nd], nd)
        write_external_DACs_neurodyn(dev, VmemProbeIn, params['VmemProbeIn'][nd], nd)

        # Set neurodyn DAC MUXOUT to REF
        # 2nd argument: 
        #   0 -- disable, 
        #   1 -- enable; 
        # last argument selects which out of the 4 neurodyn's dac to program; options -- 0, 1, 2, 3
        # external_DAC_mux_vref_neurodyn(dev, 1, nd) # AU: 1/24/23: setting this seems to affect other DAC outs...?

        print("Finished writing external DACs for nd{}!".format(nd))


def init_external_DACs_neurodyn(dev, which_neurodyn):
    # AU: 1/14/23: offset which_neurodyn by 1 to remain uniform indexing of 0-3
    which_neurodyn += 1

    tmptime = time.time()
    write_FPGA_NC(dev, NC_DAC_V_data_addr, 0x700001)
    write_FPGA_NC(dev, NC_DAC_target_addr, 2)  # target = 1 -- nisoc, 2 -- neurodyns
    write_Gap_Junction(dev, which_neurodyn,
                       0x5C00)  # options for which_neurodyn -- 1, 2, 3, 4; enable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 0, ports 29-31 output logic 0
    write_FPGA_NC(dev, NC_DAC_flag_addr, 0x06)
    while True:
        done = read_FPGA_NC(dev, NC_vdac_done_addr)
        if done == 1:
            write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
            write_Gap_Junction(dev, which_neurodyn,
                               0x5C01)  # options for which_neurodyn -- 1, 2, 3, 4; disable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 1, ports 29-31 output logic 0
            time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period.10 usec will be a wait of 5 clock cycles.
            write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
            #print("DAC reference is configured")
            break
        if (time.time() - tmptime) > 10:
            print("G Check USB connnection or Re-connect USB !")
            break

    time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period. 10 usec will be a wait of 5 clock cycles.

    write_FPGA_NC(dev, NC_DAC_V_data_addr, 0xE10000)
    write_FPGA_NC(dev, NC_DAC_target_addr, 2)  # target = 1 -- nisoc, 2 -- neurodyns
    write_Gap_Junction(dev, which_neurodyn,
                       0x5C00)  # options for which_neurodyn -- 1, 2, 3, 4; enable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 0, ports 29-31 output logic 0
    write_FPGA_NC(dev, NC_DAC_flag_addr, 0x06)
    while True:
        done = read_FPGA_NC(dev, NC_vdac_done_addr)
        if done == 1:
            write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
            write_Gap_Junction(dev, which_neurodyn,
                               0x5C01)  # options for which_neurodyn -- 1, 2, 3, 4; disable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 1, ports 29-31 output logic 0
            time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period
            write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
            #print("DAC Span is configured")
            break
        if (time.time() - tmptime) > 10:
            print("H Check USB connnection or Re-connect USB !")
            break


def write_external_DACs_neurodyn(dev, ch, value, which_neurodyn):
    """
    functional description:
    writes I/V DACs
    """
    # AU: 1/14/23: offset which_neurodyn by 1 to remain uniform indexing of 0-3
    which_neurodyn += 1

    if 0 <= ch <= 15:
        done = 0
        # V_I=ch/8
        addr = ch % 8
        data = calc_dac_values_NC(value)
        command = int(0x300000 + (addr * 0x10000) + data)


        write_FPGA_NC(dev, NC_DAC_V_data_addr, command)
        write_FPGA_NC(dev, NC_DAC_target_addr, 2)  # target = 1 -- nisoc, 2 -- neurodyns
        
        write_Gap_Junction(dev, which_neurodyn,
                           0x5C00)  # options for which_neurodyn -- 1, 2, 3, 4; enable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 0, ports 29-31 output logic 0
        write_FPGA_NC(dev, NC_DAC_flag_addr, 0x02)  # 0x02 will select V DAC

        while True:
            #  print "loop"
            done = read_FPGA_NC(dev, NC_vdac_done_addr)
            if done == 1:
                write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
                # AU: 1/13/23: offset which_neurodyn by 1 to remain uniform indexing of 0-3
                write_Gap_Junction(dev, which_neurodyn,
                                   0x5C01)  # options for which_neurodyn -- 1, 2, 3, 4; disable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 1, ports 29-31 output logic 0
                time.sleep(0.000005)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period
                write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
                #print("DAC" + str(ch) + " is updated")
                break
    else:
        print("Dac Channel 'ch' is wrong!")


def external_DAC_mux_vref_neurodyn(dev, enable, which_neurodyn):
    """
    function will instruct DACs to output REF value on MUXOUT pin
    """
    # AU: 1/14/23: offset which_neurodyn by 1 to remain uniform indexing of 0-3
    which_neurodyn += 1

    #print(enable)
    ref_command = 0xB00019  # 1011 0000 0000 0000 0001 1001
    off_command = 0xB00000  # 1011 0000 0000 0000 0000 0000
    if enable:
        write_FPGA_NC(dev, NC_DAC_V_data_addr, ref_command)
        write_FPGA_NC(dev, NC_DAC_target_addr, 2)  # target = 1 -- nisoc, 2 -- neurodyns
    else:
        write_FPGA_NC(dev, NC_DAC_V_data_addr, off_command)
        write_FPGA_NC(dev, NC_DAC_target_addr, 2)  # target = 1 -- nisoc, 2 -- neurodyns
    write_Gap_Junction(dev, which_neurodyn,
                       0x5C00)  # options for which_neurodyn -- 1, 2, 3, 4; enable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 0, ports 29-31 output logic 0
    write_FPGA_NC(dev, NC_DAC_flag_addr, 0x02)  # 0x02 will select V DAC
    # print "step1"
    while True:
        #print("loop")
        done = read_FPGA_NC(dev, NC_vdac_done_addr)
        if done == 1:
            write_FPGA_NC(dev, NC_DAC_flag_addr, 0x00)
            write_Gap_Junction(dev, which_neurodyn,
                               0x5C01)  # options for which_neurodyn -- 1, 2, 3, 4; disable chip select of 'which_neurodyn' -- port 28 of MAX7301AAX+ outputs logic 1, ports 29-31 output logic 0
            time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 0.5MHz or 2usec period
            write_FPGA_NC(dev, NC_DAC_target_addr, 0x00)
            if enable:
                #print("DAC MUXOUT configured to REF")
                None
            else:
                print("DAC MUXOUT configured to HiZ off")
            break


def write_Gap_Junction(dev, row_number, command):
    """
    functional description:
    writes gap junction
    """

    done = 0
    write_FPGA_NC(dev, GJ_V_data_addr, command)
    write_FPGA_NC(dev, GJ_row_number, row_number)  # select which of the gap junctions to access
    write_FPGA_NC(dev, GJ_flag_addr, 0x02)  # 0x02 will select the gap junction

    while True:
        #  print "loop"
        done = read_FPGA_NC(dev, GJ_done_addr)
        if done == 1:
            write_FPGA_NC(dev, GJ_flag_addr, 0x00)
            time.sleep(0.00001)                                                 # 10usec; this should be enough as gap junction clock is 0.5MHz or 2usec period
            write_FPGA_NC(dev, GJ_row_number, 0x00)
            #print("Gap junction " + str(row_number) + " is updated")
            break


############# functions for neurodyn copied from Jun's/Teddy's python code -- control_4spikes_new_chip.py #########################################

def load_matlab_data(filename):
    data_dict = {}
    loadData = scipy.io.loadmat(filename, data_dict)
    return data_dict


def clear_all_int_dacs(dev, neurodynSel):
    disable = 0
    offData = 0
    sign = 0

    for quadrant in range(4):
        for ifSynapse in range(2):
            for channelNum in range(3):
                for typ in range(4):
                    for bumpNum in range(7):
                        write_int_dac_long(dev, neurodynSel, quadrant, ifSynapse, channelNum, typ, bumpNum, disable,
                                           sign, offData)
                        #print('neurodyn= ' + str(target_neurodyn) + 'quadrant= ' + str(quadrant) + ', ifSynapse= ' + str(
                        #    ifSynapse) + ', channelNum= ' + str(channelNum) + ', typ= ' + str(
                        #    typ) + ', bumNum= ' + str(bumpNum) + ' dacs cleared')


def load_int_dacs(dev, signAlphaBeta, signgErev, biasAlphaBeta, biasgErev, quadrantSel, ifSynapseSel, neurodynSel):
    offData = 0
    disable = 0
    enable = 1

    for channelNumIndex in range(3):
        for ifBetaIndex in range(2):
            sign = signAlphaBeta[quadrantSel, ifSynapseSel, channelNumIndex, ifBetaIndex]
            if sign == -1:
                sign = 0
            for bumpNumIndex in range(7):
                iBiasValue = biasAlphaBeta[quadrantSel, ifSynapseSel, channelNumIndex, ifBetaIndex, bumpNumIndex]
                if iBiasValue == 0:
                    write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, channelNumIndex, ifBetaIndex,
                                       bumpNumIndex,
                                       disable, sign, offData)
                else:
                    write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, channelNumIndex, ifBetaIndex,
                                       bumpNumIndex,
                                       enable, sign, iBiasValue)

        for typ in range(2, 4):  # typ can be 2 and 3
            sign = signgErev[
                quadrantSel, ifSynapseSel, channelNumIndex, typ % 2]  # if typ = 2, then typ % 2 = 0 which means we are trying to access the maximal conductance. For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.
            if sign == -1:
                sign = 0

            # for bumpNumIndex in range(7):
            iBiasValue = biasgErev[
                quadrantSel, ifSynapseSel, channelNumIndex, typ % 2]  # if typ = 2, then typ % 2 = 0 which means we are trying to access the maximal conductance. For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.

            if iBiasValue == 0:
                write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, channelNumIndex, typ, bumpNumIndex,
                                   disable, sign,
                                   offData)
            else:
                write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, channelNumIndex, typ, bumpNumIndex,
                                   enable, sign,
                                   iBiasValue)


def write_int_dac_long(dev, neurodyn, quadrant, ifSynapse, channelNum, typ, bumpNum, enable, sign, data):
    """
    From matlab function OLD:
    writes internal NeuroDyn dac with long address
    addr = 10 bit address
    data = 10 bit data
    """
    
    addr = (quadrant << 8) + (ifSynapse << 7) + (channelNum << 5) + (typ << 3) + bumpNum
    write_int_dac(dev, neurodyn, addr, enable, sign, data)


def write_int_dac(dev, neurodyn, addr, enable, sign, data):
    """
    From matlab function OLD:
    writes internal NeuroDyn dac

    addr = 10 bit address
    data = 10 bit data

    dataMSB is stored in bits 7-4
    """

    # command = 98
    # IFMASK = (1<<4)+(1<<3)

    ifVoltage = bitcheck(addr, 6) == 1 and bitcheck(addr,
                                                    7) == 1  # bitcheck(d,b) returns (d >> (10 - b)) & 1; bitwise AND of d(first 10-b bits discarded) and 0b0...001; basically, bitcheck(addr, 6) checks whether addr4/a4 = 1 and bitcheck(addr, 7) checks whether addr3/a3 = 1; basically if the 'typ' bits are 1
    # addrMSB = addr >> 8                                                         # discard the first 8 bits, addr0...addr7/a0...a7; addrMSB = addr9 addr8/ a9 a8
    # addrLSB = addr & (2 ** 8 - 1)                                               # bitwise operation AND with (2 ** 8 - 1 = 255 = 0b1111 1111); basically the first 8 address bits, addr0...addr7/ a0...a7

    if ifVoltage:
        dataMSB = (sign << 2) + (data >> 8)
    else:
        dataMSB = (sign << 3) + (enable << 2) + (data >> 8)

    dataLSB = data & (
                2 ** 8 - 1)  # bitwise operation AND with (2 ** 8 - 1 = 255 = 0b1111 1111); basically the first 8 data bits, data0...data7/ d0...d7

    data = dataLSB + (dataMSB << 8)

    set_internal_dacs_address(dev, addr, neurodyn)
    set_internal_dacs_data(dev, data)
    set_WR_off(dev)
    set_WR_on(dev, neurodyn)
    set_WR_off(dev)
    

def bitcheck(d, b):
    return (d >> (10 - b)) & 1


def chip_init(dev, neurodynSel):
    set_dac_cal_off_switchrpin_on(dev)
    set_expose_off_probe_off_all_neurodyns(dev) 
    #set_probe_on_expose_off(dev, 0b0100)  # turn probe off for neurodyn 3
    clear_all_int_dacs(dev, neurodynSel)                                        # options -- 0, 1, 2, 3


def load_int_dacs_signbit_leak_channels(dev, signgErev, biasgErev, quadrantSel, ifSynapseSel, neurodynSel):
    offData = 0
    disable = 0
    enable = 1


    #set channel number index (3rd argument) to 2 for leaky channels. Set 4th argument to 3, indicates we are updating reversal potential magnitude and sign 
    sign = signgErev[quadrantSel, ifSynapseSel, 2, 3 % 2]                                      # For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.
    if sign == -1:
        sign = 0

    iBiasValue = biasgErev[quadrantSel, ifSynapseSel, 2, 3 % 2]                                # For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.

    if iBiasValue == 0:
        write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, 2, 3, 0, disable, sign, offData)                                                        # set BumpNumIndex to an arbitrary value between 0-6, say 0
    else:
        write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, 2, 3, 0, enable, sign, iBiasValue)                                                      # set BumpNumIndex to an arbitrary value between 0-6, say 0


def load_int_dacs_signbit_potassium_channels(dev, signgErev, biasgErev, quadrantSel, ifSynapseSel, neurodynSel):
    offData = 0
    disable = 0
    enable = 1


    #set channel number index (3rd argument) to 1 for potassium channels. Set 4th argument to 3, indicates we are updating reversal potential magnitude and sign 
    sign = signgErev[quadrantSel, ifSynapseSel, 1, 3 % 2]                                      # For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.
    if sign == -1:
        sign = 0

    iBiasValue = biasgErev[quadrantSel, ifSynapseSel, 1, 3 % 2]                                # For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.

    if iBiasValue == 0:
        write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, 1, 3, 0, disable, sign, offData)                                                        # set BumpNumIndex to an arbitrary value between 0-6, say 0
    else:
        write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, 1, 3, 0, enable, sign, iBiasValue)                                                      # set BumpNumIndex to an arbitrary value between 0-6, say 0

def load_int_dacs_signbit_sodium_channels(dev, signgErev, biasgErev, quadrantSel, ifSynapseSel, neurodynSel):
    offData = 0
    disable = 0
    enable = 1


    #set channel number index (3rd argument) to 0 for sodium channels. Set 4th argument to 3, indicates we are updating reversal potential magnitude and sign 
    sign = signgErev[quadrantSel, ifSynapseSel, 0, 3 % 2]                                      # For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.
    if sign == -1:
        sign = 0

    iBiasValue = biasgErev[quadrantSel, ifSynapseSel, 0, 3 % 2]                                # For typ = 3, typ % 2 = 1 which means we are accessing the reversal potential.

    if iBiasValue == 0:
        write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, 0, 3, 0, disable, sign, offData)                                                        # set BumpNumIndex to an arbitrary value between 0-6, say 0
    else:
        write_int_dac_long(dev, neurodynSel, quadrantSel, ifSynapseSel, 0, 3, 0, enable, sign, iBiasValue)                