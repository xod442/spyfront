
'''
 2017 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Flask script that processes existing vlan interface flood lists and vni
'''

from jsonrpclib import Server
from cvprac.cvp_client import CvpClient
from flask import Blueprint, render_template, send_file, request, redirect, session, url_for, abort, flash
import bcrypt
import uuid
import os
from werkzeug import secure_filename
from mongoengine import Q


vlan = "666"
new_switch_list = ['10.132.0.188', '10.132.0.185']

temp_vni = {}
new_vxlan_list = []
local_ip = []
update_list = []


for switch in new_switch_list:

    new_flood = {}
    new_vxlan = {}
    new_list = []
    local_ip = []

    local_ip.append(switch)

    # Remove local switch IP from switchlist
    new_list = set(new_switch_list) - set(local_ip)
    # Turn the set back into a python list
    new_list = list(new_list)

    new_flood[u'floods'] = new_list
    new_flood[u'vlan'] = vlan

    temp_vni['vni'] = vlan+'00'
    temp_vni['vlan'] = vlan

    #print 'this is the vinny %s' % (vxlan['vni'])
    new_vxlan['floods'] = new_flood
    new_vxlan['vni'] = temp_vni
    new_vxlan['sip'] = switch

    new_vxlan['sint'] = 'loopback 0'

    new_vxlan_list.append(new_vxlan)


print new_vxlan_list
