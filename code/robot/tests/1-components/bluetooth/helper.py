"""
    Description.
"""


import serial
import time
import threading 
import numpy as np

serial_port = '/dev/cu.HC-05-DevB';
baud_rate = 9600; 
ser = serial.Serial(serial_port, baud_rate, timeout=1)
start_t = time.time()

# ------------
def simple_sending():
    delay = 0.5 
    T = 20
    t = 0
    id_master = 0
    seq_number = 0
    instruction = 2
    while t < T:
        msg = "<" + str(id_master) + "/" + str(seq_number) + \
            "/" + str(instruction) + ">"
        seq_number += 1
        ser.write(msg.encode())
        time.sleep(delay)
        t += delay


# ------------
def simple_reception():
    while True:
        raw_msg = ser.readline().decode("utf-8");
        print("Raw msg:" + str(raw_msg))
        
        raw_msg = raw_msg.rstrip()  # remove end of line characters
        if (len(raw_msg) < 1 or raw_msg[0] != '<' or raw_msg[-1] != '>' ):
            print("Non-valid message")
            continue

        parsed_msg = raw_msg[1:-1]  # remove <> symbols
        parsed_msg = parsed_msg.split('/')
        print("Parsed msg:" + str(parsed_msg))


# ------------
def sinus_test():
    t2=threading.Thread(target=sinus_sending).start()
    t1=threading.Thread(target=sinus_receiving).start()


# ------------
def sinus_sending():
    write_to_file_path = "data/sending.csv";
    output_file = open(write_to_file_path, "w+");
    output_file.write("t;f\n")
    delay = 0.04
    T = 4.
    id_master = 0
    seq_number = 0
    start_t = time.time()
    t = 0
    while t <= 2*T:
        t = time.time() - start_t
        f = 10 * np.sin(2.*3.1415/T*t)
        output_file.write(str(t)+";"+str(f)+"\n")
        msg = "<" + str(id_master) + "/" + str(seq_number) + \
            "/" + str(f) + ">"
        seq_number += 1
        ser.write(msg.encode())
        time.sleep(delay)


# ------------
def sinus_receiving():
    write_to_file_path = "data/reception.csv";
    reception_file = open(write_to_file_path, "w+");
    reception_file.write("t;f\n")
    delay = 0.04
    T = 4
    while (time.time() - start_t) < 2*T + 20:
        raw_msg = ser.readline().decode("utf-8");   
        raw_msg = raw_msg.rstrip() 
        if (len(raw_msg) < 1 or raw_msg[0] != '<' or raw_msg[-1] != '>' ): continue
        t = time.time() - start_t
        parsed_msg = raw_msg[1:-1]  
        parsed_msg = parsed_msg.split('/')
        if len(parsed_msg) != 3: continue
        f = parsed_msg[-1]
        reception_file.write(str(t)+";"+str(f)+"\n")
        time.sleep(delay)


# ------------
if __name__ == "__main__":
    # simple_sending()
    simple_reception()
    # sinus_test()


























    