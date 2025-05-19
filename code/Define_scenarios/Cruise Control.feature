Feature: Cruise Control

    # Car part

        Scenario: The speed is 0 when the engine is off
             When I initialize the context
              And the engine is off
             Then the speed is 0

        Scenario: Turn on the car
             When I initialize the context
              And the engine is off
              And I press the engine_start_stop button
             Then the vehicle is stationary

        Scenario: Accelerate the car
             When the vehicle is stationary
              And I accelerate
             Then I am accelerating
              And the speed is 1

        Scenario: Stop accelerating
             When I am accelerating
              And I stop accelerating
             Then I am driving

        Scenario: Braking
             When I am accelerating
              And 2 seconds pass
              And I stop accelerating
              And I brake
             Then I am braking

        Scenario: The acceleration increase speed
             When I am driving
              And I accelerate
              And 10 seconds pass
             Then the speed is 133

        Scenario: Turn off the Car
             When The vehicle is stationary
              And I press the engine_start_stop button
             Then the engine is off

    # Cruise Control part

        Scenario: Turn on the CC
             When I am driving
              And I press the CC on_off button
             Then the CC is on

        Scenario: Turn off the CC
             When the CC is on
              And I press the CC on_off button
             Then the CC is off

        Scenario: Activate the CC to 50km/h
             When the CC is on
              And I accelerate to 50 km/h
              And I press the set button
             Then the CC is activated
              And the memorized speed is 50
              And state CC_driving is active

        Scenario: Desactivate with button
             When the CC is activated at 50km/h
              And I press the CC on_off button
             Then the CC is on
              And the CC is desactivated

        Scenario: Reactivate the CC
             When the CC is desactivated
              And I press the res button
             Then the CC is activated
              And the memorized speed is 50

        Scenario: Turn off the CC by stopping the car
             When the CC is on
              And I brake to 0 km/h
              And I press the engine_start_stop button
              And the CC is off

        Scenario: CC can not be set at more than the limit
             When the CC is on
              And I accelerate to 160 km/h
              And I press the set button
             Then the CC is on