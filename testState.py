from state import *

class SleepState(State):
     def __init__(self):
          State.__init__(self,"sleep",SleepState.EventTable)
          
     def Start(self, args=()):
          self.stop=False
          self.sleepTime=0
          print "Bob is now asleep."
          
     def Update(self, args=()):
          self.sleepTime+=1
          print "Bob is still asleep, as he had been the past "+str(self.sleepTime)+" turns."
          
     def Stop(self, args=()):
          print "Bob woke up!"

     def Shout(self, args=()):
          print "SHUT UP BEFORE I STAB YOU!!!"
     
     def Tickle(self, args=()):
          print "Haha...Wha..?"
          
     def Punch(self, args=()):
          print "Oof! What the...?"
          
     def Read(self, args=()):
          print "Zzz..."
          
     EventTable={ 'start': (Start, None),
                  'stop': (Stop, "wake"),
                  'update': (Update, None),
                  'shout': (Shout, "wake"),
                  'tickle': (Tickle, None),
                  'punch': (Punch, "wake"),
                  'read': (Read, None) }
                  
                  
class WakeState(State):
     def __init__(self):
          State.__init__(self,"wake",WakeState.EventTable)
          
     def Start(self, args=()):
          self.stop=False
          self.wakeTime=0
          print "Bob is now awake."
          
     def Update(self, args=()):
          self.wakeTime+=1
          print "Bob is still awake, as he had been the past "+str(self.wakeTime)+" turns."
          
     def Stop(self, args=()):
          print "Bob fell asleep!"

     def Shout(self, args=()):
          print "SHUT UP BEFORE I STAB YOU!!!"
     
     def Tickle(self, args=()):
          print "Haha...Stop it!"
          
     def Punch(self, args=()):
          print "You're dead, sucker!"
          
     def Read(self, args=()):
          print "Right...Goldilocks...Zzz..."
          
     EventTable={ 'start': (Start, None),
                  'stop': (Stop, "sleep"),
                  'update': (Update, None),
                  'shout': (Shout, None),
                  'tickle': (Tickle, None),
                  'punch': (Punch, None),
                  'read': (Read, "sleep") }
def main():
     s=StateMachine()
     s.AddState(WakeState())
     s.AddState(SleepState())
     s.startState="sleep"
     s.Start()
     
     while True:
          s.Update()
          input=raw_input("What next?")
          if input == "end":
               break
          else:
               s.OnMessage(input)
          
                  
if __name__ == '__main__': main()
