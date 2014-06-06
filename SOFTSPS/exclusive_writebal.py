#!/usr/bin/python
# -*- coding: ascii -*-
import opensps_exceptions


class ExclusiveWritebal(object):
    """ ExclusiveWritebal extends normal variables, to bring the functionalyt
    of writng controle. If you want to write the value, you have to give the
    string stored in exclusive.
    This is not a security function, but a control function, when all programms
    accept the methodes.
    Attributes:
        _exclusive (string): False, if everyone can write the variable, else
                             the given string have to match for writing.
        _value (dynamic): the value of the variable
    """
    def __init__(self, exclusive, value):
        """ Initializiate with the givven arguments.
        Args:
            exclusive (string or false): will be set to _exclusive
            value (dynamic): will be set to _value
        """
        self._value = value
        self._exclusive = exclusive
    
    def get_value(self):
        """ Returns the value. """
        return self._value
    
    def set_value(self, exclusive, new_value):
        """ Set the value, if exclusive is matching to _exclusive or _exclusite is False, else:
        Raise:
            PermissionError
        """
        if self._exclusive == False or \
           self._exclusive == exclusive:
            self._value = new_value
        else:
            raise PermissionError("The programm "+ self._exclusive + 
                                  " have exclusive writing rights on this value.")
    
    def get_exclusive(self):
        """ Return the exclusive string. """
        return self._exclusive
    
    def set_exclusive(self, new_exclusive):
        """ Set the _exclusive stringi to new_exclusive, if _exclusite is
        False, else:
        Raise:
            PermissionError
        """
        if self._exclusive != new_exclusive:
            if self._exclusive == False:
                self._exclusive = new_exclusive
            else:
                raise PermissionError("The exclusive flag is already set by " +
                                      self._exclusive + 
                                      " and should be only canged by this programm.")
    
    def del_exclusive(self, exclusive):
        """ Set the _exclusive string to False, if _exclusite is matching
        exclusive, else:
        Raise:
            PermissionError
        """
        if self._exclusive == exclusive:
            self._exclusive = False
        else:
            raise PermissionError("The exclusive flag is set by " + self._exclusive + 
                                  " and should be only reset by this programm.")


class ExclusiveWritebalWithManual(exclusive_writebal):
    """ The exclusive_writebal class with a function for set exclusive to
    manual without control.
    """
    def set_excluisve_to_manual(self):
        """ Set the _exclusive string to manual. """
        self._exclusive = "manual"
