function objStruct = initAFGAWG(struct);
% initializes either the AWG710 or AFG3102.
% Input is a structure that contains at least the following entries:
%   - gpibNum: indicating which gpib channel to connect to
%   - name: indicating what type of device we are connecting to


objStruct = struct;

try 

    if ( strcmp(objStruct.name,'AWG710') )
        objStruct.gpibObj = gpib('ni',0,objStruct.gpibNum);
        objStruct.obj = icdevice('tektronix_awg710.mdd',objStruct.gpibObj);
        connect(objStruct.obj);
        fprintf('Initialized connection to AWG710   on GPIB %d\n', objStruct.gpibNum);
        devicereset(objStruct.obj);
    elseif ( strcmp(objStruct.name,'AFG3102') )
        objStruct.gpibObj = gpib('ni',0,objStruct.gpibNum);
%         objStruct.obj = icdevice('tektronix_afg3102.mdd',objStruct.gpibObj);
%         objStruct.obj = icdevice('tek_afg3000.mdd',objStruct.gpibObj);
%         connect(objStruct.obj);
        fopen(objStruct.gpibObj);
        fprintf('Initialized connection to AFG3102  on GPIB %d\n', objStruct.gpibNum);
%         devicereset(objStruct.obj);
        fprintf(objStruct.gpibObj,'*RST');
        fprintf('Setting AFG3102 output1/2 impedance to INF\n');
        fprintf(objStruct.gpibObj,'OUTPUT1:IMPedance INF');
        fprintf(objStruct.gpibObj,'OUTPUT2:IMPedance INF');
    else
        error('AFG/AWG model name not found');
    end
    
catch
    rethrow(lasterror);
end


