Feature: the HelloWorld sensor
  
  
  Scenario: the sensor should have a default output
      Given the "helloworld" sensor
       Then the sensor state should be a string
        And the sensor state should be "Hello World!"
  
  
  Scenario: the sensor output should be configurable
      Given the "helloworld" sensor
       When the sensor's "message" configuration option is set to "test"
       Then the sensor state should be a string
        And the sensor state should be "test"
  