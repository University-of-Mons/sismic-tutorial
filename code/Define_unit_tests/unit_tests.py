import unittest
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from sismic.exceptions import ContractError
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Define_statechart.Car import Car

class CCTests(unittest.TestCase):
    def setUp(self):
        statechart = import_from_yaml(filepath="Define_statechart/statechart_with_contracts.yaml")
        self.car = Car()
        self.cc = Interpreter(statechart, initial_context={'car':self.car})
        self.cc.execute_once()

    def test_braking_when_activated(self):
        self.cc.queue("engine_start_stop_button_pressed")
        self.cc.queue("accelerate", accel=100)
        self.cc.queue("tick","tick","tick","tick","on_off_button_pressed","set_button_pressed","stop_accelerate","tick","tick","tick")
        self.cc.execute()
        self.cc.queue("brake")
        self.cc.execute_once()
        self.cc.queue("stop_brake")
        self.cc.execute_once()
        self.assertNotIn("Activated", self.cc.configuration)

    def test_changing_mem_speed_value_with_accelerate(self):
        self.cc.queue("engine_start_stop_button_pressed")
        self.cc.queue("accelerate", accel=100)
        self.cc.queue("tick","tick","tick","tick","on_off_button_pressed","set_button_pressed","stop_accelerate")
        self.cc.execute()
        self.assertEqual(self.cc.context["mem_speed"], 7)

        self.cc.queue("accelerate",accel=100)
        self.cc.queue("tick","tick","tick","tick","tick","tick","tick","tick","stop_accelerate")
        self.cc.execute()

        self.cc.queue("set_button_pressed")
        self.cc.execute_once()
        
        self.assertEqual(self.cc.context["mem_speed"], 19)


    def test_respect_contract_moving(self):
        self.cc.queue("engine_start_stop_button_pressed")
        self.cc.queue("accelerate", accel=100)
        self.cc.queue("tick","tick","tick","tick","on_off_button_pressed","set_button_pressed","tick","tick","tick")
        self.cc.execute()
        self.cc.queue("brake","tick","tick","tick","tick")
        self.cc.execute()
        self.assertEqual(self.car.get_speed(), 0)
        self.assertFalse(self.cc.configuration.__contains__("Moving"))

    
    def test_break_contract_mem_speed(self):
        self.cc.queue("engine_start_stop_button_pressed")
        self.cc.queue("accelerate", accel=100)
        self.cc.queue("tick","tick","tick","tick","on_off_button_pressed","set_button_pressed","tick","tick","tick")
        self.cc.execute()
        with self.assertRaises(ContractError):
            self.cc.context["mem_speed"] = 161
            self.cc.execute_once()


    def test_break_contract_stationary_when_activated(self):
        self.cc.queue("engine_start_stop_button_pressed")
        self.cc.queue("accelerate", accel=100)
        self.cc.queue("tick","tick","tick","tick","on_off_button_pressed","set_button_pressed","tick","tick","tick")
        self.cc.execute()
        with self.assertRaises(ContractError):
            self.car.speed = 0
            self.cc.queue("tick")
            self.cc.execute_once()
