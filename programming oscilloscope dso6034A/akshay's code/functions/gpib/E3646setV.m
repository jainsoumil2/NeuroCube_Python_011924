function E3646setV(psu,channelNum,voltage,currLim,voltLim)
% Sets output voltage of Keysight E3646 connected to gpibNum
% channelNum = 'OUT1' or 'OUT2'

try
    fprintf(psu,sprintf('INST:SEL %s',channelNum))
    fprintf(psu,sprintf('APPLy %.3e, %.3e',voltage,currLim))
    fprintf(psu,'TRIG:SOUR IMM')
    fprintf(psu,'SYSTem:CLICk:VOLume SOFT')  %
    fprintf(psu,'SYSTem:TICK:STATe OFF')  %
    fprintf(psu,sprintf('VOLT:PROT %.3e',voltLim))
    fprintf(psu,'VOLT:PROT:STAT ON')
    fprintf('Set Keysight E3646 voltage to %.3eV, %.3eA, %.3eV\n',...
        voltage,currLim,voltLim);
catch
    rethrow(lasterror);
end
