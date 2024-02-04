function [t, c1, c2, c3, c4] = tds3064b_waveforms( device )

[c1, t] = invoke(device.waveform, 'readwaveform', 'channel1');
[c2, t] = invoke(device.waveform, 'readwaveform', 'channel2');
[c3, t] = invoke(device.waveform, 'readwaveform', 'channel3');
[c4, t] = invoke(device.waveform, 'readwaveform', 'channel4');
