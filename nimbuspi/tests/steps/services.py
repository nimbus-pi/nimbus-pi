# pylint: disable=import-error,wildcard-import,unused-wildcard-import,missing-docstring,undefined-variable,function-redefined,unused-argument

"""Behavioral controls for testing the NimbusPI service"""


from nimbuspi import NimbusPI

from behave import *



@given('an instance of NimbusPI')
def step_impl(context):
    context.nimbuspi = NimbusPI()
    assert isinstance(context.nimbuspi, NimbusPI)


@given('a configured instance of NimbusPI')
def step_impl(context):
    context.nimbuspi = NimbusPI("./nimbuspi/tests/test.cfg")
    assert isinstance(context.nimbuspi, NimbusPI)


@given('an instance of NimbusPI with the configuration file "{config}"')
def step_impl(context, config):
    context.nimbuspi = NimbusPI(config)
    assert isinstance(context.nimbuspi, NimbusPI)


@when('the instance is started')
def step_impl(context):
    context.nimbuspi.run()


@when('the "{sensor}" sensor is activated')
def step_impl(context, sensor):
    try:
        context.nimbuspi.activate_sensor(sensor)
    except LookupError as err:
        context.exception = err


@when('the "{broadcaster}" broadcaster is activated')
def step_impl(context, broadcaster):
    try:
        context.nimbuspi.activate_broadcaster(broadcaster)
    except LookupError as err:
        context.exception = err


@when('the "{sensor}" sensor is deactivated')
def step_impl(context, sensor):
    context.nimbuspi.deactivate_sensor(sensor)


@when('the "{broadcaster}" broadcaster is deactivated')
def step_impl(context, broadcaster):
    context.nimbuspi.deactivate_broadcaster(broadcaster)


@then('the version should be "{version}"')
def step_impl(context, version):
    assert context.nimbuspi.VERSION == version


@then('the "{option}" configuration in the "{section}" section should be "{value}"')
def step_impl(context, option, section, value):
    assert context.nimbuspi.config.has_section(section)
    assert context.nimbuspi.config.has_option(section, option)
    assert context.nimbuspi.config.get(section, option) == value


@then('the sensor list should be empty')
def step_impl(context):
    assert len(context.nimbuspi.sensors) == 0


@then('the sensor list should not be empty')
def step_impl(context):
    assert len(context.nimbuspi.sensors) > 0


@then('the broadcaster list should be empty')
def step_impl(context):
    assert len(context.nimbuspi.broadcasters) == 0


@then('the broadcaster list should not be empty')
def step_impl(context):
    assert len(context.nimbuspi.broadcasters) > 0


@then('the "{field}" field in the global state should be "{value}"')
def step_impl(context, field, value):
    field = "{%s}" % field
    assert field.format(**context.nimbuspi.get_states()) == value


@then('the "{field}" field in the global state should not exist')
def step_impl(context, field):
    field = "{%s}" % field
    
    try:
        if field.format(**context.nimbuspi.get_states()) == "":
            raise AssertionError("Should not have existed")
    except KeyError:
        pass
