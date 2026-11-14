import socket
from logging import log, current_time_code


HOST = "0.0.0.0"
PORT = 1101

def write_request(message):
  current_time = current_time_code()
  filename = "request_" + str(current_time) + ".txt"
  with open(filename, "w", encoding="utf-8") as file:
    file.write(message)

  return filename
  

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
        file = write_request(data.decode())
        log(f"Request Saved with file named {file}")
        log(f"Sender Address: {client_sock.getpeername()}")
        log(f"Is blocking: {client_sock.getblocking()}")

        # client_sock.sendall(b"Message recieved successfully!")
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nServer: OpenSource Web Server\r\n\r\nHello from Tailscale Edge Server!"
        client_sock.sendall(response.encode())
        log(f"Response Successfully Send to the {client_address}")

        break

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

