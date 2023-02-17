class Stopwatch():
    '''The stopwatch used to record the time taken to complete the maze'''

    def __init__(self):
        self._total = -1 #total number of seconds that have passed. -1 means it immediately increments to 0
        self._seconds = 0
        self._minutes = 0
        self._display = '00:00'
    #endsub

    def getTotal(self):
        return self._total
    #endsub

    def getMinutes(self):
        return self._minutes
    #endsub

    def getDisplay(self):
        return self._display
    #endsub

    def increment(self):
        '''Add 1 second'''
        self._total+=1
        self._minutes = self._total // 60
        self._seconds = self._total % 60
        self._updateDisplay()        
    #endsub

    def _updateDisplay(self):
        '''Change the display that will be seen by the user'''
        secs = str(self._seconds)
        if len(secs) == 1:
            secs = '0'+secs
        #endif

        mins = str(self._minutes)
        if len(mins) == 1:
            mins = '0'+mins
        #endif

        self._display = '{0}{1}:{2}{3}'.format(mins[0], mins[1], secs[0], secs[1])
    #endsub

    def reset(self):
        '''Reset the stopwatch back to "00:00"'''
        self.__init__()
    #endsub
#endclass
        
