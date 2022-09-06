
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

import datetime
from health_object import HealthObject

from pyevsim.system_simulator import SystemSimulator

import google_log

class HumanCheck(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name, _id,
                 _hu):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time,
                                       name, engine_name)

        self.init_state("HUMAN_CHECK")
        #self.insert_state("IDLE", Infinite)
        self.insert_state("HUMAN_CHECK", 1)

        #self.insert_input_port("info")
        #self.insert_output_port("check")
        self.health_obj = _hu
        self.hid = _id

        self.goup = google_log.Google_update()

        self.se = SystemSimulator().get_engine(engine_name)

    def ext_trans(self, port, msg):
        pass

    def output(self):

        #print(f"!check health: {datetime.datetime.now()}")
        if self.health_obj.human.health_score < 30:
            print(
                f"{self.get_engine_name()},{self.se.get_global_time()}, {self.hid},{self.health_obj.human.health_score}, Health Danger"
            )
            _list =[f"{self.get_engine_name()}",f"{self.se.get_global_time()}",f"{self.hid}",f"{self.health_obj.human.health_score}"]
            self.goup.update_log(_list)
            return None
        elif self.health_obj.human.health_score < 50:
            print(
                f"{self.get_engine_name()},{self.se.get_global_time()}, {self.hid},{self.health_obj.human.health_score}, Health Attention "
            )
            _list =[f"{self.get_engine_name()}",f"{self.se.get_global_time()}",f"{self.hid}",f"{self.health_obj.human.health_score}"]
            self.goup.update_log(_list)            
            return None
        else:
            print(
                f"{self.get_engine_name()},{self.se.get_global_time()}, {self.hid},{self.health_obj.human.health_score}, Health Okay"
            )
            _list =[f"{self.get_engine_name()}",f"{self.se.get_global_time()}",f"{self.hid}",f"{self.health_obj.human.health_score}"]
            self.goup.update_log(_list)
            return None

    def int_trans(self):
        #점선
        if self._cur_state == "HUMAN_CHECK":
            self._cur_state = "HUMAN_CHECK"
