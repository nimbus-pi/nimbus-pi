# pylint: disable=wildcard-import,unused-wildcard-import

"""Environment controls for Behave"""


import logging

from behave import *
from testfixtures import LogCapture



def before_scenario(context, scenario):
    """Preps each scenario for log capturing"""
    
    context.log = LogCapture(level=logging.WARNING)



def after_scenario(context, scenario):
    """Clears shared variables"""
    
    if 'nimbuspi' in context:
        del context.nimbuspi
    
    if 'state' in context:
        del context.state
    
    if 'exception' in context:
        del context.exception
    
    context.log.uninstall()
