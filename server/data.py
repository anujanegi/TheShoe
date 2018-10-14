import smbus #import SMBus module of I2C from time import sleep #import

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 
Device_Address = 0x68   # MPU6050 device address

MPU_Init()
print (" Reading Data of Gyroscope and Accelerometer")
flag = 0
def getData():	
	global flag, Adx, Ady, Adz
	Adx, Ady, Adz = 0, 0, 0
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x*9.8/16384.0
	Ay = acc_y*9.8/16384.0
	Az = acc_z*9.8/16384.0
		
	if(flag == 0):
		Adx = Ax
		Ady = Ay
		Adz = Az	
		flag = 1

	else:
		Adx = (Ax + 15*Adx)/16
		Ady = (Ay + 15*Ady)/16
		Adz = (Az + 15*Adz)/16
	#print("Adx = ", Adx, " Ady = ", Ady, " Adz = ",Adz)
	Aax = Ax - Adx
	Aay = Ay - Ady
	Aaz = Az - Adz	
	#print ( "Ax=%.2f" %Aax, "\tAy=%.2f" %Aay, "\tAz=%.2f" %Aaz)
	s = str(Ax) + "," + str(Ay) + "," + str(Az) + ","+ str(Adx) + "," + str(Ady) + "," + str(Adz)
	return s 	

