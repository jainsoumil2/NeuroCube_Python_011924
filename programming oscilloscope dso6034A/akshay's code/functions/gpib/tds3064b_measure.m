function [ val ] = tds3064b_measure( device, channel, type )

% Valid measurement types:
%
%   frequency
%   mean
%   period
%   peak2peak
%   crms
%   none
%   minimum
%   maximum
%   positivewidth
%   negativewidth
%   ...and others (check .mdd file)

% Note: type midedit to look at *.mdd properties!!

% Setup the oscilliscope
meas = get(device, 'Measurement');
set(meas(5), 'Source', sprintf('Channel%d', channel));
set(meas(5), 'MeasurementType', type);
val = get(meas(5), 'Value');

end

