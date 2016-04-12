"""Defines plugin interfaces for the Nimbus Pi weather station."""

from yapsy.IPlugin import IPlugin


class ISensorPlugin(IPlugin):
    """Defines the interface for all Sensor plugins in Nimbus Pi"""
    CATEGORY = "Sensor"

    def get_state(self):
        """Returns the state of the sensor."""
        raise NotImplementedError("Sensor interface not fully implemented")




class IBroadcasterPlugin(IPlugin):
    """Defines the interface for all Broadcaster plugins in Nimbus Pi"""
    CATEGORY = "Broadcaster"
