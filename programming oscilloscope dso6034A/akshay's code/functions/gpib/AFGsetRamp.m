function AFGsetRamp(obj) 

freq_string = sprintf('%5.5fHz',obj.rampFreq);

if ( strcmp(obj.name,'AWG710') )
    % TEK AWG710

    % Set up AWG for triangle
    set(obj.obj,'ReferenceOscillator','EXT');
    set(obj.obj,'FunctionGeneratorFrequency',freq_string);
    set(obj.obj,'FunctionGeneratorShape','TRI');
    set(obj.obj,'FunctionGeneratorState',1);
    set(obj.obj,'FunctionGeneratorVoltAmp',obj.vStop-obj.vStart)
    set(obj.obj,'FunctionGeneratorVoltOffset',0.5*(obj.vStart+obj.vStop));
    set(obj.obj,'OutputState',1);
    set(obj.obj,'OutputIState',1);

elseif ( strcmp(obj.name,'AFG3102') )

    fprintf(obj.gpibObj,':SOURce:ROSCillator:SOURce:INT');
    
    % channel 1
    fprintf(obj.gpibObj,'SOURce1:FUNCtion RAMP');
    fprintf(obj.gpibObj,'OUTPUT1:IMPedance MAX');
    fprintf(obj.gpibObj,'SOURce1:FREQ %e',obj.rampFreq);
    fprintf(obj.gpibObj,'SOURce1:VOLTage:LEVel:IMMediate:AMPL %f',obj.vStop-obj.vStart);
    fprintf(obj.gpibObj,'SOURce1:VOLTage:LEVel:IMMediate:OFFSet %f',obj.ch1offset);

    % channel 2
    fprintf(obj.gpibObj,'SOURce2:FUNCtion RAMP');
    fprintf(obj.gpibObj,'OUTPUT2:IMPedance MAX');
    fprintf(obj.gpibObj,'SOURce2:FREQ %e',obj.rampFreq);
    fprintf(obj.gpibObj,'SOURce2:FREQency:FIXed %s',freq_string);
    fprintf(obj.gpibObj,'SOURce2:VOLTage:LEVel:IMMediate:AMPL %f',obj.vStop-obj.vStart);
    fprintf(obj.gpibObj,'SOURce2:VOLTage:LEVel:IMMediate:OFFSet %f',obj.ch2offset);
    fprintf(obj.gpibObj,'SOURce2:PHASE 180DEG');
    
    fprintf(obj.gpibObj,'OUTPUT1:STATE ON');
    fprintf(obj.gpibObj,'OUTPUT2:STATE ON');
    
%     fprintf(obj.gpibObj,'*SAV 1');
%     fprintf(obj.gpibObj,'*RCL 1');
    
%     % Set up AFG for triangle
%     set(obj.obj,'ReferenceOscillator','INT');
%     set(obj.obj,'FunctionGenerator1Frequency',freq_string);
%     set(obj.obj,'FunctionGenerator2Frequency',freq_string);
%     set(obj.obj,'FunctionGenerator1Shape','RAMP');
%     set(obj.obj,'FunctionGenerator2Shape','RAMP');
%     set(obj.obj,'FunctionGenerator1VoltAmp',obj.vStop-obj.vStart)
%     set(obj.obj,'FunctionGenerator1VoltOffset',obj.ch1offset);
%     set(obj.obj,'Output1Impedance','MAX');
%     set(obj.obj,'FunctionGenerator2VoltAmp',obj.vStop-obj.vStart)
%     set(obj.obj,'FunctionGenerator2VoltOffset',obj.ch2offset);
%     set(obj.obj,'FunctionGenerator2Phase',pi);
%     set(obj.obj,'Output1State',1);
%     set(obj.obj,'Output2State',1);
%     invoke(obj.obj,'AlignPhase');
end
