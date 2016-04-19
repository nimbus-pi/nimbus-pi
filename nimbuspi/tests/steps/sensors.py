# pylint: disable=import-error,wildcard-import,unused-wildcard-import,missing-docstring,undefined-variable,function-redefined,unused-argument

"""Sensor controls for testing"""


from .nimbuspi.sensors.helloworld import HelloWorld

from behave import *



@given('the "helloworld" sensor')
def step_impl(context):
    context.sensor = HelloWorld()


@when('the sensor\'s "{config}" configuration option is set to "{value}"')
def step_impl(context, config, value):
    context.sensor.config[config] = value


@then('the sensor state should be a string')
def step_impl(context):
    assert isinstance(context.sensor.get_state(), basestring)


@then('the sensor state should be "{state}"')
def step_impl(context, state):
    assert context.sensor.get_state() == state
