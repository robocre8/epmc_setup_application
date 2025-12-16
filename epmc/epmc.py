import serial
import struct

# class EPMCSerialError(Exception):
#     """Custom exception for for EPMC Comm failure"""
#     pass


# Serial Protocol Command IDs -------------
START_BYTE = 0xAA
WRITE_VEL = 0x01
WRITE_PWM = 0x02
READ_POS = 0x03
READ_VEL = 0x04
READ_UVEL = 0x05
READ_TVEL = 0x06
SET_PPR = 0x07
GET_PPR = 0x08
SET_KP = 0x09
GET_KP = 0x0A
SET_KI = 0x0B
GET_KI = 0x0C
SET_KD = 0x0D
GET_KD = 0x0E
SET_RDIR = 0x0F
GET_RDIR = 0x10
SET_CUT_FREQ = 0x11
GET_CUT_FREQ = 0x12
SET_MAX_VEL = 0x13
GET_MAX_VEL = 0x14
SET_PID_MODE = 0x15
GET_PID_MODE = 0x16
SET_CMD_TIMEOUT = 0x17
GET_CMD_TIMEOUT = 0x18
SET_I2C_ADDR = 0x19
GET_I2C_ADDR = 0x1A
RESET_PARAMS = 0x1B
READ_MOTOR_DATA = 0x2A
CLEAR_DATA_BUFFER = 0x2C
#---------------------------------------------



class EPMC:
    def __init__(self):
        pass

    def connect(self, port, baud=56700, timeOut=0.1):
        self.ser = serial.Serial(port, baud, timeout=timeOut)

    def disconnect(self):
        if self.ser.is_open:
            self.ser.close()
    
    #------------------------------------------------------------------------
    def send_packet_without_payload(self, cmd, length=0):
        length = 0
        packet = bytearray([START_BYTE, cmd, length])
        checksum = sum(packet) & 0xFF
        packet.append(checksum)
        self.ser.write(packet)
        self.ser.flush()

    def send_packet_with_payload(self, cmd, payload_bytes):
        length = len(payload_bytes)
        packet = bytearray([START_BYTE, cmd, length]) + payload_bytes
        checksum = sum(packet) & 0xFF
        packet.append(checksum)
        self.ser.write(packet)
        self.ser.flush()

    def read_packet1(self):
        """
        Reads 4 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(4)
            if len(payload) != 4:
                # print("[EPMC SERIAL ERROR]: Timeout while reading 1 values")
                return False, 0.0

            # Unpack 4 bytes as little-endian float
            (val,) = struct.unpack('<f', payload)
            return True, val
        except:
            # print("[PYSERIAL ERROR]: Read Timeout")
            return False, 0.0
    
    def read_packet2(self):
        """
        Reads 8 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(8)
            if len(payload) != 8:
                # print("[EPMC SERIAL ERROR]: Timeout while reading 2 values")
                return False, 0.0, 0.0

            # Unpack 4 bytes as little-endian float
            a, b = struct.unpack('<ff', payload)
            return True, a, b
        except:
            # print("[PYSERIAL ERROR]: Read Timeout")
            return False, 0.0, 0.0
    
    def read_packet4(self):
        """
        Reads 16 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        try:
            payload = self.ser.read(16)
            if len(payload) != 16:
                # print("[EPMC SERIAL ERROR]: Timeout while reading 4 values")
                return False, 0.0, 0.0, 0.0, 0.0

            # Unpack 4 bytes as little-endian float
            a, b, c, d = struct.unpack('<ffff', payload)
            return True, a, b, c, d
        except:
            # print("[PYSERIAL ERROR]: Read Timeout")
            return False, 0.0, 0.0, 0.0, 0.0
    
    #---------------------------------------------------------------------

    def write_data1(self, cmd, val, pos=100):
        payload = struct.pack('<Bf', pos, val)
        self.send_packet_with_payload(cmd, payload)

    def read_data1(self, cmd, pos=100):
        payload = struct.pack('<Bf', pos, 0.0)  # big-endian
        self.send_packet_with_payload(cmd, payload)
        success, val = self.read_packet1()
        return success, val
    
    def write_data2(self, cmd, a, b):
        payload = struct.pack('<ff', a, b) 
        self.send_packet_with_payload(cmd, payload)

    def read_data2(self, cmd):
        self.send_packet_without_payload(cmd, length=8)
        success, a, b = self.read_packet2()
        return success, a, b

    def read_data4(self, cmd):
        self.send_packet_without_payload(cmd, length=16)
        suceess, a, b, c, d = self.read_packet4()
        return suceess, a, b, c, d
    
    #---------------------------------------------------------------------
    def writeSpeed(self, v0, v1):
        self.write_data2(WRITE_VEL, v0, v1)
    
    def writePWM(self, pwm0, pwm1):
        self.write_data2(WRITE_PWM, pwm0, pwm1)
    
    def readPos(self):
        success, pos0, pos1 = self.read_data2(READ_POS)
        return success, round(pos0, 4), round(pos1, 4)
    
    def readVel(self):
        success, vel0, vel1 = self.read_data2(READ_VEL)
        return success, round(vel0, 4), round(vel1, 4)
    
    def readUVel(self):
        success, vel0, vel1 = self.read_data2(READ_UVEL)
        return success, round(vel0, 4), round(vel1, 4)
    
    def readTVel(self):
        success, vel0, vel1 = self.read_data2(READ_TVEL)
        return success, round(vel0, 4), round(vel1, 4)
    
    def setCmdTimeout(self, timeout):
        self.write_data1(SET_CMD_TIMEOUT, timeout)
        
    def getCmdTimeout(self):
        success, timeout = self.read_data1(GET_CMD_TIMEOUT)
        return success, int(timeout)
    
    def setPidMode(self, mode):
        self.write_data1(SET_PID_MODE, mode)
    
    def getPidMode(self):
        success, mode = self.read_data1(GET_CMD_TIMEOUT)
        return success, int(mode)
    
    def clearDataBuffer(self):
        success, res = self.read_data1(CLEAR_DATA_BUFFER)
        return success
    
    #---------------------------------------------------------------------

    def readMotorData(self):
        success, pos0, pos1, vel0, vel1 = self.read_data4(READ_MOTOR_DATA)
        return success, round(pos0, 4), round(pos1, 4), round(vel0, 4), round(vel1, 4)
    
    #---------------------------------------------------------------------

    def getMaxVel(self, motor_no):
        success, maxVel = self.read_data1(GET_MAX_VEL, motor_no)
        return success, round(maxVel, 3)

    def setPPR(self, motor_no, ppr):
        self.write_data1(SET_PPR, ppr, motor_no)
    
    def getPPR(self, motor_no):
        success, ppr = self.read_data1(GET_PPR, motor_no)
        return success, round(ppr, 3)
    
    def setKp(self, motor_no, kp):
        self.write_data1(SET_KP, kp, motor_no)
    
    def getKp(self, motor_no):
        success, kp = self.read_data1(GET_KP, motor_no)
        return success, round(kp, 3)
    
    def setKi(self, motor_no, ki):
        self.write_data1(SET_KI, ki, motor_no)
    
    def getKi(self, motor_no):
        success, ki = self.read_data1(GET_KI, motor_no)
        return success, round(ki, 3)
    
    def setKd(self, motor_no, kd):
        self.write_data1(SET_KD, kd, motor_no)
    
    def getKd(self, motor_no):
        success, kd = self.read_data1(GET_KD, motor_no)
        return success, round(kd, 3)
    
    def setRdir(self, motor_no, rdir):
        self.write_data1(SET_RDIR, rdir, motor_no)
    
    def getRdir(self, motor_no):
        success, rdir = self.read_data1(GET_RDIR, motor_no)
        return success, int(rdir)
    
    def setCutOffFreq(self, motor_no, cutOffFreq):
        self.write_data1(SET_CUT_FREQ, cutOffFreq, motor_no)
    
    def getCutOffFreq(self, motor_no):
        success, cutOffFreq = self.read_data1(GET_CUT_FREQ, motor_no)
        return success, round(cutOffFreq, 3)
    
    def setMaxVel(self, motor_no, maxVel):
        self.write_data1(SET_MAX_VEL, maxVel, motor_no)
    
    def getMaxVel(self, motor_no):
        success, maxVel = self.read_data1(GET_MAX_VEL, motor_no)
        return success, round(maxVel, 3)
    
    def setI2cAddress(self, i2cAddress):
        self.write_data1(SET_I2C_ADDR, i2cAddress)
    
    def getI2cAddress(self):
        success, i2cAddress = self.read_data1(GET_I2C_ADDR)
        return success, int(i2cAddress)
    
    def resetAllParams(self):
        success, res = self.read_data1(RESET_PARAMS)
        return success