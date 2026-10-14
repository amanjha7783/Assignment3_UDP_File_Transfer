import socket
import os
import time
import struct

HOST = "0.0.0.0"
PORT = 5000
CLIENT2_IP = "127.0.0.1"
CLIENT2_PORT = 5001
BUFFER_SIZE = 4096
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recvfrom(min(BUFFER_SIZE, size - len(data)))[0]
        data += chunk
    return data

def receive_file(sock):
    packet, client_addr = sock.recvfrom(BUFFER_SIZE)
    if not packet.startswith(b"FILE|"):
        raise ValueError("Expected FILE header from Client 1.")

    filename = packet[5:].decode("utf-8")
    filename = os.path.basename(filename)

    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, "wb") as f:
        while True:
            packet, _ = sock.recvfrom(BUFFER_SIZE)
            if packet == b"EOF":
                break
            f.write(packet)

    return filename, output_path, client_addr

def relay_file(filename, path, client2_addr):
    client2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client2.sendto(b"FILE|" + filename.encode("utf-8"), client2_addr)

    with open(path, "rb") as f:
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            client2.sendto(chunk, client2_addr)

    client2.sendto(b"EOF", client2_addr)
    client2.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"UDP Server listening on {HOST}:{PORT}")
    print("Waiting for Client 1...")

    try:
        while True:
            filename, path, client1_addr = receive_file(sock)

            print(f"\nReceived '{filename}' from Client 1 ({client1_addr[0]}:{client1_addr[1]})")
            print(f"Saved at: {path}")
            print("Holding file for 10 seconds...")
            time.sleep(10)

            print(f"Relaying '{filename}' to Client 2...")
            relay_file(filename, path, (CLIENT2_IP, CLIENT2_PORT))
            print("File sent to Client 2.")
            print("\nWaiting for next file...")
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
