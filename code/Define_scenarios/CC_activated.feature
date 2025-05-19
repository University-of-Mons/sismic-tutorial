Feature: Cruise Control activated
        Background:
             When I initialize the context
              And I press the engine_start_stop button
              And I accelerate
              And I stop accelerating
              And I press the CC on_off button
              And I accelerate to 50 km/h
              And I press the set button
 
        Scenario: Activate the CC to 50km/h
             Then the CC is activated
              And the memorized speed is 50
              And state CC_driving is active

        Scenario: Decrease mem_speed by 10
             When I press the minus button
             Then the memorized speed is 40

        Scenario: Increase mem_speed by 10
             When I press the plus button
             Then the memorized speed is 60

        Scenario: Decrease mem_speed by 1
             When I press the res button
             Then the memorized speed is 49

        Scenario: Increase mem_speed by 1
             When I press the set button
             Then the memorized speed is 51

        Scenario: Increase speed with accelerate
             When I accelerate to 70 km/h
              And I press the set button
             Then the memorized speed is 70

        Scenario: Desactivate with brake
             When I brake
             Then the CC is on
              And the CC is desactivated

        Scenario: Desactivate with button
             When I press the CC on_off button
             Then the CC is on
              And the CC is desactivated

        Scenario: CC can not be increased by 10 if it is above the limit
             When I accelerate to 150 km/h
              And I press the set button
              And I press the plus button
             Then the memorized speed is 150

        Scenario: CC can not be increased by 1 if it is above the limit
             When I accelerate to 159 km/h
              And I press the set button
              And I press the set button
             Then the memorized speed is 159

        Scenario: CC can not be decreased by 10 if it is below the limit
             When I brake to 0 km/h
              And I accelerate to 9 km/h
              And I press the set button
              And I press the minus button
             Then the memorized speed is 10

        Scenario: CC can not be increased by 1 if it is below the limit
             When I brake to 0 km/h
              And I accelerate to 1 km/h
              And I press the set button
              And I press the res button
             Then the memorized speed is 1

        Scenario: CC is maintaining the car's speed
             When 3.5 seconds pass
             Then the speed is 50