import socket
from logging import log

HOST = "0.0.0.0"
PORT = 1101

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

log(f"Listening in port {PORT} ...")

while True:
  try:
    client_sock, client_address = server.accept()
    log(f"{client_address} Connected!")
    
    while True:
      try:
        data = client_sock.recv(4096)
        
        if not data:
          log(f"[-] Client {client_address} Connection Closed!")
          break
          
        log(f"Message: {data.decode()}")
        log(f"Sender Address: {client_sock.getpeername()}")
        log(f"Is blocking: {client_sock.getblocking()}")

        client_sock.sendall(b"Message recieved successfully!")

      except Exception as e:
        print(f"Communication Error: {e}")  
        break

    client_sock.close()
    log("[-] Socket Recycled. Waiting for brand new connection...")
    
  except KeyboardInterrupt:
    log(f"\n[-] Shutting down the Edge Server Cleanly.")
    break

  except Exception as main_error:
    print(f"\n[-] Critical Problem: {main_error}")
    
  except server.timeout():
    log("Timeout!")


server.close()

