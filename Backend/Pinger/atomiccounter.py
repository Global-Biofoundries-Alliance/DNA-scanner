'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
# pylint: disable=too-few-public-methods
import threading


class AtomicCounter:
    '''
    This is a threadsafe counter.

    If you need an unique id, then call the increment function and use
    the result.'''

    def __init__(self, initialValue=1):
        '''Constructor to initialize the counter.'''
        self.value = initialValue
        self._lock = threading.Lock()

    def increment(self, inc=1):
        '''Increments the counter and returns the value in a threadsafe way.'''
        with self._lock:
            self.value += inc
            return self.value
