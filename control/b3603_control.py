import serial
import time

debug = 0  # Print debug message
info_msg = 1  # Print info message

class Control:
    

    def __init__(self, port):
        self.__port = serial.Serial()
        self.__port.baudrate = 38400
        self.__port.port = port
        self.__port.timeout = 1
        self.__connection = False  # Connection property
        # Open Com
        try:
            self.__port.open()
            print("B3603 " + self.__port.port + " port is open")
            self.__connection = True            
        except IOError:
            self.__close_connect("Can't open port")


    def __del__(self):
        self.__close_connect()
    
    
    # Print info message
    def __iprint(self, msg: str):
        if info_msg:
            print(msg)


    def __close_connect(self, msg: str = 'B3603 Commander stop'):
        print(msg)
        self.__connection = False
        if self.__port.is_open:
            self.__iprint("B3603 " + self.__port.port + " port close")
            self.__port.close()


    # Send B3603 command
    # return: array of strings or array with zero lenght
    def send_cmd(self, cmd):
        ack = []
        if self.__connection == True:  # dummy protection
            if cmd.endswith('\n') == False:
                cmd = cmd + '\n'
            self.__port.write(cmd.encode())
            self.__iprint('B3603 Send cmd: ' + cmd.replace('\n', ''))
            ack = self.__read_ack()
            if debug:
                self.print_ack(ack)
        if ack:
            self.__iprint('B3603 Cmd: OK' )
        else:
            self.__iprint('B3603 Cmd: Error')
            return 0
        return ack


    # Print B3603 ACK
    def print_ack(self, data: []):
        if data:
            print('B3603 ACK:')
            for s in data:
                print(s)


    # Get connection status
    # return: true if connect
    def get_status(self):
        return self.__connection
        
        
    # Read B3603 ACK from port
    # return: array of strings or array with zero lenght
    def __read_ack(self):
        for i in range(500):  # Waiting 500 ms maximum
            if self.__port.in_waiting:
                break
            time.sleep(.1)  # Waiting 100 ms
        if not self.__port.in_waiting:
            print('Cmd was sent, but no response')
            return
        data = []
        while self.__port.in_waiting:
            s: str = self.__port.readline().decode('utf-8')
            s = s.replace('\r\n', '')
            data.append(s)  # Remove \r\n
        return data
