import serial
import time

debug = 0  # Print debug message
info_msg = 1  # Print info message

class Control:
	__port = serial.Serial()
	connection = False  # Connection property

	def __init__(self, port):
		self.__port.baudrate = 38400
		self.__port.port = port
		self.__port.timeout = 1
		# Open Com
		try:
			self.__port.open()
			print("Port is open")
			self.connection = True			
		except IOError:
			self.__connection_fail("Can't open port")

	def __del__(self):
		self.__connection_fail('')
	
	# Print info message
	def _iprint(self, msg: str):
		if info_msg:
			print(msg)

	def __connection_fail(self, msg: str):
		print(msg)
		self.connection = False
		if self.__port.is_open:
			self._iprint("Port close")
			self.__port.close()

	# Send B3603 command
	# return: array of strings or array with zero lenght
	def send_cmd(self, cmd):
		ack = []
		if self.connection == True:  # dummy protection
			if cmd.endswith('\n') == False:
				cmd = cmd + '\n'
			self.__port.write(cmd.encode())
			self._iprint('B3603 Send cmd: ' + cmd.replace('\n', ''))
			ack = self.__read_ack()
			if debug:
				self.print_ack(ack)
		if ack:
			self._iprint('B3603 Cmd: OK' )
		else:
			self._iprint('B3603 Cmd: Error' )
		return ack[:]

	# Print B3603 ACK
	def print_ack(self, data: []):
		if data:
			print('B3603 ACK:')
			for s in data:
				print(s)

	# Read B3603 ACK from port
	# return: array of strings or array with zero lenght
	def __read_ack(self):
		for i in range(5):  # Waiting 500 ms
			if self.__port.in_waiting:
				break
			time.sleep(.1)  # Waiting 100 ms
		data = []
		while self.__port.in_waiting:
			s: str = self.__port.readline().decode('utf-8')
			s = s.replace('\r\n', '')
			data.append(s)  # Remove \r\n
		return data[:]
