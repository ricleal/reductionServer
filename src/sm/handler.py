'''
Created on Jul 23, 2013

@author: leal
'''

import handler_sm

class Turnstile:
    def __init__(self):
        self._fsm = handler_sm.Hanlder_sm(self)
    
    def testTransition(self):
        self._fsm.putCoin()
        self._fsm.putCoin()
        
        print self._fsm.
        
        self._fsm.putCoin()
        self._fsm.tryToPass()
        self._fsm.tryToPass()
        self._fsm.tryToPass()
        self._fsm.putCoin()
        self._fsm.tryToPass()
        
        
    # function defined in the sm file
    def unlock(self):
        print 'Unlocking...'
    def alarm(self):
        print 'Alarm!'
    def lock(self):
        print 'Locking...'
    def giveCoinBack(self):
        print 'Giving the coin back...'


if __name__ == '__main__':
    pass