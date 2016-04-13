Feature: the NimbusPI service
  
  
  Scenario: ensure the version number is correct
      Given an instance of NimbusPI
       Then the version should be "0.1.0-rc1"
        And there should be no warnings
  
  
  Scenario: ensure that anly-initialized service is not running
      Given an instance of NimbusPI
       Then the service should not be running
        And there should be no warnings
  
  
  Scenario: the service should be marked as running after starting
      Given an instance of NimbusPI
       When the instance is started
       Then the service should be running
        And there should be no warnings
  
  
  Scenario: the service should be marked as running after restarting
      Given an instance of NimbusPI
       When the instance is started
        And the instance is restarted
       Then the service should be running
        And there should be no warnings
  
  
  Scenario: restarting a stopped service should be marked as running
      Given an instance of NimbusPI
       When the instance is restarted
       Then the service should be running
        And there should be no warnings
  
  
  Scenario: stopping a started service should not be marked as running
      Given an instance of NimbusPI
       When the instance is started
        And the instance is stopped
       Then the service should not be running
        And there should be no warnings
  
  
  Scenario: missing configuration files should throw warnings
      Given an instance of NimbusPI with the "foobar" configuration file
       Then a warning should be logged that says "Configuration file "foobar" not found!"
  
  
  Scenario: starting an already-started service should throw a warning
      Given an instance of NimbusPI
       When the instance is started
       When the instance is started
       Then a warning should be logged that says "Attempted to start NimbusPI, but was already running"
  
  
  Scenario: stopping an already-stopped service should throw a warning
      Given an instance of NimbusPI
       When the instance is stopped
       Then a warning should be logged that says "Attempted to stop NimbusPI, but service is not running"
  