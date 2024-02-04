# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:08:03 2022

@author: isnl
"""

import sys
import visa
import ok
import string
import serial
import struct, os
import tables
import numpy as np
import scipy as sp
import pandas as pd
import openpyxl
import csv
import os
import scipy.io
import operator
import time
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.figure import Figure
from operator import itemgetter                     # for sorting the array by column
from scipy.signal import butter, lfilter, freqz


VREF            = 3.3
DAC_data_addr   = 0x19        # opal kelly's wire in endpoint address for writing data for dacs
DAC_flag_addr   = 0x1A        # opal kelly's wire in endpoint address for flag which specifies the duration over which data is written to dacs
DAC_done_addr   = 0x21        # opal kelly's wire in endpoint address for flag which specifies when the data has been written to dacs


ADC_data_addr   = 0x1C
ADC_program     = 0x1D
ADC_read        = 0x1E
ADC_done_addr   = 0x22
ADC0_data_out   = 0x23
ADC1_data_out   = 0x24


reset_FSM       = 0x00
read_sample     = 0x02


sampling_done   = 0x25
fifo0_dout      = 0x26
fifo1_dout      = 0x27
read_sample_done = 0x28


VP_RRAM         = 0             # DAC Channels 
VN_RRAM         = 1             # DAC Channels 
VREF_RRAM       = 2             # DAC Channels 


path = "C:/Users/Soumil/OneDrive - UC San Diego/research/RRAM PCB/python"
#path = "C:/Users/jains/OneDrive - UC San Diego/research/RRAM PCB/python"

class Object(object):
    pass

class SsRx:
    def __init__(self):
        self.xem = ok.okCFrontPanel()  # create xem7310 object
        #self.xem.bitfile = path + "/pcb_reset_common_clk.bit"  # Location of the bitfile
        self.xem.bitfile = path + "/python/pcb_reset_common_clk.bit"   # Location of the bitfile
        self.xem.OpenBySerial()  # find connected xem7310
        error = self.xem.ConfigureFPGA(self.xem.bitfile)  # load bitfile
        print("Inital FPGA Bit flash complete..")
        print(error)
        return 

    def initDevice(self): # set the SYS_RST
        # self.xem.LoadDefaultPLLConfiguration()
        self.xem.SetWireInValue(0x00,1, 0xffffffff)
        self.xem.UpdateWireIns()
        time.sleep(0.00001) # unit: second
        self.xem.SetWireInValue(0x00,0, 0xffffffff)
        self.xem.UpdateWireIns()
        time.sleep(0.0001)
        self.xem.SetWireInValue(0x00,1,0xffffffff)
        self.xem.UpdateWireIns()
        print("Finish SYS_RST")
        return


dev = SsRx()


def write_FPGA(dev,addr,value): 
    dev.xem.SetWireInValue(addr, value,0xffffffff)
    dev.xem.UpdateWireIns()


def SetWire(dev,addr,value): 
    dev.xem.SetWireInValue(addr, value,0xffffffff)

    
def UpdateWire(dev):
    dev.xem.UpdateWireIns()


def read_FPGA(dev,addr): 
    dev.xem.UpdateWireOuts()
    return dev.xem.GetWireOutValue(addr)


def calc_dac_values(targetV):
    """
    functional description - calculates the DAC digital value to achieve the
    target output voltage
    """
    global VREF
    if targetV == VREF:
        return np.round(2 ** 16 - 1).astype('int')
    else:
        return np.round(targetV / VREF * 2 ** 16).astype('int')


def write_DAC(dev, ch, value):
    """
    functional description:
    writes I/V DACs
    """
    if 0 <= ch <= 8:
        done = 0
        addr = ch % 8
        data = calc_dac_values(value)
        command = int(0x3000000 + (addr * 0x100000) + (data*0x10))
        
        write_FPGA(dev, DAC_data_addr, command)
        write_FPGA(dev, DAC_flag_addr, 0x01)  # 0x01 will select DAC
        
        while True:
            done = read_FPGA(dev, DAC_done_addr)
            if done == 1:
                write_FPGA(dev, DAC_flag_addr, 0x00)
                time.sleep(0.00001)                                                 # 10usec; this should be enough as dac clock is 1MHz or 1usec period. 10 usec will be a wait of 10 clock cycles
                break
    else:
        print("Dac Channel 'ch' is wrong!")
    
    
def write_ADC0(dev, command):

    done = 0  
    write_FPGA(dev, ADC_data_addr, command)
    write_FPGA(dev, ADC_read, 0x00)
    write_FPGA(dev, ADC_program, 0x01)  # 0x01 starts write to ADC0
       
    while True:
        done = read_FPGA(dev, ADC_done_addr)
        if done == 1:
            write_FPGA(dev, ADC_program, 0x00)
            break
    
        
def write_ADC1(dev, command):

    done = 0 
    write_FPGA(dev, ADC_data_addr, command)
    write_FPGA(dev, ADC_read, 0x00)
    write_FPGA(dev, ADC_program, 0x02)  # 0x02 will initiate write to ADC1
        
    while True:
        done = read_FPGA(dev, ADC_done_addr)
        if done == 2:
            write_FPGA(dev, ADC_program, 0x00)
            break 
    
        
def read_ADC0(dev, command, read_reg_type):

    done = 0
    write_FPGA(dev, ADC_data_addr, command)
    write_FPGA(dev, ADC_read, 0x01)
    write_FPGA(dev, ADC_program, 0x01)                      # 0x01 will initiate write to ADC0

    while True:
        done = read_FPGA(dev, ADC_done_addr)
        if done == 1:
            ADC0_out = read_FPGA(dev, ADC0_data_out)
            print ("ADC0 " + str(hex(ADC0_out)))
            write_FPGA(dev, ADC_program, 0x00)
            return hex(ADC0_out)

        
def read_ADC1(dev, command, read_reg_type):

    done = 0
    write_FPGA(dev, ADC_data_addr, command)
    write_FPGA(dev, ADC_read, 0x01)
    write_FPGA(dev, ADC_program, 0x02)                      # 0x02 will initiate write to ADC1

    while True:
        done = read_FPGA(dev, ADC_done_addr)
        if done == 2:
            ADC1_out = read_FPGA(dev, ADC1_data_out)
            print ("ADC1 out" + str(hex(ADC1_out)))
            write_FPGA(dev, ADC_program, 0x00)
            return hex(ADC1_out)

        
def all_switches_off(dev):
    write_FPGA(dev, 0x05, 0x00000000)                       # VPCOLSEL
    write_FPGA(dev, 0x06, 0x00000000)                       # VNCOLSEL
    write_FPGA(dev, 0x07, 0x00000000)                       # VREFCOLSEL
    write_FPGA(dev, 0x08, 0x00000000)                       # ADCCOLSEL
    write_FPGA(dev, 0x09, 0x00000000)                       # VPROWSEL
    write_FPGA(dev, 0x0A, 0x00000000)                       # VNROWSEL
    write_FPGA(dev, 0x0B, 0x00000000)                       # VREFROWSEL 
    