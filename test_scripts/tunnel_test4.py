
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
switch_list = ['10.132.0.188', '10.132.0.185', '10.132.0.182']

modified_vxlans = []
established_floods = []
counter = 0
# Iterate through all the switches, look for updates
for vx in vxlans:
    print 'for vx in vxlans counter is %s' % (counter)
    vxlan= {}
    update_list = []
    new_flood = {}
    local_ip = []
    current_flood = []
    list_member = 'no'
    vni_map = 'no'
    temp_vni = {}
    complete = 'no'

    # This switch has a vxlan interface check to see if it belongs to the vlan
    # Get the vni to vlan map...it could be a list a list
    vni = vx[u'vni']
    sip = vx[u'sip']

    if sip in switch_list:
        list_member = 'yes'
        print '=================IN switch list==============================='
        # Collect established_floods to add to new switches
        established_floods.append(vx[u'sip'])

    for vmap in vni:
        #The vxlan is part of the vlan from the end user
        if vmap[u'vlan'] == vlan:
            vni_map = 'yes'
            print '============Vlan in vni map============================'

    for flood in vx['floods']:
        local_ip = []
        new_flood = {}
        print 'this is one of the floods from the vxlan interface %s' % (flood)
        print 'this is the switch_list %s' % (switch_list)
        print 'this is the switch_ip %s' % (sip)
        if flood['vlan'] == vlan:
            print 'Found the vlan %s in the current flood' % (flood['vlan'])
            # This vxlan exists, dont change anything
            if list_member == 'yes' and vni_map == 'yes':

                print 'switch one..........................'
                # Make a list of just the local IP
                local_ip.append(vx[u'sip'])
                print 'local_ip %s' % (local_ip)

                # Remove local switch IP from switchlist
                new_list = set(switch_list) - set(local_ip)

                # Turn the set back into a python list
                new_list = list(new_list)
                print 'this is the new_list %s without local_ip' % (new_list)

                x_list = set(new_list) - set(flood[u'floods'])
                x_list = list(x_list)
                print 'this is the current flood %s' % (flood[u'floods'])
                print 'this is the x_list subtracting the current floods %s' % (x_list)
                new_flood[u'floods'] = flood[u'floods']+x_list
                new_flood[u'vlan'] = vlan

                # Add dict to temporary collection of floods
                update_list.append(new_flood)
                print 'this is the update_list a combination for floods for a switch%s' % (update_list)


                vxlan['vni'] = vni


                print 'this is the vinny %s' % (vxlan['vni'])
                vxlan['floods'] = update_list
                print 'made it though switch one this is the floods %s' % (vxlan['floods'])

                counter = counter + 1


            # Not in the switch list but needs vxlan updated
            if list_member == 'no' and vni_map == 'yes':
                print 'Switch three....................................................'
                x_list = set(switch_list) - set(flood[u'floods'])

                x_list = list(x_list)
                print 'this is the current flood %s' % (flood[u'floods'])
                print 'this is the x_list subtracting the current floods %s' % (x_list)
                new_flood[u'floods'] = flood[u'floods']+x_list
                new_flood[u'vlan'] = vlan

                # Add dict to temporary collection of floods
                update_list.append(new_flood)
                print 'This is the update list %s' % (update_list)
                vxlan['floods'] = update_list
                vxlan['vni'] = vni

        else:
            # Switch has a vxlan interface but is gettig a new vni

            print 'vlan %s  is not in current flood appending.....' % (vlan)

            print 'this is the flood without the matching vlan %s' % (flood)
            update_list.append(flood)
            print 'this is the update list for non vlan matching floods %s ' % (update_list)
            vxlan['floods'] = update_list

        if list_member == 'yes' and vni_map == 'no':
            # Have we been here befor, we only need to visit just once per switch
            if complete == 'no':
                new_flood = {}
                print 'switch two.....Build the new new_list................'

                # Make a list of just the local IP
                local_ip.append(vx[u'sip'])

                # Remove local switch IP from switchlist
                new_list = set(switch_list) - set(local_ip)

                # Turn the set back into a python list
                new_list = list(new_list)
                print 'this is the new_list %s' % (new_list)

                new_flood[u'floods'] = new_list
                new_flood[u'vlan'] = vlan
                print 'this is the new flood %s' % (new_flood)

                # Add dict to temporary collection of floods
                update_list.append(new_flood)
                print 'this is the update list %s' % (update_list)
                vxlan['floods'] = update_list
                # Add a new vni and append to the current vni
                temp_vni['vni'] = vlan+'00'
                temp_vni['vlan'] = vlan

                vxlan['vni'] = temp_vni
                print 'this is the tempvinny %s' % (vxlan['vni'])
                complete = 'yes'

    vxlan['sint'] = vx[u'sint']
    vxlan['sip'] = vx[u'sip']



    modified_vxlans.append(vxlan)
    print '================modified vxlans==========================='
    print modified_vxlans
