import smbus2  as smbus
import time

bus = smbus.SMBus(1)
addr = 0x23
reset = 0x07
con_hr_mode = 0x10


data1 = 0
data2 = 0
val = 0
light_val = 0

try:
	bus.write_byte(addr, reset)
	time.sleep(0.05)

	while True:
		bus.write_byte(addr, con_hr_mode)
		time.sleep(0.2)

		data1 = bus.read_byte(addr)
		data2 = bus.read_byte(addr)
		val = (data1 << 8) | data2
		light_val = val / 1.2

		print ('light_val = %.2f' % light_val)
		time.sleep(1)

except KeyboardInterrupt:
	# do not anything
	pass
