import threading

#
#   Desc:   This is a threadsafe counter. 
#           If you need an unique id, then call the increment function and use the result.
#
class AtomicCounter:
    # 
    #   Desc:   Constructor to initialize the counter.
    #
    def __init__(self, initialValue=1):
        self.value = initialValue
        self._lock = threading.Lock()

    #
    #   Desc:   Increments the counter and returns the value in a threadsafe way.
    #
    def increment(self, inc=1):

        with self._lock:
            self.value += inc
            return self.value
