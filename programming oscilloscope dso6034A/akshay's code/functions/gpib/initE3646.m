function psu = initE3646(gpibCh, gpibNum);
% Initializes a Keysight E3646 connected to gpibNum

try
    psu = gpib('ni', gpibCh, gpibNum);
    fopen(psu);
    fprintf(psu,'*RST');
    fprintf('Initialized connection to Keysight E3646 on GPIB %d\n', gpibNum);
catch
    rethrow(lasterror);
end
