function printStatusKeithley(keithley,supply);
% printStatusKeithley(keithley,supply);
% Prints the status of the keithley unit who is attached to the
% named supply.

fprintf('%s (%s)\n', supply, get(keithley,'Name'));

%if ~isOpen(keithley)
%  fprintf('\tCLOSED\n');
%else

  fprintf(keithley, 'SOUR:VOLT?');
  v = fscanf(keithley, '%e');
  fprintf(keithley, 'OUTP:STAT?');
  onoff = fscanf(keithley, '%d');
 
  if onoff == 1
      i = keithleyGetI(keithley)*1e6;
  else
      i = 0;
  end
  fprintf(keithley, 'CURR:PROT?');
  iComp = fscanf(keithley, '%e')*1e3;
  
  fprintf('\tV = %4.3f V    I = %6.3f uA    (comp = %5.2f mA)', v, i, iComp);

   if onoff == 1
    fprintf('  ON\n');
  else
    fprintf('  OFF\n');
  end

%end
