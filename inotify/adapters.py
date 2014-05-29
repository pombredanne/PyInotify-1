import os
import select
import logging

import inotify.calls

_logger = logging.getLogger(__name__)

def _inotify_init():
    return inotify.calls.inotify_init()

def _inotify_init1(flags=0):
    return inotify.calls.inotify_init1(flags)

def _inotify_add_watch(fd, pathname, mask):
    return inotify.calls.inotify_add_watch(fd, pathname, mask)

def _notify_rm_watch(fd, wd):
    return inotify.calls.inotify_rm_watch(fd, wd)


class Inotify(object):
    def __init__(self, flags=0):
        self.__fd = None
        self.__flags = flags
        self.__watches = {}

    def __del__(self):
        if self.__fd is not None:
            self.close()

    def open(self):
        _logger.debug("Opening inotify.")

        if self.__fd is not None:
            raise ValueError("We already have a notify handle.")

        self.__fd = _inotify_init1(self.__flags)
        self.__e = select.epoll() 

    def close(self):
        _logger.debug("Closing inotify (%d).", self.__fd)

        if self.__fd is not None:
            raise ValueError("Notify handle is already closed.")

        for wd in self.__watches.keys():
            self.__rm_watch(wd)
        
        os.close(self.__fd)
        self.__fd = None

    def __enter__(self):
        self.open()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __eq__(self, o):
        return (self.__fd == o.fd)

    def __ne__(self, o):
        return (self.__fd != o.fd)

    def __hash__(self):
        return hash(str(self.__fd))

    def add_watch(self, pathname, mask):
        wd = _inotify_add_watch(self.__fd, pathname, mask)
        self.__watches[wd] = pathname

        self.__e.register(self.__fd, select.EPOLLIN | select.EPOLLET) 

        return wd

    def rm_watch(self, wd):
        _notify_rm_watch(self.__fd, wd)

    def watch(self):
        _logger.debug("Beginning watch on (%d).", self.__fd)

        while True: 
            events = self.__e.poll() 
            for wd, event in events: 
                try:
                    path = self.__watches[wd]
                except KeyError:
                    _logger.warn("Event received for unregistered watch: "
                                 "(%d)", wd)
                    continue

                yield event

    @property
    def fd(self):
        return self.__fd
