import socket
import os

HOST = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 4096
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def receive_file():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"=== Client 2: UDP File Receiver ===")
    print(f"Listening on {HOST}:{PORT}")
    print("Waiting for Server...")

    try:
        packet, server_addr = sock.recvfrom(BUFFER_SIZE)

        if not packet.startswith(b"FILE|"):
            print("Invalid file header received.")
            return

        filename = os.path.basename(packet[5:].decode("utf-8"))
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(output_path, "wb") as f:
            total = 0

            while True:
                packet, _ = sock.recvfrom(BUFFER_SIZE)

                if packet == b"EOF":
                    break

                f.write(packet)
                total += len(packet)

        print(f"\nFile received successfully!")
        print(f"File: {filename}")
        print(f"Saved at: {output_path}")
        print(f"Total bytes received: {total}")

    finally:
        sock.close()

if __name__ == "__main__":
    receive_file()
