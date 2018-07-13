import ifcfg
import json

for name, interface in ifcfg.interfaces().items():
    # do something with interface
    print(interface['device'])
    #print(interface['inet'])         # First IPv4 found
    #print(interface['inet4'])        # List of ips
    #print(interface['inet6'])
    #print(interface['netmask'])
    #print(interface['broadcast'])

default = ifcfg.default_interface()
