import pyvisa as visa
import ok
import string
import serial, struct, os
import tables
import numpy as np
import scipy as sp
import pandas as pd
import csv
import scipy.io
import operator
import time
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from operator import itemgetter         # for sorting the array by column
from scipy.signal import butter, lfilter, freqz

# LTC 2666 DAC related parameters.
num_channel     = 2
AVDD            = 1.5;            # Analog Supply
#VREF           = 1.8             # NISoC DAC reference 
VREF_nisoc      = 1.71            # NISoC DAC reference (measured).

High_Z_muxout       = 0xb00000    # 1011 0000 0000 0000 0000 0000
VOUT0_muxout        = 0xb00010    # 1011 0000 0000 0000 0001 0000
VOUT1_muxout        = 0xb00011    # 1011 0000 0000 0000 0001 0001
VOUT2_muxout        = 0xb00012    # 1011 0000 0000 0000 0001 0010
VOUT3_muxout        = 0xb00013    # 1011 0000 0000 0000 0001 0011
VOUT4_muxout        = 0xb00014    # 1011 0000 0000 0000 0001 0100
VOUT5_muxout        = 0xb00015    # 1011 0000 0000 0000 0001 0101
VOUT6_muxout        = 0xb00016    # 1011 0000 0000 0000 0001 0110
VOUT7_muxout        = 0xb00017    # 1011 0000 0000 0000 0001 0111
REFLO_muxout        = 0xb00018    # 1011 0000 0000 0000 0001 1000
REF_muxout          = 0xb00019    # 1011 0000 0000 0000 0001 1001
Temp_monitor_muxout = 0xb0001a    # 1011 0000 0000 0000 0001 1010
V_plus_muxout       = 0xb0001b    # 1011 0000 0000 0000 0001 1011
V_minus_muxout      = 0xb0001c    # 1011 0000 0000 0000 0001 1100

#DAC Channels
IVbP_OTA        = 0;
Vinfinimp_bias  = 1;
Vclamp_p        = 2;
Vclamp_n        = 3;
IVbNP_stim      = 4; 
IVbNN_stim      = 5; 
Vref_nisoc      = 6;
All             = -1;

# NISoC related parameters.
TinOn_Disable=0
TVoutOn_Disable=0
TCoutOn_Disable=0
TSlopeOn_Disable=0
TCounterOn_Disable=0
AddrOn_Disable=0
WriteEn_Disable=0
FIFO_Disable=0
DynSarDisable=0

TinOn_Enable=1
TVoutOn_Enable=1
TCoutOn_Enable=1
TSlopeOn_Enable=1
TCounterOn_Enable=1
AddrOn_Enable=1
WriteEn_Enable=1
FIFO_Enable=1
DynSarEnable=1

CurrentClamp_Disable=0
Gain10X_Disable=0
Calibration_Disable=0

CC=1                    # By default, measure voltage
CurrentClamp_Enable=1
Gain10X_Enable=1
Calibration_Enable=1

CDS_Enable=1
CDS_Disable=0
Chip_Command=0x00000000
Fs=25000                # Sampling frequency

EXT_DAC_REF = 1.8;
DAC_bits = 16;

#Vref   =0;             # This should be 1, but channel one for Vref is not connected
#VCM    =2;
#VREFMH =3;
#IVbN_comp=4;
#VREFLH =4;
#VLow   =5;
#VREFL  =5;

Vclamp0 = 6;
Vclamp2 = 7;
VCAS    = 8;
VBN     = 9;

IVbN_slope = 10;          # for NC1
VBPH   =10;
VBPL   =11;

IVbP_stim=13;
IVbN_stim=14;
Test_In =15;

##************for NC1_0, the old PCB
#VLow=1;
#Vclamp0=2; 
#Vclamp2=3;
#Test_In=4;
#SlopeOut=5;
#IVbP_stim=8;
#IVbN_stim=9;
#IVbN_slope=10;
#IVbN_ota=11;
#IVbN_comp=12;
Pg_addr=0;
cds1_addr=1;
cc_rst_addr=2;
vc_rst1_addr=3;
vc_rst2_addr=4;
cc_ota_rst_addr=5;
vc_ota_rst_addr=6;
cds2_addr=7; # added later
BW1_addr=8; # added later
BW2_addr=9; # added later
cc_gate_addr=10; # added later
cdsEN_Notcds_delay=11;
clk_chip_addr=12;
clk_ch_scan_addr=13; # maybe not required
Strobe_addr = 14;
Sample_addr = 15; # same for Load and RST
CONV_addr = 16;
Check_addr = 17;
ReadEn_addr = 18;
WriteEn_addr = 19;
Load_addr = 20;
ColSel_addr = 21;
RowSel_addr = 22;
RST_addr =23;
Ag_addr=24;

FIFO_status_addr=0x22; # read fifo status; when it's 1, data is ready and there're at least 51200 points.

# Opal Kelly related definitions.
class OpalKelly:
    def __init__(self):
        return
      
    def InitializeDevice(self):
        
        ''' 
        self.xem = ok.okCFrontPanel()                        Creates a xem7310 object()  -- DEPRECATED.
        self.xem.OpenBySerial("")                            Finds connected xem7310     -- DEPRECATED.
        FrontPanel SDK version used - 5.3.0
        The older FrontPanel API Python class, okCFrontPanel(), is deprecated; now migrating to FrontPanelDevices().
        See https://library.opalkelly.com/library/FrontPanelAPI/migrate_fpdevices.html
        See a list of deprecated API classes and methods, as of FrontPanel SDK version 5.3.0: https://docs.opalkelly.com/fpsdk/frontpanel-api/support-matrix/
        '''
        devices = ok.FrontPanelDevices()
        deviceCount = devices.GetCount()
        print("Device Count:", deviceCount)
        
        # Open the first device we find.
        self.xem = devices.Open()                                   
        if self.xem == None:                        
            print("ERROR!\nIs the FrontPanelGui open and connected to the board? Please close the GUI and rerun!")
            return(False)
        else:
            print("                  Device Open:", self.xem.IsOpen())

            # Get some general information about the device.
            info = ok.okTDeviceInfo() 
            self.xem.GetDeviceInfo(info)                            # Populates the info of okTDeviceInfo class -- https://library.opalkelly.com/library/FrontPanelAPI/structokTDeviceInfo.html#details
            print("                      Product: " + info.productName)
            print("             Firmware version: %d.%d" % (info.deviceMajorVersion, info.deviceMinorVersion))
            print("                Serial Number: %s" % info.serialNumber)
            print("                    Device ID: %s" % info.deviceID)
            print("                    USB speed: USB %d" % info.usbSpeed + ".0")
            print(" Configures from System Flash: %s" % info.configuresFromSystemFlash)      
            if info.isPLL22150Supported == True:                    # USB 3.0 methods seem to not support PLLs. See the supported API classes and methods: https://docs.opalkelly.com/fpsdk/frontpanel-api/support-matrix/
                print("Device contains a Cypress CY22150 PLL.")
                self.xem.LoadDefaultPLLConfiguration()
            else:
                print("Device does not contain Cypress CY22150 PLL.")
            if info.isPLL22393Supported == True:
                print("Device contains a Cypress CY22393 PLL.")
                self.xem.LoadDefaultPLLConfiguration()
            else:
                print("Device does not contain Cypress CY22393 PLL.")
                
        return(True) 

    def loadBitFile(self, BIT_FILE_PATH):
        error = self.xem.ConfigureFPGA(BIT_FILE_PATH)               # load bitfile
        if error == 0:
            print("Successfully configured FPGA!")
        else:
            print("FPGA configuration error...")
            print("Error Code: ", error)

    def initDevice(self):               # set the SYS_RST
        #self.xem.ResetFPGA()                               # Not supported by USB 3.0 devices. See: https://docs.opalkelly.com/fpsdk/frontpanel-api/support-matrix/
        print("Finish SYS_RST")
        return

FPGA = OpalKelly()
if not FPGA.InitializeDevice():
    exit(-1)
    
def Lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)   
    y = lfilter(b, a, data)
    return y

def Highpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)   
    y = lfilter(b, a, data)
    return y

def Notch_Filter(data,fs=5e3, band=4, freq2remove=60,ripple=6, order=6, filter_type='butter'):
    from scipy.signal import iirfilter
    nyq  = fs/2.0
    low  = freq2remove - band/2.0
    high = freq2remove + band/2.0
    normal_low  = low/nyq
    normal_high = high/nyq
    b, a = iirfilter(order, [normal_low, normal_high], rp=ripple, btype='bandstop',
                     analog=False, ftype=filter_type)
    filtered_data = lfilter(b, a, data)
    return filtered_data

def SRS_Set(AMPL,FREQ,OFFS):
    AMPL = "AMPL " + str(AMPL/2) + "VP"
    FREQ = "FREQ "+ str(FREQ)
    OFFS = "OFFS " + str(OFFS/2)
    rm = visa.ResourceManager()
    my_SRS = rm.open_resource('GPIB0::8::INSTR')
    my_SRS.write('OUTE 0')
    my_SRS.write('FUNC 0')
    my_SRS.write(AMPL)
    my_SRS.write(FREQ)
    my_SRS.write(OFFS)
    my_SRS.write('OUTE 1')
    my_SRS.close

def write_WireIn(FPGA,addr,value):
    FPGA.xem.SetWireInValue(addr, value, 0xffffffff)
    FPGA.xem.UpdateWireIns()

def read_WireOut(FPGA,addr):
    FPGA.xem.UpdateWireOuts()
    return FPGA.xem.GetWireOutValue(addr)
   
def activate_TriggerIn(FPGA, addr, bit):
    FPGA.xem.ActivateTriggerIn(addr, bit)                           # Trigger a specific bit (second argument) at the TriggerIn endpoint address (first argument).
    
def check_TriggerOut(FPGA, addr, mask):
    FPGA.xem.UpdateTriggerOuts()
    return FPGA.xem.IsTriggered(addr, mask)                         # Check if a particular bit (or bits) on a particular TriggerOut endpoint has triggered since the last call to UpdateTriggerOuts().
    # FPGA.xem.IsTriggered(0x71, 0x80)                              # Example usage - Returns true if bit 7 of endpoint 0x71 has triggered.

def write_PipeIn(FPGA, addr, data):
    buf = bytearray(data)
    FPGA.xem.WriteToPipeIn(addr, buf)                               # Method transfers a specified buffer of data to the given Pipe In endpoint. 
    '''
    Within Python, the 'length' parameter is not used and the 'data' parameter is of the mutable type bytearray. For example, (https://library.opalkelly.com/library/FrontPanelAPI/classokCFrontPanel.html)
    buf = bytearray(81920)
    xem.WriteToPipeIn(0x80, buf)
    '''
    
def read_PipeOut(FPGA, addr, length):
    buf = bytearray([0]*4*length)                                   # should be multiple of 16, datain is 4*8-bit = 32-bit number
    error_code=FPGA.xem.ReadFromPipeOut(addr, buf)                  # Method tranfers data from a specified Pipe Out endpoint to the given buffer.
    if (error_code<0):
        print('Read failed. Check error code '+str(error_code)+' from https://docs.opalkelly.com/fpsdk/frontpanel-api/error-codes/')
    else:
        print('number of bytes read: '+str(error_code))
    return buf
    '''    
    Within Python, the 'length' parameter is not used and the 'data' parameter is of the mutable type bytearray. For example,
    buf = bytearray(15360)
    xem.ReadFromPipeOut(0x0a, buf)
    '''
    
def write_BlockPipeIn(FPGA, addr, blocksize, data):
    buf = bytearray(data)                               
    FPGA.xem.WriteToBlockPipeIn(addr, blocksize, buf)               # Method transfers a specified buffer of data to the given BlockPipeIn endpoint. 
    '''
    Block size is specified in bytes and can be a power of two [16... 16384] for a USB 3.0 SuperSpeed device.
    Within Python, the 'length' parameter is not used and the 'data' parameter is of the mutable type bytearray. For example,
    buf = bytearray(4096)
    xem.ReadFromPipeOut(0x80, 512, buf)
    '''
    
def read_BlockPipeOut(FPGA, addr, blocksize, length):
    buf = bytearray([0]*4*length)                                   # Initialise a buffer for the expected length of data from the Block Pipe Out endpoint.It should be multiple of 16, datain is 4*8-bit = 32-bit number.
    return FPGA.xem.ReadFromBlockPipeOut(addr, blocksize, buf)      # Method transfers data from a specified BlockPipeOut endpoint to the given buffer. 
    '''
    Block size is specified in bytes and can be a power of two [16... 16384] for a USB 3.0 SuperSpeed device.
    Performance Note: Optimum bandwidth performance is achieved when blocksize is a power of two.
    Within Python, the 'length' parameter is not used and the 'data' parameter is of the mutable type bytearray. For example,
    buf = bytearray(81920)
    xem.ReadFromPipeOut(0xa0, 1024, buf)
    '''

def clock_set(FPGA, ch, delaytime, lowtime, hightime, pulsemax, stoptime):
    FPGA.xem.SetWireInValue(0x02, ch)
    FPGA.xem.SetWireInValue(0x03, delaytime)
    FPGA.xem.SetWireInValue(0x04, lowtime)
    FPGA.xem.SetWireInValue(0x05, hightime)
    FPGA.xem.SetWireInValue(0x06, pulsemax)
    FPGA.xem.SetWireInValue(0x07, stoptime)
    FPGA.xem.UpdateWireIns()
    
def pulse_set(FPGA, ch, delaytime, hightime):
    FPGA.xem.SetWireInValue(0x02, ch)
    FPGA.xem.SetWireInValue(0x03, delaytime)
    FPGA.xem.SetWireInValue(0x05, hightime)
    FPGA.xem.UpdateWireIns()

def init_Bias(FPGA):
    write_DAC_nisoc(FPGA,VLow,(AVDD-1.0)/2.0) # get 1V range
    write_DAC_nisoc(FPGA,IVbN_slope,AVDD - 0.526) # experimental value
    write_DAC_nisoc(FPGA,Vref,AVDD/2.0)      
    write_DAC_nisoc(FPGA,Vclamp0,AVDD/2.0-0.1)
    write_DAC_nisoc(FPGA,Vclamp2,AVDD/2.0+0.1)
    write_DAC_nisoc(FPGA,IVbN_stim,0.341) # experimental value
    write_DAC_nisoc(FPGA,IVbP_stim,0.35) # experimental value
    write_DAC_nisoc(FPGA,IVbN_ota,0.38) # experimental value
    write_DAC_nisoc(FPGA,IVbN_comp,0.42) # experimental value    
    
'''
LTC2666 DAC configuration:
Config Reference: 0111 0000 0000 0000 0000 0001              [0]: Setting bit 1 in the configuration command enables the use of an external reference voltage applied at REF (pin 25) by activating the RD bit.
Write Span to all channels: 1110 0000 0000 0000 0000         [2:0]: 000 specify the output range from 0 to 2Vref (external reference used here).
'''
def init_DAC_nisoc(FPGA, lowtime, hightime, pulsemax):
    write_WireIn(FPGA, 0x02, 18)
    write_WireIn(FPGA, 0x04, lowtime)
    write_WireIn(FPGA, 0x05, hightime)
    write_WireIn(FPGA, 0x06, pulsemax)
    write_WireIn(FPGA, 0x08, 0x700001)                       # Config reference.
    activate_TriggerIn(FPGA, 0x42, 0)                        # Trigger DAC FSM within Verilog HDL.
    time.sleep(1)
    write_WireIn(FPGA, 0x08, 0xe00000)                       # write span.
    activate_TriggerIn(FPGA, 0x42, 0)                        # Trigger DAC FSM within Verilog HDL.
    
def calc_DAC_value(targetV):
    """
    functional description - calculates the DAC digital value to achieve the
    target output voltage
    """
    global VREF_nisoc
    return(np.round(targetV / (VREF_nisoc * 2.0) * 2 ** 16).astype('int'))

def write_DAC_nisoc(FPGA, addr, value):
    """
    functional description:
    writes Voltage DAC LTC2666.
    """
    if 0 <= addr <= 7:
        data = calc_DAC_value(value)
        command = int(0x300000 + (addr * 0x10000) + data)        # command[23:20]=0x30 writes the code to DAC with address 'addr' and only updates that specific DAC.
        write_WireIn(FPGA, 0x08, command)
        activate_TriggerIn(FPGA, 0x42, 0)                        # Trigger DAC FSM inside the FPGA to start communication over SPI.
    else:
        print("Dac address 'addr' is wrong!")
        
def DAC_muxout_nisoc(FPGA, muxout):
    """
    Function will instruct the LTC2666 DAC to output the specified device voltage on MUXOUT pin.
    """    
    write_WireIn(FPGA, 0x08, muxout)
    activate_TriggerIn(FPGA, 0x42, 0)                        # Trigger DAC FSM.


def power_down_DAC_nisoc(FPGA, addr):
    """
    Power down a splecific DAC with address, 'addr', or power down the whole chip. 
    """
    pdn_command = int(0x400000 + (addr * 0x10000))               # Power down a specific DAC with address 'addr'. A subsequent update command to the specific DAC will result in a power-up delay time of 30us.
    pdn_all_command = 0x500000                                   # Power down chip (all DACs, Mux and Reference). A subsequent update command to the DAC will result in a power-up delay time of 35us.
    if addr<0:
        write_WireIn(FPGA, 0x08, pdn_all_command)
        activate_TriggerIn(FPGA, 0x42, 0)                        # Trigger DAC FSM.
    else:
        write_WireIn(FPGA, 0x08, pdn_command)
        activate_TriggerIn(FPGA, 0x42, 0)                        # Trigger DAC FSM.
        
'''
Function definitions from old Akshay's code.
'''        
def data_recording(FPGA,datalenth,av_len,plot_len,if_savedata,savepath):
    global CC, num_channel

    #datalenth=51200
    datain=bytearray([0]*4*datalenth) #should be multiple of 16, datain is 4*8-bit =32-bit number
    pipedata_len=FPGA.xem.ReadFromPipeOut(0xA0,datain)
    datain=np.reshape(datain,(-1,4))  
#%    
    datain=datain[:,0:3] 
    datain=datain.astype(np.uint16)
    datain[:,1]=datain[:,0]+(datain[:,1]%4)*256
    datain=datain[:,1:3]
#%
    datain=np.array(sorted(datain,key=itemgetter(1)))
#%
    data_con=datain[:,0]
    data_con=np.reshape(data_con,(256,-1))
    data_converted=data_con.T
#%  
    #plt.imshow(np.arange(len(data_con[0])),data_con[0])

    if CC==1:
        x=np.arange(0,pipedata_len/4)*1/25000.0 
        with open(savepath, "a") as f:
            writer = csv.writer(f)
            for i in range(len(data_converted)):
                writer.writerow(data_converted[i])   
                    
        for i in range(len(data_con)):
            plt.plot(data_con[i],linewidth=0.1)
        plt.show()

        return data_con
    elif CC==0:
        av_len=1
        current=np.zeros(pipedata_len/8)
        current=(measure[0::2]-measure[1::2])*1 #unit pA
        current_average=np.zeros(len(current)/av_len)
        for j in range (0,len(current)/av_len):
            current_average[j]=sum(current[j*av_len:(j+1)*av_len])/av_len
        #x_raw=np.arange(0,pipedata_len/4)*1/1000.0     
        x=np.arange(0,pipedata_len/(8*av_len))*av_len/1000.0    
        #x1=np.arange(0,pipedata_len/(4*av_len))*av_len/1000.0   
        plt.close()        
        plt.figure()
        plt.plot(x[0:plot_len],current_average[0:plot_len])
        plt.grid()
        #plt.plot(x,current)
        plt.xlabel('time (s)')
        plt.ylabel('current(pA)')
        plt.show()
    else:
        print("Please make sure measurement mode is set!")

def Data_Read_USB(FPGA=FPGA,filename='./Data/default.h5',recordingtime=8):    
    columns = 4
    datalenth=51200 # fixed by 'program almost full' of FIFO defined in FPGA
    fhandle = tables.open_file(filename, "a")
    #fhandle.close()
    data_temp = fhandle.create_earray(fhandle.root, "data", tables.UInt8Atom(), shape=(0, columns))
    #data_temp = fhandle.root.data
    time_index=0
    
    write_WireIn(FPGA,0x0b,1)# FIFO_disable/clear up
    time.sleep(0.1) #wait until stable
    write_WireIn(FPGA,0x0b,0) # FIFO_enable/start filling
    start_time = time.time() 
    while True:
        fifo_status=read_WireOut(FPGA, FIFO_status_addr)
        if (fifo_status):
            time_index=time_index+1
            dataUSB=bytearray([0]*4*datalenth) #should be multiple of 16, datain is 4*8-bit =32-bit number   
            pipedata_len=FPGA.xem.ReadFromPipeOut(0xA0,dataUSB)
            dataUSB=np.reshape(dataUSB,(-1,4))
            #dataUSB=dataUSB[:,0:3] # the 3rd column is empty
            data_temp.append(dataUSB)
            #print (time_index)
            #start_time = time.time() # clear timer
        if time_index > recordingtime-1:
            time_index=0
            print ("Reading is done !")
            break
        # if time.time()-start_time > 20: # if after 20 seconds, there is still less than 51200 data points in FIFO, then claim timeout and break
        #     print ("Time is out! No enough data in FIFO!")
        #     break
    fhandle.close()

def Digi_CDS (datapath,process_len, plt_len, Fs, RST_len, CDS_len):  
    if (process_len%RST_len!=0):
        print (process_len%RST_len)
        print("process_len should be multiple of 250!")
    measure=np.loadtxt(datapath,delimiter=",")
    measure=measure.ravel()
    N=len(measure)
    if (process_len > N):
        print("ask too many data to process!")
    
    print(N)
    print(measure.shape)
    co_measure = np.ones(process_len+2)
    co_measure[0:2] = measure[RST_len-3] # fill the missed first two data
    co_measure[2:process_len+2] = measure[0:process_len]
    co_measure = co_measure[0:process_len] # remove the last two extra data

    t =np.arange(0,N*1.0/Fs,1.0/Fs)
    plt.figure(1)
    plt.subplot(2,1,1)
    plt.plot(t[0:plt_len],co_measure[0:plt_len],'*')
    plt.grid()
    plt.title('Before CDS Correction')
    #plt.xlabel('Time $(s)$')
    plt.ylabel('Binary Code')
    plt.show()

    for i in range(process_len/RST_len): # RST_len means how many data points in one CDS cycle
        cds_first  = co_measure[i*RST_len+ CDS_len/2 -1] #last CDS point of beginning CDS
        cds_second = co_measure[i*RST_len+RST_len-1] # last CDS point of ending CDS  
        cds_inter_array = np.linspace(cds_first,cds_second,RST_len-CDS_len/2) # exclude first half of points 
        #substracte reference
        co_measure[i*RST_len + CDS_len/2:i*RST_len+RST_len] = co_measure[i*RST_len+ CDS_len/2:i*RST_len+RST_len] - cds_inter_array
        if i==0:
            co_measure[i*RST_len : i*RST_len + CDS_len/2+1]=co_measure[i*RST_len + CDS_len/2+1] #replace first half of CDS with 
        elif i<process_len/RST_len:
            co_measure[i*RST_len - CDS_len/2 -1 : i*RST_len + CDS_len/2+1]= \
            np.linspace(co_measure[i*RST_len - CDS_len/2-1],co_measure[i*RST_len + CDS_len/2+1], CDS_len +2) #two lines
        if i== process_len/RST_len -1 :
            co_measure[i*RST_len + RST_len- CDS_len/2 :i*RST_len + RST_len]=co_measure[i*RST_len + RST_len-CDS_len/2 -1]

    plt_co_len = plt_len
    #plt.figure(2)
    plt.subplot(2,1,2)
    plt.plot(t[0:plt_co_len],co_measure[0:plt_co_len],'*')
    plt.grid()
    plt.title('After CDS Correction')
    plt.xlabel('Time $(s)$')
    plt.ylabel('Voltage ($mV$)')
    plt.show()
    return co_measure
    
def Config_Clocks(FPGA=FPGA,CC=1,CDS_En=0,CDS_Freq=100,CDS_Len=2,OTA_RST_Freq=100,OTA_RST_Time=10,Bandwidth=-3,Tsamp_cc=50000,Tramp=2046,Tsamp_vc=100000): 
    write_WireIn(FPGA,0x09,0) # start=1, stop=0
    clock_set(FPGA,Pg_addr,0,000,5000)
    time.sleep(0.01)
    high_time = int(Tsamp_cc/100*(CDS_Len/2.0+CDS_Len/2.0*(CDS_Len==1)))*CDS_En # unit= 1us
    low_time = int(1e6/CDS_Freq-Tsamp_cc/100*(CDS_Len/2.0+CDS_Len/2.0*(CDS_Len==1)))
    delay_time = -(int(1e6/CDS_Freq-Tsamp_cc/100*(CDS_Len/2.0+CDS_Len/2.0*(CDS_Len==1))))
    clock_set(FPGA,cds1_addr,delay_time,low_time,CC*high_time*(CDS_Len>1)) # unit is 1us, if CDS<=1, this one will be disabled
    #clock_set(FPGA,cds1_addr,-9880,9980,120)# unit is 1us
    time.sleep(0.01)
    clock_set(FPGA,cc_rst_addr,0,int(Tsamp_cc-Tramp),int(Tramp)*CC) #  unit is 10ns
    time.sleep(0.01)
    clock_set(FPGA,vc_rst1_addr,94000,int(Tsamp_vc-Tramp),int(Tramp)*(1-CC)) #  unit is 10ns 
    time.sleep(0.01)
    clock_set(FPGA,vc_rst2_addr,34000,int(Tsamp_vc-Tramp),int(Tramp)*(1-CC))#  unit is 10ns, 98000
    time.sleep(0.01)
    #clock_set(FPGA,cc_ota_rst_addr,-int(1e6/OTA_RST_Freq-OTA_RST_Time),int(1e6/OTA_RST_Freq-OTA_RST_Time),OTA_RST_Time)
    clock_set(FPGA,cc_ota_rst_addr,-int(Tsamp_cc/100-OTA_RST_Time-3),int(1e6/OTA_RST_Freq-OTA_RST_Time),OTA_RST_Time*CC)
    time.sleep(0.01)
    clock_set(FPGA,vc_ota_rst_addr,int(Tsamp_vc/100-110),500,int(Tsamp_vc/100-500)*(1-CC))
    time.sleep(0.01)
    
    clock_set(FPGA,cds2_addr,0,low_time,CC*high_time)
    time.sleep(0.05)
    write_WireIn(FPGA,0x04,1-CC) #When CC=1,CC_Notcds is delayed opposite of CDS; when CC=0,in VC mode, it is always off.
    
## bandwidth setting: 3 means widest bandwidth, no BW switch on; 2 means only BW1 on;    
## 1 means only BW2 on; 0 means both are on; all of them off during CDS!!!    
    low_time1 = int(CDS_Len*Tsamp_cc/100)
    low_time2 = low_time1       
    delay_time = -int(Tsamp_cc/100*CDS_Len/2.0)
    if Bandwidth ==3:
        high_time1 = 0
        high_time2 = 0
    elif Bandwidth ==2:
        high_time1 = int(1e6/CDS_Freq-low_time1)
        high_time2 = 0
    elif Bandwidth ==1:
        high_time1 = 0
        high_time2 = int(1e6/CDS_Freq-low_time2)
    elif Bandwidth ==0:
        high_time1 = int(1e6/CDS_Freq-low_time1)
        high_time2 = int(1e6/CDS_Freq-low_time2)
    elif Bandwidth ==-1:
        low_time1 = 0
        high_time1 = int(1e6/CDS_Freq-low_time1)
        high_time2 = int(1e6/CDS_Freq-low_time2)
    elif Bandwidth ==-2:
        low_time2 = 0
        high_time1 = int(1e6/CDS_Freq-low_time1)
        high_time2 = int(1e6/CDS_Freq-low_time2)
    elif Bandwidth ==-3:
        delay_time = 0
        low_time1 = 0
        low_time2 = 0
        high_time1 = int(1e6/CDS_Freq-low_time1)
        high_time2 = int(1e6/CDS_Freq-low_time2)
    clock_set(FPGA,BW1_addr, delay_time, low_time1, high_time1)
    time.sleep(0.01)
    clock_set(FPGA,BW2_addr, delay_time, low_time2, high_time2)
    time.sleep(0.01)
    clock_set(FPGA,cc_gate_addr,0,10*(1-CC),10*CC) 
    time.sleep(0.01)
    clock_set(FPGA,clk_chip_addr,0,1,1)
    time.sleep(0.01)
    clock_set(FPGA,clk_ch_scan_addr,0,140,140)# 0,70,70
    time.sleep(0.01)
    write_WireIn(FPGA,0x09,1) # start=1, stop=0

def Config_Control_Signals(FPGA=FPGA,TinOn=1, TVoutOn=1, InfOvrOn=0, OVERIDE=0, OverflowEn=0, ConfigOn=1, WriteEn=0,Pg=0, Ag=0, Al_IN=0, Pl_IN=0, InfRSTb=1,EXT_RES=1, EXT_STAYB=1):
    Chip_Command=(TinOn*2**3 + TVoutOn*2**4 + InfOvrOn*2**5 + OVERIDE*2**6 + OverflowEn*2**7
                    + ConfigOn*2**8 + WriteEn*2**11 + Pg*2**13 
                    + Ag*2**14 + Al_IN*2**15 + Pl_IN*2**16 + InfRSTb*2**19 + EXT_RES*2**20 + EXT_STAYB*2**21)     # 1*2^3 = 8; 16;  256;  524,288; 1,048,576; 2,097,152; total= 3,670,296
    write_WireIn(FPGA,0x00,Chip_Command)  # ok, address, MSBtoLSB: 0011 1000 0000 0001 0001 1000
                                                            #   
def Config_Mode(CurrentClamp=1,Gain10X=0):    
    if CurrentClamp==1:
        CC_mode=1
    else:
        CC_mode=0
    write_WireIn(FPGA,0x06,CC_mode) # configure FPGA CC
    write_WireIn(FPGA,0x07,Gain10X)# CC gainx10        
    #write_WireIn(FPGA,0x08,Gain10X)# VC gainx10
    Config_Clocks(CC=CC_mode,CDS_En=CC_mode*Gain10X,CDS_Freq=100,CDS_Len=2,OTA_RST_Freq=100,OTA_RST_Time=10,Bandwidth=-3,Tsamp_cc=50000,Tramp=2046,Tsamp_vc=100000)
    Restart_Clocks()#restart Clocks
      
def Restart_Clocks(FPGA=FPGA):
    write_WireIn(FPGA,0x09,0) # start=1, stop=0
    time.sleep(0.01) # approximately
    write_WireIn(FPGA,0x09,1) # start=1, stop=0

def Select_Channel(FPGA,start_col=0,end_col=31,start_row=0,end_row=31):
    if start_col>=0 and end_col<=31 and start_col<=end_col and start_row>=0 and end_row<=31 and start_row<=end_row:
        write_WireIn(FPGA,0x03,start_col + end_col*32 + 1024*(start_row + end_row*32))
    else:
        print("Channel input is not correct!")

def Config_Slope(FPGA,StartPoint,VpBias):
    write_DACs(FPGA,VLow,StartPoint)
    write_DACs(FPGA,IVbN_slope,VpBias)  

def TURN_ON_CURRENT_STIM(FPGA=FPGA,start_ch=0,end_ch=255,Pg=1, Ag=1, Al_IN=1, Pl_IN=1):    
    write_WireIn(FPGA,0x0b,1)
    time.sleep(0.01)
    for channel in range(start_ch,end_ch+1):
        Select_Channel(channel,channel)
        time.sleep(0.001) 
        Config_Control_Signals(TinOn_Disable, TVoutOn_Disable, TCoutOn_Disable, TSlopeOn_Disable, TCounterOn_Disable, AddrOn_Enable, WriteEn_Enable,Pg, Ag, Al_IN, Pl_IN)
        time.sleep(0.001)
    Config_Control_Signals(TinOn_Disable, TVoutOn_Disable, TCoutOn_Disable, TSlopeOn_Disable, TCounterOn_Disable, AddrOn_Disable, WriteEn_Enable,Pg, Ag, Al_IN, Pl_IN)
    time.sleep(0.01)
    write_WireIn(FPGA,0x0b,0) # start=1, stop=0

#% Turn off current stimualtion of Channels
def Turn_OFF_CURRENT_STIM(FPGA=FPGA, start_ch=0,end_ch=255): 
    write_WireIn(FPGA,0x0b,1) # start=1, stop=0
    Config_Control_Signals(TinOn_Disable, TVoutOn_Disable, TCoutOn_Disable, TSlopeOn_Disable, TCounterOn_Disable, AddrOn_Enable, WriteEn_Enable,0,0,0,0 )
    time.sleep(0.01) 
    for channel in range(start_ch,end_ch+1):
        Select_Channel(channel,channel)
        time.sleep(0.01)  
        
    Config_Control_Signals(TinOn_Disable, TVoutOn_Disable, TCoutOn_Disable, TSlopeOn_Disable, TCounterOn_Disable, AddrOn_Disable, WriteEn_Enable,0,0,0,0 )    
    write_WireIn(FPGA,0x0b,0) # start=1, stop=0    

#% Measure Current in VC mode
def CURRENT_MEAS(FPGA=FPGA,start_ch=0,end_ch=255,datalenth=2000,skip_len=500, av_len=5, scale=100.0,middle=511.5):
    data_dict_average={}
    #Turn_OFF_CURRENT_STIM(FPGA,0,255)
    for i in range(256):
        data_dict_average[i]=[]
    for channel in range(start_ch,end_ch+1):
        #Turn_OFF_CURRENT_STIM(FPGA,0,255)
        #print channel
        #TURN_ON_CURRENT_STIM(FPGA=FPGA,start_ch=channel,end_ch=channel, Pg=1, Ag=0, Al_IN=0, Pl_IN=1)  
        Select_Channel(channel,channel)
        Restart_Clocks()
        time.sleep(datalenth/2000)  #sampling=1K Hz, but every sample has two data point
        data_dict={}
        for i in range(256):
            data_dict[i]=[]
        datain=bytearray([0]*4*datalenth) #should be multiple of 16, datain is 4*8-bit =32-bit number   
        pipedata_len=FPGA.xem.ReadFromPipeOut(0xA0,datain)
        datain=np.reshape(datain,(-1,4))      
        datain=datain.astype(np.uint16)
        first_flag=(datain[:,1]>>4)&0b1
        datain[:,3]=first_flag
        datain[:,1]=datain[:,0]+(datain[:,1]%4)*256  
        datain=datain[:,1:4]
        
        if first_flag[0]==0:
            datain=datain[1:-1,1:4] #remove first and last data point to align data
        else:
            datain=datain[2::,1:4] #remove first two points to align data
        
        for i in range(len(datain)):
            #data_dict[datain[i][1]].append((datain[i][0]-middle)/scale+datain[i][1]+middle/scale) # scale and shift
            data_dict[datain[i][1]].append((datain[i][0]))
            ##data_dict[datain[i][1]].append(datain[i][2])
        for i in range(channel,channel+1,1):
            data_dict[i]=(np.asarray(data_dict[i][0::2],dtype = np.int64)-np.asarray(data_dict[i][1::2],dtype = np.int64))*1
            for j in range (0,(len(data_dict[i])-skip_len)/av_len):
                data_dict_average[i].append(sum(data_dict[i][j*av_len+skip_len:(j+1)*av_len+skip_len])/av_len)
        #print data_dict_average         
    
    return data_dict_average

#    fig = plt.figure()
#    fig.patch.set_alpha(0.1)
#    ax = fig.add_subplot(111)
#    ax.patch.set_alpha(0.0)
#    plt.tight_layout()    
#    #ax.patch.set_facecolor('white')
#    for i in range(0,256,1):
#        ax.plot(data_dict_average[i],linewidth=0.2,color='black')
#    plt.draw()    
#    df=pd.DataFrame.from_dict(data_dict_average, orient='index')
#    #df=pd.DataFrame(data_dict_average)
#    df.to_csv(savepath)
    
#% Measure Voltage in CC mode    
def VOLTAGE_MEAS(FPGA=FPGA,start_ch=0,end_ch=255,datalenth=65536,skip_len=500, av_len=5, scale=100.0,middle=511.5):

    Select_Channel(start_ch,end_ch)
    #Restart_Clocks()
    #middle=511.5
    datain=bytearray([0]*4*datalenth) #should be multiple of 16, datain is 4*8-bit =32-bit number   
    pipedata_len=FPGA.xem.ReadFromPipeOut(0xA0,datain)
    datain=np.reshape(datain,(-1,4))      
    #datain=datain[:,0:3] 
    datain=datain.astype(np.uint16)
    
    cds_flag=(datain[:,1]>>2)&0b1
    datain[:,3]=cds_flag
    datain[:,1]=datain[:,0]+(datain[:,1]%4)*256  
    datain=datain[:,1:4]   
    #ax.patch.set_facecolor('white')
    data_dict={}
    for i in range(256):
        data_dict[i]=[]
    for i in range(len(datain)):
        #data_dict[datain[i][1]].append((datain[i][0]-middle)/scale+datain[i][1]+middle/scale) # scale and shift
        data_dict[datain[i][1]].append((datain[i][0]-middle))       

    return data_dict
    
#% For VC Calibration
def VC_Calibration():
    
    CC=1
    Config_Mode(CC, Gain10X_Enable, Calibration_Disable)
    Restart_Clocks()#% Clocks Start/Stop
    CC=0
    OTA_RST_Time = 10
    OTA_RST_Freq = 100
    clock_set(FPGA,cc_rst_addr,0,int(Tsamp_cc-Tramp),int(Tramp)*CC) #  unit is 10ns
    time.sleep(0.01)
    clock_set(FPGA,vc_rst1_addr,94000,int(Tsamp_vc-Tramp),int(Tramp)*(1-CC)) #  unit is 10ns 
    time.sleep(0.01)
    clock_set(FPGA,vc_rst2_addr,98000,int(Tsamp_vc-Tramp),int(Tramp)*(1-CC))#  unit is 10ns
    time.sleep(0.01)
    #clock_set(FPGA,cc_ota_rst_addr,-int(1e6/OTA_RST_Freq-OTA_RST_Time),int(1e6/OTA_RST_Freq-OTA_RST_Time),OTA_RST_Time)
    clock_set(FPGA,cc_ota_rst_addr,-int(Tsamp_cc/100-OTA_RST_Time-3),int(1e6/OTA_RST_Freq-OTA_RST_Time)*CC,OTA_RST_Time)
    time.sleep(0.01)
    clock_set(FPGA,vc_ota_rst_addr,int(Tsamp_vc/100-100),100,int(Tsamp_vc/100-100))
    time.sleep(0.01)    
    write_WireIn(FPGA,0x04,1) # turn off Not_CDS
    time.sleep(0.01)
    clock_set(FPGA,cds1_addr,0,10,0) # turn on CDS
    time.sleep(0.01)
    clock_set(FPGA,cc_gate_addr,0,10,0)
    time.sleep(0.01)
    
    clock_set(FPGA,Pg_addr,0,50000,0000) # to control the polarity of current
    
    Restart_Clocks()#% Clocks Start/Stop    
#%   
def CC_Calibration(Gain10X_Enable=Gain10X_Enable):
    CC=1
    Config_Mode(CC, Gain10X_Disable, Calibration_Disable)
    clock_set(FPGA,cds1_addr,0,0,10) # turn on CDS
    Restart_Clocks()#% Clocks Start/Stop    
