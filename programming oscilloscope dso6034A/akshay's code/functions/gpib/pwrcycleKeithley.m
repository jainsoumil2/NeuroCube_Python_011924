function pwrcycleKeithley(kly, voltage, varargin);

if (size(varargin,2) > 0)
    compl = varargin{1};
end

keithleyOff(kly);
pause(2);
keithleyOn(kly);
keithleySetV(kly, voltage, compl);
pause(2);
