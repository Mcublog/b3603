from time import sleep
from b3603_control import Control


def end_connect(cmdr):
	del cmdr


def main():
	cmdr = Control('COM3')
	if cmdr.connection == 0:
		return end_connect(cmdr)
	
	if cmdr.send_cmd("VOLTAGE 8000") == 0:
		end_connect(cmdr)
	if cmdr.send_cmd("OUTPUT 1") == 0:
		end_connect(cmdr)
	sleep(5)
	if cmdr.send_cmd("OUTPUT 0") == 0:
		end_connect(cmdr)
		
	end_connect(cmdr)

if __name__ == '__main__':
	main()
