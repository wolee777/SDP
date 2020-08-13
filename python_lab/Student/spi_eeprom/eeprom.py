import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000 # 1Mhz

WREN = 0x06
WRITE = 0x02
READ = 0x03
WRDI = 0x04 
RDSR = 0x05
WRSR = 0x01

dummy = 0
max_size = 15

try:
	spi.writebytes( [WREN] )
	time.sleep(0.001)

	buff =  [WRITE, 0x00, 0x11] 
	for i in range(max_size):
		buff.append(i)
	spi.writebytes(buff)

	time.sleep(0.001)

	spi.writebytes ( [WRDI] )
	time.sleep(0.001)

	buff = [READ, 0x00, 0x11]

	for i in range(max_size):
		buff.append(dummy)

	read = spi.xfer2( buff )
	time.sleep(0.001)
	print (read)

except KeyboardInterrupt:
	pass

spi.close()
