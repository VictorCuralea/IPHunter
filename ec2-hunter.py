import time
import boto3
import argparse
import sys

def read_ips_from_file(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acquire specific Elastic IP addresses in AWS")
    parser.add_argument("-region", dest="region", help="AWS Region to use", required=True)
    parser.add_argument("-ips", dest="ip_file", help="File containing IP addresses, one per line", required=True)
    parser.add_argument("-awsid", dest="AWSAccessKeyId", help="Your AWS access key ID", required=True)
    parser.add_argument("-awssecret", dest="AWSSecretKey", help="Your AWS secret access key", required=True)
    args = parser.parse_args(sys.argv[1:])

    found = False
    mon_ips = read_ips_from_file(args.ip_file)

    # connect to ec2 service with provided keys
    ecc2 = boto3.client(
        "ec2",
        aws_access_key_id=args.AWSAccessKeyId,
        aws_secret_access_key=args.AWSSecretKey,
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
            print("Generated IP {0} does not match desired IPs. Releasing...".format(address))
            ecc2.release_address(AllocationId=allocation_id)

            # make sure to get new addresses
            time.sleep(60)
