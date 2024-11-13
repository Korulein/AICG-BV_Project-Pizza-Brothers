import serial
from time import sleep
import requests
# Note: replace "COM1" with the COM port of your Arduino

ser = serial.Serial("COM3", baudrate=9600, timeout=1)
pizzasquantity=[]
batches=[]
#keeping track of how many pizzas are able to go in oven
maxpizza=4
cmd=""

# Define where it goes in app.py
UPDATE_STATUS_URL = 'http://127.0.0.1:5000/update_pizza_quantity'

def luigi_input():
 global maxpizza, batches,cmd
 bytes_serial = ser.inWaiting() 
 
 if bytes_serial > 0:
  cmd=ser.readline().decode('utf-8')#read data from arduino
  print(cmd)
  if cmd.isdigit():
    data = int(cmd) 
    if data <= maxpizza:
     maxpizza-=data   
     print("maxpizza",maxpizza)
     batches.append(data)
    #adds how many Seconds to timer of current batch
     ser.write(str(10).encode())
     return None
    else: 
       ser.write("ERROR".encode())
       print("ERROR")
  elif cmd == "DONE":
            # Handle "DONE" command by popping completed batch
                maxpizza += batches[0]
                pizzas_done=batches[0]
                print("batches",batches)
                batches.pop(0)
                return pizzas_done

   
  
  
  


        


        
while True:                  
 pizzas_done=luigi_input()
 if pizzas_done!=None:
  response = requests.post(UPDATE_STATUS_URL, json=pizzas_done)
  pizzas_done=None

