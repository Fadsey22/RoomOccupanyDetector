import serial
import tago
import time
from knn2 import gabe
import statistics
def untilcom(st,dict):
    val = ""
    counter = 1
    for i in range(0,len(st)):
        if counter > 3:
            break
        if st[i] != ',' and st[i] != '\n' and st[i] != '\r':
            val += st[i]
        else:
            dict[counter].append((val))
            val = ""
            counter += 1
    return dict

my_device = tago.Device('579793cc-a0b0-4d9f-9a4f-4b02097a0612')
dash_vals = []
data1 = {
'variable': 'co21',
'unit' : 'ppm',
'value' : 0,
}
data2 = {
'variable': 'voc1',
'unit' : 'ug/m^3',
'value' : 0,
}
data3 = {
'variable': 'temp1',
'unit' : 'degrees',
'value' : 0,
}
data4 = {
'variable': 'co22',
'unit' : 'ppm',
'value' : 0,
}
data5 = {
'variable': 'voc2',
'unit' : 'ug/m^3',
'value' : 0,
}
data6 = {
'variable': 'temp2',
'unit' : 'degrees',
'value' : 0,
}
data7 = {
'variable': 'co23',
'unit' : 'ppm',
'value' : 0,
}
data8 = {
'variable': 'voc3',
'unit' : 'ug/m^3',
'value' : 0,
}
data9 = {
'variable': 'temp3',
'unit' : 'degrees',
'value' : 0,
}
data10 = {
'variable': 'co24',
'unit' : 'ppm',
'value' : 0,
}
data11 = {
'variable': 'voc4',
'unit' : 'ug/m^3',
'value' : 0,
}
data12 = {
'variable': 'temp4',
'unit' : 'degrees',
'value' : 0,
}

data13 = {
'variable': 'occupancy',
'unit' : 'people',
'value' : 0,
}
dash_vals.append(data1)
dash_vals.append(data2)
dash_vals.append(data3)
dash_vals.append(data4)
dash_vals.append(data5)
dash_vals.append(data6)
dash_vals.append(data7)
dash_vals.append(data8)
dash_vals.append(data9)
dash_vals.append(data10)
dash_vals.append(data11)
dash_vals.append(data12)
dash_vals.append(data13)
#dash_vals.append(data10)
d = [{1:[],2:[],3:[]},{1:[],2:[],3:[]},{1:[],2:[],3:[]},{1:[],2:[],3:[]}]
ser = serial.Serial("COM4", baudrate=115200, timeout=3.0)
readser = serial.Serial("COM9", baudrate=115200, timeout=3.0)
sample = int(input("enter the dashboard sample rate"))
max = int(input("enter max occupancy"))
print(sample,max)
c = 0
tf = 0
sensorC = 0
g = 0
st = time.time()
co2Vals1 = []
co2Vals2 = []
co2Vals3 = []
co2Vals4 = []

knnVals = [1,2,3,4]
people = 0
while 1:
    print("running")
    end = time.time()





    g += 1
    serialString = ser.readline()
    # Print the contents of the serial data
    sw = serialString.decode('Ascii')


    d[sensorC] = untilcom(sw,d[sensorC])
    print("diff",end - st)
    if sensorC == 3 and end - st > sample:
        print("in the time boy")
        st = time.time()
        for j in range(0,4):
            for i in range(1,4):
                print(tf,i,j)
                dash_vals[tf]['value'] = d[j].get(i)[len(d[j].get(i)) - 1]
                my_device.insert(dash_vals[tf])
                tf += 1
        knnVals[0] = statistics.mean(co2Vals1[len(co2Vals1) - 10:len(co2Vals1) - 1])
        knnVals[1] = statistics.mean(co2Vals2[len(co2Vals2) - 10:len(co2Vals2) - 1])
        knnVals[2] = statistics.mean(co2Vals3[len(co2Vals3) - 10:len(co2Vals3) - 1])
        knnVals[3] = statistics.mean(co2Vals4[len(co2Vals4) - 10:len(co2Vals4) - 1])

        # knnVals[0] = max(co2Vals1[len(co2Vals1) - 10:len(co2Vals1) - 1])
        # knnVals[1] = max(co2Vals2[len(co2Vals2) - 10:len(co2Vals2) - 1])
        # knnVals[2] = max(co2Vals3[len(co2Vals3) - 10:len(co2Vals3) - 1])
        # knnVals[3] = max(co2Vals4[len(co2Vals4) - 10:len(co2Vals4) - 1])

        print("SSS",knnVals)
        people = gabe(knnVals)
        print("people",people[0])
        if int(people[0]) > max:
            readser.write(b"pb r\n")
        else:
            readser.write(b"lis2dh r\n")
        dash_vals[12]['value'] = '6'
        my_device.insert(dash_vals[12])
    tf = 0
    if sensorC == 3:
        for j in range(0, 4):
            for i in range(1, 4):
                if j == 0 and i == 1:
                    co2Vals1.append(int(d[j].get(i)[len(d[j].get(i)) - 1]))
                if j == 1 and i == 1:
                    co2Vals2.append(int(d[j].get(i)[len(d[j].get(i)) - 1]))
                if j == 2 and i == 1:
                    co2Vals3.append(int(d[j].get(i)[len(d[j].get(i)) - 1]))
                if j == 3 and i == 1:
                    co2Vals4.append(int(d[j].get(i)[len(d[j].get(i)) - 1]))
    c += 1
    if sensorC == 0:
        f = open("s1.txt", "a")
        f.write(sw)
        f.close()
    elif sensorC == 1:
        f1 = open("s2.txt", "a")
        f1.write(sw)
        f1.close()
    elif sensorC == 2:
        f2 = open("s3.txt", "a")
        f2.write(sw)
        f2.close()
    else:
        f3 = open("s4.txt", "a")
        f3.write(sw)
        f3.close()

    sensorC += 1
    if sensorC > 3:
        sensorC = 0
