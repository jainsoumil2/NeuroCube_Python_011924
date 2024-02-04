# -*- coding: utf-8 -*-
"""
Created by Jun Wang on July 17 2018

"""
#%% FPGA code loading
from nc import *

#%% main

if __name__ == '__main__':
#Initialization
    #dev = ok.okCFrontPanel()
    deviceCount = dev.GetDeviceCount()
    #dev.OpenBySerial("")
    error=dev.OpenBySerial("")
    if error==0:
        print 'FPGA is connected.'
    else:
        print 'Please Connect FPGA!'
    #error = dev.ConfigureFPGA("//mcisn.ucsd.edu/jun/FPGA/NeuroChannel/NeuroChannel2_FPGA/NeuroChannel2.bit")
    #error = dev.ConfigureFPGA("//mcisn.ucsd.edu/jun/FPGA/NeuroChannel/NeuroChannel2_FPGA (copy)_20190805/NeuroChannel2.bit")
    error = dev.ConfigureFPGA("NeuroChannel2.bit")
    if error==0:
        print 'FPGA is configured.'
    else:
        print 'Configuration of FPGA is failed!'

#%   
    init_DACs(dev)
    #write_FPGA(dev,0x04,0)#calibration on/off=1/0
#% Bias voltage configuration     
    init_Bias(dev)
    clock_set(dev,cc_ota_rst_addr,0,0,10)
    Config_Mode(CurrentClamp=1,Gain10X=0)
    clock_set(dev,Pg_addr,0,100,00)
#%# Clocks setting    
    #Config_Clocks(1,CDS_Disable,100,2,100,10,0,50000,2046,100000) # para:CDS_Enable/Disable,CDS_Freq, CDS_Len{ >=1}, Bandwidth level{3,2,1,0}
#    Config_Control_Signals(TinOn_Disable, TVoutOn_Disable, TCoutOn_Disable, TSlopeOn_Disable, TCounterOn_Disable, AddrOn_Disable, WriteEn_Disable,0,0,0,0)
    
    write_DACs(dev,Vclamp0,0.5)
    write_DACs(dev,Vclamp2,1.1)
    write_DACs(dev,VCAS,0.8)
    write_DACs(dev,VBN,1.0)
    write_DACs(dev,VBPH,1.0)
    write_DACs(dev,VBPL,0.8)

    clock_set(dev,BW1_addr, 0, 0, 10 )
    time.sleep(0.01)
    clock_set(dev,BW2_addr, 0, 0, 10)
    time.sleep(0.01)
    
    write_DACs(dev,IVbN_stim,0.0) # experimental value 0.390 for ch10
    write_DACs(dev,IVbP_stim,0.0)# experimental value 0.3985 for ch10
    
    write_DACs(dev,IVbP_OTA,0.55) # experimental 
#%%    
    write_FPGA(dev,0x0c,int('1011100000000000', 2))
#%%
    Config_Mode(CurrentClamp=1,Gain10X=1)  
    clock_set(dev,cc_gate_addr,0,10,0) 
    
    #%%    
    clock_set(dev,cc_ota_rst_addr,0,10,0)
    write_FPGA(dev,0x07,1)# CC gainx10

#%% 
    write_FPGA(dev,0x04,int('000000', 2)) # 3 MSBs for HGain; 3 LSBs for BW
    
#%%    
    Config_Control_Signals(dev=dev,TinOn=1, TVoutOn=0, InfOvrOn=0, OVERIDE=0, OverflowEn=0, ConfigOn=0, WriteEn=0,Pg=0, Ag=1, Al_IN=0, Pl_IN=0, InfRSTb=1,EXT_RES=1, EXT_STAYB=1)
    clock_set(dev,cc_gate_addr,0,0,10) # allow current flows into integrator
    time.sleep(0.01)
    clock_set(dev,Pg_addr,0,0000,50000)
    time.sleep(0.01)
#%%
    write_DACs(dev,IVbP_stim,0.393)# experimental value 0.3985 for ch10    
#%%    #Config_Control_Signals(dev,TinOn_Enable, TVoutOn_Enable, TCoutOn_Disable, TSlopeOn_Disable, TCounterOn_Disable, AddrOn_Enable, WriteEn_Enable,0,0,0,0 )
    write_FPGA(dev,0x0c,int('1011100000000000', 2))
    time.sleep(0.1)
    Config_Control_Signals(dev=dev,TinOn=1, TVoutOn=0, InfOvrOn=0, OVERIDE=0, OverflowEn=0, ConfigOn=0, WriteEn=0,Pg=0, Ag=1, Al_IN=0, Pl_IN=0, InfRSTb=1,EXT_RES=1, EXT_STAYB=1)
#%% Stimulation Control
#    for row_index in range(0,32):
#        for col_index in range(0,1):
#            Select_Channel(dev, col_index, col_index, row_index, row_index)
#            time.sleep(0.003) 
    Select_Channel(dev, 10, 10, 0,0)
    time.sleep(0.1)
    Restart_Clocks()
    time.sleep(0.1)
    write_FPGA(dev,0x0c,int('1000100000000000', 2))
    Config_Control_Signals(dev=dev,TinOn=0, TVoutOn=0, InfOvrOn=0, OVERIDE=0, OverflowEn=0, ConfigOn=1, WriteEn=0,Pg=0, Ag=1, Al_IN=0, Pl_IN=0, InfRSTb=1,EXT_RES=1, EXT_STAYB=1)
    time.sleep(2)
    Config_Control_Signals(dev=dev,TinOn=0, TVoutOn=0, InfOvrOn=0, OVERIDE=0, OverflowEn=0, ConfigOn=0, WriteEn=0,Pg=0, Ag=1, Al_IN=0, Pl_IN=0, InfRSTb=1,EXT_RES=1, EXT_STAYB=1)
#%%
    write_DACs(dev,IVbN_stim,0.50) # experimental value 0.390 for ch10
    write_DACs(dev,IVbP_stim,0.51)# experimental value 0.3985 for ch10
    clock_set(dev,Pg_addr,0,50000,50000)
    time.sleep(0.01)
    clock_set(dev,cds2_addr,0,0,10)
    time.sleep(0.01)
    clock_set(dev,cc_gate_addr,0,10,0) # allow current flows into integrator
    time.sleep(0.01)
    clock_set(dev,cc_ota_rst_addr,0,10,0)
    time.sleep(0.01)
    write_FPGA(dev,0x06,1)
    time.sleep(0.01)
#%%
start_col=0
end_col=10
start_row=0
end_row=31
Select_Channel(dev, start_col, end_col, start_row, end_row)


#%%
stretch =100
scanwidth =2
clock_set(dev,vc_ota_rst_addr,-30*stretch,(125-40)*stretch,40*stretch)
time.sleep(0.01)
clock_set(dev,clk_chip_addr,0*stretch,1*stretch,1*stretch)
time.sleep(0.01)
#clock_set(dev,clk_ch_scan_addr,-90*stretch,125*stretch-2*scanwidth*(end_col-start_col+1), 2*scanwidth*(end_col-start_col+1))
clock_set(dev,clk_ch_scan_addr,0*stretch,scanwidth,scanwidth)
time.sleep(0.01)    
clock_set(dev,Strobe_addr,-123*stretch,(125-2)*stretch,2*stretch)
time.sleep(0.01)
clock_set(dev,Sample_addr,-80*stretch,(125-40)*stretch,40*stretch)
time.sleep(0.01)
clock_set(dev,CONV_addr,-1*stretch,(125-78)*stretch,78*stretch)
time.sleep(0.01)
clock_set(dev,Check_addr,-1*stretch,(125-2)*stretch,2*stretch)
time.sleep(0.01)
clock_set(dev,ReadEn_addr,-40*stretch,(125-80)*stretch,80*stretch)
time.sleep(0.01)
clock_set(dev,WriteEn_addr,-2*stretch,(125-35)*stretch,35*stretch) #   clock_set(dev,WriteEn_addr,-2*stretch,(125-35)*stretch,35*stretch)
time.sleep(0.01)
clock_set(dev,Load_addr,-80*stretch,(125-40)*stretch,40*stretch)
time.sleep(0.01)
clock_set(dev,ColSel_addr,-48*stretch,125*stretch-4*scanwidth*(end_col-start_col+1)+1, 4*scanwidth*(end_col-start_col+1)-1)
#clock_set(dev,ColSel_addr,0,10,0)
time.sleep(0.01)
clock_set(dev,RST_addr,-80*stretch,(125-40)*stretch,40*stretch)
time.sleep(0.01)    
Restart_Clocks()#% Clocks Start/Stop
#%%
write_DACs(dev,IVbP_stim,0.4340)# experimental value 0.3985 for ch10   
write_DACs(dev,IVbN_stim,0.4001)# experimental value 0.3985 for ch10 
fsamp_cc = 800e3/(stretch*(end_row-start_row+1))    
Config_Control_Signals(dev=dev,TinOn=0, TVoutOn=0, InfOvrOn=0, OVERIDE=0, OverflowEn=0, ConfigOn=0, WriteEn=0,Pg=0, Ag=1, Al_IN=0, Pl_IN=0, InfRSTb=1,EXT_RES=1, EXT_STAYB=1)
clock_set(dev,cc_gate_addr,0,10,0) # allow current flows into integrator
clock_set(dev,Pg_addr,0,50000,50000)
fig = plt.figure()
fig.patch.set_alpha(0.1)
ax = fig.add_subplot(111)
ax.patch.set_alpha(0.0)
plt.tight_layout()    
ax.patch.set_facecolor('white')
#datalenth=65536
datalenth=8000
#ch_num = end_ch - start_ch +1
#x_len=datalenth/ch_num
data_dict={}

run_num = 10
for run in range(run_num, run_num+1):    
#    CURRENT=':SOUR:CURR:LEV '+str(run)+'E-7'
#    my_K.write(CURRENT)
    print run
    ax.clear()
    start_col=run
    end_col=run
    start_row=0
    end_row=0
    write_FPGA(dev,0x0b,1)# FIFO_disable/clear up
    time.sleep(0.1)
    Select_Channel(dev, start_col, end_col, start_row, end_row)
    time.sleep(0.8) #wait until stable
    write_FPGA(dev,0x0b,0) # FIFO_enable/start filling
    time.sleep(1)
    scale=1.0
    middle=4095/2.0
    datain=bytearray([0]*4*datalenth) #should be multiple of 16, datain is 4*8-bit =32-bit number   
    pipedata_len=dev.ReadFromPipeOut(0xA0,datain)  
    datain=np.reshape(datain,(-1,4))      
    #datain=datain[:,0:3] 
    datain=datain.astype(np.uint16)
    
    cds_flag=(datain[:,3]>>2)&0b1
    #datain[:,3]=cds_flag
    #datain[:,1]=datain[:,0]+(datain[:,1]%4)*256  
    
    datain[:,1]=datain[:,0]+(datain[:,1]%16)*256 # convert 12-bit bin data to its decimal value
    datain[:,2]=datain[:,2]+(datain[:,3]%4)*256 # convert 10-bit bin channel num to its decimal value
    datain=datain[:,1:4]  #**********first data is skipped!!


    
    #data_dict={}
    for i in range(1024):
        data_dict[i]=[]
    for i in range(len(datain)):
        data_dict[datain[i][1]].append((datain[i][0]-middle)/scale)
         #data_dict[datain[i][1]].append((datain[i][0]-middle)/scale+datain[i][1]+middle/scale) # scale and shift
        #data_dict[datain[i][1]].append(((datain[i][0]-middle)/scale)) 
        ##data_dict[datain[i][1]].append(datain[i][2])
    
    
    
    for i in range(0,len(data_dict),1):
        for j in range(0,len(data_dict[i]),1):   # linear interpolation
            if data_dict[i][j]>4095-middle:
                if j==0:
                    data_dict[i][j]=data_dict[i][j+1]
                elif j==len(data_dict[i])-1:
                    data_dict[i][j]=data_dict[i][j-1]
                else:
                    data_dict[i][j]=(data_dict[i][j-1]+data_dict[i][j+1])/2.0
        if len(data_dict[i])>0:
            x_data = (np.array(range(len(data_dict[i])))+run*len(data_dict[i]))*(1.0/fsamp_cc)
            ax.plot(x_data,data_dict[i],linewidth=0.2,label='row '+str(i/32))
            print np.average(data_dict[i])
            #ax.plot(x_data,data_dict[i],'.',linewidth=0.1,color='black')
            #ax.plot(data_dict[i],linewidth=0.1,label='row '+str(i/32))
            ax.legend()
    #plt.title('1K Hz, 200 mVpp')
#    if run%10==8:
#        ax.clear()
    #
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (mV)')  
    plt.draw()    
    plt.pause(0.0001)
    ax.legend()

#%% SET Keithley for current source
rm = visa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC CURR')
#my_K.write(':SOUR:CURR:MODE FIX')
#%%
my_K.write(':SOUR:CURR:RANG 50E-7')
my_K.write(':SOUR:CURR:LEV 100E-7')
#%%
my_K.write(':SENS:FUNC "VOLT"')
my_K.write(':SENS:VOLT:PROT 0.609')
#my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')
my_K.close    

#%% SET Keithley for current measurement
rm = visa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
#%
my_K.write(':SENS:FUNC "CURR"')

my_K.write(':SENS:VOLT:PROT 0.6')
#my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP OFF')
my_K.close   





    

#%%  Calculate NSD before CDS
#from __future__ import division
      
    #measure = np.loadtxt(savepath,delimiter=",")
    measure = datain[:,0]
    measure = measure.ravel()        
    measure_av = (measure-np.average(measure))/(4096) # convert the unit of binary code to volt, 1b=0.1mV
    
    Fs=fsamp_cc # sampling frequency is 25K Hz
    N=len(measure_av) 
    mea_sq = np.sqrt(sum(measure_av**2)/N)
    print mea_sq
    measure_av= measure_av*np.blackman(N)
    ps = np.abs(np.fft.fft(measure_av)/N)**2 #do fft, then convert to density
    
    ps = ps[0:N/2+1] # use half the frequency range
    ps[1:-1] = 2*ps[1:-1]# double the amplitude
    
    freq =np.arange(0,Fs/2+Fs/N,Fs/N)
    plt.figure()
    plt.subplot(1,1,1)
    plt.loglog(freq, np.sqrt(ps)/10)
    plt.grid()
    #plt.xlim([1,100000])

    plt.ylim([1e-12,1e1])
    plt.title('Before CDS Correction')
    #plt.xlabel('Frequency $(Hz)$')
    plt.ylabel('Noise Density ($V/\sqrt{Hz}$)')
    plt.show()
#%% store data
import os
# if file does not exist write header 
if not os.path.isfile('filename.csv'):
   df.to_csv('filename.csv', header='column_names')
else: # else it exists so append without writing the header
   df.to_csv('filename.csv', mode='a', header=False)


#%%
    STD_df=pd.DataFrame.from_dict(data_dict, orient='index')
    STD_df_std=STD_df.std(axis = 1)


#%%
# para:CDS_Enable/Disable,CDS_Freq, CDS_Len{ >1}, OTA_Reset_Freq, OTA_Reset_Time, Bandwidth level{3,2,1,0}
    fsamp_cc =8e3 # Hz
    Tramp = 2046 # unit = 10ns
    fsamp_vc = 1e3 # Hz
    CDS_Freq = 100
    CDS_Len  = 2
    OTA_RST_Time = 10 # unit us
    BW_Level = 3 # integer from -3 to 3, greater means wider bandwidth
    Config_Clocks(dev,1,CDS_Disable,CDS_Freq,CDS_Len,200,OTA_RST_Time,BW_Level,Tsamp_cc=1e8/fsamp_cc,Tramp=2046,Tsamp_vc=1e8/fsamp_vc) 
    #(CC=1,CDS_En=0,CDS_Freq=100,CDS_Len=2,OTA_RST_Freq=100,OTA_RST_Time=10,Bandwidth=-3,Tsamp_cc=50000,Tramp=2046,Tsamp_vc=100000)
    Restart_Clocks()#% Clocks Start/Stop


#%%
    clock_set(dev,cdsEN_Notcds_delay,0,0,0) # set the the delay between cds and notcds    
#%%
    
    clock_set(dev,Pg_addr,0,100,00)
    #clock_set(dev,Ag_addr,0,000,100)
#%%
#%%
    Turn_OFF_CURRENT_STIM(dev,0,255)    
    
#%%
    TURN_ON_CURRENT_STIM(dev,start_ch=0,end_ch=0,Pg=1, Ag=1, Al_IN=1, Pl_IN=1)    

#%% data acquisition 
#% data acquisition
for test in range(512,1024):  
    print test
    Select_Channel(dev,test,test)
    time.sleep(1)
#%%    
savepath="C:/Users/Jun/Documents/Ph.D. Career/Projects and Research/Project -Closed Loop Neural Network/NeuroChannel/chip_testing/GUI/Gain1_Histogram1.csv"
STD_df.to_csv(savepath)    
#%%
    Voltage=VOLTAGE_MEAS(dev=dev,start_ch=0,end_ch=255,datalenth=65536,skip_len=500, av_len=5, scale=100.0,middle=511.5)
    fig = plt.figure()
    fig.patch.set_alpha(0.1)
    ax = fig.add_subplot(111)
    ax.patch.set_alpha(0.0)
    plt.tight_layout()    
    for i in range(0,len(Voltage),1):
        ax.plot(Voltage[i],linewidth=0.2,color='black')
    plt.draw()    

#%% SET Keithley
rm = visa.ResourceManager()
rm.close

my_K = rm.open_resource('GPIB0::25::INSTR')# Keithley
my_K.write('*RST')
my_K.write(':SOUR:FUNC CURR')
my_K.write(':SOUR:CURR:MODE FIX')
my_K.write(':SOUR:CURR:RANG 5E-6')
my_K.write(':SOUR:CURR:LEV 5E-7')
my_K.write(':SENS:FUNC "VOLT"')
my_K.write(':SENS:VOLT:PROT 0.6')
#my_K.write('DISPlay:ENABLe ON')
my_K.write(':OUTP ON')
my_K.close    
    
#%%
my_K.write(':OUTP OFF')   


#%%
#data_dict={}
start_ch = 0
end_ch = 255
data_points =11
fig = plt.figure()
fig.patch.set_alpha(0.1)
ax = fig.add_subplot(111)
ax.patch.set_alpha(0.0)
plt.tight_layout() 
data_dict_average={}
for i in range(start_ch,end_ch+1,1):
    #data_dict[i]=[]
    data_dict_average[i]=[]
#% VC mode
for channel in range(start_ch,end_ch+1,1):
    print channel
    start_ch =channel
    end_ch   =channel
    Select_Channel(start_ch,end_ch) 

    
    for ii in np.linspace(-0.05,0.05,data_points):
        CURRENT=':SOUR:CURR:LEV '+str(ii)+'E-9'
        my_K.write(CURRENT)
        time.sleep(2)  
        datalenth=4000
        skip_len=499
        scale=100.0
        av_len =1500
        middle=511.5
        data_dict={}
    #data_dict_average={}
        for i in range(256):
            data_dict[i]=[]
        #data_dict_average[i]=[]
        Restart_Clocks()
        time.sleep(4)  
    
        datain=bytearray([0]*4*datalenth) #should be multiple of 16, datain is 4*8-bit =32-bit number   
        pipedata_len=dev.ReadFromPipeOut(0xA0,datain)  
        datain=np.reshape(datain,(-1,4))      
        #datain=datain[:,0:3] 
        datain=datain.astype(np.uint16)
        
        first_flag=(datain[:,1]>>4)&0b1
        datain[:,3]=first_flag
        datain[:,1]=datain[:,0]+(datain[:,1]%4)*256  
        
        if first_flag[0]==0:
            datain=datain[1:-1,1:4] #remove first and last data point to align data
            first_flag=first_flag[1:-1]
        else:
            datain=datain[2::,1:4] #remove first two points to align data
            first_flag=first_flag[2::]
        
        for i in range(len(datain)):
            #data_dict[datain[i][1]].append((datain[i][0]-middle)/scale+datain[i][1]+middle/scale) # scale and shift
            data_dict[datain[i][1]].append((datain[i][0]))
            ##data_dict[datain[i][1]].append(datain[i][2])
        
        for i in range(start_ch,end_ch+1,1):
            data_dict[i]=(np.asarray(data_dict[i][0::2],dtype = np.int64)-np.asarray(data_dict[i][1::2],dtype = np.int64))*1
            for j in range (0,(len(data_dict[i])-skip_len)/av_len):
                data_dict_average[i].append(sum(data_dict[i][j*av_len+skip_len:(j+1)*av_len+skip_len])/av_len)

   
#ax.patch.set_facecolor('white')
    #for i in range(0,256,1):
    ax.plot(data_dict_average[channel],linewidth=0.2,color='black')
    plt.draw()
    plt.pause(0.0001)
#%
Current_meas_df=pd.DataFrame.from_dict(data_dict_average, orient='index')
savepath="C:/Users/Jun/Documents/Ph.D. Career/Projects and Research/Project -Closed Loop Neural Network/NeuroChannel/chip_testing/GUI/Gain1x_Current_meas_005to005.csv"
Current_meas_df.to_csv(savepath)
#%%
Config_Control_Signals(TinOn_Disable, TVoutOn_Disable, TCoutOn_Disable, TSlopeOn_Disable, TCounterOn_Disable, AddrOn_Disable, WriteEn_Enable,0,0,0,0 )
savepath=time.strftime("%Y%m%d-%H%M%S")+"Gain10xtest_Pat"+".csv"
#%%
fig = plt.figure()
fig.patch.set_alpha(0.1)
ax = fig.add_subplot(111)
ax.patch.set_alpha(0.0)
plt.tight_layout() 
#%%
Current_all={}
for i in range(256):
    Current_all[i]=[]
for ii in np.linspace(-50,50,4):
    CURRENT=':SOUR:CURR:LEV '+str(ii)+'E-10'
    #my_K.write(CURRENT)
    time.sleep(2)
    Current_single=CURRENT_MEAS(dev=dev,start_ch=0,end_ch=0,datalenth=2002,skip_len=500, av_len=500, scale=100.0,middle=511.5)
    
    #ax.patch.set_facecolor('white')
    for i in range(len(Current_single)):
        Current_all[i].append(Current_single[i])
        plt.plot(Current_single[i],'*',linewidth=0.4,color='black')
    plt.show()

#    df=pd.DataFrame.from_dict(data_dict_average, orient='index')
#    #df=pd.DataFrame(data_dict_average)
#    df.to_csv(savepath)
#%% Data Reading
filename="20190530_Leaky.csv"
Leak_df=pd.read_csv(filename,header = 0,index_col = 0)
Leak_mean=Leak_df.mean(axis = 1)
fig=plt.figure()
Leak_mean.plot.hist(color='k',alpha=0.9,bins=128)
plt.tight_layout()
#plt.grid()
plt.title('Leakage Histogram')
plt.xlabel('Leaky Current $(pA)$')
plt.xlim([-25,200])
#plt.xscale('log')
plt.ylabel('Counts')
plt.draw


#%% Voltage Offset Measurement
import matplotlib.ticker as ticker
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

Offset_df=pd.DataFrame.from_dict(data_dict, orient='index')
Offset_mean_df=Offset_df.mean(axis = 1)

Offset_mean_df.plot.hist(color='k',alpha=0.9,bins=128)
#plt.tight_layout()

plt.title('Offset Of Gain10X Mode',fontsize=20)
plt.xlabel('Offset $(mV)$', fontsize=16, position=(0.5, 0.1))
#xmajors = [0,10,20,50,100,200]
#ax.xaxis.set_major_locator(ticker.FixedLocator(xmajors))
#plt.xlim([-80,80])
plt.xticks(fontsize=12)
plt.ylabel('Channel Counts', fontsize=16, position=(0.4, 0.5))
#ymajors = [1,10,80,140,200]
#ax.yaxis.set_major_locator(ticker.FixedLocator(ymajors))
#plt.ylim([,200])

#plt.ylim([0,200])
plt.yticks(fontsize=12)


#plt.legend(loc='lower right',fontsize=24)
plt.show()
plt.savefig('C:/Users/Jun/Documents/Ph.D. Career/Projects and Research/Project -Closed Loop Neural Network/NeuroChannel/chip_testing/GUI/OffsetPlot_Gain10X.pdf')


#%%
savepath="C:/Users/Jun/Documents/Ph.D. Career/Projects and Research/Project -Closed Loop Neural Network/NeuroChannel/chip_testing/GUI/OffsetPlot_Gain10X.csv"
Offset_df.to_csv(savepath)
#%%
import matplotlib.ticker as ticker
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Move left y-axis and bottim x-axis to centre, passing through (0,0)

#ax.spines['left'].set_position('center')
#ax.spines['bottom'].set_position('center')
#ax.axhline(linewidth=2, color='black')
#ax.axvline(linewidth=2, color='black') 
#
## Eliminate upper and right axes
#ax.spines['right'].set_color('none')
#ax.spines['top'].set_color('none')
## Show ticks in the left and lower axes only
#ax.xaxis.set_ticks_position('bottom')
#ax.yaxis.set_ticks_position('left')

filename="20190530_Leaky.csv"
Leak_df=pd.read_csv(filename,header = 0,index_col = 0)
Leak_mean=Leak_df.mean(axis = 1)


Leak_mean.plot.hist(color='k',alpha=0.9,bins=128)
#plt.tight_layout()
plt.title('Leakage Histogram',fontsize=20)

plt.xlabel('Leaky Current $(pA)$', fontsize=16, position=(0.5, 0.1))
xmajors = [0,10,20,50,100,200]
ax.xaxis.set_major_locator(ticker.FixedLocator(xmajors))
plt.xlim([-4,200])
plt.xticks(fontsize=12)
plt.ylabel('Counts', fontsize=16, position=(0.4, 0.5))
ymajors = [1,10,80,140,200]
ax.yaxis.set_major_locator(ticker.FixedLocator(ymajors))
#plt.ylim([,200])

#plt.ylim([0,200])
plt.yticks(fontsize=12)


#plt.legend(loc='lower right',fontsize=24)
plt.show()
plt.savefig('C:/Users/Jun/Documents/Ph.D. Career/Projects and Research/Project -Closed Loop Neural Network/NeuroChannel/chip_testing/GUI/LeakPlot_v11.pdf')
#%% Data Writing
filename=time.strftime("%Y%m%d-%H%M%S")+"Gain10xtest_Pat"+".csv"

df=pd.DataFrame.from_dict(data_dict_average, orient='index')
#df=pd.DataFrame(data_dict_average)
df.to_csv(filename)
       
    
#%%
    import pandas as pd
    df=pd.DataFrame(data_dict_average)
    df.to_csv('current_measure2.csv')
#%%        
    for i in range(len(data_dict)):
        plt.plot(data_dict[i],linewidth=0.4,color='black')
    plt.show()

#%%
 
#%%    
with open('test.csv', "a") as f:
    writer = csv.writer(f)
    for i in range(len(data_dict)):
        writer.writerow(data_dict[i])     
        print i
            
#%%
with open('test.csv', "r") as f:
    reader = list(csv.reader(f))
    reader[1]
              
        
#%%    
    plt.close()
    write_FPGA(dev,0x09,0) # start=1, stop=0
    time.sleep(0.005) 
    write_FPGA(dev,0x09,1) # start=1, stop=0
    time.sleep(3)
    datalenth=51200
    plot_len=75000  
    average_len=1
    if_savedata=1
    #-%H%M%S
    filename=time.strftime("%Y%m%d-%H%M%S")+"Gain10xtest_Pat"+".csv"
    subpath="Documents\Ph.D. Career\Projects and Research\Project -Closed Loop Neural Network\NeuroChannel\chip_testing\Data"
    #filename=time.strftime("%Y%m%d-%H%M%S")+"test"+ str(3)+".csv"\
    savepath = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"],subpath, filename)
    measure=data_recording(dev,datalenth,average_len,plot_len,if_savedata,savepath)
  



#%% reload data
#    filename="20180902"+"test_sig"+str(21)+".csv"
#    subpath="Documents\Ph.D. Career\Projects and Research\Project -Closed Loop Neural Network\NeuroChannel\chip_testing\Data"
#    #filename=time.strftime("%Y%m%d-%H%M%S")+"test"+ str(3)+".csv"
#    savepath = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"],subpath, filename)
    co_measure=Digi_CDS(savepath,100000, 100000, Fs,int(Fs/CDS_Freq),CDS_Len)

#%% reload data
    filename="20180903-103041"+"test_sig_cell"+str(0) +".csv"
    subpath="Documents\Ph.D. Career\Projects and Research\Project -Closed Loop Neural Network\NeuroChannel\chip_testing\Data"
    #filename=time.strftime("%Y%m%d-%H%M%S")+"test"+ str(3)+".csv"
    savepath = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"],subpath, filename)
    co_measure=Digi_CDS(savepath,50000, 20000, 25000,250)
    
    
    
#%%
    from scipy.stats import norm
    SNDR = np.loadtxt(savepath,delimiter=",")

    plt.figure()
    mu, std = norm.fit(SNDR)
    # Plot the histogram.
    plt.hist(SNDR, bins=20, density=False, alpha=0.8, color='blue')
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    x = np.linspace(xmin, xmax, 20)
    title = "Error Distribution of SNDR"
    text="N=%d \n$\mu$ = %.2f \n$\sigma$ = %.2f\n$\sigma$/$\mu$= %.2f%%\n$\mu$$\pm$3$\sigma$=%.2f ~ %.2f" % (len(SNDR),mu, std,abs(std/mu*100),mu-3*std,mu+3*std)
    #plt.annotate(text, (0.8, 0.7), textcoords='axes fraction', size=10)
    plt.ylabel('SNDR (dB)')    
    plt.xlabel('Channel')
    plt.title(title)
    plt.text(xmin+0.05*(xmax-xmin),ymin+0.75*(ymax-ymin),text)
    plt.grid(True)
    plt.show()        