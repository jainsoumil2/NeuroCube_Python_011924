function keithleyOff(keithley,channel);
% keithleyOff(keithley);
% Disables the output for the Keithley.
% Note that this disables both outputs for 2400. 
% If second input channel is specified, assume a Keithley 2602 is being
% used; otherwise, assume Keithley 2400


% check to see if channel is specified
if nargin==1
    channel = 0;
end



% if no channel is specified, assume we are dealing with a Keithley 2400
if channel==0

    fprintf(keithley, 'OUTP 0');
    
% otherwise, assume we are dealing with a Keithley 2602    
elseif channel=='a' || channel=='A'
    
    fprintf(keithley,'smua.source.output = smua.OUTPUT_OFF')
    
elseif channel=='b' || channel=='B'
    
    fprintf(keithley,'smub.source.output = smua.OUTPUT_OFF')
    
else
    
    error('Wrong channel type specified for Keithley 2600 series');
    
end
