import ipaddress


class TestModule(object):

    def tests(self):
        return {
            'ipv4_address': self.validate_ipv4_address,
            'ipv4_network': self.validate_ipv4_network,
            'ipv6_address': self.validate_ipv6_address,
            'ipv6_network': self.validate_ipv6_network,
        }

    def validate_ipv4_address(self, address: str):
        try:
            ipaddress.IPv4Address(address)
        except:
            return False
        return True

    def validate_ipv4_network(self, address: str):
        try:
            ipaddress.IPv4Network(address)
        except:
            return False
        return True
    
    def validate_ipv6_address(self, address: str):
        try:
            ipaddress.IPv6Address(address)
        except:
            return False
        return True

    def validate_ipv6_network(self, address: str):
        try:
            ipaddress.IPv6Network(address)
        except:
            return False
        return True
