# lab14_eeprom
import RPi.GPIO as GPIO
import spidev
import time

# Define GPIO to LCD mapping
LCD_RS = 23
LCD_E  = 26 
LCD_D4 = 17
LCD_D5 = 18
LCD_D6 = 27
LCD_D7 = 22


# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

spi = spidev.SpiDev()

WREN = 0x06
WRITE = 0x02
READ = 0x03
WRDI = 0x04 
RDSR = 0x05
WRSR = 0x01

def analog_read(ch):
	# 12 bit 
	r = spi.xfer2([0x6 | (ch & 0x7) >> 2, ((ch & 0x7) << 6),0 ])
	adcout= ((r[1] & 0xf) << 8) + r[2]

	return adcout 

def get_cds_value():
        return analog_read(0)

def get_vr_value():
        return analog_read(1)

def get_sound_value():
        return analog_read(2)

def read_eeprom_data(buf):
	read = spi.xfer2( buf )
	time.sleep(0.001)
	return read
	
    
def write_eeprom_data(buf):
        spi.writebytes( [WREN] )
        time.sleep(0.001)
        spi.writebytes(buf)
        time.sleep(0.001)
        spi.writebytes ( [WRDI] )
        time.sleep(0.001)

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7

    # Initialise display
    lcd_init()
    
    buf =  [WRITE, 0x00, 0x11,0,0,0,0,0,0]

    while True :
        
        spi.open(0,1)
        
        val1 = get_cds_value()
        val2 = get_vr_value()

        val3 = get_sound_value()

        buf[3] = val1 & 0xff
        buf[4] = val1 >> 8
        
        buf[5] = val2 & 0xff
        buf[6] = val2 >> 8

        buf[7] = val3 & 0xff
        buf[8] = val3 >> 8

        spi.close()

        spi.open(0,0)
        spi.max_speed_hz = 1000000 # 1Mhz
        
        buf[0] = WRITE
        buf[1] = 0x00
        buf[2] = 0x11

        write_eeprom_data(buf)

        print('WRITE :',buf[3:8])

        buf[0] = READ
        
        buf = read_eeprom_data(buf)

        val1 = buf[3] + (buf[4]<<8)
        val2 = buf[5] + (buf[6]<<8)
        val3 = buf[7] + (buf[8]<<8)
        
        print('READ  :',buf[3:8],'\n')
        
        lcd_string('CdS:'+ format(val1,'d') + ' VR:' + format(val2,'d'),LCD_LINE_1)
        lcd_string('Sound :'+ format(val3,'d') ,LCD_LINE_2)
        
        spi.close()
        time.sleep(0.5)
        
            
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
