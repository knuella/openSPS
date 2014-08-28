#!/usr/bin/python
# -*- coding: ascii -*-

class InputError(Exception):
    """Exception raised for errors in the input.
    
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)


class PermissionError(Exception):
    """Exception raised, when a value can't set, because the programm which
    want to set is have not the right permissions.
    
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)


class DatabaseError(Exception):
    """Exception raised, when a value can't set, because the programm which
    want to set is have not the right permissions.
    
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)


