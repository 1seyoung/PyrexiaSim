
import requests
from bs4 import BeautifulSoup

from pyevsim.system_simulator import SystemSimulator
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.definition import *

#from pyevsim.system_executor import SysExecutor

from env import Env

import datetime

class WeatherModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _sysengine:SystemSimulator):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("CRAWLING",1)

        self.insert_input_port("event")
        self.insert_output_port("winfo")

        self.sys_engine = _sysengine

    def ext_trans(self,port, msg):
        if port == "event":
            self._cur_state = "CRAWLING"
    
    def output(self):
        if self._cur_state == "CRAWLING":

            #print("Naver Weather Update")      
            url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml")     

            sum = soup.find("dl", attrs={"class":"summary_list"})
            sensible_temp = sum.find_all("dd")[0].get_text() # 체감온도
            humidity = sum.find_all("dd")[1].get_text() # 습도
            #print(f"current sensible temp : {sensible_temp}")
            #print(f"current humidity : {humidity}")
            #print()
            
            self.sys_engine.get_engine("seni_human").insert_external_event("winfo", Env(sensible_temp, humidity))
        return None


    def int_trans(self):
        if self._cur_state == "CRAWLING":
            self._cur_state = "CRAWLING"
        else:
            self._cur_state = "IDLE"