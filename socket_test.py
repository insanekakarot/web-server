import socket


socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("0.0.0.0", 9000))


while True:
  data, addr = socket.recvfrom(1024)

  print(data.decode())
  print(f"New address added: {addr}")

  
  msg = input()
  socket.sendto(msg.encode(), (addr[0], addr[1]))

