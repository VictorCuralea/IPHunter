import json
import requests
import ipaddress
import os

def get_aws_ip_ranges():
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    return response.json()

def find_aws_region(ip, aws_ip_ranges):
    ip = ipaddress.ip_address(ip)

    for prefix in aws_ip_ranges["prefixes"]:
        subnet = ipaddress.ip_network(prefix["ip_prefix"])
        if ip in subnet:
            return prefix["region"]

    for prefix in aws_ip_ranges.get("ipv6_prefixes", []):
        subnet = ipaddress.ip_network(prefix["ipv6_prefix"])
        if ip in subnet:
            return prefix["region"]

    return None

def append_ip_to_region_file(ip, region):
    if not os.path.exists("regions"):
        os.makedirs("regions")
        
    file_path = os.path.join("regions", f"{region}.txt")
    with open(file_path, "a") as f:
        f.write(ip + "\n")

def read_ips_from_file(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    ips = read_ips_from_file("ips.txt")
    aws_ip_ranges = get_aws_ip_ranges()

    for ip in ips:
        region = find_aws_region(ip, aws_ip_ranges)
        if region:
            print(f"The IP {ip} belongs to the {region} region.")
            append_ip_to_region_file(ip, region)
        else:
            print(f"The IP {ip} was not found in AWS IP ranges.")
