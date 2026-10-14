import socket
import os
import time

HOST = "0.0.0.0"
PORT = 5000
CLIENT2_IP = "127.0.0.1"
CLIENT2_PORT = 5001
BUFFER_SIZE = 4096
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def receive_rows(sock):
    packet, client_addr = sock.recvfrom(BUFFER_SIZE)

    if not packet.startswith(b"ROWS|"):
        raise ValueError("Expected ROWS header.")

    row_count = int(packet[5:].decode("utf-8"))
    data = bytearray()

    while True:
        packet, _ = sock.recvfrom(BUFFER_SIZE)
        if packet == b"EOF":
            break
        data.extend(packet)

    return row_count, bytes(data), client_addr

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"Part B UDP Server listening on {HOST}:{PORT}")

    try:
        while True:
            row_count, data, client_addr = receive_rows(sock)

            server_file = os.path.join(OUTPUT_DIR, "received_rows.txt")
            with open(server_file, "wb") as f:
                f.write(data)

            print(f"\nReceived {row_count} rows from Client 1.")
            print("Holding for 10 seconds...")
            time.sleep(10)

            client2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client2.sendto(b"ROWS|" + str(row_count).encode("utf-8"),
                           (CLIENT2_IP, CLIENT2_PORT))

            for start in range(0, len(data), BUFFER_SIZE):
                client2.sendto(data[start:start + BUFFER_SIZE],
                               (CLIENT2_IP, CLIENT2_PORT))

            client2.sendto(b"EOF", (CLIENT2_IP, CLIENT2_PORT))
            client2.close()

            print("Selected rows sent to Client 2.")

    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
