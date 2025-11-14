pressure = int(input("Pressure(Pa): "))
volume = float(input("Volume(m^3): "))
temperature = float(input("Temperature(K): "))
R = 8.31
print((pressure*volume)/(R*temperature))