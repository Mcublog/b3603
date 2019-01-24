from time import sleep
from b3603_control import Control


def close_connect(cmdr):
    del cmdr


def main():
    cmdr = Control('COM3')  # /dev/ttyUSB0 for Linux
    if cmdr.get_status() == 0:
        return close_connect(cmdr)
    
    if cmdr.send_cmd("VOLTAGE 8000") == 0:
        return close_connect(cmdr)
    if cmdr.send_cmd("OUTPUT 1") == 0:
        return close_connect(cmdr)
    sleep(5)
    if cmdr.send_cmd("OUTPUT 0") == 0:
        return close_connect(cmdr)
        
    close_connect(cmdr)


if __name__ == '__main__':
    main()
