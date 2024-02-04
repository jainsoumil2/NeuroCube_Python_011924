function awgOff(equip);
% awgOff(equip);
% Stops the AWG and disables both of its outputs.

fprintf(equip.awg, 'AWGC:STOP');
fprintf(equip.awg, 'OUTP:STAT OFF');
fprintf(equip.awg, 'OUTP:IST OFF');
