from pymavlink import mavutil

def connect():
    # Start a connection listening to a UDP port
    mav = mavutil.mavlink_connection('udp:127.0.0.1:14550')

    # Wait for the first heartbeat 
    #   This sets the system and component ID of remote system for the link
    mav.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (mav.target_system, mav.target_system))

    return mav


def get_data64(mav):
    # Once connected, use 'mav' to get and send messages
    data64 = mav.recv_match(type='DATA64', blocking=True)
    print(data64.data)

    return data64.data

if __name__ == "__main__":
    connection = connect()
    get_data64(connection)