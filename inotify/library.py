import ctypes
import ctypes.util
import logging

_logger = logging.getLogger(__name__)

_FILEPATH = ctypes.util.find_library('c')
if _FILEPATH is None:
    _FILEPATH = 'libc.so.6'

_logger.debug("Loading library: %s", _FILEPATH)
instance = ctypes.cdll.LoadLibrary(_FILEPATH)
