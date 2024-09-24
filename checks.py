import re
import sys
import os
import write_file
from datetime import datetime


def check_filename(filename):
    if not filename.endswith('.txt'):
        filename = f'{filename.replace(".", "_")}.txt'

    if not os.path.exists(filename):
        return filename
    else:
        print(f'\nThe file {filename} already exists\n')
        sys.exit(1)


def check_ips(initial, final, filename):
    ip_template = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

    if initial and final:
        ini_divided = initial.split('.')
        fin_divided = final.split('.')

        if re.match(ip_template, initial) and 0 < int(ini_divided[0]) and 0 < int(ini_divided[3]) < 255:
            if re.match(ip_template, final) and 0 < int(fin_divided[0]) and 0 < int(fin_divided[3]) < 255:

                for octet in ini_divided:
                    if not 0 <= int(octet) <= 255:
                        print(f'\nThe initial IP ({initial}) is not a valid usable IPv4\n')
                        sys.exit(1)

                for octet in fin_divided:
                    if not 0 <= int(octet) <= 255:
                        print(f'\nThe final IP ({final}) is not a valid usable IPv4\n')
                        sys.exit(1)

                if ini_divided[:3] != fin_divided[:3]:
                    print(f'\nYour initial IP ({initial}) isn\'t equal to your final IP ({final}) for class C\n')
                    sys.exit(1)

                elif int(ini_divided[3]) > int(fin_divided[3]):
                    print(f'\nYour initial IP ({initial}) is higher then your final IP ({final}) for class C\n')
                    sys.exit(1)

                elif int(ini_divided[3]) == int(fin_divided[3]):
                    pass

                else:

                    write_file.add_new_line(filename,
                                            f'{check_actual_time()}\nThis your initial IP: {initial}  ||  This your final IP: {final}\n')
                    return [initial, final]

            else:
                print(f'\nThe final IP ({final}) is not a valid IPv4\n')
                sys.exit(1)

        else:
            print(f'\nThe initial IP ({initial}) is not a valid IPv4\n')
            sys.exit(1)

    divided = initial.split('.')

    if re.match(ip_template, initial) and 0 < int(divided[0]) and 0 < int(divided[3]) < 255:

        for octet in divided:
            if not 0 <= int(octet) <= 255:
                print(f'\nThe IP {initial} is not a valid usable IPv4\n')
                sys.exit(1)

        write_file.add_new_line(filename, f'{check_actual_time()}\nThis your IP to scan: {initial}\n')
        return [initial, final]

    else:
        print(f'\nThe IP ({initial}) is not a valid IPv4\n')
        sys.exit(1)


def check_ports(initial, final, filename):
    if initial and final:
        if 0 <= initial <= 65535:
            if 0 <= final <= 65535:

                if initial > final:
                    print(f'\nYour initial port ({initial}) is higher then your final port ({final})\n')
                    sys.exit(1)

                elif initial == final:
                    pass

                else:
                    write_file.add_new_line(filename,
                                            f'This your initial port: {initial}  ||  This your final port: {final}\n')
                    return [initial, final]

            else:
                print(f'\nThe final port ({initial}) isn\'t between (0-65535)\n')
                sys.exit(1)

        else:
            print(f'\nThe initial port ({initial}) isn\'t between (0-65535)\n')
            sys.exit(1)

    if 0 <= initial <= 65535:
        write_file.add_new_line(filename, f'This your port to scan: {initial}\n')
        return [initial, final]

    else:
        print(f'\nThe initial port ({initial}) isn\'t between (0-65535)\n')
        sys.exit(1)


def check_actual_time():
    time_now = datetime.now()
    formatted_time = time_now.strftime("%d/%m/%y %H:%M:%S")
    return formatted_time
