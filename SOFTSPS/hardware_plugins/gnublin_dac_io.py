#!/usr/bin/python
# -*- coding: ascii -*-
from opensps_exceptions import *
import gnublin
import sys
from scalings import *


class GnublinDacIO:
    """
    A class to connect to the hardware of a gnublin_module_dac as a plugin of
    the openSPS-project.
    
    It should be used to set the outputs (dacs) on the modul, the actual value
    stored in the microcontroler can be read. 
    
    Attributes:
        _good (boolean): False, if during the last operation an error accourt. 
        _actual_value (int): last value, which was read.
        _modul (gnublin_module_dac): brings the funktionality the conntct to the
            hardware (from the gnublin api)
    """
    
    def __init__(self, dac_address, scaling_type, scaling_data):
        """
        Initialize the object with the actual value reading from the hardware. 
        Initialize the actual value to 0, if there is an error during reading.
        
        Args:
            relay_address (int): 0-3
        """
        self._good = True
        self._actual_value = 0
        
        self._modul = gnublin.gnublin_module_dac()
        
        self._scaler = getattr(sys.modules[__name__],
                               scaling_type)(**scaling_data)
        
        if dac_address >= 0 and dac_address <= 3:
            self._dac_address = dac_address
        else:
            raise InputError("dacAddress have to be between 0 and 3.")
        
        self.get_value()
    
    def set_value(self, to_set_value):
        computal_value = self._scaler.get_y(to_set_value)
        
        self._modul.write(self._dac_address, (int)(computal_value))
        
        if to_set_value == self.get_value():
            self._good = True
        else:
            self._good = False
        
    def get_value(self):
        computal_value = self._modul.read(self._dac_address)
        
        self._actual_value = self._scaler.get_x(computal_value)
        #self._good = True
        return self._actual_value
    
    def get_good(self):
        return self._good



