#!/usr/bin/python
# -*- coding: ascii -*-

from openspsExceptions import *
import gnublin
import sys
from scalings import *

class gnublinDacIO:
	"""
	A class to connect to the hardware of a gnublin_module_dac as a plugin of
	the openSPS-project.
	
	It should be used to set the outputs (dacs) on the modul, the actual value
	stored in the microcontroler can be read. 
	
	Attributes:
		_good (boolean): False, if during the last operation an error accourt. 
		_actualValue (int): last value, which was read.
		_modul (gnublin_module_dac): brings the funktionality the conntct to the
			hardware (from the gnublin api)
	"""
	
	def __init__(self, dacAddress, scalingType, scalingData):
		"""
		Initialize the object with the actual value reading from the hardware. 
		Initialize the actual value to 0, if there is an error during reading.
		
		Args:
			relayAddress (int): 0-3
		"""
		
		self._good = True
		self._actualValue = 0
		
		self._modul = gnublin.gnublin_module_dac()
		
		self._scaler = getattr(sys.modules[__name__],scalingType) \
													(**scalingData)
		
		if dacAddress >= 0 and dacAddress <= 3:
			self._dacAddress = dacAddress
		
		else:
			raise InputError("dacAddress have to be between 0 and 3.")
		
		self.getValue()
			
	
	def setValue(self, toSetValue):
		
		computalValue = self._scaler.getY(toSetValue)
		
		self._modul.write(self._dacAddress, (int)(computalValue))
		
		if toSetValue == self.getValue():
			self._good = True
		else:
			self._good = False
		
	
	def getValue(self):
		
		computalValue = self._modul.read(self._dacAddress)
		
		self._actualValue = self._scaler.getX(computalValue)
		#self._good = True
		return self._actualValue
	
	
	def getGood(self):
		
		return self._good



