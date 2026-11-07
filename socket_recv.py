import socket
import json

JSON_FILE = "users.json"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 9991))

print("Connecting to 9000 port service")

# with open(JSON_FILE, "rb") as file:
#   binary_data = json.load(file)

# print(binary_data)
while True:

  msg = input()
  sock.sendto(msg.encode(), ("0.0.0.0", 9000))

  data, addr = sock.recvfrom(1024)

  print(data.decode())
  print(addr)

