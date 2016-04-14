Feature: packaged sensor plugins
  
  
  Scenario: sensors should load when starting
      Given an instance of NimbusPI
       When the instance is started
       Then the sensor list should not be empty
        And there should be no warnings
  
  
  Scenario: sensors should raise an exception if their get_state is not implemented
      Given an instance of NimbusPI
        And a new sensor named "foobar"
       When accessing the "foobar" sensor state
       Then an exception should be thrown
  
  
  Scenario: no sensors should be activated after initialization
      Given an instance of NimbusPI
       Then the sensor list should be empty
        And there should be no warnings
  
  
  Scenario: sensors should be activated after starting
      Given an instance of NimbusPI
       When the instance is started
       Then the sensor list should not be empty
        And there should be no warnings
  
  
  Scenario Outline: all sensors should return standard states by default when activated
              Given an instance of NimbusPI
               When the "<plugin>" sensor is activated
                And accessing the "<plugin>" sensor state
               Then the state should be "<response>"
                   
          Examples: Sensors
                    | plugin     | response     |
                    | helloworld | Hello World! |
  
  
  Scenario: stopping the service should unload all sensors
      Given an instance of NimbusPI
       When the instance is started
        And the instance is stopped
       Then the service should not be running
        And there should be no warnings
        And the sensor list should be empty
  
  
  Scenario: activating an already-active sensor should throw a warning
      Given an instance of NimbusPI
       When the instance is started
        And the "helloworld" sensor is activated
       Then a warning should be logged that says "Cannot activate sensor 'helloworld' - sensor already active"
  
  
  Scenario: deactivating an inactive sensor should throw a warning
      Given an instance of NimbusPI
       When the "helloworld" sensor is deactivated
       Then a warning should be logged that says "Cannot deactivate sensor 'helloworld' - sensor not active"
  