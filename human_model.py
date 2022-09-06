
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

import datetime

class HumanModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _id, _hu):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("WORK_CHECK", 0)
        
        self.insert_input_port("info")

        self.increment = 10
        #self.insert_output_port("check")
        self.health_obj = _hu
        self.hid = _id

        self.recv_info = None

    def ext_trans(self,port, msg):
        #실선
        if port == "info":
            info = msg.retrieve()[0]

            if info[0] == self.hid:
                self._cur_state = "WORK_CHECK"
                self.recv_info = info[1]
            else:
                self._cur_state = self._cur_state

    def output(self):
        #점선의 레이블 현재 상태를 기반으로 어떤 데이터를 내보낼지 결정하는 역할
        ##사람 데이터를 다 저장하고 있는 클래스 만들어야함
        #self._cur_state == "CHECK"
        
        if self.recv_info == "blue":
            print(f"\n?blue: {datetime.datetime.now()}")
            self.health_obj.human.health_score = self.health_obj.assess_health("blue")
            print(f"\nHuman[{self.hid}] Health Score Increase")
        elif self.recv_info == "red":
            print(f"\n?red: {datetime.datetime.now()}")
            self.health_obj.human.health_score = self.health_obj.assess_health("red")
            print(f"\nHuman[{self.hid}] Health Score Decrese")


    def int_trans(self):
        #점선
        if self._cur_state == "WORK_CHECK":
            self._cur_state = "IDLE"
