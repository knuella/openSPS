#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import pymongo
from pymongo import MongoClient
from hardware_plugins import *

def new_analog_output:
    """ This is the template to create a new analog output with the class
    OutputDP.
    """
    {
        "name": "",
        "shortdsc": "",
        "longdsc": "",
        "path": "~/openSPS/SOFTSPS/output.py"
        "params": 
            {
                "safety_value": 
                    {
                        "shortdsc": 
                            "This value will bring no threat, when it is
                            writed to the hardware."
                        "longdsc": 
                            "This value will be set, if there is no
                            programm, which want to set an other one.",
                        "type": "input",
                        "format": "float",
                        "exclusive": "True",
                    },
                "hardware_type":
                    {
                        "shortdsc": "The name from the hardwareplugin.",
                        "longdsc": "The hardwareplugin is used to connect to the
                                    hardware.",
                        "default": "none",
                        "type": "simple",
                        "format": "string",
                        "exclusive": "gui",
                    },
                "hardware_data": 
                    {
                        "shortdsc": "The params for the hardwareplugin.",
                        "longdsc": "This data is needed by the hardwareplugin. Here
                                    also should set the scaling options.",
                        "default": {},
                        "type": "simple",
                        "format": "dictionary",
                        "exclusive": "gui",
                    },
            }


class OutputDP:
    """ OutputDP means output datapoint.
    It contains methodes to controle something outside the software, like
    setting a voltage between 0V and 10V or switching the light.
    Stores all data to indicate the datapoint, controle the hardware and
    aditional informative data.

    Attributes:
        _dp (dict): 
            all information about the datapoint
            {
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
        self._dp = 
            {
                "safety_value": safety_value,
                "actual_value": safety_value,
                "manual_override": False,
                "manual_value": safety_value,
                "state": "don't know"
            }
        self._physical_dp = getattr(
                sys.modules[__name__], hardware_type)(**hardware_data)   

        write_physical_value()
    
    def set_actual_value(self, to_set_value): 
        """ Set the value in "_dp" to the given. 
        Writes to the hardware, if manual_override is false.
        Args:
            to_set_value (dynamic): value which will be write. Depands on the
                hardware-type.
        """
        if manual_override == False: 
            self._dp['actual_value'] = to_set_value
            write_physical_value()
    
    def set_manual_value(self, to_set_value): 
        """ Set the value in "_dp" to the given. 
        Writes to the hardware, if manual_override is true.
        Args:
            to_set_value (dynamic): value which will be write. Depands on the
                hardware-type.
        """
        self._dp['manual_value'] = to_set_value
        if manual_override == True: 
            self._dp['actual_value'] = self._dp['manual_value']
            write_physical_value()
    
    def set_manual_override(self, to_set_value):
        """ Sets the value of manual_override to true or False.
        Writes to the hardware, if manual_override have changed. 
        Args:
            to_set_value (boolean): True, if the value from manual_value should
                                    be override the actual_value.
        """
        if self._dp['manual_override'] != to_set_value:
            self._dp['manual_override'] = to_set_value
            set_actual_value(self._dp['safety_value'])
            set_manual_value(self._dp['manual_value'])
    
    def write_physical_value(self):    
        """ Write the value, stord in "_dp" to hardware.
        Sets "state" to "Hardware Error, when can't writing.
        """
        i = 0
        self._physical_dp.set_value(self._dp['actual_value'])
        
        while not self._physical_dp.get_good() and i < 3:
            self._physical_dp.set_value(self._dp['actual_value'])
            i += 1
        
        if i >= 3:
            self._dp['state'] = 'Hardware Error'
        else:
            self._dp['state'] = 'good'
    
