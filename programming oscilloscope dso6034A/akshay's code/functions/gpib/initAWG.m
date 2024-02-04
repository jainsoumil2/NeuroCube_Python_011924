function outequip = initAWG(inequip);
% equip = initAWG(equip);
% Initializes the arbitrary waveform generator.
% The struct returned is the same as the original struct with the
% addition of the AWG GPIB handle.

outequip=inequip;

outequip.awg = gpib('ni',0,5);
fopen(outequip.awg);

disp('Initialized connection to AWG');
