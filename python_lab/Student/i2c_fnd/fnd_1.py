import smbus2 as smbus
import time

bus = smbus.SMBus(1)
addr = 0x20
config_port = 0x06
out_port = 0x02

data = (0xFC,0x60,0xDA,0xF2,0x66,0xB6,0x3E,0xE0,0xFE,0xF6)
digit = (0x7F,0xBF,0xDF,0xEF,0xF7,0xFB)

out_disp=0

try:
	bus.write_word_data(addr, config_port, 0x0000)

	for i in range (0,6,1):
		for j in range (0,10,1): 
			out_disp = data[j] << 8 | digit[i]
			bus.write_word_data(addr, out_port, out_disp)
			time.sleep(0.1)

except KeyboardInterrupt:
	pass
