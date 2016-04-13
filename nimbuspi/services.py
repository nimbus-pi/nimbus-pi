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
        
        self.is_running = False
        self.sensors = dict()
        self.broadcasters = dict()
        
        
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
        
        
        # Get our server details
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
            self.__logger.debug("Plugin found: %s (%s)", plugin.name, plugin.path)
        
        self.__logger.debug("%d plugins available", len(self.__plugins.getAllPlugins()))
    
    
    
    def start(self):
        """Starts the NimbusPI Weather Station"""
        
        if self.is_running:
            self.__logger.warn('Attempted to start NimbusPI, but was already running')
            return
        
        
        self.__logger.debug('-' * 80)
        self.__logger.info('NimbusPI Weather Station v%s', self.VERSION)
        self.__logger.info('-' * 80)
        
        
        # Load all configured sensor plugins
        self.__logger.info("Activating sensor plugins...")
        
        for sensor in self.config.options('sensors'):
            self.activate_sensor(sensor)
        
        
        # # Load the broadcaster plugins
        # LOGGER.debug("Activating broadcaster plugins...")
        # # TODO
        
        
        # Mark the service active
        self.__logger.debug('Started')
        self.is_running = True
    
    
    
    def stop(self):
        """Stops the NimbusPI Weather Station"""
        
        if not self.is_running:
            self.__logger.warn('Attempted to stop NimbusPI, but service is not running')
            return
        
        self.__logger.info('Stopping the NimbusPI service')
        
        
        # Unload all configured sensor plugins
        self.__logger.info("Deactivating sensor plugins...")
        
        keys = self.sensors.keys()
        for sensor in keys:
            self.deactivate_sensor(sensor)
        
        
        # # Unload all configured broadcaster plugins
        # LOGGER.debug("Deactivating broadcaster plugins...")
        # # TODO
        
        
        # Mark the service inactive
        self.__logger.debug('Stopped')
        self.is_running = False
    
    
    
    def restart(self):
        """Restarts the NimbusPI Weather Station"""
        
        if self.is_running:
            self.stop()
        
        self.start()
    
    
    
    def activate_sensor(self, sensor):
        """Activates a sensor on the service"""
        
        if sensor in self.sensors:
            self.__logger.warn("Cannot activate sensor '%s' - sensor already active", sensor)
            return False
        
        
        self.__plugins.activatePluginByName(sensor, plugins.ISensorPlugin.CATEGORY)
        self.sensors[sensor] = self.__plugins.getPluginByName(sensor, plugins.ISensorPlugin.CATEGORY).plugin_object
        
        return True
    
    
    
    def deactivate_sensor(self, sensor):
        """Deactivates a sensor on the service"""
        
        if sensor not in self.sensors:
            self.__logger.warn("Cannot deactivate sensor '%s' - sensor not active", sensor)
            return False
        
        self.__plugins.deactivatePluginByName(sensor, plugins.ISensorPlugin.CATEGORY)
        
        del self.sensors[sensor]
        
        return True
