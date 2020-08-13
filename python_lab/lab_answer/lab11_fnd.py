# lab11_fnd
import smbus2 as smbus
import time

bus = smbus.SMBus(1)
addr = 0x20
config_port = 0x06
out_port = 0x02

data = (0xFC,0x60,0xDA,0xF2,0x66,0xB6,0x3E,0xE0,0xFE,0xF6)
digit = (0x7F,0xBF,0xDF,0xEF,0xF7,0xFB)

out_disp=0

def display_fnd(num,i):
        out_disp = data[num] << 8 | digit[i]
        bus.write_word_data(addr, out_port, out_disp )

try:
    bus.write_word_data(addr, config_port, 0x0000)
    
    while True :
        
        cur_time = time.ctime()   #  'Fri May 26 16:08:56 2017'
        hour = cur_time[11:13]    # slicing hour:minute:second
        minute = cur_time[14:16]
        second = cur_time[17:19]   
        strtime = hour + minute + second
        
        for i in range(0,6):
            num = int(strtime[i])
            display_fnd(num,i)
            #time.sleep(0.003)
            time.sleep(0.001)
            
except KeyboardInterrupt:
	pass

