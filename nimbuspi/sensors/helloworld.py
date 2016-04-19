"""HelloWorld sensor for NimbusPI"""


import nimbuspi.plugins as plugins


class HelloWorld(plugins.ISensorPlugin):
    """HelloWorld sensor that provides test data."""
    
    
    def __init__(self):
        """Creates a HelloWorld sensor plugin"""
        
        plugins.ISensorPlugin.__init__(self)
        
        self.config['message'] = "Hello World!"
        
        
        
    def activate(self):
        """Activates the HelloWorld plugin"""
        
        if self.nimbus.config.has_section('helloworld'):
            for option in self.nimbus.config.options('helloworld'):
                self.config[option] = self.nimbus.config.get('helloworld', option)
    
    
    
    def get_state(self):
        """Returns a static string"""
        
        return self.config['message']
