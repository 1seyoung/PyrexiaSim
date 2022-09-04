#from distutils.log import info
#from turtle import color
from pyevsim.system_simulator import SystemSimulator
from pyevsim.definition import *

from health_object import HealthObject
from human_model import HumanModel
from siggen import SignalGenModel
from env_model import WeatherModel

### [engine:senicam(siggen)]-----[engine:seni_human  (Human_num(create each) - check, work)]

####  model create
'''
def num_to_Human(pair):

    print("Dddddd")
    num, _ = pair
    hm = HumanModel(0, Infinite, f"HumanModel[{num}]","seni",pair)

    se.insert_input_port("info")
    se.register_entity(hm)
    se.coupling_relation(gen,"info", hm, "info")
'''
###

ss = SystemSimulator()
first = ss.register_engine("seni_cam", "REAL_TIME", 0.1)

first.insert_input_port("start")

ew = WeatherModel(0, Infinite, "Weather","seni_human", ss)
gen = SignalGenModel(0, Infinite, "SignalGen", "seni_cam", ss)

first.register_entity(gen)
first.register_entity(ew)
first.coupling_relation(None, first.start, gen, gen.event)
first.coupling_relation(None, first.start, ew, ew.event)

first.insert_external_event(first.start, None)
#ss.get_engine("seni_cam").simulate()

second=ss.register_engine("seni_human", "REAL_TIME", 0.1)
second.insert_input_port("winfo")

ss.exec_non_block_simulate(["seni_cam", "seni_human"])
ss.block()