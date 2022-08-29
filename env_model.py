
import requests
from bs4 import BeautifulSoup

from pyevsim.system_simulator import SystemSimulator
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.definition import *

from env import Env

import datetime

class WeatherModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _ew):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("CRAWLING",1)

        self.insert_input_port("event")
        self.insert_output_port("winfo")

        self.env_w = _ew

    def ext_trans(self,port, msg):
        if port == "event":
            self._cur_state = "CRAWLING"
    
    def output(self):
        if self._cur_state == "CRAWLING":

            print("-------------Naver Weather Update------------")      
            url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml")     

            sum = soup.find("dl", attrs={"class":"summary_list"})
            self.env_w.sensible_temp = sum.find_all("dd")[0].get_text() # 체감온도
            self.env_w.humidity = sum.find_all("dd")[1].get_text() # 습도
            print(self.env_w.sensible_temp)
            print(self.env_w.humidity)
        return None


    def int_trans(self):
        if self._cur_state == "CRAWLING":
            self._cur_state = "CRAWLING"
        else:
            self._cur_state = "IDLE"

ss = SystemSimulator()
ss.register_engine("env_weather", "REAL_TIME", 0.1)

ss.get_engine("env_weather").insert_input_port("start")

_ew = Env()
ewm = WeatherModel(0,Infinite,"Env_Weather","env_weather",_ew)
ss.get_engine("env_weather").register_entity(ewm)
ss.get_engine("env_weather").coupling_relation(None, "start", ewm, "event")
ss.get_engine("env_weather").insert_external_event("start", None)
ss.get_engine("env_weather").simulate()