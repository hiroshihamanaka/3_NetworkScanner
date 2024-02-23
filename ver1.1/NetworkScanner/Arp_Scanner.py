#Arp_Scanner.py
from scapy.all import srp, Ether, ARP, conf
import socket
from . import Constants
import logging

class ArpScanner:
    '''
    ARP Scanner class to perform network scans using ARP packets.
    '''
    def __init__(self, ip_range, stop):
        '''
        Initializes the ARP scanner.

        Args:
            ip_range (list): The range of IP addresses to scan.
            stop (function): A function that returns True if the scanning process should be stopped.

        '''
        self.ip_range = ip_range

        self.stop = stop

    def arp_scanner(self):
        '''
        Executes an ARP scan over the specified IP range.

        Returns:
            list: A list of dictionaries, each containing information about a detected host.
        '''
        logging.info('ARP scan started.')
        conf.verb = 0   # Suppress Scapy output to stdout
        host_list = []

        for ip in self.ip_range:
            if self.stop():
                break

            # Construct and send an ARP packet
            arp_packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip)
            answered, unanswered = srp(arp_packet, timeout=2, verbose=False)
        
            for unanswered, received in answered:
                if self.stop():
                    break
                
                ip_address = received.psrc

                try:
                    # Attempt to resolve hostname
                    hostname = socket.gethostbyaddr(ip_address)[0]
                except socket.herror:
                    hostname = Constants.UNKNOWN_HOST# Use placeholder if resolution fails

                 # Compile device info and add to list
                device_info = {
                    Constants.TABLE_COLOUM_IP: ip_address, 
                    Constants.TABLE_COLOUM_MAC: received.hwsrc, 
                    Constants.TABLE_COLOUM_HOST: hostname    # Ports are not scanned here
                    }
                device_info[Constants.TABLE_COLOUM_PORT] = []
                host_list.append(device_info)

        logging.info('ARP scan completed.')
        return host_list