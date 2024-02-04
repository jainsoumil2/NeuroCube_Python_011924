function printStatusAWG(equip);
% printStatusAWG(equip);
% Prints the status of the AWG

fprintf('AWG (%s)\n', get(equip.awg,'Name'));

if ~isOpen(equip.awg)
  fprintf('\tCLOSED\n');
else
  fprintf(equip.awg, 'FUNC:USER?');
  fprintf('\tFunction = %s\n', fscanf(equip.awg));
  
  fprintf(equip.awg, 'FREQ?');
  f = fscanf(equip.awg, '%e')/1e9;
  
  fprintf(equip.awg, 'VOLT?');
  v = round(fscanf(equip.awg, '%e')*1000);
  
  fprintf(equip.awg, 'AWGC:RST?');
  r = fscanf(equip.awg, '%d');
  if r == 0
    runstop = 'Stopped';
  elseif r == 2
    runstop = 'Running';
  end
  
  fprintf(equip.awg, 'OUTP:STAT?');
  on1 = fscanf(equip.awg, '%d');
  fprintf(equip.awg, 'OUTP:IST?');
  on2 = fscanf(equip.awg, '%d');
  
  fprintf('\tf = %4.2f GHz,  V = %3d mV,  %7s (%d/%d)\n',...
      f, v, runstop, on1, on2);
end
