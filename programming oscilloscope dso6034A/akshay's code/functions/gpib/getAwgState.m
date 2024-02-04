function state = getAwgState(equip);
% state = getAwgState(equip);
% Returns the current status of the AWG.
% The state is a struct with elements
%   state.f = AWG sampling frequency
%   state.func = AWG function name
%   state.v = AWG voltage amplitude

if ~isOpen(equip.awg)
  state = struct('f',0,'func','', 'v', 0);
else
  fprintf(equip.awg, 'FUNC:USER?');
  state = struct('func',fscanf(equip.awg));
  
  fprintf(equip.awg, 'FREQ?');
  state.f = fscanf(equip.awg, '%e');
  
  fprintf(equip.awg, 'VOLT?');
  state.v = fscanf(equip.awg, '%e');
  
end
