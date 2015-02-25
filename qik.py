###
 # Author			: E J Jonkers
 # date created		: 22-02-15
 #
 # Python class for Pololu's qik motor controllers
 # Written for the Qik2s9v1 but Qik2s12v10 should be compatible(not tested)
 # For more info see the README file.
 # Pololu documentation https://www.pololu.com/docs/0J25
 #
###

import serial

class Controller:
	def __init__(self):
		self.debug = False
#		self.ser = serial.Serial('/dev/ttyS0', 9600)		# default linux first serial port
		self.ser = serial.Serial('/dev/ttyAMA0', 9600)		# Raspberry pi first serial port
		self.pololuStartByte = chr(0xAA)
		self.deviceId = chr(0x09)
		self.pololuProtocol = self.pololuStartByte + self.deviceId
		self.highSpeedResolution = False
	def setDebug(on=True):
		self.debug = on
	def setDeviceId(self, deviceId):
		self.deviceId = deviceId
		self.pololuProtocol = self.pololuStartByte + self.deviceId
	def __testBinairyInput(self, i):
		if i != 0 and i != 1:
			return False
		return True
	def __testMotorInput(self, motor):
		if not self.__testBinairyInput(motor):
			if self.debug:
				print "motor (%s) is not 0 or 1" % motor
			return False
		return True
	def __testParameterNumber(self, parameterNumber):
		if parameterNumber < 0 or parameterNumber > 3:
			if self.debug:
				print "parameterNumber (%s) is not 0,1,2,3" % parameterNumber
			return False
		return True
	def setSpeed(self, motor, reverse, speed):
		# m0 forward low command byte = 0x08
		# m0 forward high command byte = 0x09
		# m0 reverse low command byte = 0x0A
		# m0 reverse high command byte = 0x0B
		# m1 forward low command byte = 0x0C
		# m1 forward high command byte = 0x0D
		# m1 reverse low command byte = 0x0E
		# m1 reverse high command byte = 0x0F
		# Hmmm let's do it like this
		# [motor][revers][high] 
		#		[0][0][0] = 0x08
		#		[0][0][1] = 0x09
		#		[0][1][0] = 0x0A
		#		[0][1][1] = 0x0B
		#		[1][0][0] = 0x0C
		#		[1][0][1] = 0x0D
		#		[1][1][0] = 0x0E
		#		[1][1][1] = 0x0F

		if not self.__testMotorInput(motor):
			return False
		if not self.__testBinairyInput(reverse):
			if self.debug:
				print "reverse (%s) is not 0 or 1" % reverse
			return False
		if speed < 0 or speed > 255:
			if self.debug:
				print "speed (%s) is not between 0 and 256" % speed
			return False
		command = 0x08 + motor*0x04 + reverse*0x02 + self.highSpeedResolution
		self.ser.write(self.pololuProtocol + chr(command) + chr(speed))
		self.ser.flush()
		return True
	def coast(self, motor):
		if not self.__testMotorInput(motor):
			return False
		command = 0x06 + motor
		self.ser.write(self.pololuProtocol + chr(command))
		return True
	def setParameter(self, parameterNumber, value):
		# TODO test 'value'
		if not self.__testParameterNumber(parameterNumber):
			return False
		command = chr(0x04)+chr(parameterNumber)+chr(value)+chr(0x55)+chr(0x2A)
		self.ser.write(self.pololuProtocol + command)
		return True
	def getParameter(self, parameterNumber):
		if not self.__testParameterNumber(parameterNumber):
			return False
		command = chr(0x03)+chr(parameterNumber)
		self.ser.write(self.pololuProtocol + command)
		return ord(self.ser.read())
	def getErrorByte(self):
		self.ser.write(self.pololuProtocol + chr(0x02))
		return ord(self.ser.read(1))
	def getError(self):
		errorByte = self.getErrorByte()
		if errorByte == 8:
			print "Data Overrun Error (serial receive buffer is full)"
		if errorByte == 16:
			print "Frame Error (a bytes stop bit is not detected, This error can occur if you are communicating at a baud rate that differs from the qiks baud rate)"
		if errorByte == 32:
			print "CRC Error (CRC-enable jumper is in place and computed CRC failed)"
		if errorByte == 64:
			print "Format Error (command byte does not match a known command or data bytes are outside of the allowed range, etc)"
		if errorByte == 128:
			print "Timeout (if enabled, serial timeout)"
	def getFirmware(self):
		self.ser.write(self.pololuProtocol + chr(0x01))
		return self.ser.read(1)
