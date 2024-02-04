function AFG = AFGconfigARB(AFG)

% set oscillator reference to external
fprintf(AFG.gpibObj,'SOURce:ROSCillator:SOURce EXT');

% set trigger to external
fprintf(AFG.gpibObj,'TRIGger:SEQuence:SOURce EXT');

% channel 1
fprintf(AFG.gpibObj,'SOURce1:FUNCtion EMEMory');
fprintf(AFG.gpibObj,'SOURce1:FREQ %e',AFG.freq);
fprintf(AFG.gpibObj,'SOURce1:VOLTage:LEVel:IMMediate:AMPL %f',AFG.amp);
fprintf(AFG.gpibObj,'SOURce1:VOLTage:LEVel:IMMediate:AMPL?');
amp = fscanf(AFG.gpibObj,'%e');
if (round(AFG.amp*1e3) ~= round(amp*1e3))
    error('desired AFG amplitude: %5.3f, actual: %5.3f',AFG.amp, amp);
%     fprintf('desired AFG amplitude: %5.3f, actual: %5.3f\n',AFG.amp, amp);
end
if ((AFG.amp + AFG.ch1offset) > 1.8)
    error('AFG amplitude + offset larger than 1.8V!!!!');
end
fprintf(AFG.gpibObj,'SOURce1:VOLTage:LEVel:IMMediate:OFFSet %f',AFG.ch1offset);
fprintf(AFG.gpibObj,'SOURce1:BURSt:STATE ON');
fprintf(AFG.gpibObj,'SOURce1:BURSt:MODE TRIG');
fprintf(AFG.gpibObj,'SOURce1:BURSt:NCYCles %s',AFG.nCycles);
fprintf(AFG.gpibObj,'OUTPUT1:STATE ON');

% channel 2
fprintf(AFG.gpibObj,'SOURce2:FUNCtion EMEMory');
fprintf(AFG.gpibObj,'SOURce2:FREQ %e',AFG.freq);
fprintf(AFG.gpibObj,'SOURce2:VOLTage:LEVel:IMMediate:AMPL %f',AFG.amp);
fprintf(AFG.gpibObj,'SOURce2:VOLTage:LEVel:IMMediate:AMPL?');
amp = fscanf(AFG.gpibObj,'%e');
if (round(AFG.amp*1e3) ~= round(amp*1e3))
    error('AFG amplitude not appropriate!\n');
end
fprintf(AFG.gpibObj,'SOURce2:VOLTage:LEVel:IMMediate:OFFSet %f',AFG.ch2offset);
fprintf(AFG.gpibObj,'SOURce2:BURSt:STATE ON');
fprintf(AFG.gpibObj,'SOURce2:BURSt:MODE TRIG');
fprintf(AFG.gpibObj,'SOURce2:BURSt:NCYCles %s',AFG.nCycles);
fprintf(AFG.gpibObj,'OUTPUT2:POLARITY INV');
fprintf(AFG.gpibObj,'OUTPUT2:STATE ON');
