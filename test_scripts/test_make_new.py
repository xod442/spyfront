
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
from configlets import arista_config_build
from configlet_assign.assignlet import *
from settings import APP_STATIC
from utilities.build_db import *
from utilities.tunnel import *
from utilities.vxlan_builder import *
from init.models import Vxlan, Inventory, Creds

vlan = "102"
switch_list = ['10.132.0.188', '10.132.0.185', '10.132.0.182']
processed_list = ['10.132.0.184','10.132.0.189']
vxlan = {}

new_vxlan_list = []

for switch in switch_list:

    new_flood = {}
    new_vxlan = {}
    new_list = []
    local_ip = []
    new_vni = {}
    new_vni_list = []

    local_ip.append(switch)

    print 'this is the local_ip %s' % (local_ip)

    # Remove local switch IP from switchlist
    new_list = set(switch_list) - set(local_ip)
    # Turn the set back into a python list
    new_list = list(new_list)

    new_flood['floods'] = new_list+processed_list
    new_flood['vlan'] = vlan.encode('utf-8')
    print 'this is thenew_flood %s' % (new_flood)

    xx_vni = vlan.encode('utf-8')+'00'

    print 'this is the xx_vni  %s' % (xx_vni)

    new_vni['vni'] = xx_vni
    new_vni['vlan'] = vlan.encode('utf-8')
    new_vni_list.append(new_vni)

    print 'this is the new_vni_list %s' % (new_vni_list)

    #print 'this is the vinny %s' % (vxlan['vni'])
    new_vxlan['floods'] = new_flood
    new_vxlan['sip'] = switch.encode('utf-8')
    new_vxlan['vni'] = new_vni_list

    # Now check the switch for the loopback in use and
    #device = Inventory.objects(sip = switch).first()
    new_vxlan['host'] = 'temp host'
    print 'this is the new_vxlan %s' % (new_vxlan)



    new_vxlan_list.append(new_vxlan)

    print '-----------------------------------------------------------------------'
    print new_vxlan_list
    print '-----------------------------------------------------------------------'
