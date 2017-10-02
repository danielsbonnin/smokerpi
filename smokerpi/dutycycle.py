import math
class DutyCycle:
    def __init__(self, goal_temp, duration, outside_temp=75, wind=0):
        self.temp_difference = goal_temp - outside_temp
        self.duration = duration
        self.wind = wind
        self.goal_temp = goal_temp
        self.outside_temp = outside_temp
        self.duty_prop_max = min(1.0, self.temp_difference / 250.0)
        self.duty_prop = 0.5 * self.duty_prop_max
        self.count = 0
        self.error = 0.0
    def sigmoid(self, x):
        """
        src: stackoverflow.com/questions/3985619 Neil G's answer
        """
        if x >= 0:
            z = math.exp(-x)
            return 1 / (1 + z)
        else:
            z = math.exp(x)
            return z / (1 + z)
    
    def process_pid_output(self, pid_output):
        sigOutput = self.sigmoid(pid_output)
        if abs(pid_output) < 5: # Throw out windup and outliers 
            self.count += 1
            self.error += 0.5 - sigOutput
            if self.count == 10: # number to average over
                self.duty_prop_max -= (self.error * self.duty_prop_max / 10)
                print("dutycycle.py: resetting max duty cycle to {}. Accum'd. error was: {}".format(
                    self.duty_prop_max, self.error))
                if self.duty_prop_max > 1:
                    self.duty_prop_max = 1
                elif self.duty_prop_max < 0.1:
                    self.duty_prop_max = 0.1
                self.error = 0
                self.count = 0
        cur_duty_prop = sigOutput * self.duty_prop_max
        self.duty_prop = cur_duty_prop
        return self.duty_prop 
    def get_durations(self):
        on_time = self.duty_prop * self.duration
        off_time = self.duration - on_time
        return (on_time, off_time)
    def __str__(self):
        on, off = self.get_durations()
        ret = "Duration: {}\nMax Proportion: {}\nCurrent Duty Proportion: {}\nGoal Temp: {}\nOn Time: {} Off Time: {}".format(
            self.duration, 
            self.duty_prop_max, 
            self.duty_prop, 
            self.goal_temp, 
            on,
            off)
        return ret
