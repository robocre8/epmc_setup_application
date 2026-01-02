import serial
import time

# Serial Protocol Command IDs -------------
WRITE_SPEED = 10
READ_SPEED = 11
READ_TSPEED = 12
READ_POS = 13
WRITE_PWM = 14
SET_KP = 15
GET_KP = 16
SET_KI = 17
GET_KI = 18
SET_KD = 19
GET_KD = 20
SET_PPR = 21
GET_PPR = 22
SET_CF = 23
GET_CF = 24
SET_RDIR = 25
GET_RDIR = 26
SET_PID_MODE = 27
GET_PID_MODE = 28
SET_CMD_TIMEOUT = 29
GET_CMD_TIMEOUT = 30
SET_I2C_ADDR = 31
GET_I2C_ADDR = 32
SET_MAX_SPEED = 33
GET_MAX_SPEED = 34
RESET = 35
CLEAR = 36
#---------------------------------------------



class EPMC:
    def __init__(self):
        pass

    def connect(self, port, baud=115200, timeOut=0.1):
        self.ser = serial.Serial(port, baud, timeout=timeOut)
        time.sleep(0.1)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
    
    def disconnect(self):
        if self.ser.is_open:
            self.ser.close()

    #------------------------------------------------------------------------
    def send(self, cmd, arg1=0.0, arg2=0.0):
        send_str = str(float(cmd))+" "+str(round(float(arg1),4))+" "+str(round(float(arg2),4))+"\r"
        self.ser.write(send_str.encode())

    def recv(self, cmd, arg1=0):
        try:
            self.send(cmd, arg1)
            data = self.ser.readline().decode().strip().split(' ')
            return True, round(float(data[0]),4), round(float(data[1]),4)
        except:
            # self.ser.reset_input_buffer()
            # self.ser.reset_output_buffer()
            return False, 0.0, 0.0
        
    #---------------------------------------------------------------------
    #         BASIC COMMANDS
    #---------------------------------------------------------------------
    
    def writeSpeed(self, v0, v1):
        self.send(WRITE_SPEED, v0, v1)

    def readSpeed(self):
        success, vel0, vel1 = self.recv(READ_SPEED)
        return success, vel0, vel1
    
    def writePWM(self, pwm0, pwm1):
        self.send(WRITE_PWM, pwm0, pwm1)
    
    def readPos(self):
        success, pos0, pos1 = self.recv(READ_POS)
        return success, pos0, pos1
    
    def setCmdTimeout(self, timeout):
        self.send(SET_CMD_TIMEOUT, 0.0, float(timeout))
        
    def getCmdTimeout(self):
        success, timeout, _ = self.recv(GET_CMD_TIMEOUT)
        return success, int(timeout)
    
    def setPidMode(self, mode):
        self.send(SET_PID_MODE, 0.0, mode)
    
    def getPidMode(self):
        success, mode, _ = self.recv(GET_CMD_TIMEOUT)
        return success, int(mode)
    
    def clearDataBuffer(self):
        success, _, _ = self.recv(CLEAR)
        return success
    
    def getMaxSpeed(self, motor_no):
        success, maxVel, _ = self.recv(GET_MAX_SPEED, motor_no)
        return success, round(maxVel, 3)
    
    #---------------------------------------------------------------------
    #         ADVANCED COMMANDS (USE WITH CAUTION)
    #---------------------------------------------------------------------
    
    def readTSpeed(self):
        success, vel0, vel1 = self.recv(READ_TSPEED)
        return success, vel0, vel1

    def setPPR(self, motor_no, ppr):
        self.send(SET_PPR, motor_no, ppr)
    
    def getPPR(self, motor_no):
        success, ppr, _ = self.recv(GET_PPR, motor_no)
        return success, round(ppr, 3)
    
    def setKp(self, motor_no, kp):
        self.send(SET_KP, motor_no, kp)
    
    def getKp(self, motor_no):
        success, kp, _ = self.recv(GET_KP, motor_no)
        return success, round(kp, 3)
    
    def setKi(self, motor_no, ki):
        self.send(SET_KI, motor_no, ki)
    
    def getKi(self, motor_no):
        success, ki, _ = self.recv(GET_KI, motor_no)
        return success, round(ki, 3)
    
    def setKd(self, motor_no, kd):
        self.send(SET_KD, motor_no, kd)
    
    def getKd(self, motor_no):
        success, kd, _ = self.recv(GET_KD, motor_no)
        return success, round(kd, 3)
    
    def setRdir(self, motor_no, rdir):
        self.send(SET_RDIR, motor_no, rdir)
    
    def getRdir(self, motor_no):
        success, rdir, _ = self.recv(GET_RDIR, motor_no)
        return success, int(rdir)
    
    def setCutOffFreq(self, motor_no, cutOffFreq):
        self.send(SET_CF, motor_no, cutOffFreq)
    
    def getCutOffFreq(self, motor_no):
        success, cutOffFreq, _ = self.recv(GET_CF, motor_no)
        return success, round(cutOffFreq, 3)
    
    def setMaxSpeed(self, motor_no, maxVel):
        self.send(SET_MAX_SPEED, motor_no, maxVel)
    
    def setI2cAddress(self, i2cAddress):
        self.send(SET_I2C_ADDR, 0.0, i2cAddress)
    
    def getI2cAddress(self):
        success, i2cAddress, _ = self.recv(GET_I2C_ADDR)
        return success, int(i2cAddress)
    
    def resetAllParams(self):
        success, _, _ = self.recv(RESET)
        return success