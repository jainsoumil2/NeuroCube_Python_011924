%% Instrument Connection

% Find a VISA-USB object.
obj1 = instrfind('Type', 'visa-usb', 'RsrcName', 'USB0::0x0957::0x1734::MY44003835::0', 'Tag', '');

% Create the VISA-USB object if it does not exist
% otherwise use the object that was found.
if isempty(obj1)
    disp('Trying VISA...')
    obj1 = visa('agilent', 'USB0::0x0957::0x1734::MY44003835::0');
else
    fclose(obj1);
    obj1 = obj1(1);
end

% Connect to instrument object, obj1.
fopen(obj1);

%% Instrument Configuration and Control

% Communicating with instrument object, obj1.
data1 = query(obj1, '*IDN?');
disp(data1)

%%
data2 = query(obj1, ':MEASure:VPP?');
disp(data2)

%% Close
fclose(obj1)
delete(obj1)
clear obj1

%% From Sync example 

clear
clear all
close 
close all

% Find all previously connected instruments and close them
newobjs = instrfind;  
if isempty(newobjs) == false;
    disp('new instrument objects: ');
    newobjs
    fclose(newobjs);
    delete(newobjs);
end
clear newobjs
disp('Instrument Jobs Cleared!')
instrfind
%%
SCOPE_VISA_ADDRESS = 'USB0::0x0957::0x1734::MY44003835::0';

% Define the oscilloscope via the MATHWORKS Instument Control Toolbox
KsInfiniiVisionX = visa('agilent', SCOPE_VISA_ADDRESS); % At some point, 
% one may need to change 'agilent' to 'keysight' if MATHWORKS and/or 
% Keysight ever makes that change.

% Connect to (open) the scope
fopen(KsInfiniiVisionX);

% Clear the instrument's bus
clrdevice(KsInfiniiVisionX);

% Reset the scope if desired
% fprintf(KsInfiniiVisionX, '*RST');

% Clear the scope registers; Always stop scope before setting it up; wait
% for *OPC to come back. Always do a :STOP as a :STOP;*OPC? query
%query(KsInfiniiVisionX, '*CLS;STOP;*OPC?');

% Scope is connected and initialized; ready to accept commands or do
% something

%% Do something

Vpp = str2double(query(KsInfiniiVisionX, ':MEASure:VPP?'));
fprintf('Vpp = %d V.\n',Vpp);

%% Close the scope connection (important)

fclose(KsInfiniiVisionX);
delete(KsInfiniiVisionX);
clear KsInfiniiVisionX;

disp 'Done.'