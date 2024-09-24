#!/usr/bin/python3
import argparse
import checks
import scanner
import ipaddress
import write_file
import sys

parser = argparse.ArgumentParser(description='Script used to scan ports of IP\'s')
parser.add_argument('file', action='store', type=str, metavar='Filename')

parser.add_argument('ip', action='store', type=str, metavar='IP Class C')
parser.add_argument('-i', '--end_ip', help='Option to specify the final Class C IP (255.255.255.0)', metavar='\b',
                    action='store', type=str)

parser.add_argument('port', action='store', type=int, metavar='Port')
parser.add_argument('-p', '--end_port', help='Option to specify the final port number', metavar='\b',
                    action='store', type=int)

parser.add_argument('-v', '--verbose', help='Option to make the output more detailed', action='store_true')
parser.add_argument('-t', '--time', help='Time required to ping the IP', action='store_true')
parser.add_argument('-u', '--timeout', help='Timeout for each IP port scan', metavar='\b', action='store', type=float)
parser.add_argument('-c', '--cript', help='Option to encrypt the file', action='store_true')

args = parser.parse_args()

if not args.timeout:
    timeout = 0.5

elif 0 <= args.timeout <= 10:
    timeout = args.timeout

else:
    print('\nThe timeout inserted is a negative number or is higher than 10\n')
    sys.exit()

filename = checks.check_filename(args.file)
ips = checks.check_ips(args.ip, args.end_ip, filename)
ports = checks.check_ports(args.port, args.end_port, filename)
ver = args.verbose
time = args.time


if not ips[1]:
    if scanner.verify_ip(ips[0]):
        if not ports[1]:
            if ver:
                write_file.add_new_line(filename, f'\nTested IP: {ips[0]}')
            else:
                write_file.add_new_line(filename, f'\n{ips[0]}:')

            scanner.scanning(filename, ips[0], ports[0], timeout, ver)
            write_file.add_new_line(filename, '\n')

        else:
            if not ver:
                write_file.add_new_line(filename, f'\n{ips[0]}:')

            for port in range(ports[0], ports[1] + 1):
                if ver:
                    write_file.add_new_line(filename, f'\n{ips[0]}:')

                scanner.scanning(filename, ips[0], port, timeout, ver)

                if ver:
                    write_file.add_new_line(filename, '\n')

            if not ver:
                write_file.add_new_line(filename, '\n')

    else:
        if ver:
            write_file.add_new_line(filename, f'\nTested IP {ips[0]} is unavailable to connect')
        else:
            write_file.add_new_line(filename, f'\n{ips[0]}: Unavailable to connect')

else:
    initial = ipaddress.ip_address(ips[0])
    final = ipaddress.ip_address(ips[1])

    while initial <= final:
        if scanner.verify_ip(str(initial)):
            if not ports[1]:
                if ver:
                    write_file.add_new_line(filename, f'\nTested IP: {initial}')
                else:
                    write_file.add_new_line(filename, f'\n{initial}:')
                scanner.scanning(filename, str(initial), ports[0], timeout, ver)
                write_file.add_new_line(filename, '\n')
                initial += 1

            else:
                if not ver:
                    write_file.add_new_line(filename, f'\n{initial}:')

                for port in range(ports[0], ports[1] + 1):
                    if ver:
                        write_file.add_new_line(filename, f'\nTested IP: {initial}')
                    scanner.scanning(filename, str(initial), port, timeout, ver)
                    if ver:
                        write_file.add_new_line(filename, '\n')

                if not ver:
                    write_file.add_new_line(filename, '\n')
                initial += 1

        else:
            if ver:
                write_file.add_new_line(filename, f'\nTested IP {initial} is unavailable to connect\n')
            else:
                write_file.add_new_line(filename, f'\n{initial}: Unavailable to connect\n')
            initial += 1

if scanner.open_ports == {}:
    pass
else:
    if not ver:
        write_file.add_new_line(filename, f'\nOpened ports:\n')

    for port, count in scanner.open_ports.items():
        if ver:
            write_file.add_new_line(filename, f'\nThe port {port} is open in {count} IP\'s\n')
        else:
            write_file.add_new_line(filename, f'    Port: {port}  ||  Count: {count}\n')

if time:
    write_file.add_new_line(filename, f'\nTotal scan time {scanner.ping_time}ms')

print(f'\nThe scan has been successfully saved in file {filename}\n')
