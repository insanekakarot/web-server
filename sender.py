import socket
import ssl 
from logging import log


HOST = "PUT_YOUR_FUNNEL_ADDRESS"
PORT = 10000

raw_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
raw_client.settimeout(10)

context = ssl.create_default_context()
secure_socket = context.wrap_socket(raw_client, server_hostname=HOST)

log(f"Dialing to the server in {HOST}")
try:
  secure_socket.connect((HOST, PORT))
  log(f"Connected to the {HOST}")

except Exception as e:
  print(e)


while True:
  msg = input(f"Type your message: ")
  secure_socket.sendall(msg.encode())
  response = secure_socket.recv(1024)
  if response:
    log(f"Response From server: {response.decode()}")
