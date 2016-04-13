import nimbuspi.plugins as plugins

class HelloWorld(plugins.ISensorPlugin):
    """HelloWorld sensor that provides test data."""
    
    def get_state(self):
        return "Hello World!"
    