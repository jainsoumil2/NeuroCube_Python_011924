'''
List of API functions:
https://library.opalkelly.com/library/FrontPanelAPI/functions_func.html
'''

import ok

# okCFrontPanel is deprecated, migrating to FrontPanelDevices()
# see: https://library.opalkelly.com/library/FrontPanelAPI/migrate_fpdevices.html

devices = ok.FrontPanelDevices()

deviceCount = devices.GetCount()
print("Device Count:\t", deviceCount)

for ndx in range(deviceCount):
	print("Device Serial:\t", devices.GetSerial(ndx))

xem = devices.Open() # open the first device
if xem == None: # None
	print("ERROR!\nIs the FrontPanelGui open and connected to the board? Please close the GUI and rerun!")
else:
	print("Device Open:\t", xem.IsOpen())
	print("Board Model:\t", xem.GetBoardModel())

	info = ok.okTDeviceInfo() 
	xem.GetDeviceInfo(info)
	# https://library.opalkelly.com/library/FrontPanelAPI/structokTDeviceInfo.html#details
	print("Device Info:")
	print(info.deviceID)
	print(info.productName)

# don't need to close the device