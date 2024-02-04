function v = keithleyGetV(keithley,channel,average,pauseDur)
% v = keithleyGetV(keithley);
% If second input channel is specified, assume a Keithley 2602 is being
% used; otherwise, assume Keithley 2400. Averaging only supported for 2600
% at the moment.

% check to see if channel is specified
if nargin==1
    channel = 0;
end

if nargin==2
    average = 1;
end

if nargin==3
    pauseDur = 0;
end

% if no channel is specified, assume we are dealing with a Keithley 2400
if channel==0

    fprintf(keithley, 'FORM:ELEM VOLT');
%     fprintf(keithley, 'INIT');
%     fprintf(keithley, 'FETCH?');
    fprintf(keithley, 'READ?');  % shorter version that INIT, FETCH
    v = fscanf(keithley, '%e');
    
% otherwise, assume we are dealing with a Keithley 2602    
elseif channel=='a' || channel=='A'
    
    if average == 1
        fprintf(keithley,'print(smua.measure.v())');
        v=fscanf(keithley, '%e');
    else
        for i=1:average
            fprintf(keithley,'print(smua.measure.v())');
            vtemp(i)=fscanf(keithley, '%e');
            pause(pauseDur);
        end
        v = mean(vtemp);
    end
    
elseif channel=='b' || channel=='B'
    
    if average == 1
        fprintf(keithley,'print(smub.measure.v())');
        v=fscanf(keithley, '%e');
    else
        for i=1:average
            fprintf(keithley,'print(smub.measure.v())');
            vtemp(i)=fscanf(keithley, '%e');
            pause(pauseDur);
        end
        v = mean(vtemp);
    end
    
else
    
    error('Wrong channel type specified for Keithley 2600 series');
    
end
