# Sismic tutorial through example

The purpose of this tutorial is to explain how to implement and test a statechart using the [Sismic library](https://github.com/AlexandreDecan/sismic), through a complete example. It will also follow the methodology described in the scientific article [A method for testing and validating executable statechart models](https://doi.org/10.1007/s10270-018-0676-3), that is supported by Sismic.

# Context and methodology

The example in this tutorial is a statechart modelizing the Adaptative Cruise Control feature of a car. To create it with sismic and following the scientific article's methodology, we will go through the following steps :

1. Design phase
   1. Design statechart
      1. Declaring the statechart
      2. Integrating code into the statechart
   2. Define scenarios
   3. Define properties
   4. Enrich statechart with contracts
   5. Define unit tests 
2. Getting results from tests
3. Interface to External Components
   1. Integrating the statechart in the code
4. Second iteration

A prior work should be done about analysing the problem by making a user-story, a UI mock-up and a component diagram but it will not be covered in this tutorial.

The methodology also suggests working by iterations. This means that we will go through all the aforementioned steps for the Cruise Control feature and then going throught theses steps again to add the Adaptative Cruise Control feature.

# Design phase

## Design statechart

It is suggested to start by designing your statechart on paper or on a software before implementing it for the first time in sismic.

![Cruise control statechart](Cruise_Control/Define_statechart/Statechart.png)

The statechart is in 2 parts. The first part represents the behaviour of a simplified car and the second part represents the Cruise Control behaviour.


### Car

The car begins with its engine off. If we press the start_stop button, we have a vehicle that is stationary but with the engine on. Then, by accelerating, the car is now moving and we can alter between 3 states :
- Accelerating : We press the acceleration pedal or the Cruise Control accelerates
- Braking : We press the brake pedal
- Driving : We are nor accelerating, nor braking

In each of these cases, each time a tick is triggered from the external clock, it will evaluate the speed of the car following its actual state :

- If it is accelerating, it will increase the speed by a provided acceleration rate
- If it is braking, it will decrease the speed a lot
- If it is driving, it will decrease the speed slowly

We can do all the inverse steps to get back to the initial state, the engine off.


### Cruise Control

The Cruise Control part has a lot more possibilities. Only the main operations will be described to make it short.

As the car is turned on, the Cruise Control (CC) goes from Unavailable to Off. Then, when the on_off button is pressed, the CC is On and ready to take control of the speed. But before that, it has to know at which speed it has to go. For that, the driver has to accelerate to a certain speed and press the SET button. This will have for effect to activate the CC at the speed the driver was going.

When the CC is activated, either it is accelerating if the current speed is below the target speed (mem_speed) or either it is not accelerating. At any moment, the driver can accelerate by itself which will Pause the CC and resume it when releasing the acceleration pedal. He can also brake, which will deactivate the CC. The target speed can be changed through the +/-/SET/RES buttons.