import datetime
import time
import threading

class Clock:

    def __init__(self, sys_time = datetime.datetime.now(), drift_rate = 1):
        """
        Creates a clock object with a local time and a drift rate.
        """
        self.local_time = sys_time
        self.thread = threading.Thread(target=self.tick, args=(drift_rate))
        self.thread.start()
    
    def tick(self, drift_rate = 1):
        """
        Keeps the clock ticking at every millisecond with a specified drift rate
        """
        while True:
            time.sleep(0.001)
            self.local_time = self.local_time + datetime.timedelta(seconds = 0.001 * drift_rate)
    
    def setTime(self, new_time):
        """
        Set the local clock time
        This will be used for synchronization
        """
        self.local_time = new_time
    
    def getTime(self):
        """
        Get the local clock time
        """
        return self.local_time
    
    def __del__(self):
        """
        Stop the clock thread when the object is deleted
        """
        self.thread.stop()

    