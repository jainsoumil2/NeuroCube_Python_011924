function awgOutputsOff(equip);
% awgOff(equip);
% Disables both of the AWG outputs.

fprintf(equip.awg, 'OUTP:STAT OFF');
fprintf(equip.awg, 'OUTP:IST OFF');
