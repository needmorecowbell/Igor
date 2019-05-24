import os
import socket
import multiprocessing
import subprocess
import os

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
            except:
                pass

    def get_my_ip(self):
        """
        Find my IP address
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip


    def map_network(self, pool_size=255):
        """
        Maps the network
        :param pool_size: amount of parallel ping processes
        :return: list of valid ip addresses
        """

        ip_list = list()

        # get local IP and compose a base like 192.168.1.xxx
        ip_parts = self.get_my_ip().split('.')
        base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()

        pool = [multiprocessing.Process(target=self.ping_job, args=(jobs, results)) for i in range(pool_size)]

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

    def port_scan(self, ip, portlist=[22,21,3306,80,443]):
        results = []

        for port in portlist:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                con = s.connect((ip,port))
                results.append(port)
                s.close()
            except Exception as e:
                pass


        return results

if __name__ == '__main__':

    print('Mapping...')
    i = Igor()
    ips = i.map_network()

    for ip in ips:
        print("target: "+ ip)
        print(i.port_scan(ip))
