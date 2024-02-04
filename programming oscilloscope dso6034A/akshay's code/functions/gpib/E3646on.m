function E3646on(psu)
% Turns the psu on

try
    fprintf(psu,'OUTPUT ON')
    fprintf('Keysight E3646 turned on\n');
catch
    rethrow(lasterror);
end
