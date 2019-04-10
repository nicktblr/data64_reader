from pymavlink import mavutil
import pandas as pd

def connect():
    # Start a connection listening to a UDP port
    mav = mavutil.mavlink_connection('udp:127.0.0.1:14560')

    # Wait for the first heartbeat 
    #   This sets the system and component ID of remote system for the link
    mav.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (mav.target_system, mav.target_system))

    return mav


def get_data64(mav):
    # Once connected, use 'mav' to get and send messages
    data64 = mav.recv_match(type='DATA64', blocking=True)
    ascii64 = ''.join(chr(i) for i in data64.data)
    #print(ascii64)
    #print(data64.data)

    return ascii64

def get_line(connection, partial, arr):
    line = get_data64(connection)
    lines = line.splitlines()
    #print(lines)
    partial = partial + lines[0]
    partial = partial.replace('\x00','')
    data = partial.split(',')
    print(len(data))
    if len(data) < 13 and len(lines) > 1:
        partial = lines[1]
    elif len(lines) > 1:
        arr = arr.append(pd.DataFrame([data],
                             columns=['StationID',
                             'Date',
                             'Time',
                             'S1',
                             'S2',
                             'S3',
                             'S4',
                             'S5',
                             'S6',
                             'S7',
                             'Lattitude',
                             'Longitude',
                             'Battery'
                             ]),
                             ignore_index=True
        )
        partial = lines[1]
    print(arr)
    return partial, arr

if __name__ == "__main__":
    connection = connect()
    #get_data64(connection)
    partial = ''
    data = pd.DataFrame(columns=['StationID',
                             'Date',
                             'Time',
                             'S1',
                             'S2',
                             'S3',
                             'S4',
                             'S5',
                             'S6',
                             'S7',
                             'Lattitude',
                             'Longitude',
                             'Battery'
                             ])
    while True:
        #ascii64 = get_data64(connection)
        partial, data = get_line(connection, partial, data)
