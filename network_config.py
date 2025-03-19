import sys
import json
import re
import random
from ipaddress import IPv4Network, IPv6Network

# Predefined IP ranges
IPv4_SUBNET = "192.168.1.0/24"
IPv6_SUBNET = "2001:db8::/64"

# Lease database (simulated)
lease_db = {}

# Function to validate MAC address
def validate_mac(mac):
    pattern = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
    return bool(pattern.match(mac))

# Function to generate an IPv4 address dynamically
def generate_ipv4():
    network = list(IPv4Network(IPv4_SUBNET).hosts())
    available_ips = [str(ip) for ip in network if str(ip) not in lease_db.values()]
    return random.choice(available_ips) if available_ips else None

# Function to generate an IPv6 address using EUI-64 format
def generate_ipv6(mac):
    mac_clean = mac.replace(":", "").replace("-", "").lower()
    mac_split = mac_clean[:6] + "fffe" + mac_clean[6:]
    mac_split = list(mac_split)
    mac_split[1] = hex(int(mac_split[1], 16) ^ 2)[-1]  # Flip the 7th bit
    eui64 = ":".join(["".join(mac_split[i:i+4]) for i in range(0, len(mac_split), 4)])
    return f"{IPv6_SUBNET.rstrip('::')}{eui64}"

# Function to assign an IP based on user request
def assign_ip(mac, dhcp_version):
    if not validate_mac(mac):
        return json.dumps({"error": "Invalid MAC address format"})

    if mac in lease_db:
        assigned_ip = lease_db[mac]
    else:
        if dhcp_version == "DHCPv4":
            assigned_ip = generate_ipv4()
        elif dhcp_version == "DHCPv6":
            assigned_ip = generate_ipv6(mac)
        else:
            return json.dumps({"error": "Invalid DHCP version"})
        
        if assigned_ip is None:
            return json.dumps({"error": "No available IPs in subnet"})

        lease_db[mac] = assigned_ip

    response = {
        "mac_address": mac,
        "assigned_ip": assigned_ip,
        "lease_time": "3600 seconds",
        "subnet": IPv4_SUBNET if dhcp_version == "DHCPv4" else IPv6_SUBNET
    }
    return json.dumps(response)

# Main execution (for command-line call from PHP)
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    mac_address = sys.argv[1]
    dhcp_version = sys.argv[2]
    
    print(assign_ip(mac_address, dhcp_version))
