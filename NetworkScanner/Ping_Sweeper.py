#Ping_Sweeper.py
from scapy.all import sr, IP, ICMP, conf
import socket
from . import Constants
import logging

class PingSweeper:
    '''
    Ping Sweeper class for network discovery using ICMP echo requests.
    '''
    def __init__(self, timeout, ttl, interval, packet_size, ip_range, stop):
        '''
        Initializes the Ping Sweeper.

        Args:
            timeout (float): Maximum time to wait for a response, in seconds.
            ttl (int): Time to live for packets.
            interval (float): Interval between packet sends, in seconds.
            packet_size (int): Size of the payload in ICMP packets.
            ip_range (list): The range of IP addresses to scan.
            stop (function): A function that returns True if the scanning process should be stopped.
        '''
        self.timeout = timeout
        self.ttl = ttl
        self.interval = interval
        self.packet_size = packet_size
        self.ip_range = ip_range

        self.stop = stop

    def ping_sweeper(self):
        '''
        Executes a ping sweep over the specified IP range.

        Returns:
            list: A list of dictionaries, each containing information about a detected host.
        '''
        conf.verb = 0    # Suppress Scapy output to stdout
        host_list = []

        for ip in self.ip_range:
            if self.stop():    # Check if the scan should be stopped
                break

            # Construct and send an ICMP echo request packet
            icmp_packet = IP(dst=ip) / ICMP() / ('X' * self.packet_size)
            answered, unanswered = sr(icmp_packet, timeout=self.timeout, inter=self.interval, verbose=False)
                
            for unanswered, received in answered:
                if self.stop():
                    break
                
                ip_address = received.src
                try:
                    # Attempt to resolve hostname
                    hostname = socket.gethostbyaddr(ip_address)[0]
                except socket.herror:
                    hostname = Constants.UNKNOWN_HOST    # Use placeholder if resolution fails

                # Compile device info and add to list
                device_info = {
                    Constants.TABLE_COLOUM_IP: received.src,
                    Constants.TABLE_COLOUM_MAC: '',    # MAC address is not available here
                    Constants.TABLE_COLOUM_HOST: hostname,
                    Constants.TABLE_COLOUM_PORT: []    # Ports are not scanned here
                }
                host_list.append(device_info)

        logging.info('Ping sweep completed.')
        return host_list