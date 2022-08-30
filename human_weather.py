
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

import datetime
from health_object import HealthObject

class HumanWeather(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _id, _hi):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
               
        self.insert_input_port("winfo")

        self.health_obj = _hi
        self.hid = _id

    def ext_trans(self,port, msg):
        if port == "winfo":
            self.health_obj.env = msg.retrieve()[0]
        
        pass

    def output(self):
        return None

    def int_trans(self):
        #점선
        if self._cur_state == "IDLE":
            self._cur_state = "IDLE"