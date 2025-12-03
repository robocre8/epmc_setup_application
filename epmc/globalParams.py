import time
from math import sin, pi

class g():
  dirConfigTextList = ['left wheel', 'right wheel']
  durationList = [5,10, 15, 20] # in sec
  signalList = ["square", "step", "triangle", "sine"]

  app = None
  epmc = None
  port = "None"

  i2cAddress = None

  motorTestPwm = [0, 0] 
  motorTestDuration = [durationList[1], durationList[1]]
  
  motorInitialTheta = [-90, -90]
  motorTheta = [0.0, 0.0]

  motorPPR = [1000.0, 1000.0]
  motorDirConfig = [1, 1]
  motorDirConfigText = [dirConfigTextList[0], dirConfigTextList[0]]

  motorStartTime = [time.time(), time.time()]
  motorIsOn = [False, False]

  motorAngPos = [0.0, 0.0]
  motorAngVel = [0.0, 0.0]


  motorKp = [0.0, 0.0]
  motorKi = [0.0, 0.0]
  motorKd = [0.0, 0.0]
  motorCf = [0.0, 0.0]

  motorMaxVel = [10.0, 10.0]
  motorTargetMaxVel = [0.0, 0.0]
  motorTestSignal = [signalList[0], signalList[0]]

  motorTargetVel = [0.0, 0.0]
  motorActualVel = [0.0, 0.0]
  #######################################################






###################################################################

def stepSignal(targetMax, deltaT, duration):
  if (deltaT>(2/10*duration)):
     targetCtrl = targetMax
  else:
     targetCtrl = 0              
  return targetCtrl

def squareSignal(targetMax, deltaT, duration):
  if (deltaT>(1/10*duration)) and (deltaT < (4/10*duration)):
     targetCtrl = targetMax
  elif (deltaT>(6/10*duration)) and (deltaT < (9/10*duration)):
     targetCtrl = -1*targetMax
  else:
     targetCtrl = 0              
  return targetCtrl

def sineSignal(targetMax, deltaT, duration):
  targetCtrl = targetMax * sin(2*pi*(deltaT/duration))
  return targetCtrl

def triangleSignal(targetMax, deltaT, duration):
    # Normalized time in range [0,1)
    t = (deltaT / duration) % 1.0
    
    # Triangle wave goes 0 → +max → 0 → -max → 0
    if t < 0.25:  
        targetCtrl = 4 * targetMax * t
    elif t < 0.75:  
        targetCtrl = 2 * targetMax - 4 * targetMax * t
    else:  
        targetCtrl = -4 * targetMax + 4 * targetMax * t
    return targetCtrl


def selectSignal(type, targetMax, deltaT, duration):
  if type == g.signalList[0]:
    targetCtrl = squareSignal(targetMax, deltaT, duration)
  elif type == g.signalList[1]:
    targetCtrl = stepSignal(targetMax, deltaT, duration)
  elif type == g.signalList[2]:
    targetCtrl = triangleSignal(targetMax, deltaT, duration)
  elif type == g.signalList[3]:
    targetCtrl = sineSignal(targetMax, deltaT, duration)
  else:
    targetCtrl = 0.0
  
  return targetCtrl


##############################################################################