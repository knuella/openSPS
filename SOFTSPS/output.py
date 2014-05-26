#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import pymongo
from pymongo import MongoClient
from hardware_plugins import *


class OutputDP:
    """ OutputDP means output datapoint.
    It contains methodes to controle something outside the software, like
    setting a voltage between 0V and 10V or switching the light.
    Stores all data to indicate the datapoint, controle the hardware and
    aditional informative data.

    Attributes:
        _client (MongoClient): to conntect to the mongoDB
        _outputs (MongoDB collection): the used mongoDB collection
        _dp (dict): all information about the datapoint 
        _physical_dp (dynamic): to connect to the hardware, depends on
            hardware_type
    """

    def __init__(self, dp_name):
        """ Reads the data,  is associated with the given dp_name from
        the mongo Database.

        Creates two types of the datapoint as attributes, a dict ("_dp") and a
        instance of the class given in "hardware_type" ("_physical_dp"). The
        hardware_type is a class, programmed against the interface
        "OpenSPSHardwarePlugin".

        Args:
            dp_name (string): name of the datapoint in the database

        Raise: 
            InputError, when the given dp_name can't found.
        """
        self._client = MongoClient()
        self._outputs = self._client.ios.outputs
        
        self._dp = self._outputs.find_one({'name': dp_name})
        if self._dp == None:
            raise InputError("Can't find DP with the Name " + dp_name)
        
        self._physical_dp = getattr(
                sys.modules[__name__],
                self._dp['hardware_type'])(**self._dp['hardware_data'])   
    
    def set_value(self, to_set_value): 
        """ Set the value in "_dp" to the given. 
        Args:
            to_set_value (dynamic): value which will be write. Depands on the
                hardware-type.
        """
        self._dp['actual_value'] = to_set_value
    
    def write_physical_value(self):    
        """ Write the value, stord in "_dp" to hardware.
        TODO: Writes only, if the values have bigger differents, than specified
        in "cov" or have changed (strings, boolean).
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
    
    def update_to_db(self):
        """ Write the value and state, stord in "_dp" to database.
        TODO: Writes only, if the values have bigger differents, than specified
        in "cov" or have changed (strings, boolean).
        """
        self._outputs.update(
            {'_id': self._dp['_id']}, 
            {'$set': 
                {
                    'state': self._dp['state'], 
                    'actual_value': self._dp['actual_value']
                }
            })


