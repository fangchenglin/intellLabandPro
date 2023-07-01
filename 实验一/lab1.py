import threading
import serial

# 创建串口对象
ser = serial.Serial('COM3', 9600)  # 替换成正确的串口和波特率

# 定义读取数据的线程
def read_thread():
    while True:
        # 从串口读取数据
        data = ser.readline().decode().strip()
        # 处理读取到的数据
        if data == 'YES':
            # 执行相应的操作，例如控制其他设备
            print('检测到障碍物')
        elif data == 'NO':
            # 执行相应的操作，例如控制其他设备1
        
            print('无障碍物')
        else:
            # 处理其他数据
            pass

# 定义写入数据的线程
def write_thread():
    while True:
        # 从用户输入获取数据
        user_input = input('请输入控制指令（0为关灯，1为开灯）：')
        # 写入数据到串口
        ser.write(user_input.encode())

# 创建并启动读取数据的线程
read_t = threading.Thread(target=read_thread)
read_t.daemon = True  # 设置为守护线程，主线程结束时自动退出1
read_t.start()

# 创建并启动写入数据的线程
write_t = threading.Thread(target=write_thread)
write_t.start()

# 等待线程结束（这里使用主线程作为示例）
while True:
    pass
