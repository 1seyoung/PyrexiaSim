
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

import datetime
from health_object import HealthObject

class HumanCheck(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _id, _hu):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("HUMAN_CHECK")
        #self.insert_state("IDLE", Infinite)
        self.insert_state("HUMAN_CHECK", 1)
        
        #self.insert_input_port("info")
        #self.insert_output_port("check")
        self.health_obj = _hu
        self.hid = _id


    def ext_trans(self,port, msg):
        pass

    def output(self):

        print(f"!check health: {datetime.datetime.now()}")
        if self.health_obj.human.health_score <30:
            print(f"Humnan[{self.hid}][{self.health_obj.human.health_score}] Health Danger!!!: {datetime.datetime.now()}")
            return None
        elif self.health_obj.human.health_score <50:
            print(f"Humnan[{self.hid}][{self.health_obj.human.health_score}] Health Attention: {datetime.datetime.now()}")  
            return None          
        else:
            print(f"Humnan[{self.hid}][{self.health_obj.human.health_score}] Health is Okay: {datetime.datetime.now()}")
            return None

    def int_trans(self):
        #점선
        if self._cur_state == "HUMAN_CHECK":
            self._cur_state = "HUMAN_CHECK"