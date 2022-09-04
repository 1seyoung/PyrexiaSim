

from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_message import SysMessage
from pyevsim.definition import *
from pyevsim.system_simulator import SystemSimulator

import datetime
import random

from health_object import HealthObject
from env import Env
from human_model import HumanModel
from human_check import HumanCheck
from human_weather import HumanWeather

from camfind2 import camera_data


class SignalGenModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _sysengine):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("Generate", 1)

        self.insert_input_port("event")
        self.insert_output_port("info")

        

        self.sys_engine = _sysengine

        self.detect_map = {}


    def ext_trans(self,port, msg):
        if port == "event":
            self._cur_state = "Generate"


    def output(self):
        #print("out")
        if self._cur_state == "Generate":
            # color = random.choice(self.color_)
            # num = random.choice(self.num_)
            # # color = "red"
            # # num = "one"
            
            # len_num, color, num = SignalGenModel.data_len_data(self.color_, self.num_)
            self.color_,self.num_  = camera_data.main()
            print(f'색{self.color_},숫자{self.num_}')
            for i in range(len(self.color_)):
                for j in range(len(self.num_)):
                    color = self.color_[i]
                    num = self.num_[i][j-1]
             
                    print("------------------------------------")
                    print(f"Detect Person Info: {num}" )
                    print(f"Detect Color Info : {color}")
                    print("------------------------------------")
                
                    info = [num, color]

                    print(f"[SigGen]!info: {datetime.datetime.now()}")
                    
                    if num not in self.detect_map:
                        print("Dddddd")
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
                    print("요기까지왔음")
            # return SignalGenModel(0, Infinite, f"HumanModel[{num}]","seni_human", self.sys_engine)
            return None
            #return info

    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"
        else:
            self._cur_state = "IDLE"