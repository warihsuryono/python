from labjack import ljm

# Open first found LabJack
handle = ljm.openS("ANY", "ANY", "ANY")

# Call eReadName to read the serial number from the LabJack.
name = "AIN0"
result = ljm.eReadName(handle, name)

print("\neReadName result: ")
print("    %s = %f" % (name, result))