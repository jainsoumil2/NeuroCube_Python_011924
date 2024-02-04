function keithley = initKeithley(gpibNum,channelNum);
% keithley = initKeithley(gpibNum);
% Initializes the Keithely connected to gpibNum

try
    keithley = gpib('ni', channelNum, gpibNum);
    fopen(keithley);
%     fprintf(keithley,'*RST');
    fprintf('Initialized connection to Keithley on GPIB %d\n', gpibNum);
catch
    rethrow(lasterror);
end
