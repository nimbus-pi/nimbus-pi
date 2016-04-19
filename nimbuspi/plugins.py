"""Defines plugin interfaces for the Nimbus Pi weather station."""

from yapsy.IPlugin import IPlugin

import nimbuspi.threads as threads


class INimbusPlugin(IPlugin):
    """Parent class for all NimbusPI plugins"""
    
    
    def __init__(self):
        """Creates a nimbus plugin"""
        
        IPlugin.__init__(self)
        
        self.config = dict()
        self.nimbus = None
        
        self.thread = threads.NimbusThread(config=self.config, nimbus=self.nimbus)
    
    
    def set_nimbus(self, nimbus):
        """Sets the nimbus object for the plugin"""
        
        self.nimbus = nimbus
        self.thread.nimbus = nimbus



class ISensorPlugin(INimbusPlugin):
    """Defines the interface for all Sensor plugins in Nimbus Pi"""
    
    CATEGORY = "Sensor"
    
    def get_state(self):
        """Returns the state of the sensor."""
        
        raise NotImplementedError



class IBroadcasterPlugin(INimbusPlugin):
    """Defines the interface for all Broadcaster plugins in Nimbus Pi"""
    
    CATEGORY = "Broadcaster"
