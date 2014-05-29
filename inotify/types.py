import ctypes

class INotifyEvent(ctypes.Structure):
    _fields_ = [
        # watch descriptor
        ('wd', ctypes.c_int32),
        
        # watch mask
        ('mask', ctypes.c_uint32),
        
        # cookie to synchronize two events
        ('cookie', ctypes.c_uint32),
        
        # length (including nulls) of name
        ('len', ctypes.c_uint32),

        # stub for possible name
        ('name', ctypes.c_char_p)]
