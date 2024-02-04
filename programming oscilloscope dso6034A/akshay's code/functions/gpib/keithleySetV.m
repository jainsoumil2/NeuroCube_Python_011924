function keithleySetV(keithley, v, complianceIn, currRangeIn, channel);
% keithleySetV(keithley, v);
% keithleySetV(keithley, v, compliance);
% Default compliance as 10mA.

% If input channel is specified, assume a Keithley 2602 is being
% used; otherwise, assume Keithley 2400

compliance = 10e-3;
currRange = 10e-3;

if nargin>2
  compliance = complianceIn;
end

if nargin>3
    currRange = currRangeIn;
end

% for distinguising between 2602 and 2400's
if nargin<5
    channel=0;
end

if v>10
    warning('VOLTAGE HIGHER THAN 10V!!');
end



% if no channel is specified, assume we are dealing with a Keithley 2400
if channel==0

    fprintf(keithley, 'SOUR:FUNC VOLT'); % make sure we're in voltage mode first.    
    fprintf(keithley, 'SOUR:VOLT %.3e', v);
    fprintf(keithley, 'CURR:PROT %.3e', compliance);
    fprintf(keithley, 'SENS:CURR:RANG:AUTO OFF');   % turn off auto ranging
    fprintf(keithley, 'SENS:CURR:RANG %.3e',currRange);
    
    
% otherwise, assume we are dealing with a Keithley 2602    
elseif channel=='a' || channel=='A'
    
    % make sure we are in voltage-source mode first
    fprintf(keithley,'smua.source.func = smua.OUTPUT_DCVOLTS');
    fprintf(keithley,'smua.source.levelv = %.3e', v);
    fprintf(keithley,'smua.source.limiti = %.3e', compliance);
%     fprintf(keithley,'smua.source.rangei = %.3e', currRange);
    % autoRange on 2602's instead
    fprintf(keithley,'smua.source.autorangei = smua.AUTORANGE_ON');
    
    
elseif channel=='b' || channel=='B'
    
    % make sure we are in voltage-source mode first
    fprintf(keithley,'smub.source.func = smub.OUTPUT_DCVOLTS');
    fprintf(keithley,'smub.source.levelv = %.3e', v);
    fprintf(keithley,'smub.source.limiti = %.3e', compliance);
%     fprintf(keithley,'smub.source.rangei = %.3e', currRange);
    % autoRange on 2602's instead
    fprintf(keithley,'smub.source.autorangei = smub.AUTORANGE_ON');
    
else
    
    error('Wrong channel type specified for Keithley 2600 series');
    
end


