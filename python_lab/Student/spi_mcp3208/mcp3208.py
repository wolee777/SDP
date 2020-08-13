import spidev
import time

spi = spidev.SpiDev()
spi.open(0,1)
adc_read =[0,0,0]

def analog_read(ch):
	# 12 bit 
	r = spi.xfer2([0x6 | (ch & 0x7) >> 2, ((ch & 0x7) << 6),0 ])
	adcout= ((r[1] & 0xf) << 8) + r[2]

	# 10 bit
	#r= spi.xfer2([1, (8+channel)<<4, 0])
	#ret = ((r[1]&3) << 8) + r[2]
	return adcout 
	
try:
	while 1:
		adc_read[0] = analog_read(0)
		adc_read[1] = analog_read(1)
		adc_read[2] = analog_read(2)
		print("[csd  vr  sound]")
		print(adc_read)
		time.sleep(1)
finally:
	pass
