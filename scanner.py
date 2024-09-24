import socket
import sys
import subprocess
import platform
import write_file
import re

open_ports = {}


def scanning(filename, ip, port, timeout, ver):
    global open_ports

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.settimeout(timeout)

        result = sock.connect_ex((ip, port))

        if ver:
            output = f'  ||  Port: {str(port)}\nResult:'
        else:
            output = f'\n    Port {str(port)}'

        if result == 0:
            if port not in open_ports:
                open_ports[port] = 1
            else:
                open_ports[port] = open_ports[port] + 1
            output += ' OPEN'

        else:
            output += ' CLOSED'

        write_file.add_new_line(filename, output)
        sock.close()

    except KeyboardInterrupt:
        print('\nYou pressed Ctrl+C\n')
        sys.exit()

    except socket.error:
        print('\nCouldn\'t connect to server\n')
        sys.exit()


def verify_ip(host):
    global ping_time

    if platform.system().lower() == "windows":
        ping_comm = ["ping", "-n", "1", host]
        time_pattern = r"time=(\d+)ms"
    else:
        ping_comm = ["ping", "-c", "1", host]
        time_pattern = r"time=(\d+\.\d+)"

    ping_process = subprocess.Popen(ping_comm, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    ping_process.wait()

    ping_result = ping_process.communicate()[0].decode()

    if "ttl" in ping_result.lower():
        match = re.search(time_pattern, ping_result)
        if match:
            ping_time += int(match.group(1))
        else:
            ping_time += 1

        return True

    else:
        return False


ping_time = 0
