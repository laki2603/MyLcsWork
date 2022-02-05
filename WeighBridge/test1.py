import serial
import serial.tools.list_ports
def decode(x):
    i=0
    # x = '2 02345'
    num = x[2:7]
    dpoint = int(x[0])
    # print(dpoint)
    rnum = str(num[::-1])
    n = len(rnum)
    # print(n)
    res = ''
    while i<n:
        if i == dpoint:
            res+='.'
            res+=rnum[i]
            #continue

        else:
            res+=rnum[i]
        i+=1
    w = res[::-1]
    if w[0]=='0':
        w = w[1::]
    return w




def FindPorts():
    pts = serial.tools.list_ports.comports()
    ports = []

    NumOfPorts = len(pts)
    for p in pts:
        p = str(p)
        p = p.split(" ")
        port = p[0]
        ports.append(port)
        print(port)
    return 0
FindPorts()


ip = serial.Serial(port=pt, baudrate=19200, bytesize=8, parity=serial.PARITY_NONE, stopbits= serial.STOPBITS_ONE)
while True:
    l = str(ip.read(13))

    val = l[2:15]
    # print(val)
    x = val[4:11]
    weight = decode(x)




# ip.close()

