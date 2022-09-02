
import env

class Human(object):
    def __init__(self):
        self.health_score = 80

class HealthObject(object):
    def __init__(self):
        self.human = Human()
        self.env = env.Env(0, 0)

    def assess_health(self, state):
        #self.env.
        if state == "blue":
            self.human.health_score += 10
            return self.human.health_score
        else:
            self.human.health_score -= 10
            return self.human.health_score

    