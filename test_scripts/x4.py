from pyhpeimc.auth import *
from pyhpeimc.plat.icc import *
from pyhpeimc.plat.device import *


auth = IMCAuth("http://", "10.132.0.15", "8080", "admin", "admin")
filecontent = 'sample file content'

print auth

vendors = get_system_vendors(auth.creds, auth.url)

#print vendors


create_new_file = create_cfg_segment('CW7SNMP.cfg',filecontent,'My New Template',auth.creds,auth.url)
template_id = get_template_id('CW7SNMP.cfg', auth.creds, auth.url)


print template_id
