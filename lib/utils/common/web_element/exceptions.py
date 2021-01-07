""" Exceptions """


class MoveToError(Exception):
    """ Failed to move to element """


class FocusToError(Exception):
    """ Failed to focus to element """


class OskOperationError(Exception):
    """ Failed to operation of OSK """


class MemoryExceeded(Exception):
    """ Set Memory Limit has been exceeded during test"""
