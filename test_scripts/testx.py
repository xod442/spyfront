
from jsonrpclib import Server
from cvprac.cvp_client import CvpClient
from utilities.build_db import *

cvp = '10.132.0.77'
cvp_user = 'cvpadmin'
cvp_word = 'Grape123'



#inventory = get_inventory(cvp,cvp_user,cvp_word)
#vlans = get_vlan(inventory,cvp_user,cvp_word)
#loops = get_loopback(inventory,cvp_user,cvp_word)

device = get_device(cvp,cvp_user,cvp_word)
print device
print type(device)

vxlans = get_vxlan_interface(cvp,cvp_user,cvp_word)
print vxlans
for flood in vxlans:
    if flood['floods']:
        print flood
