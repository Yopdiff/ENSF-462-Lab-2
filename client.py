from socket import *
import time
import numpy as np

UDP_IP = "127.0.0.1"
UDP_PORT = 12000
times = []
success = 0
fail = 0
#message = Ping sequence_number time
#sequence num starts from 1 and ends at 10.
#time = when packet is sent to the server
socket = socket(AF_INET, SOCK_DGRAM)
socket.settimeout(1)
for sequence_number in range(1, 11):
    start = time.time()
    socket.sendto((f'Ping {sequence_number} {time.time()}').encode(), (UDP_IP, UDP_PORT))
    try:
        response, address = socket.recvfrom(1024)
        time_taken = time.time() - start
        times.append(time_taken)
        print(f'Sequence Number: {sequence_number}')
        print(f'Response: {response.decode()}')
        print(f'Round-Trip Time: {time_taken}')
    except timeout:
        print(f'Sequence Number: {sequence_number}')
        print("\033[91mRequest time out\033[0m")
        fail += 1
loss_rate = ((fail / 10) * 100) 
print(f'Minimum RTT: {np.min(times)}')
print(f'Maximum RTT: {np.max(times)}')
print(f'Average RTT: {np.mean(times)}')
print(f'Packet loss rate: {loss_rate}%')
socket.close()