# lab12_i2c
import RPi.GPIO as GPIO
import smbus2 as smbus
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


# FOR I2C TEMP & HUMIDITY
bus = smbus.SMBus(1)
th_addr = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe
temp = 0.0
humi = 0.0
th_val = 0
th_data = [0, 0]

# FOR I2C LIGHT SENSOR
light_addr = 0x23
reset = 0x07
con_hr_mode = 0x10

light_data1 = 0
light_data2 = 0
light_val = 0

def get_temp_value():
        # temperature
        bus.write_byte(th_addr, cmd_temp)
        time.sleep(0.260)

        for i in range(0,2,1):
            th_data[i] = bus.read_byte(th_addr)

        th_val = th_data[0] << 8 | th_data[1]
        temp = -46.85+175.72/65536*th_val
        return temp
    
def get_humi_value():    
	# humidity
	bus.write_byte(th_addr, cmd_humi)
	time.sleep(0.260)
	
	for i in range(0,2,1):
            th_data[i] = bus.read_byte(th_addr)

	th_val = th_data[0] << 8 | th_data[1]
	humi = -6.0+125.0/65536*th_val
	return humi

def get_light_value():
        #light
    	bus.write_byte(light_addr, con_hr_mode)
    	time.sleep(0.2)
    	light_data1 = bus.read_byte(light_addr)
    	light_data2 = bus.read_byte(light_addr)
    	light_val = (light_data1 << 8) | light_data2
    	light_val = light_val / 1.2
    	return light_val

    
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
  
    while True :

        val1 = get_temp_value()

        val2 = get_humi_value()
        print('temp : %.2f ' %val1,' humi : %.2f' %val2)

        lcd_string('T:'+ format(val1,'.2f') + ' H:' + format(val2,'.2f'),LCD_LINE_1)

        val3 = get_light_value()
        print('light : %.2f' %val3)
        lcd_string('L:'+ format(val3,'.2f') ,LCD_LINE_2)
        
            
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
