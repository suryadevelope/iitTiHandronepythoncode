from pymavlink import mavutil
import time
import sys
 # Init connection
connection_string = '/dev/ttyACM0'
master = None
while master is None:
    try:
        print("mavlink connecting")
        master = mavutil.mavlink_connection(connection_string)
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("exit")
        sys.exit(0)
    except:
        pass
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_system)) # <<<< I used system and component IDs to seperate messages from the drone and gimbal.
# Get the messages
msg = None
while not msg:
    master.mav.request_data_stream_send(0, 0, mavutil.mavlink.MAV_DATA_STREAM_ALL,10,1)# rate = 10, turn on = 1
    msg = master.recv_match()
    time.sleep(0.01)
print(msg)