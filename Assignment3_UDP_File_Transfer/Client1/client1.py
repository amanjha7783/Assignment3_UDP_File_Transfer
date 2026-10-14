import socket
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 4096
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def send_file(file_path):
    if not os.path.isfile(file_path):
        print("File not found.")
        return

    filename = os.path.basename(file_path)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send file name/header
        sock.sendto(b"FILE|" + filename.encode("utf-8"),
                    (SERVER_IP, SERVER_PORT))

        # Send file as binary chunks
        with open(file_path, "rb") as f:
            total = 0
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break
                sock.sendto(chunk, (SERVER_IP, SERVER_PORT))
                total += len(chunk)

        # End-of-file marker
        sock.sendto(b"EOF", (SERVER_IP, SERVER_PORT))

        print(f"Sent: {filename}")
        print(f"Total bytes sent: {total}")
    finally:
        sock.close()

def main():
    print("=== Client 1: UDP File Sender ===")
    print(f"Client1 directory: {BASE_DIR}")

    while True:
        filename = input("\nEnter file name/path to send (or 'exit'): ").strip()

        if filename.lower() == "exit":
            break

        if not os.path.isabs(filename):
            filename = os.path.join(BASE_DIR, filename)

        send_file(filename)

if __name__ == "__main__":
    main()
