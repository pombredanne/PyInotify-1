import ctypes

import inotify.library

_lib = inotify.library.instance

def _check_int_result(value):
    if value < 0:
        raise ValueError("Function returned failure: %d" % (value))

    return value

inotify_init = _lib.inotify_init
inotify_init.argtypes = []
inotify_init.restype = _check_int_result

inotify_init1 = _lib.inotify_init1
inotify_init1.argtypes = [ctypes.c_int]
inotify_init1.restype = _check_int_result

inotify_add_watch = _lib.inotify_add_watch
inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_void_p, c_uint32]
inotify_add_watch.restypes = _check_int_result

inotify_rm_watch = _lib.inotify_rm_watch
inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]
inotify_rm_watch.restype = _check_int_result
