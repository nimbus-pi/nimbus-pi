# pylint: disable=import-error,wildcard-import,unused-wildcard-import,missing-docstring,undefined-variable,function-redefined,unused-argument

"""Behavioral controls for testing the NimbusPI service"""


from nimbuspi import NimbusPI

from behave import *



@given('an instance of NimbusPI')
def step_impl(context):
    context.nimbuspi = NimbusPI("./nimbuspi/tests/test.cfg")
    assert isinstance(context.nimbuspi, NimbusPI)



@given('an instance of NimbusPI with the "{config}" configuration file')
def step_impl(context, config):
    context.nimbuspi = NimbusPI(config)
    assert isinstance(context.nimbuspi, NimbusPI)



@when('the instance is started')
def step_impl(context):
    context.nimbuspi.start()



@when('the instance is restarted')
def step_impl(context):
    context.nimbuspi.restart()



@when('the instance is stopped')
def step_impl(context):
    context.nimbuspi.stop()



@then('the version should be "0.1.0-rc1"')
def step_impl(context):
    assert context.nimbuspi.VERSION == '0.1.0-rc1'



@then('the service should be running')
def step_impl(context):
    assert context.nimbuspi.is_running



@then('the service should not be running')
def step_impl(context):
    assert not context.nimbuspi.is_running
