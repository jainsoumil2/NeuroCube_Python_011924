%%Akshay Scope script
instrfindall
instrreset
%% Interface configuration and instrument connection

% The second argument to the VISA function is the resource string for your
% instrument
visaObj = visa('agilent','USB0::0x0957::0x17B4::MY54100520::0::INSTR');  %'TCPIP0::172.31.57.44::inst0::INSTR'
% Set the buffer size
visaObj.InputBufferSize = 1250000; %100000;
% Set the timeout value
visaObj.Timeout = 10;
% Set the Byte order
visaObj.ByteOrder = 'littleEndian';
% Open the connection
fopen(visaObj);

%%
fprintf(visaObj,':TIMEBASE:MODE MAIN');
fprintf(visaObj,':ACQUIRE:TYPE NORMAL');
fprintf(visaObj,':WAV:POINTS:MODE RAW');
fprintf(visaObj,':WAV:POINTS MAXimum');
fprintf(visaObj,':TIMebase:RANGe 5E-4');
query(visaObj,':TIMebase:RANge?')

%%
%fprintf(visaObj,'DIGitize POD1, DIGital8, DIGital9, DIGital10');
fprintf(visaObj,':WAVEFORM:SOURCE BUS2'); 
query(visaObj,':WAVEFORM:SOURce?')
%%
fprintf(visaObj,':WAVEFORM:UNSigned ON');
fprintf(visaObj, ':DIGitize BUS2');

%%
operationComplete = str2double(query(visaObj,'*OPC?'));
while ~operationComplete
    operationComplete = str2double(query(visaObj,'*OPC?'));
end

% Get the data back as a WORD (i.e., INT16), other options are ASCII and BYTE
fprintf(visaObj,':WAVEFORM:FORMAT WORD');
% Set the byte order on the instrument as well
fprintf(visaObj,':WAVEFORM:BYTEORDER LSBFirst');
% Get the preamble block
preambleBlock = query(visaObj,':WAVEFORM:PREAMBLE?');

%%
fprintf(visaObj,':WAV:DATA?');
%test2 = query(visaObj,':WAV:DATA?');
% read back the BINBLOCK with the data in specified format and store it in
% the waveform structure. FREAD removes the extra terminator in the buffer
waveform.RawData = binblockread(visaObj,'uint16'); fread(visaObj,1);
% Read back the error queue on the instrument
instrumentError = query(visaObj,':SYSTEM:ERR?');
while ~isequal(instrumentError,['+0,"No error"' char(10)])
    disp(['Instrument Error: ' instrumentError]);
    instrumentError = query(visaObj,':SYSTEM:ERR?');
end

%%
fclose(visaObj);

%%
fprintf(visaObj,':BUS2:BITS (@0:15), OFF');
fprintf(visaObj,':BUS2:BITS (@0:10), ON');
fprintf(visaObj,':BUS2:DISPlay ON');
query(visaObj,':BUS2:BITS?')


%%
test7 = str2num(test6(2:end));
test7 = test7(2:end);
%%
figure();plot(test7);

%%
%POD1 contains 8 Digital channels (D0,...,D7)

D0 = ascii_read_num(1:8:end);
D1 = ascii_read_num(2:8:end);
D2 = ascii_read_num(3:8:end);
D3 = ascii_read_num(4:8:end);
D4 = ascii_read_num(5:8:end);
D5 = ascii_read_num(6:8:end);
D6 = ascii_read_num(7:8:end);
D7 = ascii_read_num(8:8:end);

%% 
datatest = zeros(length(waveform.RawData),16);
for i = 1:length(waveform.RawData)
    datatest(i,:) = de2bi(waveform.RawData(i),16);
end

%% 
figure();
hold on
for i = 1:11
    plot(datatest(:,i)+((i-1)*2))
end
