import socket

def udp_client(host, port, message):
  

   client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   client_socket.sendto(message.encode('utf-8'), (host, port))
   data, address = client_socket.recvfrom(1024)
   print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
  host = '127.0.0.1'  
  port = 9999
  message = input("Hello from client: ")
  udp_client(host, port, message)