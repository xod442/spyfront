
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

Flask script that builds a configlet of interface vxlan 1 as saves file
'''

from jsonrpclib import Server
from cvprac.cvp_client import CvpClient
from flask import Blue#print, render_template, send_file, request, redirect, session, url_for, abort, flash
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
x = {}
y = {}
x[u'sint'] = "loopback0"
x[u'vni'] = [ { "vlan" : "102", "vni" : 10200 }, { "vlan" : "3000", "vni" : 30000 } ]
x[u'floods']= [ { "floods" : [ "10.132.0.189","10.10.10.10","12.12.12.12"], "vlan" : "102" }, { "floods" : [ "10.132.0.189" ], "vlan" : "30000" } ]
x[u'sip'] = '10.132.0.184'
x[u'host'] = 'pod2.leaf01'

y['sint'] = "loopback1"
y[u'vni'] = [ { "vlan" : "102", "vni" : 10200 }]
y[u'floods'] = [ { "floods" : [ "10.132.0.184","10.132.0.111","10.132.0.12" ], "vlan" : "102" } ]
y[u'sip'] = "10.132.0.189"
y[u'host'] = 'pod2.leaf06'

vxlans = [x,y]
vlan = "666"
switch_list = ['10.132.0.188', '10.132.0.185', '10.132.0.182','10.132.0.184','10.132.0.189']
new_vxlan_list = []
modified_vxlan_list = []
established_floods = []
counter = 0
processed_list = []
# Iterate through all the switches, look for updates
for vx in vxlans:
    #print 'for vx in vxlans counter is %s' % (counter)
    vxlan = {}
    update_list = []
    new_flood = {}
    local_ip = []
    current_flood = []
    new_vxlan = {}
    mod_vxlan = {}
    # This switch has a vxlan interface check to see if it belongs to the vlan
    # Get the vni to vlan map...it could be a list a list
    vni = vx[u'vni']
    sip = vx[u'sip']

    temp_vni = []
    for vmap in vni:
        #The vxlan is part of the vlan from the end user
        temp = vmap[u'vlan']
        temp_vni.append(temp)

    #print 'this is the temp vni list %s' % (temp_vni)

    if vlan in temp_vni and sip in switch_list:
        #print 'match vni list ..match switch..modifying...'
        # Modify the floods, keep vni the same
        mod_vxlan =  modify_existing_vxlan(vx,switch_list,vlan)
        mod_vxlan['sint'] = vx[u'sint']
        mod_vxlan['sip'] = vx[u'sip']
        #print '======111111111111111111111111111======='
        #print 'This is the mod vxlan '
        #print mod_vxlan

        processed_list.append(mod_vx['sip'])
        #print 'processed_list %s' % processed_list
        #print '======111111111111111111111111111======='
        modified_vxlan_list.append(mod_vxlan)

    if vlan in temp_vni and sip not in switch_list:
        #print 'match vni list not in switchlist...modifying...'
        # Modify the floods, keep vni the same
        mod_vxlan =  modify_existing_vxlan(vx,switch_list,vlan)
        mod_vxlan['sint'] = vx[u'sint']
        mod_vxlan['sip'] = vx[u'sip']
        #print '======22222222222222222222222222======='
        #print 'This is the mod vxlan '
        #print mod_vxlan
        #print '======222222222222222222222222222======='
        processed_list.append(mod_vxlan['sip'])
        modified_vxlan_list.append(mod_vxlan)

    if vlan not in temp_vni and sip in switch_list:
        #print 'match vni list ....need to modify the vinny modifying...'
        # Modify the floods, keep vni needs to be modified as well
        mod_vxlan =  modify_existing_vxlan_a(vx,switch_list,vlan)
        mod_vxlan['sint'] = vx[u'sint']
        mod_vxlan['sip'] = vx[u'sip']
        #print '======3333333333333333333333333333======='
        #print 'This is the mod vxlan '
        #print mod_vxlan

        processed_list.append(vx['sip'])
        #print '======3333333333333333333333333333======='
        #print 'processed_list %s' % processed_list
        modified_vxlan_list.append(mod_vxlan)



#print 'this is the modified list %s' % (modified_vxlan_list)
#print 'this is the new list %s' % (new_vxlan_list)
#print 'this is the processed list %s' % (processed_list)
