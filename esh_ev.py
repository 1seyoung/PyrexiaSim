#from distutils.log import info
#from turtle import color
from pyevsim.system_simulator import SystemSimulator
from pyevsim.definition import *

from human import Human
from human_model import HumanModel
from siggen import SignalGenModel

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
ss.register_engine("seni_cam", "REAL_TIME", 0.1)

ss.get_engine("seni_cam").insert_input_port("start")

gen = SignalGenModel(0, Infinite, "SignalGen", "seni_cam", ss)
ss.get_engine("seni_cam").register_entity(gen)
ss.get_engine("seni_cam").coupling_relation(None, "start", gen, "event")

ss.get_engine("seni_cam").insert_external_event("start", None)
#ss.get_engine("seni_cam").simulate()

ss.register_engine("seni_human", "REAL_TIME", 0.1)
#ss.get_engine("seni_human").insert_input_port("info")

ss.exec_non_block_simulate(["seni_cam", "seni_human"])
ss.block()