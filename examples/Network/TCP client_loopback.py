import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
from adafruit_espatcontrol import adafruit_espatcontrol


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False
#LED = board.GP25

RX = board.GP5
TX = board.GP4
resetpin = DigitalInOut(board.GP20)
rtspin = False
uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
#edit host and port to match server
Dest_IP = "10.0.1.74"
Dest_PORT= 5000

print("ESP AT commands")
# For Boards that do not have an rtspin like challenger_rp2040_wifi set rtspin to False.
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
print("Resetting ESP module")
esp.hard_reset()

esp.at_response("at")
counter = 1
print (counter)
print("Checking connection")

while not esp.is_connected:
  try:
    # Some ESP do not return OK on AP Scan.
    # See https://github.com/adafruit/Adafruit_CircuitPython_ESP_ATcontrol/issues/48
    # Comment out the next 3 lines if you get a No OK response to AT+CWLAP
    print("Scanning for AP's")
    for ap in esp.scan_APs():
        print(ap)
    print("Checking connection...")
    # secrets dictionary must contain 'ssid' and 'password' at a minimum
    print("Connecting...")
    esp.connect(secrets)
    print("Connected to AT software version ", esp.version)
    print("IP address ", esp.local_ip)
    
  except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
    print("Failed to get data, retrying\n", e)
    print("Resetting ESP module")
    esp.hard_reset()
    continue


esp.socket_connect("TCP",Dest_IP,Dest_PORT) #connect to a PC - Dest_IP: 10.0.1.75, Dest_PORT:5000
while True:
    data = esp.socket_receive(1)
    if data:
        print(data)
        esp.socket_send(data)

      
