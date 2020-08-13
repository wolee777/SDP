import smbus2 as smbus
import time

bus = smbus.SMBus(1)
addr = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe
temp = 0.0
humi = 0.0
val = 0
data = [0, 0]

try:
	bus.write_byte (addr, soft_reset)
	time.sleep(0.05)

	while True:
		# temperature
		bus.write_byte(addr, cmd_temp)
		time.sleep(0.260)
		
		for i in range(0,2,1):
			data[i] = bus.read_byte(addr)

		val = data[0] << 8 | data[1]
		temp = -46.85+175.72/65536*val


		# humidity
		bus.write_byte(addr, cmd_humi)
		time.sleep(0.260)
		
		for i in range(0,2,1):
			data[i] = bus.read_byte(addr)

		val = data[0] << 8 | data[1]
		humi = -6.0+125.0/65536*val

		print ('temp : %.2f, humi : %.2f' %(temp, humi))
		time.sleep(1)

except KeyboardInterrupt:
	pass
