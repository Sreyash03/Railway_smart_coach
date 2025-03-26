import socket

def udp_server(host, port):
  

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_socket.bind((host, port))
  print(f"UDP server started on {host}:{port}")

  while True:
    data, address = server_socket.recvfrom(1024)
    data = data.decode('utf-8')  
    if data=='terminate':
      break
    print(f"Received message from {address}: {data}")
    response = data.upper()
    server_socket.sendto(response.encode('utf-8'), address)

if __name__ == "__main__":
  host = '127.0.0.1'  
  port = 9999
  udp_server(host, port)



