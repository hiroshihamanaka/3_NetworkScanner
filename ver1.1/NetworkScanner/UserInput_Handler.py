#UserInput_Handler.py
import ipaddress
from . import Constants

class UserInputHandler():
	'''
	Handles validation of user inputs for network scanning parameters.
    Validates inputs such as IP addresses, subnet prefix, timeout, TTL, interval, packet size, and port numbers.
	'''
	def __init__(self, **kwargs):
		'''
        Initializes the UserInputHandler with scan parameters.
        :param kwargs: Keyword arguments containing scan parameters.
		'''
		self.Current_ScanType = kwargs.get(Constants.KEY_CURRENT_SCAN_TYPE)
		self.start_ip = kwargs.get(Constants.KEY_START_IP)
		self.end_ip=kwargs.get(Constants.KEY_END_IP)
		self.prefix=kwargs.get(Constants.KEY_PREFIX)
		self.timeout=kwargs.get(Constants.KEY_TIMEOUT)
		self.ttl=kwargs.get(Constants.KEY_TTL)
		self.interval=kwargs.get(Constants.KEY_INTERVAL)
		self.packet_size=kwargs.get(Constants.KEY_PACKET_SIZE)
		self.start_port=kwargs.get(Constants.KEY_START_PORT)
		self.end_port=kwargs.get(Constants.KEY_END_PORT)
	
	def validate_all(self):
		'''
        Validates all user inputs and returns a dictionary of validated parameters.
        :return: Dictionary of validated scan parameters.
        :raises ValueError: If any input validation fails.
		'''
		validated_ip_addr = self.ip_addr_validator()
		validated_prefix = self.prefix_validator()
		validated_network_addr = self.network_addr_validator()
		validated_timeout = self.timeout_validator()
		validated_ttl = self.ttl_validator()
		validated_interval = self.interval_validator()
		validated_packet_size = self.packet_size_validator()
		validated_start_port, validated_end_port = self.port_num_validator()
		ip_range = self.setup_ip_range()

		return {
			Constants.KEY_IP_RANGE: ip_range,
			Constants.KEY_TIMEOUT: validated_timeout,
			Constants.KEY_TTL: validated_ttl,
			Constants.KEY_INTERVAL: validated_interval,
			Constants.KEY_PACKET_SIZE: validated_packet_size,
			Constants.KEY_START_PORT: validated_start_port,
			Constants.KEY_END_PORT: validated_end_port
		}

	def ip_addr_validator(self):
		'''
		Validates start and end IP addresses.
        :return: Tuple of validated start and end IP addresses.
        :raises ValueError: If IP addresses are invalid or start IP is greater than end IP.
		'''
		try:
			validated_start_ip = ipaddress.ip_address(self.start_ip)
			validated_end_ip = ipaddress.ip_address(self.end_ip) if self.end_ip else ipaddress.ip_address(self.start_ip)


			if validated_start_ip > validated_end_ip:
				raise ValueError(Constants.MSG_START_IP_LESS_THAN_END_IP)

		except ValueError:
			raise ValueError(Constants.MSG_INVALID_IP_FORMAT)
		
		return validated_start_ip, validated_end_ip

	def prefix_validator(self):
		'''
		Validates the subnet prefix.
        :return: Validated prefix as an integer.
        :raises ValueError: If the prefix is not between 0 and 32.
		'''
		try:
			validated_prefix = int(self.prefix)
			if not (0 <= validated_prefix <= 32):
				raise ValueError(Constants.MSG_PREFIX_BETWEEN)
		except ValueError:
			raise ValueError(Constants.MSG_INVALID_PREFIX)
		
		return validated_prefix

	def network_addr_validator(self):
		'''
		Validates that the start and end IP addresses are within the same network as defined by the subnet prefix.
        :return: The validated network address as an ipaddress.IPv4Network or ipaddress.IPv6Network object.
        :raises ValueError: If the IPs are not within the subnet defined by the prefix.
		'''
		validated_start_ip, validated_end_ip = self.ip_addr_validator()
		validated_prefix = self.prefix_validator()

		try:
			validate_network_addr = ipaddress.ip_network(f'{validated_start_ip}/{validated_prefix}', strict=False)
			if not (validated_start_ip in validate_network_addr and validated_end_ip in validate_network_addr):
				raise ValueError(Constants.MSG_IPS_WITHIN_SUBNET)
		except ValueError as e:
			raise ValueError(e)
		
		return validate_network_addr
	
	def timeout_validator(self):
		'''
        Validates the timeout value ensuring it is within an acceptable range.
        :return: Validated timeout as a float.
        :raises ValueError: If the timeout is not within the range 0 to 60 seconds.
		'''
		try:
			validated_timeout = float(self.timeout)
			if not (0 < validated_timeout <= 60):
				raise ValueError(Constants.MSG_TIMEOUT_RANGE)
		except ValueError:
			raise ValueError(Constants.MSG_TIMEOUT_RANGE2)

		return validated_timeout

	def ttl_validator(self):
		'''
        Validates the Time To Live (TTL) value for packets.
        :return: Validated TTL as an integer.
        :raises ValueError: If the TTL is not between 1 and 255.
		'''
		try:
			validated_ttl = int(self.ttl)
			if not (1 <= validated_ttl <= 255):
				raise ValueError(Constants.MSG_TTL_RANGE)
		except ValueError:
			raise ValueError(Constants.MSG_TTL_RANGE2)

		return validated_ttl

	def interval_validator(self):
		'''
        Validates the interval between sending packets.
        :return: Validated interval as a float.
        :raises ValueError: If the interval is not within the range 0 to 60 seconds.
		'''
		try:
			validated_interval = float(self.interval)
			if not (0 < validated_interval <= 60):
				raise ValueError(Constants.MSG_INTERVAL_RANGE)
		except ValueError:
			raise ValueError(Constants.MSG_INTERVAL_RANGE2)

		return validated_interval

	def packet_size_validator(self):
		'''
        Validates the packet size for ICMP packets.
        :return: Validated packet size as an integer.
        :raises ValueError: If the packet size is not between 1 and 65507 bytes.
		'''
		try:
			validated_packet_size = int(self.packet_size)
			if not (1 <= validated_packet_size <= 65507):
				raise ValueError(Constants.MSG_PACKET_SIZE_RANGE)
		except ValueError:
			raise ValueError(Constants.MSG_PACKET_SIZE_RANGE2)

		return validated_packet_size
		
	def port_num_validator(self):
		'''
        Validates the start and end port numbers for port scanning.
        :return: Tuple of validated start and end port numbers.
        :raises ValueError: If port numbers are not between 1 and 65535, or end port is less than start port.
		'''
		if self.Current_ScanType != Constants.SCAN_TYPE_PORT:
			return None, None

		try:
			validated_start_port = int(self.start_port) if self.start_port.isdigit() else None
			validated_end_port = int(self.end_port) if self.end_port and self.end_port.isdigit() else int(self.start_port)

			if not (1 <= validated_start_port <= 65535):
				raise ValueError(Constants.MSG_START_PORT_RANGE)
			if not (1 <= validated_end_port <= 65535):
				raise ValueError(Constants.MSG_END_PORT_RANGE)
			if validated_end_port < validated_start_port:
				raise ValueError(Constants.MSG_END_PORT_LESS_THAN_START_PORT)
			
		except ValueError:
			raise ValueError(Constants.MSG_INVALID_PORT_NUMBER)
		
		return validated_start_port, validated_end_port

	def setup_ip_range(self):
		'''
		Generates an IP range based on validated start and end IP addresses.
        :return: List of IP addresses within the range.
		'''
		validated_start_ip, validated_end_ip = self.ip_addr_validator()

		start_ip = ipaddress.ip_address(validated_start_ip)
		end_ip = ipaddress.ip_address(validated_end_ip)

		ip_range = [str(ip) for ip in ipaddress.summarize_address_range(start_ip, end_ip)]
    
		return ip_range