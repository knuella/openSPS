#!/usr/bin/python
# -*- coding: ascii -*-

from openspsExceptions import *
import gnublin

class gnublinRelayIO:
	"""
	A class to connect to the hardware of a gnublin_relay_modul as a plugin of
	the openSPS-project.
	
	It should be used to set the outputs (relays) on the modul, the actual value
	stored in the microcontroler can be read. 
	
	Attributes:
		_good (boolean): False, if during the last operation an error accourt. 
		_actualValue (int): last value, which was read.
		_modul (gnublin_modul_relay): brings the funktionality the conntct to the
			hardware (from the gnublin api)
	"""
	
	def __init__(self, modulAddress, relayAddress):
		"""
		Initialize the object with the actual value reading from the hardware. 
		Initialize the actual value to 0, if there is an error during reading.
		
		Args:
			modulAddress (int): hexadecimal z.B. 0x20
			relayAddress (int): 1-4
		"""
		
		self._good = False
		self._actualValue = 0
		
		self._modul = gnublin.gnublin_module_relay()
		self._modul.setAddress(modulAddress)
		if relayAddress >= 1 and relayAddress <= 4:
			self._relayAddress = relayAddress
		else:
			raise InputError("relayAddress have to be between 1 and 4.")
		
		self.getValue()
			
	
	def setValue(self, toSetValue):
		
		if self._modul.switchPin(self._relayAddress, toSetValue) != -1:
			self._good = True
		else:
			self._good = False

	
	def getValue(self):
		
		value = self._modul.readState(self._relayAddress)
		if value != -1:
			self._actualValue = value
			self._good = True
			return self._actualValue
		else:
			self._good = False
	
	
	def getGood(self):
		
		return self._good



