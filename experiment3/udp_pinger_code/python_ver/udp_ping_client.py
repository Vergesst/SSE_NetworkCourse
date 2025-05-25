# UDPPingerClient.py
# This client sends 10 pings to a UDP server and measures RTT and packet loss.

import socket
import time

# Server details
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12000
TIMEOUT_SECONDS = 1  # Timeout for receiving a response (1 second)
MAX_PINGS = 10       # Number of pings to send

# Create a UDP socket
# SOCK_DGRAM is for UDP packets
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout for the socket's receive operation
clientSocket.settimeout(TIMEOUT_SECONDS)

# Lists to store RTTs for calculation
rtts = []
packets_sent = 0
packets_received = 0

print("Starting UDP Pinger Client...")

# Loop to send 10 pings
for i in range(1, MAX_PINGS + 1):
    packets_sent += 1
    start_time = time.time()  # Record the time when the ping is sent
    message = f"Ping {i} {start_time}" # Message format: "Ping <seq_num> <timestamp>"

    try:
        # Send the message to the server
        clientSocket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
        print(f"Sent: {message}")

        # Receive the server's response
        # The buffer size is 1024 bytes
        modified_message, server_address = clientSocket.recvfrom(1024)
        end_time = time.time()  # Record the time when the response is received

        rtt = (end_time - start_time) * 1000  # Calculate RTT in milliseconds
        rtts.append(rtt)
        packets_received += 1

        print(f"Received: {modified_message.decode()} from {server_address[0]}:{server_address[1]}. RTT: {rtt:.2f} ms")

    except socket.timeout:
        # Handle timeout if no response is received within the TIMEOUT_SECONDS
        print(f"Ping {i} Request timed out")
    except Exception as e:
        # Handle other potential socket errors
        print(f"Error sending/receiving ping {i}: {e}")

# Close the client socket after all pings are sent
clientSocket.close()

# --- Ping Statistics ---
print("\n--- Ping Statistics ---")
print(f"Packets Sent: {packets_sent}")
print(f"Packets Received: {packets_received}")

# Calculate packet loss percentage
packet_loss = ((packets_sent - packets_received) / packets_sent) * 100 if packets_sent > 0 else 0
print(f"Packet Loss: {packet_loss:.2f}%")

if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = sum(rtts) / len(rtts)
    print(f"Minimum RTT: {min_rtt:.2f} ms")
    print(f"Maximum RTT: {max_rtt:.2f} ms")
    print(f"Average RTT: {avg_rtt:.2f} ms")
else:
    print("No successful pings to calculate RTT statistics.")

