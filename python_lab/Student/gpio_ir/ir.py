import lirc
import time

sockid = lirc.init("Peri0","/etc/lirc/lircrc",blocking=False)
	
while True:
	try:
            button = lirc.nextcode()

            if len(button) == 0:
                	continue

            print(button[0])
            

	except KeyboardInterrupt:
		lirc.deinit()
		break

