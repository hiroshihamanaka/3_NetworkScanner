#Port_Scanner.py
from scapy.all import sr, IP, TCP, conf
from . import Constants
import logging

class PortScanner:
    '''
    Port Scanner class for scanning TCP ports of active hosts.
    '''
    def __init__(self, start_port, end_port, active_hosts, stop):
        '''
        Initializes the Port Scanner.

        Args:
            start_port (int): The starting port number for the scan.
            end_port (int): The ending port number for the scan.
            active_hosts (list): A list of active hosts to scan.
            stop (function): A function that returns True if the scanning process should be stopped.
        '''
        self.start_port = start_port
        self.end_port = end_port
        self.active_hosts = active_hosts

        self.stop = stop

    def port_scanner(self):
        '''
        Scans the specified range of ports for each active host.

        Returns:
            list: A list of dictionaries, each containing information about a host and its open ports.
        '''
        conf.verb = 0    # Suppress Scapy output to stdout
        open_ports_info = []

        for host_info in self.active_hosts:
            if self.stop():    # Check if the scan should be stopped
                break

            ip = host_info[Constants.TABLE_COLOUM_IP]
            open_ports = []

            for port in range(self.start_port, self.end_port + 1):
                if self.stop():
                    break
                
                # Send a TCP SYN packet to each port
                tcp_packet = IP(dst=ip) / TCP(dport=port, flags='S')
                answered, _ = sr(tcp_packet, timeout=1, verbose=False)

                for _, received in answered:
                    # Check if the port responded with SYN-ACK
                    if received.haslayer(TCP) and received[TCP].flags & 0x12:
                        open_ports.append(port)

                        # Send a RST to close the connection
                        rst_packet = IP(dst=ip) / TCP(dport=port, flags='R')
                        sr(rst_packet, timeout=1, verbose=False)

            # Compile host and port information
            host_info_dict = {
                Constants.TABLE_COLOUM_IP: ip,
                Constants.TABLE_COLOUM_MAC: host_info.get(Constants.TABLE_COLOUM_MAC),
                Constants.TABLE_COLOUM_HOST: host_info.get(Constants.TABLE_COLOUM_HOST),
                Constants.TABLE_COLOUM_PORT: open_ports
            }
            open_ports_info.append(host_info_dict)

        logging.info('Port scan completed.')
        return open_ports_info
