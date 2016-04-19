"""Logging broadcaster for NimbusPI"""


import logging

import nimbuspi.plugins as plugins
import nimbuspi.threads as threads


class Logger(plugins.IBroadcasterPlugin):
    """Broadcaster that periodically logs information to the Python logging module"""
    
    
    def __init__(self):
        """Creates a Logger broadcaster plugin"""
        
        plugins.IBroadcasterPlugin.__init__(self)
        
        self.config = dict()
        
        self.config['delay'] = 2
        self.config['level'] = logging.INFO
        self.config['format'] = "{config[name]} @ {config[location]}"
        
        self.thread = LoggerThread(
            delay=self.config['delay'],
            config=self.config,
            nimbus=self.nimbus
        )
    
    
    
    def activate(self):
        """Activates the logger broadcaster plugin"""
        
        # Override the defaults with any configuration settings
        if self.nimbus.config.has_section('logger'):
            for option in self.nimbus.config.options('logger'):
                self.config[option] = self.nimbus.config.get('logger', option)
        
        # Start the subprocess
        self.thread.set_delay(self.config['delay'])
        self.thread.start()
    
    
    
    def deactivate(self):
        """Deactivates the logger broadcaster plugin"""
        
        if self.thread and self.thread.isAlive():
            self.thread.stop()



class LoggerThread(threads.NimbusThread):
    """Logs information periodically to the Python logger"""
    
    
    def update(self):
        """Logs the formatted data"""
        
        try:
            output = self.config['format'].format(**self.nimbus.get_states())
            logging.getLogger('broadcaster').log(self.config['level'], output)
            
        except KeyError as err:
            logging.getLogger('broadcaster').warn('Logging failed - could not parse keyword "%s"', err.message)
