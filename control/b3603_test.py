from time import sleep
import datetime


from b3603_control import Control


def log_cmd(func):
    def wrapper(arg):
        f = open('log.txt', 'a')
        f.write(str(datetime.datetime.now()) + '\n')
        f.write('Send cmd: ' + arg + '\n')
        ret = func(arg);
        if (ret):
            f.write('Send cmd: OK\r\n')
        else:
            f.write('Send cmd: Fail\r\n')
        return ret
    return wrapper;


def close_connect(cmdr):
    del cmdr


def main():
    cmdr = Control('COM3')  # /dev/ttyUSB0 for Linux
    if cmdr.get_status() == 0:
        return close_connect(cmdr)
        
    cmdr.send_cmd = log_cmd(cmdr.send_cmd);
    
    if cmdr.send_cmd("VOLTAGE 3300") == 0:
        return close_connect(cmdr)
    if cmdr.send_cmd("OUTPUT 1") == 0:
        return close_connect(cmdr)
    sleep(5)
    if cmdr.send_cmd("OUTPUT 0") == 0:
        return close_connect(cmdr)
        
    close_connect(cmdr)


if __name__ == '__main__':
    main()
