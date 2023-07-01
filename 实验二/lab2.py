import random
from experta import *
import time

switchtime=30
TotalCars=60
WECars=30

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
        time.sleep(0.1)
        self.retract(oldFact)
        self.declare(Fact(Ticks = times + 1))
        #print("{}s".format(times))
    #每分钟内的时间变化
    @Rule(AS.oldFact << Fact(curTicks=MATCH.times),
          salience=1
          
          )
    def ticker1(self,times,oldFact):
        time.sleep(0.1)
        self.retract(oldFact)
        self.declare(Fact(curTicks = times + 1))
        print("{}s".format(times)) 

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
        self.declare(Fact(NSsign = 'GREEN'))
        self.declare(Fact(WEsign = 'RED'))
        self.retract(oldSwtich)
        self.retract(oldWE)
        self.retract(oldNS) 
       # self.retract(oldct)  
    @Rule(
        AS.oldSwtich << Fact(switch = True),
        AS.oldNS << Fact(NSsign = 'GREEN'),
        AS.oldWE << Fact(WEsign = 'RED'),
        AS.oldct<<Fact(curTicks=MATCH.times),
        salience = 2
      )
    def switch2(self,oldSwtich,oldNS,oldWE,oldct):
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
        if WECars==(TotalCars/2):
            switchtime=30
        if WECars>(TotalCars/2):
            switchtime=40
        if WECars<(TotalCars/2):
            switchtime=20
        print("switchtime=",switchtime)
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
        TotalCars = random.randint(10, 100)
        WECars= random.randint(0,TotalCars)
        print("TotalCars=",TotalCars,"\n")
        print("WECars=",WECars,"\n")
engine = TrafficLights()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!