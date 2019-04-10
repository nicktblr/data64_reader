import mavlink_udp as mav
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

s1 = {}
s2 = {}
s3 = {}
s4 = {}
s5 = {}
s6 = {}
s7 = {}
measureables = [s1, s2, s3, s4, s5, s6, s7]
meas_str = ['S1','S2', 'S3', 'S4', 'S5', 'S6', 'S7']
lat = {}
lng = {}
labels = {}

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

connection = mav.connect()

#data = pd.read_csv('data.csv')

fig = plt.figure()
    

def animate(i):
    plt.clf()

    global partial
    global data

    partial, data = mav.get_line(connection, partial, data)
    
    #print(len(data.index))

    if len(data.index) > 2:

        last = len(data.index) - 1

        stationID = data['StationID'][last]

        lat[stationID] = float(data['Lattitude'][last])
        lng[stationID] = float(data['Longitude'][last])

        j = 0 
        for meas in measureables:
            if data[meas_str[j]][last] is not 'E':
                meas[stationID] = float(data[meas_str[j]][last])
            else: 
                meas[stationID] = float(data[meas_str[j]][last-1])
            j = j + 1 

        lngx = list(lng.values())
        laty = list(lat.values())

        xdiff = np.amax(lngx) - np.amin(lngx)
        ydiff = np.amax(laty) - np.amin(laty)

        j = 1
        for vals in measureables:
            for item in vals.items():
                labels[item[0]] = str(item[0]) + ": " + str(item[1])

            vals_list = list(vals.values())
            labels_list = list(labels.values())

            #print(vals)

            plt.subplot(3,3,j)
            plt.scatter(lngx, laty, c=vals_list, s=100, cmap='viridis')

            plt.xlim(np.amin(lngx) - 0.2*xdiff, np.amax(lngx) + 0.2*xdiff)
            plt.ylim(np.amin(laty) - 0.2*ydiff, np.amax(laty) + 0.2*ydiff)

            plt.xlabel('Longitude')
            plt.ylabel('Latitude')

            plt.yticks([])
            plt.xticks([])

            for label, x, y in zip(labels_list, lngx, laty):
                plt.annotate(
                    label,
                    xy=(x, y), xytext=(-20, 20),
                    textcoords='offset points', ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
            j = j+1

animate = anim.FuncAnimation(fig, animate)
plt.show()
