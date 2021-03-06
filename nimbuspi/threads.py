"""Provides threading controls for plugins"""

import threading


class NimbusThread(threading.Thread):
    """A thread with a stop flag"""
    
    
    def __init__(self, config, delay=0.5, nimbus=None):
        """Creates a NimbusThread"""
        
        threading.Thread.__init__(self)
        
        self.stop_event = threading.Event()
        
        self.delay = delay
        self.config = config
        self.nimbus = nimbus
    
    
    
    def update(self):
        """Updates the thread data"""
        
        raise NotImplementedError
    
    
    
    def run(self):
        """Runs the thread until flagged to stop"""
        
        while not self.stop_event.wait(self.delay):
            self.update()
            
    
    
    def stop(self):
        """Marks the thread to stop after the next iteration"""
        
        self.stop_event.set()
    
    
    def set_delay(self, delay):
        """Sets the delay for the thread"""
        
        self.delay = delay
