function awgOn(equip);
% awgOn(equip);
% Starts the AWG running and enables both of its outputs.

fprintf(equip.awg, 'AWGC:RUN');
fprintf(equip.awg, 'OUTP:STAT ON');
fprintf(equip.awg, 'OUTP:IST ON');
