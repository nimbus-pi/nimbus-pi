"""Contains services provided for the NimbusPi weather station."""


import logging
import os

import configparser

from yapsy.PluginManager import PluginManager

import nimbuspi.plugins as plugins



class NimbusPI(object):
    """The NimbusPi Weather Station"""
    
    
    # Current NimbusPI Version
    VERSION = "0.1.0-rc1"
    
    
    
    def __init__(self, config='nimbus.cfg'):
        """Initializes the NimbusPI Weather Station"""
        
        self.sensors = dict()
        self.broadcasters = dict()
        self.threads = []
        
        
        # Initialize a named logger
        self.__logger = logging.getLogger('nimbuspi')
        
        
        # Load our config defaults
        self.config = configparser.ConfigParser(allow_no_value=True)
        
        self.config.add_section('station')
        self.config.set('station', 'name', 'N/A')
        self.config.set('station', 'location', 'N/A')
        self.config.set('station', 'longitude', '0.000000')
        self.config.set('station', 'latitude', '0.000000')
        self.config.set('station', 'altitude', '0')
        
        self.config.add_section('sensors')
        self.config.add_section('broadcasters')
        
        
        # Load the provided config file
        if not os.path.isfile(config):
            self.__logger.warn('Configuration file "%s" not found!', config)
            
        else:
            self.__logger.debug('Loading configuration from "%s"', config)
            self.config.read(config)
        
        
        # Get our station details
        self.__logger.debug('         name :: %s', self.config.get('station', 'name'))
        self.__logger.debug('     location :: %s', self.config.get('station', 'location'))
        self.__logger.debug('     latitude :: %s', self.config.get('station', 'latitude'))
        self.__logger.debug('    longitude :: %s', self.config.get('station', 'longitude'))
        self.__logger.debug('     altitude :: %s feet', self.config.get('station', 'altitude'))
        
        self.__logger.debug('Sensors Configured:')
        
        for sensor in self.config.options('sensors'):
            self.__logger.debug('    %s', sensor)
        
        self.__logger.debug('Broadcasters Configured:')
        
        for broadcaster in self.config.options('broadcasters'):
            self.__logger.debug('    %s', broadcaster)
        
        
        # Search for available plugins
        self.__logger.debug("Searching for available plugins...")
        
        self.__plugins = PluginManager(plugin_info_ext='info')
        
        self.__plugins.setPluginPlaces([
            './sensors',
            './broadcasters',
            './nimbuspi/sensors',
            './nimbuspi/broadcasters'
        ])
        
        self.__plugins.setCategoriesFilter({
            plugins.ISensorPlugin.CATEGORY      : plugins.ISensorPlugin,
            plugins.IBroadcasterPlugin.CATEGORY : plugins.IBroadcasterPlugin
        })
        
        self.__plugins.collectPlugins()
        
        for plugin in self.__plugins.getAllPlugins():
            self.__logger.debug("    %s (%s)", plugin.name, plugin.path)
            plugin.plugin_object.set_nimbus(self)
        
        self.__logger.debug("%d plugins available", len(self.__plugins.getAllPlugins()))
    
    
    
    def run(self):
        """Runs the NimbusPI Weather Station loop"""
        
        self.__logger.debug('-' * 80)
        self.__logger.info('NimbusPI Weather Station v%s', self.VERSION)
        self.__logger.info('-' * 80)
        
        
        # Load all configured sensor plugins
        self.__logger.info("Activating sensor plugins...")
        
        for sensor in self.config.options('sensors'):
            try:
                self.activate_sensor(sensor)
            except LookupError:
                self.__logger.error("Could not load sensor '%s'", sensor)
                return
        
        if len(self.sensors) <= 0:
            self.__logger.error('Cannot continue - no sensors configured')
            return
        
        
        # Load all configured broadcaster plugins
        self.__logger.info("Activating broadcaster plugins...")
        
        for broadcaster in self.config.options('broadcasters'):
            try:
                self.activate_broadcaster(broadcaster)
            except LookupError:
                self.__logger.error("Could not load broadcaster '%s'", broadcaster)
                return
        
        if len(self.broadcasters) <= 0:
            self.__logger.error('Cannot continue - no broadcasters configured')
            return
        
        
        # # Thread run loop until keyboard interrupt
        self.__logger.debug("Entering thread loop")
        
        while len(self.threads) > 0:
            try:
                self.threads = [t.join(30) for t in self.threads if t is not None and t.isAlive()]
        
            except (KeyboardInterrupt, SystemExit):
                self.__logger.info("Shutting down plugins (this may take a minute)...")
        
                for thread in self.threads:
                    thread.stop()
        
        self.__logger.debug("Exiting thread loop")
        
        
        # Deactivate plugins
        self.__logger.debug("Deactivating sensors")
        
        sensors = self.sensors.keys()
        for sensor in sensors:
            self.deactivate_sensor(sensor)
        
        self.__logger.debug("Deactivating broadcasters")
        
        broadcasters = self.broadcasters.keys()
        for broadcaster in broadcasters:
            self.deactivate_broadcaster(broadcaster)
    
    
    
    def activate_sensor(self, sensor):
        """Activates a sensor on the service"""
        
        if sensor in self.sensors:
            self.__logger.warn("Cannot activate sensor '%s' - sensor already active", sensor)
            return False
        
        self.__logger.debug("Activating sensor '%s'", sensor)
        
        self.sensors[sensor] = self.__plugins.getPluginByName(sensor, plugins.ISensorPlugin.CATEGORY)
        
        if not self.sensors[sensor]:
            raise LookupError
        
        self.__plugins.activatePluginByName(sensor, plugins.ISensorPlugin.CATEGORY)
        self.threads.append(self.sensors[sensor].plugin_object.thread)
        
        return True
    
    
    
    def deactivate_sensor(self, sensor):
        """Deactivates a sensor on the service"""
        
        if sensor not in self.sensors:
            self.__logger.warn("Cannot deactivate sensor '%s' - sensor not active", sensor)
            return False
        
        self.__logger.debug("Deactivating sensor '%s'", sensor)
        
        if self.sensors[sensor].plugin_object.thread:
            self.sensors[sensor].plugin_object.thread.stop()
        
        self.__plugins.deactivatePluginByName(sensor, plugins.ISensorPlugin.CATEGORY)
        
        del self.sensors[sensor]
        
        return True
    
    
    
    def activate_broadcaster(self, broadcaster):
        """Activates a broadcaster on the service"""
        
        if broadcaster in self.broadcasters:
            self.__logger.warn("Cannot activate broadcaster '%s' - broadcaster already active", broadcaster)
            return False
        
        self.__logger.debug("Activating broadcaster '%s'", broadcaster)
        
        self.broadcasters[broadcaster] = self.__plugins.getPluginByName(
            broadcaster,
            plugins.IBroadcasterPlugin.CATEGORY
        )
        
        if not self.broadcasters[broadcaster]:
            raise LookupError
        
        self.__plugins.activatePluginByName(broadcaster, plugins.IBroadcasterPlugin.CATEGORY)
        self.threads.append(self.broadcasters[broadcaster].plugin_object.thread)
        
        return True
    
    
    
    def deactivate_broadcaster(self, broadcaster):
        """Deactivates a broadcaster on the service"""
        
        if broadcaster not in self.broadcasters:
            self.__logger.warn("Cannot deactivate broadcaster '%s' - broadcaster not active", broadcaster)
            return False
        
        self.__logger.debug("Deactivating broadcaster '%s'", broadcaster)
        
        if self.broadcasters[broadcaster].plugin_object.thread:
            self.broadcasters[broadcaster].plugin_object.thread.stop()
        
        self.__plugins.deactivatePluginByName(broadcaster, plugins.IBroadcasterPlugin.CATEGORY)
        
        del self.broadcasters[broadcaster]
        
        return True
    
    
    
    def get_states(self):
        """Returns the current state of all sensors"""
        
        states = dict()
        
        # Add our station configuration information as well
        states['config'] = dict()
        
        for option in self.config.options('station'):
            states['config'][option] = self.config.get('station', option)
        
        
        # Add all current plugin states
        for sensor in self.sensors:
            states[sensor] = self.sensors[sensor].plugin_object.get_state()
        
        return states
