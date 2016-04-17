# pylint: disable=import-error,wildcard-import,unused-wildcard-import,missing-docstring,undefined-variable,function-redefined,unused-argument

"""Behavioral controls for testing the NimbusPI service"""


from behave import *



@then('an exception should be thrown')
def step_impl(context):
    assert hasattr(context, 'exception')


@then('the state should be "{state}"')
def step_impl(context, state):
    assert context.state == state


@then('there should be no warnings')
def step_impl(context):
    context.log.check()


@then('a warning should be logged that says "{log}"')
def step_impl(context, log):
    context.log.check(('nimbuspi', 'WARNING', log))


@then('an error should be logged that says "{log}"')
def step_impl(context, log):
    context.log.check(('nimbuspi', 'ERROR', log))
