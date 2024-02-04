import sys
from pathlib import Path
import platform

script_dir = Path("NISoC_1bit_then_12bit.py").resolve().parent

ok_files_path = {
    'Darwin': script_dir / 'okFiles' / 'Mac',
    'Windows': script_dir / 'okFiles' / 'Win'
}

sys_path_to_append = ok_files_path.get(platform.system())           # Specify the location of supporting API files (ok.py, _ok.so, ...). 

if sys_path_to_append:
    sys.path.append(str(sys_path_to_append))                        # Add the location of supporting API files to systems's path.
else:
    print(f'We might need Opal Kelly drivers for {platform.system()}')

from nisoc_functions import *
from NeuroCube_functions import *

bit_file_path = script_dir / 'BIT_FILES' / 'top.bit'                # Specify the location of the bitfile.
#LOAD_BIT_FILE = True                                               # Load the bitfile onto Opal Kelly (load bit file on power reset).
LOAD_BIT_FILE = False                                               # Load THE bitfile onto Opal Kelly.
if LOAD_BIT_FILE:
    FPGA.loadBitFile(str(bit_file_path))                            # skip loading bitfile (rely on flash)

RESET_DEVICE = False                                                # reset the device. Currently, does not do anything.
if RESET_DEVICE:
    FPGA.initDevice() 
    
#%% Initialise DAC and set voltage outputs.
write_WireIn(FPGA,0x00,int('11', 2))    # Reset clocks: [1] fifo_rst, [0] rstClks.
write_WireIn(FPGA,0x00,int('00', 2))     
'''
Clock address:          18.
Clock low time:         3*10ns = 30ns.
Clock high time:        3*10ns = 30ns.
Clock pulse max:        24.

Old values:
IVbNP_stim:             0.9V.
IVbNN_stim:             0.9V. 
Vinfinimp_bias:         0.850V.
IVbP_OTA:               0.6V.
Vclamp_p:               0.7V.
Vclamp_n:               0.5V.
Vref_nisoc:             0.6V.
'''
init_DAC_nisoc(FPGA, 2, 2, 24)
write_DAC_nisoc(FPGA, IVbP_OTA, 0.600)          # 0.826, 0.800
write_DAC_nisoc(FPGA, Vinfinimp_bias, 1.278)    # 1.278
write_DAC_nisoc(FPGA, Vclamp_p, 1.25)
write_DAC_nisoc(FPGA, Vclamp_n, 0.8)
write_DAC_nisoc(FPGA, IVbNP_stim, 0.5)
write_DAC_nisoc(FPGA, IVbNN_stim, 0.5)
write_DAC_nisoc(FPGA, Vref_nisoc, 0.9)          # 1.053, 1.13
DAC_muxout_nisoc(FPGA, REF_muxout)              # Select one of the LTC2666 device voltages to the MUXOUT pin.

# Optional power down functionality.
power_down_DAC_nisoc(FPGA, 7)                   # Turn off the unused channel 7 (conserve power).
#power_down_DAC_nisoc(FPGA, All)

#%%
'''
Configure Clocks.
 
Time is entered in units of 10ns.

_rstota.
Clock address:          1.
Held fixed at logic high by keeping the clock enable at logic low.

RSL.
Clock address:          2.
Clock delay time:       100*10ns = 1us. 
Clock delay sign:       1 (positive delay).
Clock low time:         3,250*10ns = 32.5us.
Clock high time:        750*10ns = 7.5us.
Clock pulse max:        1.
Clock stop time:        1 (0s).

Conv.
Clock address:          3.
Clock delay time:       900*10ns = 9us.
Clock delay sign:       1 (positive delay).
Clock low time:         2,500*10ns = 25us.
Clock high time:        1,500*10ns = 15us.
Clock pulse max:        1.
Clock stop time:        1 (0s).

Fconv.
Clock address:          4.
Clock delay time:       900*10ns = 9us.
Clock delay sign:       1 (positive delay).
Clock low time:         50*10ns = 0.5us.
Clock high time:        50*10ns = 0.5us.
Clock pulse max:        15.
Clock stop time:        2,500*10ns = 25us.

Done.
Clock address:          5.
Clock delay time:       2,300*10ns = 23us.
Clock delay sign:       1 (positive delay).
Clock low time:         3,900*10ns = 39us.
Clock high time:        100*10ns = 1us.
Clock pulse max:        1.
Clock stop time:        1 (0s).

Strobe.
Clock address:          6.
Clock delay time:       2,400*10ns = 24us.
Clock delay sign:       1 (positive delay).
Clock low time:         3,950*10ns = 39.5us.
Clock high time:        50*10ns = 0.5us.
Clock pulse max:        1.
Clock stop time:        1 (0s).

CDS.
Clock address:          7.
Clock delay time:       850*10ns = 8.5us.
Clock delay sign:       1 (positive delay).
Clock low time:         4,000*10ns = 40us.
Clock high time:        4,000*10ns = 40us.
Clock pulse max:        1.
Clock stop time:        1 (0s).

SPI Read.
Clock address:          8.
Clock delay time:       2,450*10ns = 24.5us.
Clock delay sign:       1 (positive delay).
Clock low time:         3,950*10ns = 39.5us.
Clock high time:        50*10ns = 0.5us.
Clock pulse max:        1.
Clock stop time:        1 (0s).

SPI Clk.
Clock address:          9.
Clock delay time:       2,475*10ns = 24.75us.
Clock delay sign:       1 (positive delay).
Clock low time:         50*10ns = 0.5us.
Clock high time:        50*10ns = 0.5us.
Clock pulse max:        16.
Clock stop time:        2,400*10ns = 24us.

FIFO_Wr (Clock is optional).
Clock address:          14.
Clock delay time:       4,075*10ns = 40.75us.
Clock delay sign:       1 (positive delay).
Clock low time:         3,999*10ns = 39.99us.
Clock high time:        1*10ns = 10ns.
Clock pulse max:        1.
Clock stop time:        1 (0s).

ReadEn.
Clock address:          17.
Held fixed at logic high by keeping the clock enable at logic low.
'''
write_WireIn(FPGA, 0x09, 0x00000)  # Func_Gen_Trig = ep09wire[17] ? Ext_Trig : spi_read. Set function generator's external trigger control from the SPI read signal.          
clock_set(FPGA, 2,  100,    3250, 750,  1,  1   )
clock_set(FPGA, 3,  900,    2500, 1500, 1,  1   )
clock_set(FPGA, 4,  900,    50,   50,   15, 2500)
clock_set(FPGA, 5,  2300,   3900, 100,  1,  1   )
clock_set(FPGA, 6,  2400,   3950, 50,   1,  1   )
clock_set(FPGA, 7,  850,    4000, 4000, 1,  1   )
clock_set(FPGA, 8,  2450,   3950, 50,   1,  1   )
clock_set(FPGA, 9,  2475,   50,   50,   16, 2400)
clock_set(FPGA, 14, 4075,   3999, 1,    1,  1   )

'''
Enable clocks.
[0] _rstota, [1] rsl, [2] conv, [3] fconv, 
[4] done, [5] strobe, [6] CDS, [7] SPI read, 
[8] SPI clock, [9] SPI write clock (manual), [10] write configuration FSM enable, 
[12] arst, [13] ainc, [14] FIFO_wr, [15] Ag, 
[16] Pg, [17] ReadEn, [18] LTC2666_en.
'''
write_WireIn(FPGA,0x01,int('000_0100_0001_1111_1110', 2)) 

#%% Disable clocks.
write_WireIn(FPGA,0x01,int('0', 2))

#%% 
'''
Configure NISoC GLOBAL registers.

Configuration write FSM.
Clock address:          11.
SPI clock delay time:   50*10ns = 0.5us.
SPI clock delay sign:   1 (positive delay).
SPI clock low time:     50*10ns = 0.5us.
SPI clock high time:    50*10ns = 0.5us.
SPI clock pulse max:    16.
SPI Write pulse duration: 50*10ns = 0.5us.

Global register list:
[0] 0 = Voltage clamping, 1 = Current Clamping; [1] 0 = Single CDS, 1 = Double CDS; [2] 0 = Single conv, 1 = full conv; [3] Gain<0>;
[4] Gain<1>; [5] Gain<2>; [6] BW<0>; [7] BW<1>;
[8] BW<2>; [9] EXT_RES; [10] EXT_STAYB; [11] OVERRIDE;
[12] OverflowEN; [13] RST command 0; [14] RST command 1; [15] 1 = global, 0 = Local.
             
Example configurations: '1001_1110_0000_0101'         # default configuration, CC
                        '1111_1110_0000_0101'         # CC, RST 0 HIGH and RST 1 HIGH 
                        '1110_0000_0000_0101'         # new default, CC, full conv, 0 gain, no BW limit, RSTs 1, SAR Ctrls 0
                        '1110_0000_0011_1101'         # CC, full conv, full gain, no BW limit, RSTs 1, SAR Ctrls 0
                        '1001_1110_0000_0100'         # default except VC
                        '1001_1110_0011_1101'         # no BW limit; full gain
                        '1001_1111_1111_1100'         # BW limited configuration; gain !
                        '0010_0000_0111_1001'
                        '0101_0101_0101_0101'         # this one just works
                        '0010_0100_1001_0010'         # this one breaks
                        '1000_1000_0000_0001'
                        '1001_0010_0100_1001'
                        '00000101000001010010010010010010',   # 100 ns period
                        '00110010 00110010 0101010101010101'  # 1000 ns period
                        '01001100010011000101010101010101'    # 1000 ns period
Some more configuration values from Akshay's old code:
if full_conv:
    write_FPGA(FPGA,0x07,int('1111_0000_0000_0101', 2))         # CC, full conv, 1 gain, full BW limit, RSTs 1, SAR Ctrls 0.
    write_FPGA(FPGA,0x07,int('1_11_1000_111_000_101', 2))       # CC, full conv, 1 gain, full BW limit, RSTs 1, SAR Ctrls 0
else:
    print ('single bit chip config')
    write_FPGA(FPGA,0x07,int('1110_0001_1111_1001', 2))         # CC, 1-bit, 0 gain, full BW limit, RSTs 1, SAR Ctrls 0
'''
write_WireIn(FPGA,0x08,int('0000_0000_1001_1111_1111_1110', 2))
clock_set(FPGA, 11, 50, 50, 50, 16, 50)

'''
Enable FSM.
[0] _rstota, [1] rsl, [2] conv, [3] fconv, 
[4] done, [5] strobe, [6] CDS, [7] SPI read, 
[8] SPI clock, [9] SPI write clock (manual), [10] write configuration FSM enable, 
[12] arst, [13] ainc, [14] FIFO_wr, [15] Ag, 
[16] Pg, [17] ReadEn, [18] LTC2666_en.
'''
write_WireIn(FPGA,0x01,int('000_0000_0100_0000_0000', 2))
write_WireIn(FPGA,0x01,int('0', 2))   # Clock [10] has to be disabled before re-writing a new configuration.

#%% 
'''
Configure NISoC LOCAL registers.

Configuration write FSM.
Clock address:          11.
SPI clock delay time:   50*10ns = 0.5us.
SPI clock delay sign:   1 (positive delay).
SPI clock low time:     50*10ns = 0.5us.
SPI clock high time:    50*10ns = 0.5us.
SPI clock pulse max:    16.
SPI Write pulse duration: 50*10ns = 0.5us.

Local register list:
[0] Al, [1] Pl, [2:5] strt_indx, [6] AmpSense, [7] InfinImpSense,
[8] AmpOverwrite, [9] InfinImpOverwrite, [10] Channel_off, [11] ADC_off, [12:14] N/A, [15] 1 = global, 0 = local.
'''
write_WireIn(FPGA,0x08,int('0000_0000_0_000_00_0001_0110_01', 2))   
clock_set(FPGA, 11, 50, 50, 50, 16, 50)
 
'''
Enable FSM.
[0] _rstota, [1] rsl, [2] conv, [3] fconv, 
[4] done, [5] strobe, [6] CDS, [7] SPI read, 
[8] SPI clock, [9] SPI write clock (manual), [10] write configuration FSM enable, 
[12] arst, [13] ainc, [14] FIFO_wr, [15] Ag, 
[16] Pg, [17] ReadEn, [18] LTC2666_en.
'''
write_WireIn(FPGA,0x01,int('00_0000_0100_0000_0000', 2))   
write_WireIn(FPGA,0x01,int('0', 2))   # Clock [10] has to be disabled before re-writing a new configuration.

#%% Channel configuration clocks.
'''
arst.
Clock address:          12.
Clock delay time:       30*10ns = 0.3us.
Clock delay sign:       1 (positive delay).
Clock low time:         1e8*10ns = 1s.
Clock high time:        20*10ns = 0.2us.
Clock pulse max:        1.
Clock stop time:        1 (0s).

ainc.
Clock address:          13.
Clock delay time:       4,075*10ns = 40.75us.
Clock delay sign:       1 (positive delay).
Clock low time:         3,980*10ns = 39.8us.
Clock high time:        20*10ns = 0.2us.
Clock pulse max:        1.
Clock stop time:        1 (0s).
'''
clock_set(FPGA, 12, 30,     int(1e8),  20, 1, 1)
clock_set(FPGA, 13, 4075,   3980, 20, 1, 1)

'''
Enable clocks.
[0] _rstota, [1] rsl, [2] conv, [3] fconv, 
[4] done, [5] strobe, [6] CDS, [7] SPI read, 
[8] SPI clock, [9] SPI write clock (manual), [10] write configuration FSM enable, 
[12] arst, [13] ainc, [14] FIFO_wr, [15] Ag, 
[16] Pg, [17] ReadEn, [18] LTC2666_en.
'''
write_WireIn(FPGA,0x01,int('00_0011_0000_0000_0000', 2))

#%% Disable clocks.
write_WireIn(FPGA,0x01,int('0', 2))

#%% 
'''
Channel configuration pulse.

arst.
Clock address:          12.
Clock delay time:       30*10ns = 0.5us.
Clock high time:        50*10ns = 0.5us.

ainc.
Clock address:          13.
Clock delay time:       30*10ns = 0.5us.
Clock high time:        50*10ns = 0.5us.
'''
pulse_set(FPGA, 12, 50, 50)
pulse_set(FPGA, 13, 50, 50)

#%% Trigger address reset (arst) pulse.
activate_TriggerIn(FPGA, 0x40, 0)                  # Trigger address reset pulse. D11 channel on scope/logic analyzer.

#%% Trigger address increment (ainc) pulse.
activate_TriggerIn(FPGA, 0x40, 1)                  # Trigger address increment pulse. D12 channel on scope/logic analyzer.

#%% 
'''
External Trigger input to function generator.
arst.
Clock address:          19.
Clock delay time:       50*10ns = 0.5us.
Clock high time:        50*10ns = 0.5us.
'''
pulse_set(FPGA, 19, 50, 50)
write_WireIn(FPGA, 0x09, 0x20000)               
activate_TriggerIn(FPGA, 0x40, 2)               # Trigger an External Trigger function generator pulse.

#%% 
'''
Test data write by writing 2024 datapoints to ADC data output FIFO.

ep21wire: 
[31:16](fifo_test ? ep0awire[16:1] : 16'd0), 
[15:6] 10'd0, [5] underflow, [4] valid, [3] empty, [2] overflow, [1] wr_ack, [0] full.        -- FIFO Status flags.
(Test using data explicitly sent from Python over the ep0Awire input to the FPGA).

ep22wire: [31:26] 15'd0, [16:0] rd_data_count.
ep23wire: [31:26] 15'd0, [16:0] wr_data_count. 
'''
write_WireIn(FPGA, 0x00, int('10', 2))               # Reset FIFO: [1] fifo_rst, [0] rstClks.
write_WireIn(FPGA, 0x00, int('00', 2))      
# Enable the FIFO test. Use data explicitly sent from Python through the ep0awire input to the FPGA for writing into the FIFO.
for i in range(2024):
    write_WireIn(FPGA, 0x09, (i<<1)+1)               # Enable FIFO test by sending a series of integers to FIFO, where adding 1 acts as the enable signal.
    activate_TriggerIn(FPGA, 0x41, 1)              # Trigger a FIFO write enable pulse at bit 1 of the 32-bit wide trigger input.   
    ep21 = read_WireOut(FPGA, 0x21)                     
    ep22 = read_WireOut(FPGA, 0x22)
    ep23 = read_WireOut(FPGA, 0x23)     
    print("Data written: "+str((ep21&0xffff0000)>>16)) # bit-wise AND with 0xffff0000 and right-shift by 16 positions to extract bits [31:16].
    print("FIFO status [5:0]: "+str(bin(ep21&0x3f)))   # bit-wise AND with 0xffff to extract bits [5:0].
    print("FIFO write data count: "+str(ep22))
    print("FIFO read data count: "+str(ep23)+'\n')

#%% 
'''
Test Pipe In/Out functionality.
PipeOut data contents:
[31:24] 8'd64, [23:16] 8'd127, [15:0] dout (FIFO data output bus).
'''
datalength = 131068                         # The actual write depth of the FIFO is 131,071. When reading from PipeOut, ensure the bytearray's size (4*datalength) that stores pipe data is a multiple of 16.
buf = read_PipeOut(FPGA, 0xa0, datalength)
buf=np.reshape(buf,(-1,4))                  # Reshape the bytearray into a 2D Numpy array with 4 columns. Each group of 4 bytes from the original bytearray forms a single row in the new 2D array, representing a 32-bit packet from PipeOut.
buf=buf.astype(np.uint16)                   # Convert all elements in the buffer into 16-bit unsigned integers, preparing the data for the next step which involves manipulating specific bits from PipeOut.
buf[:,1]=buf[:,0]+(buf[:,1])*256            # Reconstruct the actual 16-bit FIFO data output by combining the least significant byte (LSB) and the next byte (LSB+1) from PipeOut. Shift the LSB+1 byte left by 8 bits (equivalent to multiplying by 256) and add it to the LSB.
buf = buf[:, 1:4]                           # Remove the LSB column from the buffer, keeping only the columns with the combined bytes and any additional data.
print(buf)

#%% 
'''
Read FIFO a single address at a time.
ep20wire: [31:16] dout (FIFO data output), [15:0] ADC direct output.
'''
activate_TriggerIn(FPGA, 0x41, 0)          # Trigger a FIFO read enable pulse at bit 0 of the 32-bit wide trigger input.
ep20 = read_WireOut(FPGA, 0x20)                     
ep21 = read_WireOut(FPGA, 0x21)
ep22 = read_WireOut(FPGA, 0x22)
ep23 = read_WireOut(FPGA, 0x23)
print("FIFO data: "+str(ep20>>16))
print("FIFO status [5:0]: "+str(bin(ep21&0x3f)))  # bit-wise AND with 0xffff to extract bits [5:0].
print("FIFO write data count: "+str(ep22))    
print("FIFO read data count: "+str(ep23))

#%%
'''
Disable testing mode of operation and reset FIFO.
'''
write_WireIn(FPGA, 0x00, int('10', 2))               # Reset FIFO: [1] fifo_rst, [0] rstClks.
write_WireIn(FPGA, 0x00, int('00', 2))               
write_WireIn(FPGA, 0x09, int('0',2))                 # Disable FIFO test.
ep21 = read_WireOut(FPGA, 0x21)                     
ep22 = read_WireOut(FPGA, 0x22)
ep23 = read_WireOut(FPGA, 0x23)     
print("FIFO status [5:0]: "+str(bin(ep21&0x3f)))   # bit-wise AND with 0xffff to extract bits [5:0].
print("FIFO write data count: "+str(ep22))
print("FIFO read data count: "+str(ep23))




#%% Continuous capture with FIFO Prog_Full flag

savepath="C:/Users/isnl/OneDrive - UC San Diego/research/NeuroCube/NISoC_updated_python/plots/24 June, 2021/"
filename=savepath+time.strftime("%Y%m%d-%H%M%S"+ "_QFP7_Ch0_lab_scope_laptop_pluggedin_25kHz_gain1_dig_and_analog_CDS_BW000_flags_10_600mVpp_sine_input"+".h5") 

#filename=savepath+time.strftime("%Y%m%d-%H%M%S")+ "CC_gate_current_measurement_"+"Keithley_on_Ch0_AL_1_PL_1_Vsrc_0.7v"+".h5" 
Data_Read_USB(FPGA=FPGA,filename=filename,recordingtime=5);  

#%% load usb saved data and plot
#prefile = '20210611-121723_QFP4_Ch0_Battery_Bear_sanity_gain60_noCDS_60secs_3M_20';
#filename = prefile + ".h5"

start_time = time.time()    
f = tables.open_file(filename, "r")
datain=f.root.data.read()
f.close()
data_check = datain
datain=datain.astype(np.int16)

# convert the loaded integer USB data to decimal 

data_dict={}

if full_conv:   
    datain_dec = np.zeros(len(datain));
    res_io = np.zeros(len(datain));
    cds_flag = np.zeros(len(datain));
    rstota_flag = np.zeros(len(datain));
    for i in range(0,len(datain)):
        temp_str0 = "{0:b}".format(datain[i,0]);
        if len(temp_str0) < 8:
            numfill = 8 - len(temp_str0);
            for j in range(numfill):
                temp_str0 = '0' + temp_str0;
        #bitstring.append(temp_str0);
        temp_str0d = temp_str0[:4][::-1];
        temp_str1 = "{0:b}".format(datain[i,1]);
        if len(temp_str1) < 8:
            numfill = 8 - len(temp_str1);
            for j in range(numfill):
                temp_str1 = '0' + temp_str1;
        temp_str1 = temp_str1[::-1];
        datain_dec[i] = int(temp_str0d+temp_str1,2)
        res_io[i] = int(temp_str0[4:][::-1],2);
        
        temp_str2 = "{0:b}".format(datain[i,2]);
        if len(temp_str2) < 8:
            numfill = 8 - len(temp_str2);
            for j in range(numfill):
                temp_str2 = '0' + temp_str2;
        temp_str2 = temp_str2[::-1];
        cds_flag[i] = int(temp_str2[:],2);
        rstota_flag[i] = int(temp_str2[-1],2);
        
    data_dict[0] = datain_dec;
    print ('Full Conv, USB to Decemial conversion complete')
    
else:   
    datain_dec = np.zeros(len(datain));
    compbits = np.zeros(len(datain));
    for i in range(0,len(datain)):
        temp_str0 = "{0:b}".format(datain[i,0]);
        if len(temp_str0) < 8:
            numfill = 8 - len(temp_str0);
            for j in range(numfill):
                temp_str0 = '0' + temp_str0;
        #bitstring.append(temp_str0);
        temp_str0d = temp_str0[:4][::-1];
        temp_str1 = "{0:b}".format(datain[i,1]);
        if len(temp_str1) < 8:
            numfill = 8 - len(temp_str1);
            for j in range(numfill):
                temp_str1 = '0' + temp_str1;
        temp_str1 = temp_str1[::-1];
        compbits[i] = int(temp_str1[-2:-1],2);
    
    data_dict[0] = compbits; 
    print('1-bit Conv, USB to Decemial conversion complete')    
        
#%% plot
plt.ion()
if full_conv:
    fig, ax1 = plt.subplots();
    #ax1.plot(datain_dec)
    #ax2 = ax1.twinx();
    #ax2.plot(res_io, '.r')
    toplot = [];
    for i in range(0,len(data_dict)):
        toplot = np.append(toplot, data_dict[i]);
    ax1.plot(toplot)
    plt.show()
    
    #ax_cds_flag.plot(cds_flag)
    ax1.set_xlim([0,2500])
    #ax1.set_ylim([0, 4095])
    
    
    print(np.max(datain_dec))
    print(np.min(datain_dec))
else:
    fig, ax1 = plt.subplots();
    ax1.plot(compbits)
    ax1.set_xlim([650,780])
    ax1.set_ylim([-1, 2])
    plt.show()
    
#%% save USB load converted decimal data to csv
#with open("20210611-115930_QFP4_Ch1_Battery_Bear_sanity_gain60_noCDS_60secs_flatcnt_9.csv", "a") as f:
#with open(prefile +".csv", "a") as f:
with open(filename[:-3] +".csv", "a") as f:
    writer = csv.writer(f)
    #writer.writerow(datain_dec)
    writer.writerow(data_dict[0])

#%% 1-bit load 
filename = "210519_QFP4_Ch1_VrefShorted_1bit_1.csv"
with open(filename, 'rb') as f:
    onebit = csv.reader(f)
    print ('csv being read ...')
    for row in onebit:
        compbitload = map(int,map(float,row))   #convert csv loaded data which is string to float to int
        
#%% 1-bit algorithm 
from gates_ap import *
# main dir loop
done_check = 0;
RST = 0;
RSTb = not RST; 
fconv_cnt = 0;
surpress = 0;
res_pre = 0;
res_pre_log = [];
sign_changed = 0;
sign_changed_bar = 1;
prev_dir = 0;
res_dir = [];
stayb = [];
dir = [];
sign_changed_log = [];

R = [0, 0, 0, 0];                   # ** How to set the starting radix? Should it match what's set on the chip register? Yes, e.g. [0010] = 4
RB = [1, 1, 1, 1];
R_log = [];
gater_clk = 0;
r_count = 0;
r_count_log = [];

GTB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
cnt_clk = 0;
d_count = 0;
d_count_log = [];
addval = 0;

ndirc = 0; # ndir loop count 

# main loop scans through saved comp_bit outputs. 
# ndir here is the actual comp_bit, not the index or count (ndirc)
# think of each loop here as an fconv clock cycle
for ndir in compbitload:
    # need to put RST flag captured here
    fconv_cnt = fconv_cnt + 1;
    # assuming rst following every 19th fconv      # ** Is an assumed RSL RST sufficient?
    if fconv_cnt > 19:
        fconv_cnt = 0;
        RST = 1;
        RSTb = not RST;
    else: 
        RST = 0;
        RSTb = not RST;
        
    if RST == 1:  # added reset conditions, needs to match (incl. dffsrpq, etc)
        #print 'RST'
        sign_changed_bar = 1;
        sign_changed = not sign_changed_bar;
        #sign_changed_log.append(int(sign_changed));
            
        #ndir = 0;
        prev_dir = 0;
        
        d_count_log.append(d_count)     # 12-bit output (IO_Data)
        #d_count = 0;                    # should only be reset to 2048 during config register write
    # reset during reset_data
    #d_count_log.append(d_count)     # 12-bit output (IO_Data)
    #d_count = 0;                
    
 
    # direction control
    res_pre = OR(surpress, XNOR(ndir,prev_dir)) 
    prev_dir = ndir;
    res_pre_log.append(res_pre);
    
    if (NAND(res_pre, sign_changed_bar) == 1):
        sign_changed_bar = 0;
        sign_changed = not sign_changed_bar;
     
    elif (NAND(res_pre, sign_changed_bar) == 0):
        if (RSTb == 1):
            sign_changed_bar = not NAND(res_pre, sign_changed_bar);
            sign_changed = not sign_changed_bar;
    sign_changed_log.append(int(sign_changed));
                
    res_dir.append(NOR(res_pre, sign_changed_bar));
    stayb.append(int(AND(NAND(res_pre, sign_changed), not surpress))); 
    dir.append(ndir); 

    # Res_center_preload: res_clk_gater_preload
    #gater_clk = AND(AND(stayb[ndirc] ,NAND(not res_dir[ndirc],AND(R[2],R[3]))), NAND(res_dir[ndirc] ,AND(AND(not R[1],not R[2]), not R[3])))
    I30 = AND(R[2],R[3]);                           # ** Review these logic blocks with Preston; not sure how to implement R table here
    I21 = NAND(not res_dir[ndirc],I30);
    I2 = AND(AND(RB[1],RB[2]),RB[3]);
    I19 = NAND(res_dir[ndirc], I2);
    gater_clk = AND(AND(stayb[ndirc],I21),I19);
    res_dirb = not res_dir[ndirc];
    
    if gater_clk:
        #print [gater_clk, len(res_dir), ndirc, res_dir[ndirc]]
        if res_dir[ndirc]:
            #print res_dir[ndirc]
            r_count = r_count + 1; 
        elif res_dir[ndirc] == 0: 
            r_count = r_count - 1;
        
        if r_count > 11:
            r_count = 0;
        elif r_count < 0:
            r_count = 0; 
        r_count_log.append(r_count)
            
        for r in range(len(R[:])):
            bintmp = "{0:b}".format(r_count);
            if len(bintmp) < 4:
                numfill = 4 - len(bintmp);
                for j in range(numfill):
                    bintmp = '0' + bintmp;
            R[r] = int(bintmp[-(1+r)])
        for p in range(len(R)): RB[p] = not R[p]; 
        R_log.append(R);
        
        
    # c_btou_decoder11, Radix to GTB mask
    GTB = decodeGTB(R);                             # ** The decoder table in Jun's cbtou_11 schematic doesn't match, so made GTB function
        
    # c_btou_decoder11, GTB 1s are locked bits 
#    if R[:] == [0, 1, 0, 0]: 
#        for g in range(len(GTB)): GTB[g] = 0;
#    elif R[:] == [1, 1, 0, 0]: 
#        for g in range(len(GTB)): GTB[g] = 0;
#        GTB[0] = 1;
#    elif R[:] == [1, 0, 1, 1]: 
#        for g in range(len(GTB)): GTB[g] = 1;
#        GTB[11] = 0;
#    elif R[:] == [0, 1, 1, 1]: 
#        for g in range(len(GTB)): GTB[g] = 0;
    
    # cnt_clk_gen
    
    #cnt_clk = AND(NAND(dir[ndirc],AND(GTB[0],done_check)), 1);
    cnt_clk = 1;
    addval = 0;
    
    #DAC ctrl, check this because it only happens during done check, fconv increment dcount everytime
    if cnt_clk:  
        #print GTB                                               # ** Still not sure why d_count increments when cnt_clk not high
        #for i in range(len(GTB)):
        #    if GTB[i] == 1:
        #        break;
        #addval = 2**(i);
        #print r_count                                        # ** The GTB mask supposedly locks when 1, is my method correct?
        addval = 2**(r_count);
        if ndir:
            d_count = d_count + addval;
            print (d_count)
        else:
            d_count = d_count - addval; 
    
    ndirc = ndirc + 1; 

#%% GTB Decoder Func

def decodeGTB(R):
    bR = [0, 0, 0, 0];
    GTB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    for i in range(len(R)): bR[i] = not R[i];
    GTB[0] = AND(bR[3], AND(bR[2],bR[1])); 
    GTB[1] = AND(bR[3], AND(bR[2],OR(bR[1],bR[0]))); #check cadence 
    GTB[2] = AND(bR[3],bR[2]);
    GTB[3] = AND(bR[3],OR(bR[2],AND(bR[1],bR[0])));
    GTB[4] = AND(bR[3],OR(bR[2],bR[1]));
    GTB[5] = AND(bR[3],NAND(R[2], AND(R[1],R[0])));
    GTB[6] = not R[3];
    GTB[7] = NAND(R[3],NAND(bR[2],AND(R[1],R[0])));
    GTB[8] = NAND(R[3],OR(R[2],R[1]));
    GTB[9] = NAND(R[3],OR(R[2], AND(R[1],R[0])));
    GTB[10] = NAND(R[3],R[2]);
    GTB = list(map(int, GTB));
    return GTB

#%% Radix Func

def radixCount(stayb, res_dir, r_count):
    if stayb:
        r_count = r_count + 1;
        
#%% Plot
plt.figure();
plt.plot(dir);

#%% Direct Signal Into NISoC, varying the frequency and amplitude 
# initialize and set DACs

savepath="C:/Users/a1pau/Desktop/VLSI2020_Demo/sweep/"
rec_len = 30; # seconds

srt_V = 0.0;
end_V = 1.2;
step_V = 0.01;
amps = np.arange(srt_V,end_V+step_V,step_V);
#srt_f = 1;
#end_f = 12500;
a1 = 10.**(np.arange(0, 4));
a2 = np.arange(1,11,1);
freqs = np.outer(a1, a2).flatten();

time_step = 30;
start_time = '180600'

while(1):
    if (time.strftime("%H%M%S") == start_time):
        for k in amps:
            for i in freqs: 
                
                write_FPGA(FPGA,0x00,int('0000000000001100', 2))
                #print '[0] 0-Full/1-SingleConv, [2] RSTOTA enabled, [3] DS mode OFF.'
                time.sleep(1)
                write_FPGA(FPGA,0x00,int('0000000000001000', 2))
                
                while int(time.strftime("%Y%m%d-%H%M%S")[-2:])%time_step != 0: pass
                #print 'after while'    
                print (i)
                # Acquire data from NISoC 
                filename=savepath+time.strftime("%Y%m%d-%H%M%S")+ "_QFP4_Ch0_"+"amp_"+str(k)+"_freq_"+str(i)+".h5" 
                Data_Read_USB(FPGA=FPGA,filename=filename,recordingtime=rec_len);
            
        break


# Disable clocks
write_FPGA(FPGA,0x03,int('0000000000000000', 2))
print ('Clocks output disabled.')   
