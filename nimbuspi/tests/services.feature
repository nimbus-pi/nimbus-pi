Feature: the NimbusPI service
  
  
  Scenario: the version number should be correct
      Given an instance of NimbusPI
       Then the version should be "0.1.0-rc1"
  
  
  Scenario: the station information should be available without a config file
      Given an instance of NimbusPI
       Then the "name" configuration in the "station" section should be "N/A"
        And the "location" configuration in the "station" section should be "N/A"
        And the "latitude" configuration in the "station" section should be "0.000000"
        And the "longitude" configuration in the "station" section should be "0.000000"
        And the "altitude" configuration in the "station" section should be "0"
  
  
  Scenario: the station information should update properly from a config file
      Given a configured instance of NimbusPI
       Then the "name" configuration in the "station" section should be "Test Station"
        And the "location" configuration in the "station" section should be "My Test Location, Chicago, IL 60606"
        And the "latitude" configuration in the "station" section should be "1.111111"
        And the "longitude" configuration in the "station" section should be "-2.222222"
        And the "altitude" configuration in the "station" section should be "8000"
  
  
  Scenario: a warning should be logged if the config file is missing
      Given an instance of NimbusPI with the configuration file "foobar"
       Then a warning should be logged that says "Configuration file "foobar" not found!"
  
  
  Scenario: the plugins lists should be empty without a config file
      Given an instance of NimbusPI
       Then the sensor list should be empty
        And the broadcaster list should be empty
  
  
  # Scenario: the plugin lists should contain the sensors from a given config file when started
  #     Given a configured instance of NimbusPI
  #      When the instance is started
  #      Then the sensor list should not be empty
  #      Then the broadcaster list should not be empty
  
  
  Scenario: a warning should be thrown for a missing sensor when started
      Given an instance of NimbusPI with the configuration file "./nimbuspi/tests/test-bad-sensor.cfg"
       When the instance is started
       Then an error should be logged that says "Could not load sensor 'foobar'"
  
  
  Scenario: a warning should be thrown for a missing broadcaster when started
      Given an instance of NimbusPI with the configuration file "./nimbuspi/tests/test-bad-broadcaster.cfg"
       When the instance is started
       Then an error should be logged that says "Could not load broadcaster 'foobar'"
  
  
  Scenario: an error should be thrown if there are no sensors active when started
      Given an instance of NimbusPI with the configuration file "./nimbuspi/tests/test-no-sensor.cfg"
       When the instance is started
       Then an error should be logged that says "Cannot continue - no sensors configured"
  
  
  Scenario: an error should be thrown if there are no broadcasters active when started
      Given an instance of NimbusPI with the configuration file "./nimbuspi/tests/test-no-broadcaster.cfg"
       When the instance is started
       Then an error should be logged that says "Cannot continue - no broadcasters configured"
  
  
  # Scenario: there should be no threads running after shutdown
  #     Given a configured instance of NimbusPI
  #      When the instance is started
  #       And the instance is stopped
  #      Then the thread list should be empty
  
  
  # Scenario: all plugins should be deactivated after shutdown
  #     Given a configured instance of NimbusPI
  #      When the instance is started
  #       And the instance is stopped
  #      Then the sensor list should be empty
  #       And the broadcaster list should be empty
  
  
  Scenario: activating a missing sensor should raise an exception
      Given an instance of NimbusPI
       When the "foobar" sensor is activated
       Then an exception should be thrown
  
  
  Scenario: activating a missing broadcaster should raise an exception
      Given an instance of NimbusPI
       When the "foobar" broadcaster is activated
       Then an exception should be thrown
  
  
  Scenario: activating a sensor that is already active should log a warning
      Given a configured instance of NimbusPI
       When the "helloworld" sensor is activated
        And the "helloworld" sensor is activated
       Then a warning should be logged that says "Cannot activate sensor 'helloworld' - sensor already active"
  
  
  # Scenario: activating a broadcaster that is already active should log a warning
  #     Given a configured instance of NimbusPI
  #      When the "logger" sensor is activated
  #       And the "logger" sensor is activated
  #      Then a warning should be logged that says "Cannot activate broadcaster 'logger' - broadcaster already active"
  
  
  Scenario: deactivating a sensor that is not active should log a warning
      Given a configured instance of NimbusPI
       When the "helloworld" sensor is deactivated
       Then a warning should be logged that says "Cannot deactivate sensor 'helloworld' - sensor not active"
  
  
  Scenario: deactivating a broadcaster that is not active should log a warning
      Given a configured instance of NimbusPI
       When the "logger" broadcaster is deactivated
       Then a warning should be logged that says "Cannot deactivate broadcaster 'logger' - broadcaster not active"
  
  
  Scenario: activating a sensor should add it to the sensor list
      Given a configured instance of NimbusPI
       When the "helloworld" sensor is activated
      Then the sensor list should not be empty
  
  
  Scenario: deactivating an active sensor should unload the plugin
      Given a configured instance of NimbusPI
       When the "helloworld" sensor is activated
        And the "helloworld" sensor is deactivated
       Then the sensor list should be empty
  
  
  # Scenario: activating a broadcaster should add it to the broadcaster list
  #     Given a configured instance of NimbusPI
  #      When the "logger" broadcaster is activated
  #     Then the broadcaster list should not be empty
  
  
  # Scenario: deactivating an active broadcaster should unload the plugin
  #     Given a configured instance of NimbusPI
  #      When the "logger" broadcaster is activated
  #       And the "logger" broadcaster is deactivated
  #      Then the broadcaster list should be empty
  
  
  Scenario: retrieving global state should contain station configuration information
      Given a configured instance of NimbusPI
       Then the "config[name]" field in the global state should be "Test Station"
        And the "config[location]" field in the global state should be "My Test Location, Chicago, IL 60606"
        And the "config[latitude]" field in the global state should be "1.111111"
        And the "config[longitude]" field in the global state should be "-2.222222"
        And the "config[altitude]" field in the global state should be "8000"
  
  
  # Scenario: retrieving global state should contain all configured and activated sensors when running
  #     Given a configured instance of NimbusPI
  #      When the instance is started
  #      Then the "helloworld" field in the global state should be "Hello World!"
  
  
  Scenario: retrieving global state from a service that isn't running should only contain config information
      Given a configured instance of NimbusPI
       Then the "config[name]" field in the global state should be "Test Station"
        And the "helloworld" field in the global state should not exist
  