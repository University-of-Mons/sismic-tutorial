from sismic.bdd import map_action, map_assertion
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from behave import when, then
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Define_statechart.Car import Car
from Define_statechart.FrontCar import FrontCar


# Car part

@when('I initialize the context')
def initialize(context):
    statechart = import_from_yaml(filepath='Define_statechart/statechart_with_contracts.yaml')
    car = Car()
    front_car = FrontCar(700,701)
    inter = Interpreter(statechart, initial_context={'car':car,'front_car':front_car})
    context.interpreter = inter


@then('the speed is {value}')
def speed(context, value):
    assert context.interpreter.context["car"].get_speed() == int(value)

map_action('the engine is off', 'I do nothing')

map_action('I press the engine_start_stop button', 'I send event engine_start_stop_button_pressed')
map_assertion('the vehicle is stationary', 'state Stationary_vehicle is active')

map_action('the vehicle is stationary', 'I reproduce "Turn on the car"')
map_action('I accelerate', 'I send event accelerate with accel = 100')
map_assertion('I am accelerating', 'state Accelerating is active')
map_assertion('I am driving', 'state Driving is active')

map_action('I am driving','I reproduce "Stop accelerating"')

map_action('I am accelerating','I reproduce "Accelerate the car"')
map_action('I stop accelerating','I send event stop_accelerate')

@when('{value} seconds pass')
def pass_seconds(context, value):
    for _ in range(int(float(value)*10)):
        context.execute_steps('when I send event tick')

map_action('I brake', 'I send event brake with decel=100')
map_assertion('I am braking', 'state Braking is active')

map_assertion('the engine is off','state Engine_off is active')


# Cruise Control part

map_action('the CC is off', "I do nothing")
map_action('I press the CC on_off button','I send event on_off_button_pressed')
map_assertion('the CC is on', 'state On is active')

map_action('the CC is on', 'I reproduce "Turn on the CC"')
map_assertion('the CC is off','state Off is active')

@when('I accelerate to {value} km/h')
def accelerate_to(context, value):
    context.execute_steps('when I send event accelerate with accel=100')
    
    while context.interpreter.context["car"].get_real_speed() <= int(value):
        context.execute_steps('when I send event tick')

    context.execute_steps('when I send event stop_accelerate')



map_action('I press the set button', 'I send event set_button_pressed')

map_assertion('the CC is activated', 'state Activated is active')
map_assertion('the memorized speed is {value}', 'variable mem_speed equals {value}')

map_action('the CC is activated at 50km/h', 'I reproduce "Activate the CC to 50km/h"')
map_action('I press the minus button', 'I send event minus_button_pressed')
map_action('I press the plus button', 'I send event plus_button_pressed')
map_action('I press the res button', 'I send event res_button_pressed')

map_assertion('the CC is desactivated','state Activated is not active')

map_action('the CC is desactivated', 'I reproduce "Desactivate with button"')

map_action('I decelerate of {value} km/h','I repeat "I brake" {value} times')

@when('I brake to {value} km/h')
def brake_to(context, value):
    context.execute_steps('when I send event brake with decel=100')
    
    while context.interpreter.context["car"].get_real_speed() > int(value):
        context.execute_steps('when I send event tick')

    context.execute_steps('when I send event stop_braking')
