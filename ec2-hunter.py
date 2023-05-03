import time
import boto3
import argparse
import sys

def read_ips_from_file(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acquire specific Elastic IP addresses in AWS")
    parser.add_argument("region", help="AWS Region to use")
    parser.add_argument("ip_file", help="File containing IP addresses, one per line")
    args = parser.parse_args(sys.argv[1:])

    found = False
    mon_ips = read_ips_from_file(args.ip_file)

    # connect to ec2 service with provided keys
    ecc2 = boto3.client(
        "ec2",
        region_name=args.region
    )

    # acquiring Elastic IP and release it until we acquire specific IP
    while not found:
        allocation = ecc2.allocate_address(Domain="vpc")
        address = allocation["PublicIp"]
        allocation_id = allocation["AllocationId"]
        if address in mon_ips:
            found = True
            print("Acquired IP {0}".format(address))
        else:
            ecc2.release_address(AllocationId=allocation_id)

            # make sure to get new addresses
            time.sleep(60)
