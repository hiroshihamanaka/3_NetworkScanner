#Scan_Thread.py
from PyQt5.QtCore import QThread, pyqtSignal
from NetworkScanner.Arp_Scanner import ArpScanner
from NetworkScanner.Ping_Sweeper import PingSweeper
from NetworkScanner.Port_Scanner import PortScanner
from . import Constants

class ScanThread(QThread):
    '''A QThread subclass designed to perform network scans in a separate thread to prevent GUI freezing.'''

    # Signals to communicate with the main thread
    result_signal = pyqtSignal(object)    # Emit scan results
    error_signal = pyqtSignal(str)        # Emit error messages

    def __init__(self, Current_ScanType, ip_range, timeout, ttl, interval, packet_size, start_port, end_port):
        '''Initializes the scan thread with parameters for the scan.'''
        super(ScanThread, self).__init__()
        # Scan parameters
        self.Current_ScanType = Current_ScanType
        self.ip_range = ip_range
        self.timeout = timeout
        self.ttl = ttl
        self.interval = interval
        self.packet_size = packet_size
        self.start_port = start_port
        self.end_port = end_port

        # Flag to indicate when the thread should stop
        self.stop_thread_flag = False
        # Flag to indicate if an error occurred during the scan
        self.error = False

    def run(self):
        '''Performs the network scan based on the initialized parameters.'''
        try:
            # Lambda function to check if the thread has been asked to stop
            stop_arg = lambda: self.stop_thread_flag

            scan_result = None

            # Perform ARP scan
            if self.Current_ScanType == Constants.SCAN_TYPE_ARP:
                ARP_ScannerInstance = ArpScanner(ip_range=self.ip_range, stop=stop_arg)
                scan_result = ARP_ScannerInstance.arp_scanner()

            # Perform Ping sweep
            elif self.Current_ScanType == Constants.SCAN_TYPE_PING:        
                PING_SweeperInstance = PingSweeper(timeout=self.timeout, ttl=self.ttl, interval=self.interval, packet_size=self.packet_size, ip_range=self.ip_range, stop=stop_arg)
                scan_result = PING_SweeperInstance.ping_sweeper()

            # Perform Port scan
            elif self.Current_ScanType == Constants.SCAN_TYPE_PORT:
                PING_SweeperInstance = PingSweeper(timeout=self.timeout, ttl=self.ttl, interval=self.interval, packet_size=self.packet_size, ip_range=self.ip_range, stop=stop_arg)
                active_hosts = PING_SweeperInstance.ping_sweeper()

                PORT_ScannerInstance = PortScanner(start_port=self.start_port, end_port=self.end_port, active_hosts=active_hosts, stop=stop_arg)
                scan_result = PORT_ScannerInstance.port_scanner()
            
            # If scan_result is not None, emit the results
            if scan_result is not None:
                self.result_signal.emit(scan_result)
                print(scan_result)

        except ValueError as e:
            # Emit error signal and set error flag
            self.error_signal.emit(str(e))
            self.error = True
            return

    def stop(self):
        '''Sets the flag to stop the running thread.'''
        self.stop_thread_flag = True