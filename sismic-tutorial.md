# SISMIC tutorial by example

The purpose of this tutorial is to explain how to implement and test a statechart using [the SISMIC library](https://github.com/AlexandreDecan/sismic), by a means of a complete example created from scratch. We follow the methodology described in the scientific article [A method for testing and validating executable statechart models](https://doi.org/10.1007/s10270-018-0676-3).

# Context and methodology

The example used in this tutorial is a statechart to model and simulate the Adaptative Cruise Control of a car. To create the statechart with SISMIC we will go through the following steps :

1. Design phase
   1. Statechart design
      1. Defining the statechart
      2. Integrating code into the statechart
   2. Defining scenarios
   3. Defining properties
   4. Enriching the statechart with contracts
   5. Defining unit tests 
2. Getting results from the tests
3. Interfacing to External Components
   1. Integrating the statechart in the code
4. Second iteration

According to the methodology described in the article, one should first analyse the problem by making a user story, a UI mock-up and a component diagram, but this will not be covered in the current tutorial. 

Here is the UI mock-up of the GUI that will interact with the statechart. Different buttons can send events to the statechart (acceleration pedal, brake pedal, engine start button, ...) and some data from the statechart can be viewved on the dashboard (the speed, the memorized speed, indicator of Cruise Control switched on).

<p align="center">
   <img src="figures/mock-up.png">
</p>

The methodology also suggests to work in an iterative way. We will do so by first carrying out all the aforementioned steps for implementing a basic Cruise Control and then iterating over these steps again to add extend the model to an Adaptative Cruise Control.

# Design phase

## Design statechart

We suggest that you start designing your statechart on a piece of paper or some software application before actually implementing it for the first time in SISMIC. (In our case, we used the statechart modeling capabilities of the Itemis Create tool for creating the statechart model.)

<p align="center"> 
   <img src="Cruise_Control/Define_statechart/Statechart.png">
</p>

The statechart is composed of 2 parallel regions. The first region represents the behaviour of a simplified car and the second region represents the Cruise Control behaviour. As described before, the statechart will interact with a GUI. Then, most of the events in the statechart are triggered by buttons (acceleration pedal, brake pedal, engine start button, ...).

#### Car

The statechart in the Car region starts with its engine off. If we press the start_stop button, the vehicle will be stationary but with its engine on. Then, by accelerating, the car will start moving and can alter between 3 substates :
- Accelerating : when the driver presses the acceleration pedal or the Cruise Control accelerates
- Braking : when the driver presses the brake pedal
- Driving : when there is no acceleration or braking happening

In each of these cases, whenever a tick is triggered from an external clock, the model will evaluate the speed of the car following its actual state :

- If the car is accelerating, the speed will increase in function of the provided acceleration rate
- If the car is driving, the speed will decrease slowly (to simulate the friction of the car with the road)
   If the car is braking, the speed will be decrease much faster

A similar process as described above can be used to return back to the engine off state.

#### Cruise Control

The statechart in the Cruise Control (CC) region is considerably more complex. Only the main operations are described below to keep things short and clear.

When the car engine is turned on, the CC transitions from Unavailable to Off. Then, when the on_off button is pressed, the CC transitions to On and becomes ready to take control of the car speed. But before that, it has to know at which speed it needs to remain. To do so, the driver has to accelerate to a certain speed and press the SET button. This will have for effect to activate the CC at the speed the car was driving.

When the CC is activated, either it is not accelerating, or it is accelerating if the current speed is still below the target speed (mem_speed). At any moment, the driver can decide to accelerate the car by itself. This will pause the CC and resume it when releasing the acceleration pedal. The driver can also decide to brake, which will deactivate the CC. The target speed can be changed through the +/-/SET/RES buttons.


### Defining the statechart in SISMIC

Once the statechart is designed, we can now implement it in SISMIC. [This page of the SISMIC documentation](https://sismic.readthedocs.io/en/latest/format.html) explains the syntax to follow for the differents states and transitions. Here, we will be explain, in a top-down approach, how to assemble these states to define a complex statechart.

#### Parallel states

The initial configuration of the statechart is modeled in SISMIC as two parallel state representing the Car and Cruise Control parts. The code then starts with the following syntax. 

<p align="center">
| <img src="figures/parallel-states-statechart.png">
<br></br>
<img src="figures/parallel-states-yaml.png">
</p>


#### Composite states

If we look deeper in the statechart, each parallel state contains several substates, of which some or basic states and some are composite states. For example, the parallel state Car contains two basic states Engine_off and Stationary_Vehicle, and one composite substate Moving. This composite state is itself composed of 3 nested substates, of which the initial one is Accelerating. This is declared as follows.


| <img src="figures/car-composite-states.png"> | <img src="figures/car-composite-states-yaml.png"> |
|----------------------------------------------|----------------------------------------------------|

#### States & transitions

Now that the composite states has been defined, we can move on to the basic states. These ones are defined by their names, their (optional) external transitions and an (optional) on-entry event. Code execution in states will be discussed in the next section. Here is an example of transitions' definition.

| <img src="figures/transition.png"> | <img src="figures/transitions-yaml.png"> |
|------------------------------------|-------------------------------------------|

### Integrating code into the statechart


