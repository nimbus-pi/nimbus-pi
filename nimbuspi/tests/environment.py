# pylint: disable=wildcard-import,unused-wildcard-import

"""Environment controls for Behave"""


import logging
import traceback

from behave import *
from testfixtures import LogCapture



DETAILS_ON_FAILURE = False
FAILURES = []



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



def setup_debug_on_error(userdata):
    global DETAILS_ON_FAILURE
    
    DETAILS_ON_FAILURE = userdata.getbool("details-on-failure")



def before_all(context):
    setup_debug_on_error(context.config.userdata)



def after_step(context, step):
    global FAILURES
    
    if DETAILS_ON_FAILURE and step.status == "failed":
        FAILURES.append({
            'scenario' : context.scenario,
            'step'     : step
        })


def after_all(context):
    if FAILURES:
        print("\n")
        print("-" * 80)
        print("Failure Details:")
        print("-" * 80)
        
        for failure in FAILURES:
            print("\n")
            print(failure['scenario'].filename)
            print("    %s (line %s)" % (failure['scenario'].name, failure['scenario'].line))
            print("        %s %s (line %s)" % (failure['step'].keyword, failure['step'].name, failure['step'].line))
            print("")
            print(failure['step'].error_message)
            print("-" * 80)
        
        print("\n")
