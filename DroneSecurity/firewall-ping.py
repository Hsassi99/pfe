import os
import time
from scapy.all import sniff, IP, ICMP

# Threshold settings
PING_THRESHOLD = 100  # Number of ping requests per second
BLOCK_TIME = 600  # Block duration in seconds

# Dictionary to store IP addresses and their ping request count
ping_count = {}
blocked_ips = {}

def block_ip(ip):
    """Block an IP address using iptables."""
    os.system(f"iptables -A INPUT -s {ip} -j DROP")
    blocked_ips[ip] = time.time()
    print(f"Blocked IP: {ip}")

def unblock_ip(ip):
    """Unblock an IP address using iptables."""
    os.system(f"iptables -D INPUT -s {ip} -j DROP")
    del blocked_ips[ip]
    print(f"Unblocked IP: {ip}")

def monitor_icmp(pkt):
    """Monitor ICMP traffic and block IPs exceeding the threshold."""
    if pkt.haslayer(ICMP):
        ip_src = pkt[IP].src
        current_time = time.time()
        
        # Initialize or update ping count
        if ip_src in ping_count:
            ping_count[ip_src] += 1
        else:
            ping_count[ip_src] = 1

        # Check if the IP exceeds the threshold
        if ping_count[ip_src] > PING_THRESHOLD:
            if ip_src not in blocked_ips:
                block_ip(ip_src)

def main():
    print("Starting ICMP monitor...")
    sniff(filter="icmp", prn=monitor_icmp, store=0)

    # Continuously check to unblock IPs after the block duration
    while True:
        current_time = time.time()
        for ip in list(blocked_ips.keys()):
            if current_time - blocked_ips[ip] > BLOCK_TIME:
                unblock_ip(ip)
        time.sleep(1)

if __name__ == "__main__":
    main()
