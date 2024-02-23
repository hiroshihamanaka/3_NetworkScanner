#Constants.py
## Init_GUI.py
### Window Titles
WINDOW_TITLE = 'Network Scanner'

### Scan Types
SCAN_TYPE = 'Scan Type:'
SCAN_TYPE_ARP = 'ARP scan'
SCAN_TYPE_PING = 'Ping sweep'
SCAN_TYPE_PORT = 'Port scan'

### Labels
START_IP = 'Start IP (e.g., 192.168.1.0):    *Enter only the start IP to scan a single IP.'
END_IP = 'End IP (e.g., 192.168.1.10):'
PREFIX = 'Subnet Prefix (e.g., 24):'
TIMEOUT = 'Timeout (s):'
TTL = 'TTL (s):'
INTERVAL = 'Interval (s):'
PACKET_SIZE = 'Packet Size (bytes):'
START_PORT = 'Start Port#:'
END_PORT = 'End Port#:'

### Button Labels
START_SCAN_BUTTON = 'Start Scan'
ABORT_SCAN_BUTTON = 'Abort Scan'
EXPORT_DATA_BUTTON = 'Export Data'

### Status Messages
SCAN_IN_PROGRESS = 'Scan in Progress...'
SCAN_ABORTED = 'Scan aborted'
SCAN_COMPLETED = 'Scan completed'

### Table Coloums
TABLE_COLOUM_IP = 'IP Address'
TABLE_COLOUM_MAC = 'MAC Address'
TABLE_COLOUM_HOST = 'Host Name'
TABLE_COLOUM_PORT = 'Open Port Number'

### Default Inputs
DEFAULT_TIMEOUT = '4'
DEFAULT_TTL = '128'
DEFAULT_INTERVAL = '1'
DEFAULT_PACKET_SIZE = '32'

## UserInput_Handler.py
### Dictionary keys
KEY_CURRENT_SCAN_TYPE = 'Current_ScanType'
KEY_START_IP = 'start_ip'
KEY_END_IP = 'end_ip'
KEY_PREFIX = 'prefix'
KEY_TIMEOUT = 'timeout'
KEY_TTL = 'ttl'
KEY_INTERVAL = 'interval'
KEY_PACKET_SIZE = 'packet_size'
KEY_START_PORT = 'start_port'
KEY_END_PORT = 'end_port'

### Validation messages
MSG_START_IP_LESS_THAN_END_IP = 'Start IP must be less than End IP.'
MSG_INVALID_IP_FORMAT = 'Invalid IP address format. Please enter a valid IP address.'
MSG_PREFIX_BETWEEN = 'Prefix must be between 0 and 32.'
MSG_INVALID_PREFIX = 'Invalid prefix. Prefix must be an integer between 0 and 32.'
MSG_IPS_WITHIN_SUBNET = 'Both IPs should be within the subnet range defined by the prefix.'
MSG_TIMEOUT_RANGE = 'Timeout must be between 0 and 60 seconds.'
MSG_TIMEOUT_RANGE2 = 'Invalid input for timeout. Please enter a numeric value between 0 and 60 seconds.'
MSG_TTL_RANGE = 'TTL must be between 1 and 255.'
MSG_TTL_RANGE2 = 'Invalid input for TTL. Please enter a numeric value between 1 and 255 seconds.'
MSG_INTERVAL_RANGE = 'Interval must be between 0 and 60 seconds.'
MSG_INTERVAL_RANGE2 = 'Invalid input for interval. Please enter a numeric value between 0 and 60 seconds.'
MSG_PACKET_SIZE_RANGE = 'Packet size must be between 1 and 65507 bytes.'
MSG_PACKET_SIZE_RANGE2 = 'Invalid input for packet size. Please enter a numeric value between 0 and 60 seconds.'
MSG_START_PORT_RANGE = 'Start port number must be between 1 and 65535.'
MSG_END_PORT_RANGE = 'End port number must be between 1 and 65535.'
MSG_END_PORT_LESS_THAN_START_PORT = 'End port number cannot be less than start port number.'
MSG_INVALID_PORT_NUMBER = 'Invalid input for port number. Please enter a numeric value between 1 and 65535.'

### Constants for result keys
KEY_IP_RANGE = 'ip_range'

## Logging_Config.py
### Log File Name
LOG_FILE_NAME = 'NetworkScanner.log'

## Arp_Scanner.py / Ping_Sweepeer.py / Port_Scanner.py
### Unknown host
UNKNOWN_HOST = 'Unknown'