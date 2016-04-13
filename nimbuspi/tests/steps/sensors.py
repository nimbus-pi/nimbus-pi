# pylint: disable=import-error,wildcard-import,unused-wildcard-import,missing-docstring,undefined-variable,function-redefined,unused-argument,bare-except

"""Behavioral controls for testing sensors"""


import sys

import nimbuspi.plugins as plugins

from behave import *



@given('a new sensor named "{sensor}"')
def step_impl(context, sensor):
    
    class NewSensor(plugins.ISensorPlugin):
        def reflect(self):
            return self
        
        def get_name(self):
            return self.__name__
    
    context.nimbuspi.sensors[sensor] = NewSensor()



@when('the "{sensor}" sensor is activated')
def step_impl(context, sensor):
    context.nimbuspi.activate_sensor(sensor)
    assert sensor in context.nimbuspi.sensors



@when('the "{sensor}" sensor is deactivated')
def step_impl(context, sensor):
    context.nimbuspi.deactivate_sensor(sensor)
    assert sensor not in context.nimbuspi.sensors



@when('accessing the "{sensor}" sensor state')
def step_impl(context, sensor):
    try:
        context.state = context.nimbuspi.sensors[sensor].get_state()
    except:
        context.exception = sys.exc_info()[0]



@then('the sensor list should be empty')
def step_impl(context):
    assert len(context.nimbuspi.sensors) == 0



@then('the sensor list should not be empty')
def step_impl(context):
    assert len(context.nimbuspi.sensors) > 0
