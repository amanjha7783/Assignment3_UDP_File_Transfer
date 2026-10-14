import socket
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 4096
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def send_selected_rows(file_path, number_of_rows):
    if not os.path.isfile(file_path):
        print("File not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if number_of_rows < 1:
        print("Number of rows must be at least 1.")
        return

    if number_of_rows > len(lines):
        print(f"File contains only {len(lines)} rows.")
        return

    selected_text = "".join(lines[:number_of_rows]).encode("utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(b"ROWS|" + str(number_of_rows).encode("utf-8"),
                    (SERVER_IP, SERVER_PORT))

        for start in range(0, len(selected_text), BUFFER_SIZE):
            sock.sendto(selected_text[start:start + BUFFER_SIZE],
                        (SERVER_IP, SERVER_PORT))

        sock.sendto(b"EOF", (SERVER_IP, SERVER_PORT))

        print(f"Sent first {number_of_rows} rows to Server.")
    finally:
        sock.close()

def main():
    print("=== Part B: Client 1 ===")

    filename = input("Enter text file name: ").strip()
    file_path = filename if os.path.isabs(filename) else os.path.join(BASE_DIR, filename)

    try:
        n = int(input("How many rows do you want to send? "))
        send_selected_rows(file_path, n)
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    main()
