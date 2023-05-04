import time
import boto3
import argparse
import sys
import os
from concurrent.futures import ThreadPoolExecutor

# other functions remain the same

def acquire_ip(ecc2, mon_ips, output_file):
    found = False
    while not found:
        allocation = ecc2.allocate_address(Domain="vpc")
        address = allocation["PublicIp"]
        allocation_id = allocation["AllocationId"]
        if address in mon_ips:
            found = True
            print_and_log("Acquired IP {0}".format(address), output_file)
            print_and_log("Found IP: {0}".format(address), output_file)
        else:
            print_and_log("Generated IP {0} does not match desired IPs. Releasing...".format(address), output_file)
            ecc2.release_address(AllocationId=allocation_id)
            time.sleep(60)

if __name__ == "__main__":
    # parse arguments
    # same as before

    mon_ips = read_ips_from_file(args.ip_file)

    ecc2 = boto3.client(
        "ec2",
        aws_access_key_id=args.AWSAccessKeyId,
        aws_secret_access_key=args.AWSSecretKey,
        region_name=args.region
    )

    num_threads = 10  # Adjust this number based on the number of concurrent threads you want
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(acquire_ip, ecc2, mon_ips, args.output_file)
