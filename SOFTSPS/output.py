#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import opensps_exceptions
from exclusive_writebal import *
from hardware_plugins import *

def new_analog_output():
    """ This is the template to create a new analog output with the class
    OutputDP.
    """
    {
        "name": "",
        "shortdsc": "",
        "longdsc": "",
        "path": '~/openSPS/SOFTSPS/output.py',
        "params": 
            {
                "safety_value": 
                    {
                        "shortdsc": 
                            "This value will bring no threat, when it is " +
                            "writed to the hardware.",
                        "longdsc": 
                            "This value will be set, if there is no" +
                            "programm, which want to set an other one.",
                        "type": "input",
                        "format": "float",
                        "exclusive": "True",
                    },
                "hardware_type":
                    {
                        "shortdsc": "The name from the hardwareplugin.",
                        "longdsc": "The hardwareplugin is used to connect to the" + 
                                   "hardware.",
                        "default": "none",
                        "type": "simple",
                        "format": "string",
                        "exclusive": "gui",
                    },
                "hardware_data": 
                    {
                        "shortdsc": "The params for the hardwareplugin.",
                        "longdsc": "This data is needed by the hardwareplugin. Here" + 
                                   "also should set the scaling options.",
                        "default": {},
                        "type": "simple",
                        "format": "dictionary",
                        "exclusive": "gui",
                    },
            }
    }


class OutputDP:
    """ OutputDP means output datapoint.
    It contains methodes to controle something outside the software, like
    setting a voltage between 0V and 10V or switching the light.
    Stores all data to indicate the datapoint, controle the hardware and
    aditional informative data.
    
    Attributes:
        _dp (dict of name and instance): 
            all information about the datapoint
            {
                safety_value (boolean or float): 
                    This value will be set, if there is no programm, which want to
                    set an other one. This shoult bring no threat, when writed to
                    the hardware.
                actual_value (boolean or float): 
                    The value, whitch will be write to the hardware.
                state (string): 
                    The return-state from the last operation.
                manual_override (boolean): 
                    True, if the actual_value will be overridden
                    by manual_value.
                manual_value (boolean or float):
                    This value will be set to actual_value and write to the
                    hardware, when manual_override is true.
            }
            The instances itself have mostly two Attributes, value and
            exclusive. If exclusive is set to a programmname, this programm is
            the only one, whitch should set the value.

        _physical_dp (dynamic): 
            to connect to the hardware, depends on hardware_type
    """
    
    def __init__(self, safety_value, hardware_type, hardware_data):
        """ Reads the data,  is associated with the given hardwaretype.
        Creates two types of the datapoint as attributes, a dict, called _dp and a
        instance of the class given in hardware_type, called _physical_dp. The
        hardware_type is a class, programmed against the interface
        "OpenSPSHardwarePlugin".
        Args:
            safety_value (boolean or float): 
                This value will be set, if there is no programm, which want to
                set an other one. This shoult bring no threat, when writed to
                the hardware.
            
            hardware_type (string): 
                The name of the hardwareplugin, which will be used to connect
                to the hardware.
        
            hardware_data (dict):
                The params, which the hardwareplugin needs to connect to the
                hardware and write the right value.
        """
        self._dp = {
            "safety_value": ExclusiveWritebal(safety_value, "gui")
            "actual_value": ExclusiveWritebalWithManual(safety_value, False)
            "manual_override": ExclusiveWritebal(False, "gui")
            "manual_value": ExclusiveWritebal(safety_value, "gui")
            "state": "don't know"
            
        self._physical_dp = getattr(
                sys.modules[__name__], hardware_type)(**hardware_data)   
        
        self.write_physical_value()
    
    def set_exclusive(self, value, programm):
        """ Set the exclusive flag in value to the programm.
        If this flag is set, the programm is the only one,
        which can use the set_value method.
        Args:
            value (string): The name of the value, which exclusive flag will be
                            chaged.
            programmname (string): The name from the programm with exclusive
                                   writing rights.
        """
        try:
            self._dp[value].set_exclusive(programm)
        except KeyError:
            raise InputError("The value " + value + " can't be found."
        except AttributeError:
            raise InputError("The value " + value + " have ne exclusive flag."
    
    def del_exclusive(self, value, programm):
        """ Set the exclusive flag of actaul_value to false.
        Args:
            value (string): The name of the value, which exclusive flag will be
                            chaged.
            programm (string): the name from the programm with exclusive
            writing rights.
        """
        try:
            self._dp[value].del_exclusive(programm)
        except KeyError:
            raise InputError("The value " + value + " can't be found."
        except AttributeError:
            raise InputError("The value " + value + " have ne exclusive flag."
    
    def set_actual_value(self, programm, to_set_value): 
        """ Set the value in "_dp" to the given. 
        Writes to the hardware, if manual_override is false.
        Args:
            programmname (string): the programm, which want to set the value. 
            to_set_value (dynamic): value which will be write. Depands on the
                                    hardware-type.
        """
        if self._dp['manual_override'].get_value() == False: 
            self._dp[value].set_value(programm, to_set_value)
            self.write_physical_value()
        else:
            raise PermissionError("The actual value is actualy overrided by manual_value.")
    
    def set_manual_value(self, programm, to_set_value): 
        """ Set the value in "_dp" to the given. 
        Writes to the hardware, if manual_override is true.
        Args:
            programm (string): the programm, which want to set the value. 
            to_set_value (dynamic): value which will be write. Depends on the
                                    hardware-type.
        """
        self._dp['manual_value'].set_value(programm, value)
        if self._dp['manual_override'].get_value() == True: 
            self._dp['actual_value'].set_value("manual",
                                               self._dp['manual_value'].get_value())
            self.write_physical_value()
    
    def set_manual_override(self, programm, to_set_value):
        """ Sets the value of manual_override to true or False.
        Writes to the hardware, if manual_override have changed. 
        Args:
            programm (string): the programm, which want to set the value. 
            to_set_value (boolean): True, if the value from manual_value should
                                    be override the actual_value.
        """
        self._dp['manual_override'].set_(programm, value)
        if self._dp['manual_override'].get_value() == True: 
            self._dp['actual_value'].set_exclusive_to_manual()
            self._dp['actual_value'].set_value("manual",
                                               self._dp['manual_value'].get_value())
            self.write_physical_value()
        else:
            self._dp['actual_value'].set_value("manual",
                                               self._dp['safety_value'].get_value())
            self._dp['actual_value'].del_exclusive("manual")
            self.write_physical_value()
    
    def write_physical_value(self):    
        """ Write the value, stord in "_dp" to hardware.
        Sets "state" to "Hardware Error, when can't writing.
        """
        i = 0
        self._physical_dp.set_value(self._actual_value['value'])
        
        while not self._physical_dp.get_good() and i < 3:
            self._physical_dp.set_value(self._actual_value['value'])
            i += 1
        
        if i >= 3:
            self._state = 'Hardware Error'
        else:
            self._state = 'good'
 
