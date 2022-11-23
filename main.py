import matplotlib.pyplot as plt
import socket
import numpy as np
from skimage.measure import label, regionprops

host = "84.237.21.36"
port = 5152
packet_size = 80004//2

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data

plt.ion()
plt.figure()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, packet_size)
        rows, cols = bts[:2]
        im1 = np.frombuffer(bts[2:rows*cols+2], dtype="uint8").reshape(rows, cols)

        im1[im1 > 0] = 1
        labeled = label(im1)
        regions = regionprops(labeled)
        pos = []
        for region in regions:
            cy, cx = region.centroid
            pos.append((round, cy))

        print(pos)

        distance = ((pos[0][0] - pos[1][0])**2 + (pos[0][1]-pos[1][1])**2)**0.5
        distance = round(distance, 1)

        
        plt.clf()
        plt.imshow(im1)
        plt.pause(2)

        print(distance, pos)

        sock.send(f"{distance}".encode())
        print(sock.recv(20))

        sock.send(b"beat")
        beat = sock.recv(20)

print("Done")
