import socket
import os

HOST = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 4096
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"Part B Client 2 listening on {HOST}:{PORT}")
    print("Waiting for selected rows...")

    try:
        packet, server_addr = sock.recvfrom(BUFFER_SIZE)

        if not packet.startswith(b"ROWS|"):
            print("Invalid header.")
            return

        row_count = int(packet[5:].decode("utf-8"))
        data = bytearray()

        while True:
            packet, _ = sock.recvfrom(BUFFER_SIZE)
            if packet == b"EOF":
                break
            data.extend(packet)

        output_path = os.path.join(OUTPUT_DIR, "received_rows.txt")
        with open(output_path, "wb") as f:
            f.write(data)

        print("\nRows received successfully!")
        print(f"Expected rows: {row_count}")
        print(f"Saved at: {output_path}")

    finally:
        sock.close()

if __name__ == "__main__":
    main()
