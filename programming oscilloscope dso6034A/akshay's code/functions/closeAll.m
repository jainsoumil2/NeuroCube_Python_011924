function closeAll()

% close open connections (e.g. GPIB)
delete(instrfind);

% unload the ok library
% if libisloaded('okFrontPanel')
% 	unloadlibrary('okFrontPanel');
% end





