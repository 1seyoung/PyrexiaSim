
import env

class Human(object):
    def __init__(self):
        self.health_score = 80

class HealthObject(object):
    def __init__(self):
        self.human = Human()
        self.env = env.Env(0, 0)
    
    def control_dec(self):
        #red
        ctemp= self.env.sensible_temp
        if ctemp ==0:
            return 10
        else:
                
            decrease = 10 #증가

            ctemp= float(self.env.sensible_temp[:-1])
            if ctemp >= 37.0:
                #danger
                return decrease * 1.8
            elif ctemp >=34.0:
                return decrease * 1.6
            elif ctemp >= 31.0:
                return decrease * 1.4
            else:
                return decrease 

    def control_inc(self):
        #blue
        ctemp= self.env.sensible_temp
        if ctemp == 0:
            return 10
        else:

            increase = 10 #감소

            ctemp= float(self.env.sensible_temp[:-1])
            if ctemp >= 37.0:
                return increase * 0.4
            elif ctemp >=34.0:
                return increase * 0.6
            elif ctemp >=31.0:
                return increase * 0.8
            else :
                return increase


    def assess_health(self, state):

        if state == "blue":
            ins = self.control_inc()
            print(f"{ins}점```수 변화가 있니아용ㅇ")
            self.human.health_score += ins
            return self.human.health_score
        else:
            dec = self.control_dec()
            self.human.health_score -= dec
            return self.human.health_score

    