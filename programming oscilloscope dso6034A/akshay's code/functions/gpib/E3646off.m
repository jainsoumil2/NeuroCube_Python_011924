function E3646off(psu)
% Turns the psu on

try
    fprintf(psu,'OUTPUT OFF')
    fprintf('Keysight E3646 turned off\n');
catch
    rethrow(lasterror);
end
