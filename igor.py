import os
import socket
import multiprocessing
import subprocess
import os
import argparse
import urllib.request
import sys


class Igor():

    def ping_job(self, job, results):
        """
        Ping target
        :param job:
        :param results:
        :return:
        """
        DEVNULL = open(os.devnull, 'w')

        while True:
            ip = job.get()
            if ip is None:
                break

            try:
                subprocess.check_call(['ping', '-c1', ip],
                                      stdout=DEVNULL)
                results.put(ip)
            except BaseException:
                pass

    def get_local_ip(self):
        """
        Find my IP address
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def get_public_ip(self):
        try:
            ip = urllib.request.urlopen(
                'https://ipinfo.io/ip').read().decode('utf8')
        except Exception as e:
            print(e)
            return None

        return ip

    def map_network(self, pool_size=255):
        """
        Maps the network
        :param pool_size: amount of parallel ping processes
        :return: list of valid ip addresses
        """

        ip_list = list()

        # get local IP and compose a base like 192.168.1.xxx
        ip_parts = self.get_local_ip().split('.')
        base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()

        pool = [
            multiprocessing.Process(
                target=self.ping_job,
                args=(
                    jobs,
                    results)) for i in range(pool_size)]

        for p in pool:
            p.start()

        # queue the ping processes 1-255
        for i in range(1, 255):
            jobs.put(base_ip + '{0}'.format(i))

        for p in pool:
            jobs.put(None)

        for p in pool:
            p.join()

        # collect the results
        while not results.empty():
            ip = results.get()
            ip_list.append(ip)

        return ip_list

    def port_scan_network(self, ips, pool_size=10):
        """
        Runs port scan on the network
        :param pool_size: amount of parallel scan jobs
        :return: list of valid ip addresses
        """

        report = []
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()

        pool = [
            multiprocessing.Process(
                target=self.port_scan_job,
                args=(
                    jobs,
                    results)) for i in range(pool_size)]

        for p in pool:
            p.start()

        for ip in ips:
            jobs.put(ip)

        for p in pool:
            jobs.put(None)

        for p in pool:
            p.join()

        # collect the results
        while not results.empty():
            scan = results.get()
            report.append(scan)

        return report

    def port_scan_job(self, jobs, results, portlist=[22, 21, 3306, 80, 443]):

        report = {}

        while True:
            ip = jobs.get()

            if ip is None:
                break

            try:
                open_ports = []

                for port in portlist:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(5)
                        con = s.connect((ip, port))
                        open_ports.append(port)
                        s.close()
                    except Exception as e:
                        pass

                report.update({ip: open_ports})
                results.put(report)
            except BaseException:
                pass

    def retrieve_ssh_passlist(self):
        try:
            authlist = urllib.request.urlopen(
                'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/ssh-betterdefaultpasslist.txt').read().decode('utf8')
        except Exception as e:
            print(e)
            return None
        return authlist

    def retrieve_ftp_passlist(self):
        try:
            authlist = urllib.request.urlopen(
                'https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt').read().decode('utf8')
        except Exception as e:
            print(e)
            return None
        return authlist


    def retrieve_mysql_passlist(self):
        try:
            authlist = urllib.request.urlopen(
                'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/mysql-betterdefaultpasslist.txt').read().decode('utf8')
        except Exception as e:
            print(e)
            return None
        return authlist


    def get_os(self):
        return os.name

        return results

    def get_hostname(self):
        return socket.gethostname()

    def get_platform(self):
        return sys.platform

    def brute_force_ssh(self, host, authlist):
        if(authlist is None):
            print("No authlist available")
            return None

        for combo in authlist.split('\n'):
            try:
                user = combo.split(":", 1)[0]
                pswd = combo.split(":", 1)[1]

                # if combo is successful...
                    #print(user+"@"+host+" :: "+pswd)
            except Exception as e:
                #print(e)
                pass

    def brute_force_ftp(self, host, authlist):
        if(authlist is None):
            print("No authlist available")
            return None

        for combo in authlist.split('\n'):
            try:
                user = combo.split(":", 1)[0]
                pswd = combo.split(":", 1)[1]

                # if combo is successful...
                    #print(user+"@"+host+" :: "+pswd)
            except Exception as e:
                #print(e)
                pass

    def brute_force_mysql(self, host, authlist):
        if(authlist is None):
            print("No authlist available")
            return None

        for combo in authlist.split('\n'):
            try:
                user = combo.split(":", 1)[0]
                pswd = combo.split(":", 1)[1]

                # if combo is successful...
                    #print(user+"@"+host+" :: "+pswd)
            except Exception as e:
                #print(e)
                pass


def setupArgs(parser):
    parser.add_argument("-w", "--worm", action="store_true",
                        help="sets Igor into worm mode")

    parser.add_argument("-m", "--map", action="store_true",
                        help="return ips in local network")

    parser.add_argument("-p", "--pscan", action="store_true",
                        help="return port scan of ips in local network")

    parser.add_argument("--who", action="store_true",
                        help="return useful notes about the executing system")

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-o", "--out", dest="output",
                        help="write results to FILE", metavar="FILE")


if __name__ == '__main__':
    print("""
██╗ ██████╗  ██████╗ ██████╗
██║██╔════╝ ██╔═══██╗██╔══██╗
██║██║  ███╗██║   ██║██████╔╝
██║██║   ██║██║   ██║██╔══██╗
██║╚██████╔╝╚██████╔╝██║  ██║
╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝

    """)
    parser = argparse.ArgumentParser()
    setupArgs(parser)
    args = parser.parse_args()

    igor = Igor()

    if(args.worm):
        if(args.verbose):
            print("Worm Mode activated")

        if(args.verbose):
            print("Grabbing auth combos...")

        ssh_list = igor.retrieve_ssh_passlist()  # get basic auth list
        ftp_list = igor.retrieve_ftp_passlist()
        mysql_list = igor.retrieve_mysql_passlist()

        if(args.verbose):
            print("Mapping network...")

        ips = igor.map_network()
        print(ips)

        if(args.verbose):
            print("Scanning network...")
        reports = igor.port_scan_network(ips)

        for report in reports:
            open_ports = list(report.values())[0]

            if(22 in open_ports):
                host=list(report.keys())[0]
                if(args.verbose):
                    print("Bruteforce SSH attempt on "+host+"...")
                igor.brute_force_ssh(host, ssh_list)

            if(21 in open_ports):
                host = list(report.keys())[0]
                if(args.verbose):
                    print("Bruteforce FTP attempt on"+host+"...")
                igor.brute_force_ftp(host,ftp_list)

            if(3306 in open_ports):
                host = list(report.keys())[0]
                if(args.verbose):
                    print("Bruteforce MYSQL attempt on"+host+"...")
                igor.brute_force_mysql(host,mysql_list)




    elif(args.map):
        if(args.verbose):
            print('Mapping...')

        ips = igor.map_network()
        print(ips)

    elif(args.who):
        if(args.verbose):
            print("Getting info about host...")
        print("Local IP: " + igor.get_local_ip())
        print("Public IP: " + igor.get_public_ip())
        print("Hostname: " + igor.get_hostname())
        print("Operating System: " + igor.get_os())
        print("Platform: " + igor.get_platform())

    elif(args.pscan):
        if(args.verbose):
            print('Mapping...')

        ips = igor.map_network()

        if(args.verbose):
            print("Scanning...")

        scan = igor.port_scan_network(ips)

        for report in scan:
            print(report)
