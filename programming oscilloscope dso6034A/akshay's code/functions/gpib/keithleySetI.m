function keithleySetI(keithley, i, complianceIn, vRangeIn, channel);
% keithleySetV(keithley, v);
% keithleySetV(keithley, v, compliance);
% Default compliance as 2V.

% If input channel is specified, assume a Keithley 2602 is being
% used; otherwise, assume Keithley 2400

compliance = 2;
vRange = 10;

if nargin>2
  compliance = complianceIn;
end

if nargin>3
    vRange = vRangeIn;
end

% for distinguising between 2602 and 2400's
if nargin<5
    channel=0;
end

if i>100e-3
    error('CURRENT IS HIGHER THAN 100mA!!');
end



% if no channel is specified, assume we are dealing with a Keithley 2400
if channel==0

%     warning('Keithley 2400 not fully tested for this function yet');
    fprintf(keithley, 'SOUR:FUNC CURR'); % make sure we're in current mode first.
    fprintf(keithley,'SOUR:CURR %.3e', i);
    fprintf(keithley,'VOLT:PROT %.3e', compliance);
    fprintf(keithley,'SENS:VOLT:RANG %.3e', vRange);
    
% otherwise, assume we are dealing with a Keithley 2602    
elseif channel=='a' || channel=='A'
    
    % make sure we are in current-source mode first
    fprintf(keithley,'smua.source.func = smua.OUTPUT_DCAMPS');
    fprintf(keithley,'smua.source.leveli = %.3e', i);
    fprintf(keithley,'smua.source.limitv = %.3e', compliance);
    fprintf(keithley,'smua.source.rangev = %.3e', vRange);

    
elseif channel=='b' || channel=='B'
    
    % make sure we are in current-source mode first
    fprintf(keithley,'smub.source.func = smub.OUTPUT_DCAMPS');
    fprintf(keithley,'smub.source.leveli = %.3e', i);
    fprintf(keithley,'smub.source.limitv = %.3e', compliance);
    fprintf(keithley,'smub.source.rangev = %.3e', vRange);
    
else
    
    error('Wrong channel type specified for Keithley 2600 series');
    
end


