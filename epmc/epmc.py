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
    def __init__(self, port, baud=115200, timeOut=0.1):
        self.ser = serial.Serial(port, baud, timeout=timeOut)
    
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
        payload = self.ser.read(4)
        if len(payload) != 4:
            return 0.0
            # print("[EPMC SERIAL ERROR]: Timeout while reading 1 values")
            # raise EPMCSerialError("[EPMC SERIAL ERROR]: Timeout while reading 1 value")

        # Unpack 4 bytes as little-endian float
        (val,) = struct.unpack('<f', payload)
        return val
    
    def read_packet2(self):
        """
        Reads 8 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        payload = self.ser.read(8)
        if len(payload) != 8:
            return 0.0, 0.0
            # print("[EPMC SERIAL ERROR]: Timeout while reading 2 values")
            # raise EPMCSerialError("[EPMC SERIAL ERROR]: Timeout while reading 2 values")

        # Unpack 4 bytes as little-endian float
        a, b = struct.unpack('<ff', payload)
        return a, b
    
    def read_packet4(self):
        """
        Reads 16 bytes from the serial port and converts to a float (little-endian).
        Returns (success, value-array)
        """
        payload = self.ser.read(16)
        if len(payload) != 16:
            return 0.0, 0.0, 0.0, 0.0
            # print("[EPMC SERIAL ERROR]: Timeout while reading 4 values")
            # raise EPMCSerialError("[EPMC SERIAL ERROR]: Timeout while reading 4 values")

        # Unpack 4 bytes as little-endian float
        a, b, c, d = struct.unpack('<ffff', payload)
        return a, b, c, d
    
    #---------------------------------------------------------------------

    def write_data1(self, cmd, val, pos=100):
        payload = struct.pack('<Bf', pos, val)
        self.send_packet_with_payload(cmd, payload)
        val = self.read_packet1()
        return val

    def read_data1(self, cmd, pos=100):
        payload = struct.pack('<Bf', pos, 0.0)  # big-endian
        self.send_packet_with_payload(cmd, payload)
        val = self.read_packet1()
        return val
    
    def write_data2(self, cmd, a, b):
        payload = struct.pack('<ff', a, b) 
        self.send_packet_with_payload(cmd, payload)

    def read_data2(self, cmd):
        self.send_packet_without_payload(cmd, length=8)
        a, b = self.read_packet2()
        return a, b

    def read_data4(self, cmd):
        self.send_packet_without_payload(cmd, length=16)
        a, b, c, d = self.read_packet4()
        return a, b, c, d
    
    #---------------------------------------------------------------------
    def writeSpeed(self, v0, v1):
        self.write_data2(WRITE_VEL, v0, v1)
    
    def writePWM(self, pwm0, pwm1):
        self.write_data2(WRITE_PWM, pwm0, pwm1)
    
    def readPos(self):
        pos0, pos1 = self.read_data2(READ_POS)
        return round(pos0, 4), round(pos1, 4)
    
    def readVel(self):
        vel0, vel1 = self.read_data2(READ_VEL)
        return round(vel0, 4), round(vel1, 4)
    
    def readUVel(self):
        vel0, vel1 = self.read_data2(READ_UVEL)
        return round(vel0, 4), round(vel1, 4)
    
    def readTVel(self):
        vel0, vel1 = self.read_data2(READ_TVEL)
        return round(vel0, 4), round(vel1, 4)
    
    def setCmdTimeout(self, timeout):
        res = self.write_data1(SET_CMD_TIMEOUT, timeout)
        return int(res)
        
    def getCmdTimeout(self):
        timeout = self.read_data1(GET_CMD_TIMEOUT)
        return int(timeout)
    
    def setPidMode(self, mode):
        res = self.write_data1(SET_PID_MODE, mode)
        res = True if int(res) == 1 else False
        return res
    
    def getPidMode(self):
        mode = self.read_data1(GET_CMD_TIMEOUT)
        return int(mode)
    
    def clearDataBuffer(self):
        res = self.write_data1(CLEAR_DATA_BUFFER, 0.0)
        res = True if int(res) == 1 else False
        return res
    
    #---------------------------------------------------------------------

    def readMotorData(self):
        pos0, pos1, vel0, vel1 = self.read_data4(READ_MOTOR_DATA)
        return round(pos0, 4), round(pos1, 4), round(vel0, 4), round(vel1, 4)
    
    #---------------------------------------------------------------------

    def setPPR(self, motor_no, ppr):
        res = self.write_data1(SET_PPR, ppr, motor_no)
        res = True if int(res) == 1 else False
        return res
    
    def getPPR(self, motor_no):
        ppr = self.read_data1(GET_PPR, motor_no)
        return round(ppr, 3)
    
    def setKp(self, motor_no, kp):
        res = self.write_data1(SET_KP, kp, motor_no)
        res = True if int(res) == 1 else False
        return res
    
    def getKp(self, motor_no):
        kp = self.read_data1(GET_KP, motor_no)
        return round(kp, 3)
    
    def setKi(self, motor_no, ki):
        res = self.write_data1(SET_KI, ki, motor_no)
        res = True if int(res) == 1 else False
        return res
    
    def getKi(self, motor_no):
        ki = self.read_data1(GET_KI, motor_no)
        return round(ki, 3)
    
    def setKd(self, motor_no, kd):
        res = self.write_data1(SET_KD, kd, motor_no)
        res = True if int(res) == 1 else False
        return res
    
    def getKd(self, motor_no):
        kd = self.read_data1(GET_KD, motor_no)
        return round(kd, 3)
    
    def setRdir(self, motor_no, rdir):
        res = self.write_data1(SET_RDIR, rdir, motor_no)
        res = True if int(res) == 1 else False
        return res
    
    def getRdir(self, motor_no):
        rdir = self.read_data1(GET_RDIR, motor_no)
        return int(rdir)
    
    def setCutOffFreq(self, motor_no, cutOffFreq):
        res = self.write_data1(SET_CUT_FREQ, cutOffFreq, motor_no)
        res = True if int(res) == 1 else False
        return res
    
    def getCutOffFreq(self, motor_no):
        cutOffFreq = self.read_data1(GET_CUT_FREQ, motor_no)
        return round(cutOffFreq, 3)
    
    def setMaxVel(self, motor_no, maxVel):
        res = self.write_data1(SET_MAX_VEL, maxVel, motor_no)
        res = True if int(res) == 1 else False
        return res
    
    def getMaxVel(self, motor_no):
        maxVel = self.read_data1(GET_MAX_VEL, motor_no)
        return round(maxVel, 3)
    
    def setI2cAddress(self, i2cAddress):
        res = self.write_data1(SET_I2C_ADDR, i2cAddress)
        res = True if int(res) == 1 else False
        return res
    
    def getI2cAddress(self):
        i2cAddress = self.read_data1(GET_I2C_ADDR)
        return int(i2cAddress)
    
    def resetAllParams(self):
        res = self.write_data1(RESET_PARAMS, 0.0)
        res = True if int(res) == 1 else False
        return res