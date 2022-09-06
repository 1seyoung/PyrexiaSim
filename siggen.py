

from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

import datetime
import random
import pygsheets

from health_object import HealthObject
from env import Env
from human_model import HumanModel
from human_check import HumanCheck
from human_weather import HumanWeather

class SignalGenModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _sysengine):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("Generate", 5)

        self.insert_input_port("event")
        self.insert_output_port("info")

        self.color_ = ["red","blue"]
        self.num_ = ["one", "two", "three"]

        self.sys_engine = _sysengine


        self.detect_map = {}


    def ext_trans(self,port, msg):
        if port == "event":
            self._cur_state = "Generate"

                        
    def output(self):
        #print("out")
        if self._cur_state == "Generate":
            color = random.choice(self.color_)
            num = random.choice(self.num_)
            #color = "red"
            #num = "one"

            print()
            print(f"[SigGen]!info: {datetime.datetime.now()}")


            print(f"Detect Person Info: {num}" )
            print(f"Detect Color Info : {color}")



        
            info = [num, color]

            
            
            if num not in self.detect_map:
                
                _ho = HealthObject()
                hm = HumanModel(0, Infinite, f"HumanModel[{num}]","seni_human", num, _ho)
                hc = HumanCheck(0, Infinite, f"HumanCheck[{num}]","seni_human", num, _ho)
                hw = HumanWeather(0, Infinite, f"HumanWeather[{num}]","seni_human", num, _ho)
                
                self.sys_engine.get_engine("seni_human").insert_input_port(f"info[{num}]")

                self.sys_engine.get_engine("seni_human").register_entity(hm)
                self.sys_engine.get_engine("seni_human").coupling_relation(None,f"info[{num}]", hm, "info")
                self.sys_engine.get_engine("seni_human").coupling_relation(None,f"winfo", hw, "winfo")

                self.sys_engine.get_engine("seni_human").register_entity(hc)

                self.detect_map[num] = hm


                #ew = WeatherModel((0, Infinite, f"HumanCheck[{num}]","seni_human", num, _ev))
                #self.sys_engine.get_engine("seni_human").coupling_relation(self.env_model, f"winfo", hm, "info")

            self.sys_engine.get_engine("seni_human").insert_external_event(f"info[{num}]", info)

            return None
            #return info

    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"
        else:
            self._cur_state = "IDLE"