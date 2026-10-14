ASSIGNMENT 3 - UDP FILE TRANSFER
=================================

Based on Lecture 13 Assignment 3.

PART A
------
Client 1 sends a file to Client 2 through a UDP server.
The server receives the file, waits 10 seconds, then relays it to Client 2.

Folders:
    Client1/
    Server/
    Client2/

Files:
    Client1/client1.py
    Server/server.py
    Client2/client2.py

Windows setup:
1. Install Python 3.
2. Open THREE PowerShell/Command Prompt windows.
3. Navigate to this Assignment3 folder.

Terminal 1:
    cd Server
    python server.py

Terminal 2:
    cd Client2
    python client2.py

Terminal 3:
    cd Client1
    python client1.py

Put any test file inside Client1, for example:
    hello.txt
    sample.pdf
    image.jpg

Then in Client1 enter:
    hello.txt

The file will be saved in:
    Server/
and then, after 10 seconds:
    Client2/

IMPORTANT:
This lab version is designed for testing all three programs on the same computer.
For three separate VirtualBox machines, replace 127.0.0.1 with the destination VM IP.

PART B
------
A text file contains X rows. Client 1 asks how many rows to send.
Only the selected first N rows are transferred through the server.

Use:
    Client1/partb_client1.py
    Server/partb_server.py
    Client2/partb_client2.py

Example:
    text file has 20 rows
    user enters 5
    only rows 1-5 are sent

Run:
Terminal 1:
    cd Server
    python partb_server.py

Terminal 2:
    cd Client2
    python partb_client2.py

Terminal 3:
    cd Client1
    python partb_client1.py

Then provide the text file name and number of rows.

NOTES
-----
- UDP uses SOCK_DGRAM.
- Files are transferred in binary chunks for Part A.
- Do not use Ctrl+C until you want to stop the server/client.
- Ports used:
      Server: 5000
      Client 2: 5001
- For a different computer/VM, change CLIENT2_IP and SERVER_IP to the
  appropriate VM IP addresses.
