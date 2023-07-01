from asyncio import Lock
import random
from experta import *
import time

import serial
from infer import InferenceEngine
from infer import rules
import  threading
switchtime=30
TotalCars=20
WECars=0
crossnumber=0
ledstate=1

inference_engine = InferenceEngine(rules)
class TrafficLights(KnowledgeEngine):
    @DefFacts()
    def first(self):
        yield Fact(Ticks = 0)
        yield Fact(curTicks=0)  #每次转换后归零
        yield Fact(NSsign = 'RED')
        yield Fact(WEsign = 'GREEN')
        yield Fact(switchTime = 30)   #max=50,min=10
        yield Fact(period = 200)
        yield Fact(TotalCars=60)
        yield Fact(WECars=30)

    #总的时间
    @Rule(AS.oldFact << Fact(Ticks=MATCH.times))
    def ticker(self,times,oldFact):
        time.sleep(0.3)
        self.retract(oldFact)
        self.declare(Fact(Ticks = times + 1))
        #print("{}s".format(times))
    #每分钟内的时间变化
    @Rule(AS.oldFact << Fact(curTicks=MATCH.times),
          salience=1
          
          )
    def ticker1(self,times,oldFact):
        time.sleep(0.3)
        self.retract(oldFact)
        self.declare(Fact(curTicks = times + 1))
        color='RED'
        if ledstate==1:
            color='GREEN'
        print("{}s".format(times),"WEsign{}".format(color))
        

    @Rule(AS.oldFact << Fact(Ticks=MATCH.times),
          Fact(period = MATCH.period),
          TEST(lambda times,period: times == period),
          salience = 2
         )
    def exit(self,oldFact):
        choice = input('are you going to quit?')
        if 'Y' in choice.upper(): 

            self.declare(Fact(action = 'halt'))
        else:
            self.retract(oldFact)
            self.declare(Fact(Ticks = 0))
  


    #curTicks=switchTime, isSwitch=true
    @Rule(AS.oldtimes<<Fact(curTicks = MATCH.times),
          TEST(lambda times:times == switchtime),
          salience= 2)
    def switchSgin1(self,times):
        self.declare(Fact(switch=True))
        #curTicks=switchTime, isSwitch=true
    #每分钟归零并且准备changecars
    @Rule(AS.oldtimes<<Fact(curTicks = MATCH.times),
          TEST(lambda times:times == 60),
          salience= 2)
    def switchSgin2(self,times,oldtimes):
        self.declare(Fact(switch=True))
        self.declare(Fact(changecars=True))
        self.declare(Fact(curTicks=0))
        self.retract(oldtimes)


    #switch
    @Rule(
        AS.oldSwtich << Fact(switch = True),
        AS.oldNS << Fact(NSsign = 'RED'),
        AS.oldWE << Fact(WEsign = 'GREEN'),
        AS.oldct<<Fact(curTicks=MATCH.times),
        salience = 2
      )
    def switch1(self,oldSwtich,oldNS,oldWE,oldct): 
        global ledstate
        self.declare(Fact(NSsign = 'GREEN'))
        self.declare(Fact(WEsign = 'RED'))
        self.retract(oldSwtich)
        self.retract(oldWE)
        self.retract(oldNS) 
        ledstate=0
       # self.retract(oldct)  
    @Rule(
        AS.oldSwtich << Fact(switch = True),
        AS.oldNS << Fact(NSsign = 'GREEN'),
        AS.oldWE << Fact(WEsign = 'RED'),
        AS.oldct<<Fact(curTicks=MATCH.times),
        salience = 2
      )
    def switch2(self,oldSwtich,oldNS,oldWE,oldct):

        global ledstate
        ledstate =1
        self.declare(Fact(NSsign = 'RED'))
        self.declare(Fact(WEsign = 'GREEN'))
        self.retract(oldSwtich)
        self.retract(oldWE)
        self.retract(oldNS)

        #self.retract(oldct)


    #假设车辆每分钟变化啊一次

    @Rule(AS.oldf<<Fact(changecars=True),

          salience= 2)
    def switchCars(self,oldf):
        self.declare(Fact(changetime=True))
        self.retract(oldf)
        self.generateCars()

    @Rule(AS.oldf<<Fact(changetime=True),
          salience=2)
    def switchwetime(self,oldf):
        global switchtime
        car_info = {'WECars': WECars,'TotalCars': TotalCars}
        inference_engine.infer(car_info)

    # 输出结果
        # print(f"Switch time for east-west direction - {car_info['switchTime']} seconds")
        switchtime =car_info['switchTime']
        self.retract(oldf)
    @Rule(
        Fact(NSsign = MATCH.NScolor),
        Fact(WEsign = MATCH.WEcolor),
        salience = 2
      )
    def show(self,NScolor,WEcolor):
        print('\nNS:WE={}:{}\n'.format(NScolor,WEcolor))


    @Rule(
        Fact(action = 'halt'),
        salience = 2
      )
    def halts(self):
        print('bye')
        self.halt()
    
    def generateCars(self):
        global TotalCars
        global WECars
        global crossnumber
        WECars = crossnumber
        crossnumber=0
        print("WECars=",WECars,"\n")



# 创建串口对象
ser = serial.Serial('COM3', 9600)  # 替换成正确的串口和波特率

# 定义读取数据的线程
def read_thread():
    while True:
        # 从串口读取数据
        # Lock.acquire()
        global crossnumber
        data = ser.readline().decode().strip()
        # 处理读取到的数据
        if data == 'YES':
            crossnumber=crossnumber+1
        time.sleep(0.1)
        # Lock.release()
# 定义写入数据的线程
def write_thread():
    while True:
        # Lock.acquire()
        user_input='0'
        if ledstate==1:
            user_input='1'
        elif ledstate==0:
            user_input='0'
        # 写入数据到串口
        
        ser.write(user_input.encode())

        time.sleep(0.1)
        # Lock.release()
if __name__ == '__main__':
    # 创建并启动读取线程
    read_thread = threading.Thread(target=read_thread)
    read_thread.start()

    # 创建并启动写入线程
    write_thread = threading.Thread(target=write_thread)
    write_thread.start()

    # 创建并运行专家库
    engine = TrafficLights()
    engine.reset()  # Prepare the engine for the execution.
    engine.run()  # Run it!


